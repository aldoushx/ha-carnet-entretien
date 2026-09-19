// Carte Lovelace "Carnet d'entretien" — thèmes visuels premium
// Custom element vanilla JS, sans dépendance externe, servi automatiquement
// par le composant (voir __init__.py: register_static_path + add_extra_js_url).
// Les couleurs sont pilotées par variables CSS (--ce-*) selon l'attribut
// data-theme posé sur <ha-card>, ce qui permet de changer de thème sans
// toucher au JS : voir le bloc THEMES en bas de fichier.

const DOMAIN = "carnet_entretien";

const STATUS_LABEL = { ok: "OK", bientot: "Bientôt", echue: "Échue", non_applicable: "Non applicable" };
const SEVERITY_LABEL = { mineur: "Mineur", majeur: "Majeur", securite: "Sécurité" };
const DIY_LABEL = { facile: "🟢 Facile en DIY", moyen: "🟠 Moyen en DIY", difficile: "🔴 Difficile en DIY", non_recommande: "⛔ Déconseillé en DIY" };
const CATEGORY_EMOJI = {
  moteur: "🛢️", freinage: "🛑", pneumatiques: "🛞", distribution: "⚙️",
  filtration: "🌬️", carrosserie: "🚗", electronique: "🔌",
  controle_technique: "📋", revision: "🛠️", autre: "🔩", boite_de_vitesses: "⚙️",
  suspension: "🔩", climatisation: "❄️",
};
const THEMES_META = [
  { id: "gt_cuir", name: "Grand tourisme cuir", icon: "🛞", swatches: ["#2B1B12", "#C08A4E", "#EDE0C8", "#5A4230"] },
  { id: "horlogerie", name: "Manufacture horlogère", icon: "⏱️", swatches: ["#0F1B2E", "#8A94A6", "#A6192E", "#C9CDD3"] },
  { id: "carbone", name: "Carbone et titane", icon: "⚡", swatches: ["#0B0C0E", "#4A5560", "#35D0E0", "#9AA3AC"] },
  { id: "vintage", name: "Atelier vintage", icon: "🧭", swatches: ["#EDE6D6", "#5B3A29", "#14532D", "#B08D57"] },
];
const VALID_THEME_IDS = THEMES_META.map((t) => t.id);

function statusVar(status) {
  return `var(--ce-status-${status || "ok"})`;
}
function severityVar(sev) {
  return `var(--ce-severity-${sev || "mineur"})`;
}

class CarnetEntretienCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._vehicles = [];
    this._view = "list"; // list | add | detail | settings
    this._preSettingsView = "list";
    this._selectedId = null;
    this._tab = "entretien"; // entretien | historique
    this._loading = false;
    this._loadingMsg = "";
    this._addForm = { brand: "", model: "", motorisation: "", year: "", mileage: "", plate: "", photo: "" };
    this._brandOptions = [];
    this._modelOptions = [];
    this._mileageSourceEditing = false;
    this._pendingSensorEntity = "";
    this._theme = "gt_cuir";
    this._settings = { hide_not_applicable: false, notifications_enabled: true };
    this._motorisationKey = null;
    this._motorisationFullList = null;
    this._diyLoading = {}; // { [itemId]: bool } — état de chargement de l'explication DIY
  }

  setConfig(config) {
    this._config = config || {};
  }

  set hass(hass) {
    const first = !this._hass;
    this._hass = hass;
    if (first) this._fetchVehicles();
  }

  getCardSize() {
    return 8;
  }

  async _ws(message) {
    return this._hass.connection.sendMessagePromise({ type: `${DOMAIN}/${message.type}`, ...message.data });
  }

  async _fetchVehicles() {
    try {
      const res = await this._ws({ type: "get_vehicles" });
      this._vehicles = res.vehicles || [];
      if (res.settings) {
        this._settings = { ...this._settings, ...res.settings };
        if (res.settings.theme && VALID_THEME_IDS.includes(res.settings.theme)) {
          this._theme = res.settings.theme;
        }
      }
    } catch (e) {
      console.error("carnet_entretien: échec du chargement", e);
    }
    this._render();
  }

  get _selectedVehicle() {
    return this._vehicles.find((v) => v.id === this._selectedId) || null;
  }

  // ---------------------------------------------------------------- actions

  async _submitAddVehicle(e) {
    e.preventDefault();
    const f = this._addForm;
    if (!f.brand || !f.model || !f.year || f.mileage === "") return;
    this._loading = true;
    this._loadingMsg = "Recherche des informations constructeur…";
    this._render();
    const steps = [
      "Recherche des informations constructeur…",
      "Génération du plan d'entretien…",
      "Analyse des retours d'expérience connus…",
      "Vérification des rappels constructeur…",
    ];
    let i = 0;
    const timer = setInterval(() => {
      i = Math.min(i + 1, steps.length - 1);
      this._loadingMsg = steps[i];
      this._render();
    }, 1800);
    try {
      const res = await this._ws({
        type: "add_vehicle",
        data: {
          brand: f.brand,
          model: f.model,
          motorisation: f.motorisation,
          year: parseInt(f.year, 10),
          mileage: parseInt(f.mileage, 10),
          plate: f.plate,
          photo: f.photo || undefined,
        },
      });
      await this._fetchVehicles();
      this._selectedId = res.vehicle.id;
      this._view = "detail";
      this._tab = "entretien";
      this._addForm = { brand: "", model: "", motorisation: "", year: "", mileage: "", plate: "", photo: "" };
    } catch (err) {
      alert("Erreur lors de la génération : " + (err.message || err.code || err));
    } finally {
      clearInterval(timer);
      this._loading = false;
      this._render();
    }
  }

  async _searchBrand(query) {
    const res = await this._ws({ type: "search_referentiel", data: { query } });
    this._brandOptions = res.results || [];
    this._renderSuggestions("brand", this._brandOptions);
  }

  async _searchModel(brand, query) {
    const res = await this._ws({ type: "search_referentiel", data: { brand, query } });
    this._modelOptions = res.results || [];
    this._renderSuggestions("model", this._modelOptions);
  }

  // Recherche des motorisations existantes pour marque+modèle+année : le
  // premier appel par combinaison déclenche Gemini (mis en cache côté
  // serveur), les frappes suivantes filtrent la liste déjà récupérée côté
  // client — instantané, comme pour le référentiel marque/modèle.
  async _searchMotorisation(query) {
    const f = this._addForm;
    if (!f.brand || !f.model || !f.year) {
      this._renderSuggestions("motorisation", []);
      return;
    }
    const key = `${f.brand}|${f.model}|${f.year}`;
    if (this._motorisationKey !== key) {
      this._motorisationKey = key;
      this._motorisationFullList = null;
      this._renderSuggestions("motorisation", []);
      try {
        const res = await this._ws({
          type: "search_motorisations",
          data: { brand: f.brand, model: f.model, year: parseInt(f.year, 10), query: "" },
        });
        if (this._motorisationKey !== key) return; // la sélection a changé entre-temps
        this._motorisationFullList = res.results || [];
      } catch (e) {
        this._motorisationFullList = [];
      }
    }
    if (this._motorisationFullList === null) return; // chargement en cours
    const q = query.trim().toLowerCase();
    const filtered = q ? this._motorisationFullList.filter((m) => m.toLowerCase().includes(q)) : this._motorisationFullList;
    this._renderSuggestions("motorisation", filtered);
  }

  // Met à jour uniquement le menu de suggestions (jamais tout le shadow DOM)
  // pour ne pas faire perdre le focus/curseur du champ en cours de frappe.
  _renderSuggestions(kind, options) {
    const box = this.shadowRoot.getElementById(`${kind}-suggestions`);
    if (!box) return;
    const opts = (options || []).slice(0, 8);
    if (!opts.length) {
      box.innerHTML = "";
      box.classList.remove("open");
      return;
    }
    box.innerHTML = opts.map((o) => `<div class="suggestion-item" data-value="${esc(o)}">${esc(o)}</div>`).join("");
    box.classList.add("open");
    box.querySelectorAll(".suggestion-item").forEach((el) => {
      // mousedown (pas click) : se déclenche avant le blur du champ texte
      el.addEventListener("mousedown", (e) => {
        e.preventDefault();
        this._selectSuggestion(kind, el.dataset.value);
      });
    });
  }

  _selectSuggestion(kind, value) {
    const root = this.shadowRoot;
    if (kind === "brand") {
      this._addForm.brand = value;
      root.getElementById("f-brand").value = value;
      this._closeSuggestions("brand");
      this._addForm.model = "";
      root.getElementById("f-model").value = "";
      this._searchModel(value, "");
    } else if (kind === "model") {
      this._addForm.model = value;
      root.getElementById("f-model").value = value;
      this._closeSuggestions("model");
    } else if (kind === "motorisation") {
      this._addForm.motorisation = value;
      root.getElementById("f-motorisation").value = value;
      this._closeSuggestions("motorisation");
    }
  }

  _closeSuggestions(kind) {
    const box = this.shadowRoot.getElementById(`${kind}-suggestions`);
    if (box) {
      box.innerHTML = "";
      box.classList.remove("open");
    }
  }

  async _updateMileage(vehicleId, mileage) {
    await this._ws({ type: "update_mileage", data: { vehicle_id: vehicleId, mileage: parseInt(mileage, 10) } });
    await this._fetchVehicles();
  }

  async _setMileageSource(vehicleId, source, entityId) {
    await this._ws({ type: "set_mileage_source", data: { vehicle_id: vehicleId, source, entity_id: entityId || undefined } });
    this._mileageSourceEditing = false;
    await this._fetchVehicles();
  }

  async _refreshPlan(vehicleId) {
    this._loading = true;
    this._loadingMsg = "Régénération du plan d'entretien…";
    this._render();
    try {
      await this._ws({ type: "refresh_plan", data: { vehicle_id: vehicleId } });
      await this._fetchVehicles();
    } catch (err) {
      alert("Erreur : " + (err.message || err.code || err));
    } finally {
      this._loading = false;
      this._render();
    }
  }

  async _setItemApplicable(vehicleId, itemId, applicable) {
    await this._ws({ type: "set_item_applicable", data: { vehicle_id: vehicleId, item_id: itemId, applicable } });
    await this._fetchVehicles();
  }

  async _setItemOverride(vehicleId, itemId, dueKm, dueDate) {
    const data = { vehicle_id: vehicleId, item_id: itemId };
    if (dueKm !== undefined) data.due_km = dueKm;
    if (dueDate !== undefined) data.due_date = dueDate;
    await this._ws({ type: "set_item_override", data });
    await this._fetchVehicles();
  }

  async _addPlanItem(vehicleId, item) {
    await this._ws({ type: "add_plan_item", data: { vehicle_id: vehicleId, ...item } });
    await this._fetchVehicles();
  }

  async _removePlanItem(vehicleId, itemId) {
    if (!confirm("Retirer cet entretien du plan ?")) return;
    await this._ws({ type: "remove_plan_item", data: { vehicle_id: vehicleId, item_id: itemId } });
    await this._fetchVehicles();
  }

  async _generateDiyExplanation(vehicleId, itemId) {
    this._diyLoading[itemId] = true;
    this._render();
    try {
      await this._ws({ type: "generate_diy_explanation", data: { vehicle_id: vehicleId, item_id: itemId } });
      await this._fetchVehicles();
    } catch (err) {
      alert("Erreur : " + (err.message || err.code || err));
    } finally {
      delete this._diyLoading[itemId];
      this._render();
    }
  }

  async _refreshKnownIssues(vehicleId) {
    this._loading = true;
    this._loadingMsg = "Analyse des retours d'expérience…";
    this._render();
    try {
      await this._ws({ type: "refresh_known_issues", data: { vehicle_id: vehicleId } });
      await this._fetchVehicles();
    } catch (err) {
      alert("Erreur : " + (err.message || err.code || err));
    } finally {
      this._loading = false;
      this._render();
    }
  }

  async _refreshRecalls(vehicleId) {
    this._loading = true;
    this._loadingMsg = "Vérification des rappels constructeur…";
    this._render();
    try {
      await this._ws({ type: "refresh_recalls", data: { vehicle_id: vehicleId } });
      await this._fetchVehicles();
    } catch (err) {
      alert("Erreur : " + (err.message || err.code || err));
    } finally {
      this._loading = false;
      this._render();
    }
  }

  async _valueSnapshot(vehicleId) {
    this._loading = true;
    this._loadingMsg = "Estimation de la valeur de revente…";
    this._render();
    try {
      await this._ws({ type: "value_snapshot", data: { vehicle_id: vehicleId, condition: "correct" } });
      await this._fetchVehicles();
    } catch (err) {
      alert("Erreur : " + (err.message || err.code || err));
    } finally {
      this._loading = false;
      this._render();
    }
  }

  async _logMaintenance(vehicleId, payload) {
    await this._ws({ type: "log_maintenance", data: { vehicle_id: vehicleId, ...payload } });
    await this._fetchVehicles();
  }

  async _removeVehicle(vehicleId) {
    if (!confirm("Supprimer ce véhicule et toutes ses données ?")) return;
    await this._ws({ type: "remove_vehicle", data: { vehicle_id: vehicleId } });
    this._view = "list";
    this._selectedId = null;
    await this._fetchVehicles();
  }

  async _setPhoto(vehicleId, photo) {
    await this._ws({ type: "set_photo", data: { vehicle_id: vehicleId, photo: photo || undefined } });
    await this._fetchVehicles();
  }

  async _selectTheme(themeId) {
    if (themeId === this._theme) return;
    this._theme = themeId;
    this._render();
    try {
      await this._ws({ type: "set_settings", data: { theme: themeId } });
    } catch (e) {
      console.error("carnet_entretien: échec de l'enregistrement du thème", e);
    }
  }

  async _updateSetting(key, value) {
    this._settings = { ...this._settings, [key]: value };
    this._render();
    try {
      await this._ws({ type: "set_settings", data: { [key]: value } });
    } catch (e) {
      console.error("carnet_entretien: échec de l'enregistrement du réglage", e);
    }
  }

  // ---------------------------------------------------------------- render

  _render() {
    if (!this.shadowRoot) return;
    const content =
      this._view === "settings"
        ? this._renderSettings()
        : this._view === "add"
        ? this._renderAddForm()
        : this._view === "detail" && this._selectedVehicle
        ? this._renderDetail(this._selectedVehicle)
        : this._renderList();

    const showSettingsBtn = this._view !== "settings";
    const primaryBtn =
      this._view === "settings"
        ? `<button class="btn ghost" id="back-btn">← Retour</button>`
        : this._view === "list"
        ? `<button class="btn primary" id="add-btn">➕ Ajouter</button>`
        : `<button class="btn ghost" id="back-btn">← Retour</button>`;

    this.shadowRoot.innerHTML = `
      <style>${STYLE}</style>
      <ha-card data-theme="${this._theme}">
        <div class="header">
          <div class="title">🚗 Carnet d'entretien</div>
          <div class="header-actions">
            ${showSettingsBtn ? `<button class="btn ghost icon" id="settings-btn" title="Réglages">⚙️</button>` : ""}
            ${primaryBtn}
          </div>
        </div>
        ${this._loading ? `<div class="loading"><div class="spinner"></div>${this._loadingMsg}</div>` : ""}
        <div class="body">${content}</div>
      </ha-card>
    `;
    this._bindEvents();
  }

  _renderList() {
    if (!this._vehicles.length) {
      return `<div class="empty">Aucun véhicule pour l'instant. Ajoutez-en un avec « ➕ Ajouter ».</div>`;
    }
    return `<div class="grid">
      ${this._vehicles
        .map((v) => {
          const next = (v.maintenance_plan || []).find((it) => it.statut !== "non_applicable");
          const color = next ? statusVar(next.statut) : "var(--ce-text-dim)";
          return `
          <div class="tile" data-id="${v.id}">
            ${v.photo ? `<img class="tile-photo" src="${v.photo}" alt="" />` : ""}
            <div class="tile-badge" style="background:${color}"></div>
            <div class="tile-title">${esc(v.brand)} ${esc(v.model)}</div>
            <div class="tile-sub">${v.year} · ${fmtKm(v.mileage)}${v.plate ? ` · ${esc(v.plate.toUpperCase())}` : ""}</div>
            ${
              next
                ? `<div class="tile-next">${CATEGORY_EMOJI[next.category] || "🔩"} ${esc(next.name)} — ${STATUS_LABEL[next.statut]}</div>`
                : `<div class="tile-next muted">Plan non généré</div>`
            }
          </div>`;
        })
        .join("")}
    </div>`;
  }

  _renderSettings() {
    return `
      <p class="section-label">Thème visuel</p>
      <div class="theme-grid">
        ${THEMES_META.map(
          (t) => `
          <div class="theme-card ${this._theme === t.id ? "active" : ""}" data-theme-id="${t.id}">
            <div class="theme-card-head">
              <span>${t.icon} ${esc(t.name)}</span>
              ${this._theme === t.id ? `<span class="accent small">✓ actif</span>` : ""}
            </div>
            <div class="swatches">
              ${t.swatches.map((c) => `<span style="background:${c}"></span>`).join("")}
            </div>
          </div>`
        ).join("")}
      </div>
      <p class="section-label">Notifications &amp; affichage</p>
      <label class="checkbox-row" style="margin-bottom:10px;">
        <input type="checkbox" id="setting-notifications" ${this._settings.notifications_enabled ? "checked" : ""} />
        Notification persistante HA quand une échéance est dépassée
      </label>
      <label class="checkbox-row">
        <input type="checkbox" id="setting-hide-na" ${this._settings.hide_not_applicable ? "checked" : ""} />
        Masquer les entretiens non applicables dans la liste
      </label>
      <p class="muted small" style="margin-top:14px;">D'autres réglages arriveront ici (unités, devise…).</p>
    `;
  }

  _renderAddForm() {
    const f = this._addForm;
    return `
      <form id="add-form" class="form">
        <label>Marque
          <div class="autocomplete">
            <input id="f-brand" value="${esc(f.brand)}" placeholder="Ex : Peugeot" autocomplete="off" />
            <div class="suggestions" id="brand-suggestions"></div>
          </div>
        </label>
        <label>Modèle
          <div class="autocomplete">
            <input id="f-model" value="${esc(f.model)}" placeholder="Ex : 308" autocomplete="off" />
            <div class="suggestions" id="model-suggestions"></div>
          </div>
        </label>
        <label>Année
          <input type="number" id="f-year" value="${esc(f.year)}" min="1970" max="2100" />
        </label>
        <label>Motorisation <span class="muted">(optionnel — suggestions une fois marque/modèle/année remplis)</span>
          <div class="autocomplete">
            <input id="f-motorisation" value="${esc(f.motorisation)}" placeholder="Ex : 1.5 BlueHDi 130" autocomplete="off" />
            <div class="suggestions" id="motorisation-suggestions"></div>
          </div>
        </label>
        <div class="row-2">
          <label>Kilométrage
            <input type="number" id="f-mileage" value="${esc(f.mileage)}" min="0" />
          </label>
          <label>Immatriculation <span class="muted">(opt.)</span>
            <input id="f-plate" value="${esc(f.plate)}" placeholder="AB-123-CD" />
          </label>
        </div>
        <label>Photo <span class="muted">(optionnel)</span>
          <input type="file" id="f-photo" accept="image/*" capture="environment" />
        </label>
        <img id="add-photo-preview" class="photo-preview" style="display:${f.photo ? "block" : "none"};" src="${f.photo || ""}" />
        <button type="submit" class="btn primary full">Générer le carnet d'entretien</button>
      </form>
    `;
  }

  _renderDetail(v) {
    const tabs = [
      ["entretien", "🔧 Entretien"],
      ["historique", "📓 Historique"],
    ];
    return `
      <div class="detail-header">
        <div class="detail-header-main">
          ${
            v.photo
              ? `<img class="vehicle-photo" src="${v.photo}" alt="" />`
              : `<div class="vehicle-photo placeholder">🚗</div>`
          }
          <div>
            <div class="detail-title">${esc(v.brand)} ${esc(v.model)} <span class="muted">(${v.year})</span></div>
            <div class="muted small">${esc(v.motorisation || "")}</div>
            ${v.plate ? `<div class="plate-chip mono">${esc(v.plate.toUpperCase())}</div>` : ""}
            <div class="photo-controls">
              <label class="link-btn">
                📷 ${v.photo ? "Changer" : "Ajouter"} une photo
                <input type="file" id="photo-input" accept="image/*" capture="environment" style="display:none;" />
              </label>
              ${v.photo ? `<button class="link-btn" id="remove-photo-btn">Retirer</button>` : ""}
            </div>
          </div>
        </div>
        <button class="btn danger small" id="remove-btn">🗑️</button>
      </div>
      ${
        this._vehicles.length > 1
          ? `<div class="switcher-row">
              <span class="muted small">🚗</span>
              <select id="vehicle-switcher">
                ${this._vehicles
                  .map((v2) => `<option value="${v2.id}" ${v2.id === v.id ? "selected" : ""}>${esc(v2.brand)} ${esc(v2.model)} (${v2.year})</option>`)
                  .join("")}
              </select>
            </div>`
          : ""
      }
      ${this._renderMileageRow(v)}
      <div class="tabs">
        ${tabs.map(([id, label]) => `<div class="tab ${this._tab === id ? "active" : ""}" data-tab="${id}">${label}</div>`).join("")}
      </div>
      <div class="tab-content">
        ${this._tab === "entretien" ? this._renderTabEntretien(v) : this._renderTabHistorique(v)}
      </div>
    `;
  }

  _renderMileageRow(v) {
    if (v.mileage_source === "sensor") {
      return `
        <div class="mileage-row">
          <span>🔗 <b>${fmtKm(v.mileage)}</b></span>
          <span class="muted small">lié à ${esc(v.mileage_sensor_entity_id || "")}</span>
          <button class="btn small ghost" id="unlink-sensor-btn">Délier</button>
        </div>`;
    }
    if (this._mileageSourceEditing) {
      return `
        <div class="mileage-row">
          <span>Kilométrage :</span>
          <input type="number" id="mileage-input" value="${v.mileage}" min="0" />
          <button class="btn small" id="mileage-btn">Mettre à jour</button>
        </div>
        <div class="sensor-link-box">
          <div class="muted small" style="margin-bottom:6px;">Lier un capteur existant (odomètre constructeur, OBD, input_number…) :</div>
          <div id="entity-picker-slot"></div>
          <div class="row-2" style="margin-top:8px;">
            <button class="btn small primary" id="confirm-link-btn">Lier</button>
            <button class="btn small ghost" id="cancel-link-btn">Annuler</button>
          </div>
        </div>`;
    }
    return `
      <div class="mileage-row">
        <span>Kilométrage :</span>
        <input type="number" id="mileage-input" value="${v.mileage}" min="0" />
        <button class="btn small" id="mileage-btn">Mettre à jour</button>
        <button class="btn small ghost" id="link-sensor-btn" title="Lier un capteur existant">🔗</button>
      </div>`;
  }

  _renderTabEntretien(v) {
    return `
      ${this._renderRecallsPanel(v)}
      ${this._renderVigilancePanel(v)}
      ${this._renderValeurPanel(v)}
      <p class="section-label">Entretien à prévoir</p>
      ${this._renderPlanList(v)}
    `;
  }

  _renderRecallsPanel(v) {
    const recalls = v.recalls || [];
    return `
      <details class="panel">
        <summary>
          <span>🚨 Rappels constructeur</span>
          <span class="small" style="${recalls.length ? "color:var(--ce-danger-text);font-weight:600;" : "color:var(--ce-text-muted);"}">
            ${recalls.length ? recalls.length + " actif" + (recalls.length > 1 ? "s" : "") : "aucun connu"}
          </span>
        </summary>
        <div class="panel-body">
          <div class="disclaimer">Synthèse IA, non exhaustive — vérifiez systématiquement sur le site du constructeur ou rappel.conso.gouv.fr avant toute décision.</div>
          ${
            recalls.length
              ? `<div class="issue-list">
                  ${recalls
                    .map(
                      (r) => `
                    <div class="issue-item">
                      <div class="issue-head">
                        <span>🚨 ${esc(r.title)}</span>
                        <span class="status-chip" style="background:${severityVar(r.severity)}">${SEVERITY_LABEL[r.severity] || r.severity}</span>
                      </div>
                      ${r.reference || r.date ? `<div class="muted small">${[r.reference, r.date].filter(Boolean).map(esc).join(" · ")}</div>` : ""}
                      <div class="small">${esc(r.description || "")}</div>
                      ${r.action_required ? `<div class="muted small">➡️ ${esc(r.action_required)}</div>` : ""}
                    </div>`
                    )
                    .join("")}
                </div>`
              : `<div class="empty small">Aucun rappel identifié pour ce véhicule.</div>`
          }
          ${
            v.recalls_sources
              ? `<div class="sources-box">📚 <b>Sources :</b> <span class="muted small">${esc(v.recalls_sources)}</span></div>`
              : ""
          }
          ${
            v.recalls_checked_at
              ? `<div class="muted small" style="margin-top:6px;">Dernière vérification : ${fmtDate(v.recalls_checked_at)}</div>`
              : ""
          }
          <button class="btn small ghost full" id="refresh-recalls-btn">↻ Vérifier à nouveau</button>
        </div>
      </details>
    `;
  }

  _renderVigilancePanel(v) {
    const issues = v.known_issues || [];
    return `
      <details class="panel">
        <summary>
          <span>⚠️ Points de vigilance</span>
          <span class="muted small">${issues.length ? issues.length + " point" + (issues.length > 1 ? "s" : "") : "—"}</span>
        </summary>
        <div class="panel-body">
          <div class="disclaimer">Synthèse IA à partir de retours d'expérience courants — à titre indicatif, ne remplace pas un diagnostic professionnel.</div>
          ${
            issues.length
              ? `<div class="issue-list">
                  ${issues
                    .map(
                      (it) => `
                    <div class="issue-item">
                      <div class="issue-head">
                        <span>${CATEGORY_EMOJI[it.category] || "🔩"} ${esc(it.title)}</span>
                        <span class="status-chip" style="background:${severityVar(it.severity)}">${SEVERITY_LABEL[it.severity] || it.severity}</span>
                      </div>
                      ${it.typical_occurrence ? `<div class="muted small">Apparaît généralement : ${esc(it.typical_occurrence)}</div>` : ""}
                      <div class="small">${esc(it.description || "")}</div>
                      ${it.cost_estimate ? `<div class="muted small">💰 Coût indicatif : ${esc(it.cost_estimate)}</div>` : ""}
                    </div>`
                    )
                    .join("")}
                </div>`
              : `<div class="empty small">Aucun point recensé pour l'instant.</div>`
          }
          ${
            v.known_issues_sources
              ? `<div class="sources-box">📚 <b>Source des données :</b> <span class="muted small">${esc(v.known_issues_sources)}</span></div>`
              : ""
          }
          <button class="btn small ghost full" id="refresh-issues-btn">↻ Regénérer</button>
        </div>
      </details>
    `;
  }

  _renderValeurPanel(v) {
    const history = v.value_history || [];
    const last = history[history.length - 1];
    return `
      <details class="panel">
        <summary>
          <span>💶 Valeur estimée</span>
          <span class="mono accent small">${last ? fmtEur(last.value_avg) : "—"}</span>
        </summary>
        <div class="panel-body">
          ${
            last
              ? `<div class="value-range small muted">Fourchette : ${fmtEur(last.value_min)} – ${fmtEur(last.value_max)}</div>
                 ${history.length > 1 ? renderValueChart(history) : ""}
                 ${
                   last.sources_tendance
                     ? `<div class="sources-box">📚 <b>Sources &amp; tendance :</b> <span class="muted small">${esc(last.sources_tendance)}</span></div>`
                     : ""
                 }`
              : `<div class="empty small">Aucune estimation pour l'instant.</div>`
          }
          <button class="btn small primary full" id="snapshot-btn">💶 Estimer maintenant</button>
        </div>
      </details>
    `;
  }

  _renderPlanList(v) {
    const allItems = v.maintenance_plan || [];
    if (!allItems.length) {
      return `<div class="empty">Aucun plan généré. <button class="btn small" id="refresh-plan-btn">Générer</button></div>`;
    }
    const items = this._settings.hide_not_applicable
      ? allItems.filter((it) => it.statut !== "non_applicable")
      : allItems;
    const annualKm = allItems.find((it) => it.annual_km)?.annual_km;
    const hiddenCount = allItems.length - items.length;
    return `
      <div class="toolbar">
        <button class="btn small ghost" id="refresh-plan-btn">↻ Regénérer le plan</button>
        ${annualKm ? `<span class="muted small">📊 ~${fmtKm(annualKm)}/an</span>` : ""}
      </div>
      ${hiddenCount ? `<div class="muted small" style="margin-bottom:8px;">${hiddenCount} entretien(s) non applicable(s) masqué(s) (réglages).</div>` : ""}
      <div class="plan-list">
        ${items.map((it) => this._renderPlanRow(it, v)).join("")}
      </div>
      <button class="btn small ghost full" id="add-item-btn" style="margin-top:10px;">+ Ajouter un entretien</button>
      <div id="add-item-form" class="add-item-form" style="display:none;"></div>
    `;
  }

  _renderPlanRow(it, v) {
    const isNA = it.statut === "non_applicable";
    const applicableChecked = it.applicable !== false;
    const diyBadge = !isNA && it.diy_difficulty ? `<span class="diy-badge diy-${it.diy_difficulty}">${DIY_LABEL[it.diy_difficulty] || it.diy_difficulty}</span>` : "";

    let summaryBody = "";
    if (isNA) {
      summaryBody = `
        <div class="plan-row-head">
          <span>${CATEGORY_EMOJI[it.category] || "🔩"} ${esc(it.name)}</span>
          <span class="muted small">non applicable</span>
        </div>
        <div class="muted small">${esc(it.not_applicable_reason || "Ne concerne pas ce véhicule.")}</div>`;
    } else {
      const color = statusVar(it.statut);
      const overdue =
        (it.km_restants != null && it.km_restants <= 0) || (it.jours_restants != null && it.jours_restants <= 0);
      const pctFromKm = it.km_restants != null && it.interval_km ? 100 - (it.km_restants / it.interval_km) * 100 : null;
      const pctFromDays =
        it.jours_restants != null && it.interval_months ? 100 - (it.jours_restants / (it.interval_months * 30)) * 100 : null;
      const pct = overdue ? 100 : Math.max(0, Math.min(100, pctFromKm ?? pctFromDays ?? 30));
      let rightLabel = "";
      if (overdue) {
        rightLabel = it.depasse_de_km != null ? `-${fmtKm(it.depasse_de_km)}` : it.jours_restants != null ? `-${Math.abs(it.jours_restants)} j` : "⚠️";
      } else if (it.km_restants != null) {
        rightLabel = fmtKm(it.km_restants);
      } else if (it.jours_restants != null) {
        rightLabel = `${it.jours_restants} j`;
      }
      summaryBody = `
        <div class="plan-row-head">
          <span>${CATEGORY_EMOJI[it.category] || "🔩"} ${esc(it.name)} ${diyBadge}</span>
          <span class="mono small" style="color:${overdue ? "var(--ce-danger-text)" : "var(--ce-text-muted)"}">${rightLabel}</span>
        </div>
        <div class="bar"><div class="bar-fill" style="width:${pct}%;background:${color}"></div></div>
        <div class="plan-row-meta muted small">
          ${it.prevu_vers && !overdue ? `📅 ${esc(it.prevu_vers)}` : overdue ? "⚠️ à faire dès que possible" : ""}
          ${it.cost_estimate_eur != null ? ` · 💰 ${fmtEur(it.cost_estimate_eur)} (garage)` : ""}
          ${it.diy_cost_estimate_eur != null ? ` · 🔧 ${fmtEur(it.diy_cost_estimate_eur)} (pièces DIY)` : ""}
        </div>`;
    }

    return `
      <details class="plan-row ${isNA ? "na" : ""}">
        <summary class="plan-row-summary">${summaryBody}</summary>
        <div class="plan-row-edit">
          <label class="checkbox-row">
            <input type="checkbox" class="applicable-cb" data-item-id="${it.id}" ${applicableChecked ? "checked" : ""} />
            Applicable à mon véhicule
          </label>
          ${it.custom ? `<button class="link-btn" id="remove-item-${it.id}" data-item-id="${it.id}" style="margin-top:4px;">Retirer cet entretien ajouté manuellement</button>` : ""}

          ${
            !isNA
              ? `
          <div class="edit-divider"><span>dernière intervention</span></div>
          <div class="muted small" style="margin-bottom:10px;">
            🔧 ${it.last_done_date ? `<b>${fmtDate(it.last_done_date)}</b> à <b>${fmtKm(it.last_done_km)}</b>` : "non renseignée (calcul basé sur la mise en circulation)"}
          </div>
          <button class="btn primary full done-today-btn" data-item-id="${it.id}" data-item-name="${esc(it.name)}">✓ Fait aujourd'hui (${fmtKm(v.mileage)})</button>
          <div class="edit-divider"><span>ou une date antérieure</span></div>
          <div class="row-2">
            <label>Date de l'intervention
              <input type="date" class="log-date-input" data-item-id="${it.id}" value="${it.last_done_date ? isoDateFromUnix(it.last_done_date) : todayIso()}" max="${todayIso()}" />
            </label>
            <label>Kilométrage
              <input type="number" class="log-km-input" data-item-id="${it.id}" value="${it.last_done_km ?? v.mileage}" min="0" />
            </label>
          </div>
          <button class="btn small ghost full log-save-btn" data-item-id="${it.id}" data-item-name="${esc(it.name)}">Enregistrer cette date</button>

          <div class="edit-divider"><span>ou fixer l'échéance directement</span></div>
          <div class="row-2">
            <label>Échéance (km)
              <input type="number" class="override-km-input" data-item-id="${it.id}" value="${it.due_km_override ?? ""}" placeholder="${it.due_km ?? ""}" min="0" />
            </label>
            <label>Échéance (date)
              <input type="date" class="override-date-input" data-item-id="${it.id}" value="${it.due_date_override ? isoDateFromUnix(it.due_date_override) : ""}" />
            </label>
          </div>
          <button class="btn small ghost full override-save-btn" data-item-id="${it.id}">Appliquer cet ajustement</button>

          <div class="edit-divider"><span>bricolage (DIY)</span></div>
          ${this._renderDiySection(it)}
          `
              : ""
          }
        </div>
      </details>`;
  }

  _renderDiySection(it) {
    if (this._diyLoading[it.id]) {
      return `<div class="muted small">🔎 Génération de l'explication…</div>`;
    }
    if (it.diy_explanation) {
      return `
        <div class="diy-box">
          ${it.diy_safety_warning ? `<div class="diy-warning">⚠️ ${esc(it.diy_safety_warning)}</div>` : ""}
          <div class="small">${esc(it.diy_explanation)}</div>
          ${it.diy_estimated_time_minutes ? `<div class="muted small" style="margin-top:6px;">⏱️ Temps estimé : ~${it.diy_estimated_time_minutes} min</div>` : ""}
          ${
            it.diy_tools_needed && it.diy_tools_needed.length
              ? `<div class="muted small">🧰 Outillage spécifique : ${it.diy_tools_needed.map(esc).join(", ")}</div>`
              : ""
          }
        </div>`;
    }
    return `<button class="btn small ghost full diy-generate-btn" data-item-id="${it.id}">🔧 Comment le faire soi-même ?</button>`;
  }

  _renderTabHistorique(v) {
    const log = (v.maintenance_log || []).slice().reverse();
    return `
      <div class="toolbar"><button class="btn small ghost" id="add-log-btn">+ Ajouter une intervention</button></div>
      ${
        log.length
          ? `<div class="log-list">${log
              .map(
                (l) => `
            <div class="log-item">
              <div><b>${esc(l.item_name || "Intervention")}</b> — ${fmtKm(l.km)}</div>
              <div class="muted small">${new Date(l.date * 1000).toLocaleDateString("fr-FR")}${l.garage ? " · " + esc(l.garage) : ""}${l.cost ? " · " + l.cost + " €" : ""}</div>
              ${l.notes ? `<div class="small">${esc(l.notes)}</div>` : ""}
            </div>`
              )
              .join("")}</div>`
          : `<div class="empty">Aucune intervention enregistrée.</div>`
      }
    `;
  }

  // ---------------------------------------------------------------- events

  _bindEvents() {
    const root = this.shadowRoot;

    root.getElementById("add-btn")?.addEventListener("click", () => {
      this._view = "add";
      this._searchBrand("");
      this._render();
    });
    root.getElementById("settings-btn")?.addEventListener("click", () => {
      this._preSettingsView = this._view;
      this._view = "settings";
      this._render();
    });
    root.getElementById("back-btn")?.addEventListener("click", () => {
      if (this._view === "settings") {
        this._view = this._preSettingsView || "list";
      } else {
        this._view = "list";
        this._mileageSourceEditing = false;
      }
      this._render();
    });

    root.querySelectorAll(".theme-card").forEach((el) =>
      el.addEventListener("click", () => this._selectTheme(el.dataset.themeId))
    );
    root.getElementById("setting-notifications")?.addEventListener("change", (e) => this._updateSetting("notifications_enabled", e.target.checked));
    root.getElementById("setting-hide-na")?.addEventListener("change", (e) => this._updateSetting("hide_not_applicable", e.target.checked));

    root.querySelectorAll(".tile").forEach((el) =>
      el.addEventListener("click", () => {
        this._selectedId = el.dataset.id;
        this._view = "detail";
        this._tab = "entretien";
        this._render();
      })
    );

    root.getElementById("vehicle-switcher")?.addEventListener("change", (e) => {
      this._selectedId = e.target.value;
      this._tab = "entretien";
      this._mileageSourceEditing = false;
      this._render();
    });

    const addForm = root.getElementById("add-form");
    if (addForm) {
      addForm.addEventListener("submit", (e) => this._submitAddVehicle(e));

      const brandInput = root.getElementById("f-brand");
      brandInput.addEventListener("input", (e) => {
        this._addForm.brand = e.target.value;
        this._searchBrand(e.target.value);
      });
      brandInput.addEventListener("focus", (e) => this._searchBrand(e.target.value));
      brandInput.addEventListener("blur", () => setTimeout(() => this._closeSuggestions("brand"), 150));

      const modelInput = root.getElementById("f-model");
      modelInput.addEventListener("input", (e) => {
        this._addForm.model = e.target.value;
        this._searchModel(this._addForm.brand, e.target.value);
      });
      modelInput.addEventListener("focus", (e) => this._searchModel(this._addForm.brand, e.target.value));
      modelInput.addEventListener("blur", () => setTimeout(() => this._closeSuggestions("model"), 150));

      root.getElementById("f-year").addEventListener("input", (e) => (this._addForm.year = e.target.value));

      const motoInput = root.getElementById("f-motorisation");
      motoInput.addEventListener("input", (e) => {
        this._addForm.motorisation = e.target.value;
        this._searchMotorisation(e.target.value);
      });
      motoInput.addEventListener("focus", (e) => this._searchMotorisation(e.target.value));
      motoInput.addEventListener("blur", () => setTimeout(() => this._closeSuggestions("motorisation"), 150));

      root.getElementById("f-mileage").addEventListener("input", (e) => (this._addForm.mileage = e.target.value));
      root.getElementById("f-plate").addEventListener("input", (e) => (this._addForm.plate = e.target.value));
      root.getElementById("f-photo").addEventListener("change", async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        try {
          const dataUrl = await fileToCompressedDataUrl(file);
          this._addForm.photo = dataUrl;
          const preview = root.getElementById("add-photo-preview");
          preview.src = dataUrl;
          preview.style.display = "block";
        } catch (err) {
          console.error("carnet_entretien: échec de lecture de l'image", err);
        }
      });
    }

    root.querySelectorAll(".tab").forEach((el) =>
      el.addEventListener("click", () => {
        this._tab = el.dataset.tab;
        this._render();
      })
    );

    root.getElementById("remove-btn")?.addEventListener("click", () => this._removeVehicle(this._selectedId));
    root.getElementById("photo-input")?.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      try {
        const dataUrl = await fileToCompressedDataUrl(file);
        await this._setPhoto(this._selectedId, dataUrl);
      } catch (err) {
        console.error("carnet_entretien: échec de lecture de l'image", err);
      }
    });
    root.getElementById("remove-photo-btn")?.addEventListener("click", () => this._setPhoto(this._selectedId, null));
    root.getElementById("mileage-btn")?.addEventListener("click", () => {
      const val = root.getElementById("mileage-input").value;
      this._updateMileage(this._selectedId, val);
    });
    root.getElementById("link-sensor-btn")?.addEventListener("click", () => {
      this._pendingSensorEntity = this._selectedVehicle.mileage_sensor_entity_id || "";
      this._mileageSourceEditing = true;
      this._render();
    });
    root.getElementById("cancel-link-btn")?.addEventListener("click", () => {
      this._mileageSourceEditing = false;
      this._render();
    });
    root.getElementById("confirm-link-btn")?.addEventListener("click", () => {
      if (!this._pendingSensorEntity) {
        alert("Choisissez un capteur avant de valider.");
        return;
      }
      this._setMileageSource(this._selectedId, "sensor", this._pendingSensorEntity);
    });
    root.getElementById("unlink-sensor-btn")?.addEventListener("click", () => {
      this._setMileageSource(this._selectedId, "manual", null);
    });

    root.getElementById("refresh-plan-btn")?.addEventListener("click", () => this._refreshPlan(this._selectedId));
    root.getElementById("refresh-issues-btn")?.addEventListener("click", () => this._refreshKnownIssues(this._selectedId));
    root.getElementById("refresh-recalls-btn")?.addEventListener("click", () => this._refreshRecalls(this._selectedId));
    root.getElementById("snapshot-btn")?.addEventListener("click", () => this._valueSnapshot(this._selectedId));

    root.querySelectorAll(".done-today-btn").forEach((btn) =>
      btn.addEventListener("click", () => {
        this._logMaintenance(this._selectedId, {
          item_id: btn.dataset.itemId,
          item_name: btn.dataset.itemName,
          km: this._selectedVehicle.mileage,
          date: Math.floor(Date.now() / 1000),
        });
      })
    );
    root.querySelectorAll(".log-save-btn").forEach((btn) =>
      btn.addEventListener("click", () => {
        const itemId = btn.dataset.itemId;
        const itemName = btn.dataset.itemName;
        const dateInput = root.querySelector(`.log-date-input[data-item-id="${itemId}"]`);
        const kmInput = root.querySelector(`.log-km-input[data-item-id="${itemId}"]`);
        const km = parseInt(kmInput.value, 10);
        if (!dateInput.value || isNaN(km)) {
          alert("Merci de renseigner une date et un kilométrage valides.");
          return;
        }
        const dateTs = Math.floor(new Date(dateInput.value + "T12:00:00").getTime() / 1000);
        this._logMaintenance(this._selectedId, { item_id: itemId, item_name: itemName, km, date: dateTs });
      })
    );

    root.querySelectorAll(".applicable-cb").forEach((cb) =>
      cb.addEventListener("change", (e) => {
        this._setItemApplicable(this._selectedId, e.target.dataset.itemId, e.target.checked);
      })
    );
    root.querySelectorAll(".override-save-btn").forEach((btn) =>
      btn.addEventListener("click", () => {
        const itemId = btn.dataset.itemId;
        const kmInput = root.querySelector(`.override-km-input[data-item-id="${itemId}"]`);
        const dateInput = root.querySelector(`.override-date-input[data-item-id="${itemId}"]`);
        const km = kmInput.value.trim() === "" ? null : parseInt(kmInput.value, 10);
        const dateTs = dateInput.value ? Math.floor(new Date(dateInput.value + "T12:00:00").getTime() / 1000) : null;
        this._setItemOverride(this._selectedId, itemId, km, dateTs);
      })
    );
    root.querySelectorAll(".diy-generate-btn").forEach((btn) =>
      btn.addEventListener("click", () => this._generateDiyExplanation(this._selectedId, btn.dataset.itemId))
    );
    root.querySelectorAll("[id^='remove-item-']").forEach((btn) =>
      btn.addEventListener("click", () => this._removePlanItem(this._selectedId, btn.dataset.itemId))
    );

    root.getElementById("add-item-btn")?.addEventListener("click", () => {
      const box = root.getElementById("add-item-form");
      if (box.style.display === "none") {
        box.style.display = "block";
        box.innerHTML = `
          <div class="sensor-link-box" style="margin-top:8px;">
            <label>Nom de l'entretien<input type="text" id="new-item-name" placeholder="Ex : Remplacement rotule de direction" /></label>
            <div class="row-2">
              <label>Intervalle (km)<input type="number" id="new-item-km" min="0" value="0" /></label>
              <label>Intervalle (mois)<input type="number" id="new-item-months" min="0" value="0" /></label>
            </div>
            <label>Coût estimé (€, optionnel)<input type="number" id="new-item-cost" min="0" /></label>
            <button class="btn small primary full" id="new-item-save-btn" style="margin-top:8px;">Ajouter</button>
          </div>`;
        root.getElementById("new-item-save-btn").addEventListener("click", () => {
          const name = root.getElementById("new-item-name").value.trim();
          if (!name) {
            alert("Donnez un nom à cet entretien.");
            return;
          }
          const interval_km = parseInt(root.getElementById("new-item-km").value, 10) || 0;
          const interval_months = parseInt(root.getElementById("new-item-months").value, 10) || 0;
          const costRaw = root.getElementById("new-item-cost").value;
          this._addPlanItem(this._selectedId, {
            name, interval_km, interval_months,
            cost_estimate_eur: costRaw ? parseFloat(costRaw) : undefined,
          });
        });
      } else {
        box.style.display = "none";
      }
    });
    root.getElementById("add-log-btn")?.addEventListener("click", () => {
      const item_name = prompt("Intervention réalisée :");
      if (!item_name) return;
      const km = prompt("Kilométrage :", this._selectedVehicle.mileage);
      if (km === null) return;
      this._logMaintenance(this._selectedId, { item_name, km: parseInt(km, 10) });
    });

    this._mountEntityPicker();
  }

  _mountEntityPicker() {
    const root = this.shadowRoot;
    const slot = root.getElementById("entity-picker-slot");
    if (!slot) return;
    if (customElements.get("ha-entity-picker")) {
      const picker = document.createElement("ha-entity-picker");
      picker.hass = this._hass;
      picker.value = this._pendingSensorEntity || "";
      picker.includeDomains = ["sensor", "input_number"];
      picker.label = "Capteur de kilométrage";
      picker.style.display = "block";
      picker.style.width = "100%";
      picker.addEventListener("value-changed", (e) => {
        this._pendingSensorEntity = e.detail.value;
      });
      slot.appendChild(picker);
    } else {
      slot.innerHTML = `<input type="text" id="sensor-entity-fallback" placeholder="sensor.mon_capteur_km" value="${esc(this._pendingSensorEntity || "")}" />`;
      slot.querySelector("#sensor-entity-fallback").addEventListener("input", (e) => {
        this._pendingSensorEntity = e.target.value;
      });
    }
  }
}

// ---------------------------------------------------------------- helpers

function esc(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}
function fmtKm(n) {
  return n == null ? "" : `${Math.round(n).toLocaleString("fr-FR")} km`;
}
function fmtEur(n) {
  return n == null ? "" : `${Math.round(n).toLocaleString("fr-FR")} €`;
}
function fmtDate(unixSeconds) {
  if (!unixSeconds) return "";
  return new Date(unixSeconds * 1000).toLocaleDateString("fr-FR");
}
function todayIso() {
  return new Date().toISOString().slice(0, 10);
}
function isoDateFromUnix(unixSeconds) {
  return new Date(unixSeconds * 1000).toISOString().slice(0, 10);
}

// Compresse/redimensionne une image côté navigateur avant envoi, pour ne
// pas gonfler le fichier de stockage JSON local (photos gardées < ~150 Ko).
function fileToCompressedDataUrl(file, maxDim = 480, quality = 0.72) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const img = new Image();
      img.onload = () => {
        let { width, height } = img;
        if (width > height && width > maxDim) {
          height = Math.round((height * maxDim) / width);
          width = maxDim;
        } else if (height > maxDim) {
          width = Math.round((width * maxDim) / height);
          height = maxDim;
        }
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        canvas.getContext("2d").drawImage(img, 0, 0, width, height);
        resolve(canvas.toDataURL("image/jpeg", quality));
      };
      img.onerror = reject;
      img.src = reader.result;
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

function renderValueChart(history) {
  const w = 300, h = 110, pad = 20;
  const values = history.map((p) => p.value_avg);
  const min = Math.min(...values) * 0.95;
  const max = Math.max(...values) * 1.05;
  const points = history.map((p, i) => {
    const x = pad + (i / Math.max(history.length - 1, 1)) * (w - 2 * pad);
    const y = h - pad - ((p.value_avg - min) / Math.max(max - min, 1)) * (h - 2 * pad);
    return `${x},${y}`;
  });
  return `
    <svg viewBox="0 0 ${w} ${h}" class="chart">
      <polyline points="${points.join(" ")}" fill="none" stroke="var(--ce-accent)" stroke-width="2.5" />
      ${points
        .map((p) => {
          const [x, y] = p.split(",");
          return `<circle cx="${x}" cy="${y}" r="3" fill="var(--ce-accent)" />`;
        })
        .join("")}
    </svg>
  `;
}

const STYLE = `
  :host { display:block; }
  ha-card {
    padding: 14px 16px 18px;
    container-type: inline-size;
    background: var(--ce-bg);
    color: var(--ce-text);
    border-radius: 14px;
    box-shadow: none;
  }
  .header { display:flex; align-items:center; justify-content:space-between; margin-bottom: 8px; }
  .header-actions { display:flex; align-items:center; gap:6px; }
  .title { font-family: var(--ce-font-header); font-size: 1.2em; font-weight: 600; letter-spacing:0.2px; color: var(--ce-text); }
  .btn { border:none; border-radius: 8px; padding: 8px 14px; font-size: 0.9em; cursor:pointer; background: var(--ce-surface); color: var(--ce-text); font-family: inherit; }
  .btn.primary { background: var(--ce-accent); color: var(--ce-accent-contrast); font-weight:600; }
  .btn.danger { background: var(--ce-danger); color: #F5E6E0; }
  .btn.ghost { background: transparent; border: 1px solid var(--ce-border); color: var(--ce-text-muted); }
  .btn.icon { padding: 8px 10px; }
  .btn.small { padding: 5px 10px; font-size: 0.82em; }
  .btn.tiny { padding: 3px 8px; font-size: 0.75em; margin-top: 8px; }
  .btn.full { width: 100%; margin-top: 8px; }
  .empty { padding: 20px 8px; text-align:center; color: var(--ce-text-dim); }
  .muted { color: var(--ce-text-muted); }
  .small { font-size: 0.82em; }
  .mono { font-family: 'Courier New', monospace; }
  .accent { color: var(--ce-accent); font-weight:600; }

  .grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }
  .tile { position:relative; background: var(--ce-surface); border: 1px solid var(--ce-border); border-radius: 10px; padding: 12px; cursor:pointer; overflow:hidden; }
  .tile-photo { width:100%; height:80px; object-fit:cover; border-radius:6px; margin-bottom:8px; display:block; }
  .tile-badge { position:absolute; top:0; left:0; width:4px; height:100%; }
  .tile-title { font-family: var(--ce-font-header); font-weight:600; margin-left: 6px; color: var(--ce-text); }
  .tile-sub { margin-left:6px; font-size:0.85em; color: var(--ce-text-muted); }
  .tile-next { margin-left:6px; margin-top:8px; font-size:0.8em; color: var(--ce-text-muted); }

  .autocomplete { position:relative; }
  .suggestions { display:none; position:absolute; top:100%; left:0; right:0; margin-top:4px; background: var(--ce-surface); border: 1px solid var(--ce-border); border-radius: 8px; max-height:190px; overflow-y:auto; z-index:30; }
  .suggestions.open { display:block; }
  .suggestion-item { padding: 9px 12px; font-size: 0.9em; cursor:pointer; color: var(--ce-text); }
  .suggestion-item:hover { background: var(--ce-surface-2); }
  .photo-preview { max-width:100%; border-radius:8px; margin-top:2px; max-height:160px; object-fit:cover; }

  .detail-header-main { display:flex; align-items:center; gap:12px; }
  .vehicle-photo { width:56px; height:56px; border-radius:10px; object-fit:cover; flex-shrink:0; }
  .vehicle-photo.placeholder { display:flex; align-items:center; justify-content:center; background: var(--ce-surface); font-size:24px; }
  .photo-controls { display:flex; gap:10px; margin-top:4px; }
  .link-btn { background:none; border:none; padding:0; color: var(--ce-accent); font-size: 0.76em; cursor:pointer; font-family:inherit; }
  .checkbox-row { display:flex; align-items:center; gap:8px; font-size:0.85em; color: var(--ce-text); cursor:pointer; }
  .checkbox-row input { width:auto; }
  .diy-badge { font-size:0.68em; padding:1px 6px; border-radius:999px; background: var(--ce-surface-2); color: var(--ce-text-muted); white-space:nowrap; }
  .diy-box { background: var(--ce-surface-2); border-radius: 8px; padding: 8px 10px; margin-top: 4px; font-size: 0.85em; line-height:1.45; }
  .diy-warning { color: var(--ce-danger-text); font-size: 0.85em; margin-bottom: 6px; font-weight:600; }

  .theme-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px; }
  .theme-card { background: var(--ce-surface); border: 1px solid var(--ce-border); border-radius: 10px; padding: 12px; cursor:pointer; }
  .theme-card.active { border-color: var(--ce-accent); }
  .theme-card-head { display:flex; justify-content:space-between; align-items:center; font-size:0.88em; margin-bottom:8px; }
  .swatches { display:flex; gap:6px; }
  .swatches span { width:16px; height:16px; border-radius:4px; display:inline-block; }

  .form { display:flex; flex-direction:column; gap: 10px; }
  .form label { display:flex; flex-direction:column; gap:4px; font-size:0.85em; color: var(--ce-text-muted); }
  .form input { padding: 8px 10px; border-radius: 8px; border: 1px solid var(--ce-border); background: var(--ce-surface); color: var(--ce-text); font-size: 0.95em; }
  .row-2 { display:flex; gap:10px; }
  .row-2 label, .row-2 .btn { flex:1; }

  .detail-header { display:flex; align-items:flex-start; justify-content:space-between; padding-bottom:12px; border-bottom-width:1px; border-bottom-style:var(--ce-divider-style); border-bottom-color:var(--ce-border); }
  .detail-title { font-family: var(--ce-font-header); font-size: 1.15em; font-weight: 600; color: var(--ce-text); }
  .plate-chip { display:inline-block; margin-top:5px; padding:2px 8px; border:1px solid var(--ce-border); border-radius:4px; font-size:0.76em; letter-spacing:1px; color: var(--ce-text-muted); }

  .switcher-row { display:flex; align-items:center; gap:8px; margin-top:10px; }
  .switcher-row select { flex:1; padding:7px 8px; border-radius:8px; border:1px solid var(--ce-border); background: var(--ce-surface); color: var(--ce-text); font-size:0.88em; }

  .mileage-row { display:flex; align-items:center; gap:8px; margin: 12px 0 4px; flex-wrap:wrap; }
  .mileage-row input { width: 100px; padding:6px 8px; border-radius:8px; border:1px solid var(--ce-border); background: var(--ce-surface); color: var(--ce-text); }
  .sensor-link-box { background: var(--ce-surface); border: 1px solid var(--ce-border); border-radius: 10px; padding: 10px 12px; margin: 8px 0 4px; }
  .sensor-link-box ha-entity-picker { --mdc-theme-primary: var(--ce-accent); }

  .tabs { display:flex; gap: 4px; overflow-x:auto; border-bottom-width:1px; border-bottom-style:var(--ce-divider-style); border-bottom-color:var(--ce-border); margin: 10px 0; }
  .tab { padding: 8px 10px; font-size: 0.85em; cursor:pointer; white-space:nowrap; border-bottom: 2px solid transparent; color: var(--ce-text-muted); }
  .tab.active { color: var(--ce-accent); border-bottom-color: var(--ce-accent); font-weight:600; }

  .panel { background: var(--ce-surface); border-radius: 10px; margin-bottom: 8px; overflow:hidden; }
  .panel summary { cursor:pointer; list-style:none; display:flex; justify-content:space-between; align-items:center; padding: 10px 12px; font-size: 0.9em; }
  .panel summary::-webkit-details-marker { display:none; }
  .panel summary::after { content:"›"; color: var(--ce-text-dim); margin-left:8px; transform: rotate(90deg); display:inline-block; transition: transform .15s ease; }
  .panel[open] summary::after { transform: rotate(-90deg); }
  .panel-body { padding: 0 12px 12px; }

  .section-label { font-size: 0.72em; text-transform:uppercase; letter-spacing:0.6px; color: var(--ce-text-dim); margin: 16px 2px 8px; }

  .toolbar { margin-bottom: 8px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:6px; }
  .plan-list { display:flex; flex-direction:column; }
  .plan-row { padding: 9px 2px; border-top-width:1px; border-top-style:var(--ce-divider-style); border-top-color:var(--ce-border); }
  .plan-row.na { opacity:0.65; }
  .plan-row-summary { cursor:pointer; list-style:none; }
  .plan-row-summary::-webkit-details-marker { display:none; }
  .plan-row-head { display:flex; justify-content:space-between; align-items:center; font-size:0.92em; margin-bottom:6px; color: var(--ce-text); }
  .plan-row-meta { margin-top:5px; }
  .plan-row-edit { padding: 12px 2px 4px; }
  .plan-row-edit label { display:flex; flex-direction:column; gap:4px; font-size:0.8em; color: var(--ce-text-muted); margin-bottom:8px; }
  .plan-row-edit input { padding: 7px 9px; border-radius: 8px; border: 1px solid var(--ce-border); background: var(--ce-surface-2); color: var(--ce-text); font-size: 0.9em; width:100%; box-sizing:border-box; }
  .edit-divider { display:flex; align-items:center; gap:8px; margin:12px 0; font-size:0.7em; color: var(--ce-text-dim); }
  .edit-divider::before, .edit-divider::after { content:""; flex:1; height:1px; background: var(--ce-border); }
  .bar { height:5px; border-radius:3px; background: var(--ce-border); overflow:hidden; }
  .bar-fill { height:100%; border-radius:3px; }

  .issue-list, .log-list { display:flex; flex-direction:column; gap:8px; }
  .issue-item, .log-item { border-top-width:1px; border-top-style:var(--ce-divider-style); border-top-color:var(--ce-border); padding: 8px 2px; }
  .issue-head { display:flex; align-items:center; justify-content:space-between; font-weight:600; font-size:0.9em; margin-bottom:3px; }
  .status-chip { color: var(--ce-chip-text); font-size:0.72em; font-weight:600; padding: 2px 8px; border-radius: 999px; white-space:nowrap; }

  .disclaimer { color: var(--ce-text-dim); font-size: 0.78em; line-height:1.4; margin: 8px 0; }
  .sources-box { background: var(--ce-surface-2); border-radius: 8px; padding: 8px 10px; margin: 10px 0; font-size: 0.82em; line-height:1.45; }
  .value-range { margin: 6px 0 8px; }

  .chart { width:100%; height:110px; margin: 8px 0; }

  .loading { display:flex; align-items:center; gap:10px; padding: 8px 4px; font-size:0.85em; color: var(--ce-text-muted); }
  .spinner { width:16px; height:16px; border-radius:50%; border:2px solid var(--ce-border); border-top-color: var(--ce-accent); animation: spin 0.8s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }

  @container (max-width: 420px) {
    .grid, .theme-grid { grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); }
  }

  /* ---------------- Thèmes ---------------- */

  ha-card[data-theme="gt_cuir"] {
    --ce-bg:#2B1B12; --ce-surface:#3A2519; --ce-surface-2:#45301F; --ce-border:#5A4230; --ce-divider-style:dashed;
    --ce-accent:#C08A4E; --ce-accent-contrast:#2B1B12;
    --ce-text:#EDE0C8; --ce-text-muted:#B8A088; --ce-text-dim:#8A755F; --ce-chip-text:#2B1B12;
    --ce-danger:#B33A3A; --ce-danger-text:#D98A8A;
    --ce-font-header: Georgia, 'Times New Roman', serif;
    --ce-status-ok:#8A9A5B; --ce-status-bientot:#C08A4E; --ce-status-echue:#B33A3A; --ce-status-non_applicable:#7A6350;
    --ce-severity-mineur:#8A9A5B; --ce-severity-majeur:#C08A4E; --ce-severity-securite:#B33A3A;
  }
  ha-card[data-theme="horlogerie"] {
    --ce-bg:#0F1B2E; --ce-surface:#16263D; --ce-surface-2:#1C2F4A; --ce-border:#2A3E5C; --ce-divider-style:solid;
    --ce-accent:#7C93B5; --ce-accent-contrast:#0F1B2E;
    --ce-text:#E8EBEF; --ce-text-muted:#9DA8B8; --ce-text-dim:#5C6A80; --ce-chip-text:#E8EBEF;
    --ce-danger:#A6192E; --ce-danger-text:#E08A8A;
    --ce-font-header: 'Helvetica Neue', Arial, sans-serif;
    --ce-status-ok:#5C8A6E; --ce-status-bientot:#C9A227; --ce-status-echue:#A6192E; --ce-status-non_applicable:#5C6A80;
    --ce-severity-mineur:#5C8A6E; --ce-severity-majeur:#C9A227; --ce-severity-securite:#A6192E;
  }
  ha-card[data-theme="carbone"] {
    --ce-bg:#0B0C0E; --ce-surface:#16181C; --ce-surface-2:#1E2126; --ce-border:#2A2E35; --ce-divider-style:solid;
    --ce-accent:#35D0E0; --ce-accent-contrast:#0B0C0E;
    --ce-text:#E4E7EA; --ce-text-muted:#9AA3AC; --ce-text-dim:#5A6470; --ce-chip-text:#0B0C0E;
    --ce-danger:#E0473F; --ce-danger-text:#FF8A80;
    --ce-font-header: 'Courier New', monospace;
    --ce-status-ok:#35D0E0; --ce-status-bientot:#E0A93F; --ce-status-echue:#E0473F; --ce-status-non_applicable:#5A6470;
    --ce-severity-mineur:#35D0E0; --ce-severity-majeur:#E0A93F; --ce-severity-securite:#E0473F;
  }
  ha-card[data-theme="vintage"] {
    --ce-bg:#EDE6D6; --ce-surface:#E3D9C2; --ce-surface-2:#D8CBAE; --ce-border:#C9B98F; --ce-divider-style:dashed;
    --ce-accent:#14532D; --ce-accent-contrast:#EDE6D6;
    --ce-text:#3A2E22; --ce-text-muted:#7A6A52; --ce-text-dim:#A8987C; --ce-chip-text:#EDE6D6;
    --ce-danger:#8C2F2F; --ce-danger-text:#8C2F2F;
    --ce-font-header: Georgia, 'Times New Roman', serif;
    --ce-status-ok:#14532D; --ce-status-bientot:#B08D57; --ce-status-echue:#8C2F2F; --ce-status-non_applicable:#A8987C;
    --ce-severity-mineur:#14532D; --ce-severity-majeur:#B08D57; --ce-severity-securite:#8C2F2F;
  }
`;

customElements.define("carnet-entretien-card", CarnetEntretienCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "carnet-entretien-card",
  name: "Carnet d'entretien",
  description: "Suivi d'entretien véhicule avec 4 thèmes visuels premium, plan généré par IA, points de vigilance et valeur de revente.",
});
