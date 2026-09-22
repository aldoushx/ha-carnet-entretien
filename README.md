<p align="center"><img src="badge.svg" width="360" height="360" alt="CARnet - Garage Log" /></p>

<h1 align="center">CARnet - Garage Log</h1>
<p align="center">Smart vehicle maintenance logbook for Home Assistant</p>

<p align="center">
<img alt="HACS Custom" src="https://img.shields.io/badge/HACS-Custom-41BDF5?logo=homeassistantcommunitystore&logoColor=white">
<img alt="Home Assistant" src="https://img.shields.io/badge/Home%20Assistant-2024.1%2B-41BDF5?logo=home-assistant&logoColor=white">
<img alt="License" src="https://img.shields.io/badge/license-MIT-blue">
<img alt="Version" src="https://img.shields.io/badge/version-1.4.1-orange">
</p>

<p align="center"><a href="#english">English</a> · <a href="#français">Français</a></p>

---

<a id="english"></a>
## 🇬🇧 English

**CARnet - Garage Log** is a smart maintenance logbook for **cars,
motorcycles, scooters and e-bikes** in Home Assistant. It uses **Google
Gemini** (free tier available) to generate and keep up to date:
a maintenance plan built from a fixed catalog of operations per vehicle
type, known issues/weak points for the exact model, active manufacturer
recalls, and a resale value estimate over time — all shown on a dedicated
Lovelace card with four visual themes and full support for English,
French, German, Spanish and Italian.

Storage is 100% local (no cloud account, no telemetry). The card is
served directly by the integration — nothing to copy into `www/` — you
only need to register it as a dashboard resource once (see
[§4](#4-add-the-card-to-a-dashboard)). 

### 🌟 Beyond a basic logbook

A spreadsheet or a paper logbook can log what you've already done. CARnet
is built to do the part that's actually tedious: figuring out **what needs
doing, when, at what cost, and how** — for your exact vehicle, not a
generic one.

- 🔍 **A maintenance plan built from real research, not a generic
  template.** For the exact brand/model/engine/year you enter, Gemini
  researches the manufacturer's official service schedule and
  garage/technical-guide sources to decide which of the catalog's fixed
  operations actually apply and at what interval — instead of one generic
  "every 10,000 km" rule applied blindly to every car.
- 🛠️ **DIY cost and step-by-step guidance, generated on demand.** Every
  item shows an estimated parts-only cost alongside the garage price, and
  a "how do I do this myself?" button generates a detailed, model-specific
  DIY explanation (tools, steps, difficulty) — not just a checkbox telling
  you an operation is due.
- 💶 **Estimated cost per operation**, garage price and DIY price side by
  side, so you can decide in advance whether a given job is worth doing
  yourself.
- 🔔 **Due-date notifications**, not just a dashboard you have to
  remember to check — the integration raises a Home Assistant persistent
  notification (and can drive your own automations/`notify.*` calls, see
  [§6](#6-automate-with-services)) as soon as an item becomes overdue or a
  mileage-based reminder is reached.
- 🔗 **Real mileage, not a manual guess.** Link an existing Home Assistant
  sensor (OBD dongle, OEM odometer integration, `input_number`...) instead
  of typing the mileage in by hand every time — due dates and "km
  remaining" recalculate automatically as the linked sensor updates.
- 📈 **A resale value estimate grounded in the current market**, not a
  static depreciation curve — Gemini looks at market trend, mileage
  versus the segment average and the vehicle's condition to produce a
  price range with a written rationale, trackable over time.
- ⚠️ **An inventory of the most frequently reported issues** for that
  exact model — the weak points other owners and garages report most
  often, with severity and an indicative repair cost — so you know what
  to watch for before it becomes an expensive surprise, plus active
  manufacturer recalls researched on creation.

### ✨ Features

- 🚗🏍️🛵🚲 **Cars, motorcycles/scooters and e-bikes**, each with a
  completely separate maintenance catalog: a car never sees a motorcycle
  item, even as "not applicable" — brand/model/engine autocomplete
  (local reference list + cached Gemini suggestions), year, mileage,
  plate, photo.
- 🛠️ **Fixed maintenance catalog per vehicle type** (46 operations for a
  car, 26 for a motorcycle/scooter, 15 for an e-bike): oil change, every
  filter, timing belt/chain and accessory belt as separate entries,
  front/rear discs and pads as separate entries, battery, A/C,
  DPF/EGR, roadworthiness inspection, manufacturer service schedule,
  motorcycle chain kit, traction battery diagnostics... The AI only
  decides applicability and intervals for each fixed entry — nothing can
  ever be silently dropped between two generations. Each item shows:
  km/month interval, estimated garage cost, a real forecast date, DIY
  difficulty and parts-only cost, with a detailed how-to generated on
  demand.
- ✏️ **Manual corrections at any time**: an applicable/not-applicable
  checkbox per item, direct override of a due date or due mileage, and
  the ability to add a missing operation without regenerating the whole
  plan.
- ⚠️ **Known issues & weak points** specific to the exact model, with
  severity, an indicative repair cost and cited source types.
- 🚨 **Active manufacturer recalls**, researched by the AI on creation,
  shared across identical vehicles and refreshable on demand, with a
  reminder to double-check on official channels.
- 💶 **Resale value tracking** over time, with a price range and a
  written rationale (market trend, depreciation, mileage).
- 📆 **Timestamped maintenance history**: every item can be expanded to
  log a service ("done today" button, or an earlier date/mileage), which
  immediately recalculates the next due dates.
- 🔗 **Manual mileage or linked to an existing Home Assistant sensor**
  (OEM odometer, OBD dongle, `input_number`...).
- 🎨 **4 visual themes**: Grand Tourisme Leather, Watchmaker's Workshop,
  Carbon & Titanium, Vintage Atelier — persisted through a dedicated
  settings panel.
- 🌍 **Multilingual**: English, French, German, Spanish, Italian — one
  language for the whole installation (card, catalog names, AI-generated
  text, persistent notifications), chosen once when you add the
  integration (see [§3](#3-configure-the-integration)).
- 🚙 **Multiple vehicles** with a quick switcher and a tile overview.
- 🔧 **Home Assistant services** to drive everything from automations
  (`add_vehicle`, `update_mileage`, `log_maintenance`, `value_snapshot`,
  `set_mileage_source`...).

### 1. Requirements

- Home Assistant 2024.1 or newer.
- (Optional but recommended) A free Gemini API key — without a key you
  can still create vehicles and fill in the logbook manually, but without
  automatic generation of the plan, known issues or the value estimate.
  To get one:
  1. Go to [aistudio.google.com](https://aistudio.google.com) and sign in
     with a Google account.
  2. Click **Get API key** (left sidebar) → **Create API key**.
  3. Pick an existing Google Cloud project or let it create a new one for
     you — no billing information is required for the free tier.
  4. Copy the key (starts with `AIza...`) and paste it into the
     integration's setup screen (see [§3](#3-configure-the-integration)).
     The free tier's daily quota is generous for personal use; if you ever
     hit it, the integration automatically retries with other Gemini
     models (see [§8](#8-troubleshooting)).
- HACS if you want the "custom repository" route (a manual install works
  just as well, see below).

### 2. Installation

**Option A — HACS (custom repository)**

1. In HACS → ⋮ (top-right menu) → **Custom repositories**.
2. Paste this repository's URL, category **Integration**.
3. Search for "CARnet - Garage Log" in HACS, install it, then **restart
   Home Assistant**.

**Option B — Manual installation**

1. Copy the `custom_components/carnet_entretien/` folder as-is into
   `config/custom_components/` on your Home Assistant instance (via
   Samba, SSH, or the File Editor add-on).
2. Check the resulting tree:
   ```
   config/
     custom_components/
       carnet_entretien/
         __init__.py
         config_flow.py
         const.py
         catalog_i18n.py
         gemini_client.py
         maintenance_catalog.py
         manifest.json
         sensor.py
         services.yaml
         storage.py
         utils.py
         strings.json
         translations/
         data/referentiel.json
         brand/icon.png, icon@2x.png
         www/carnet-entretien-card.js
   ```
3. **Restart Home Assistant** (Settings → System → Restart).

### 3. Configure the integration

1. **Settings → Devices & services → Add integration**.
2. Search for **CARnet - Garage Log**.
3. Fill in your Gemini API key if you have one (optional field, leave it
   empty otherwise), and **choose the content language** (English,
   French, German, Spanish or Italian) — this single setting drives the
   card's interface, the catalog's item names, everything Gemini
   generates, and persistent notifications.
4. Confirm. No device/entity appears yet — they are created as you add
   vehicles from the card.

Both the API key and the language can be changed later from
**Settings → Devices & services → CARnet - Garage Log → Configure**
(the integration's Options). Changing the language does not retroactively
translate content Gemini already generated for existing vehicles (notes,
known issues, recalls, DIY explanations, resale value) — that stays in
its original language until you regenerate it (the "↻ Regenerate plan"
button, refreshing known issues/recalls, or a new DIY request). This is
intentional: switching languages never silently spends AI quota on its
own.

### 4. Add the card to a dashboard

**One-time manual step** — unlike some similar integrations, the card's
JS resource is **not** auto-registered: that mechanism
(`add_extra_js_url`) turned out to be unreliable on some Home Assistant
versions (silent failure, nothing in the logs). Adding it by hand through
the standard HA UI is guaranteed to work on any version:

1. **Settings → Dashboards** → **⋮** (top-right menu) → **Resources**.
2. **Add resource**:
   - URL: `/carnet_entretien/carnet-entretien-card.js`
   - Resource type: **JavaScript module**
3. Save, then **force a full browser cache reload**
   (Ctrl+Shift+R / Cmd+Shift+R).
4. Open a dashboard → **Edit dashboard** → **Add card** → search for
   **"CARnet - Garage Log"** in the list (or pick "Manual" and paste the
   YAML below).
5. Minimal YAML:
   ```yaml
   type: custom:carnet-entretien-card
   ```

After updating the integration, the file's content changes but not its
URL: reloading the browser cache is enough, no need to touch the resource
again.

#### The card doesn't appear / "Custom element doesn't exist"

This is almost always the resource above missing, misspelled, or cached
by the browser. Go through this checklist in order:

1. **Resource actually registered?** Settings → Dashboards → ⋮ →
   Resources. You should see `/carnet_entretien/carnet-entretien-card.js`
   with type **JavaScript module** (not "CSS" or "HTML"). If it's
   missing, add it as described above.
2. **Typo in the URL?** It must be exactly
   `/carnet_entretien/carnet-entretien-card.js` — no `www/`, no version
   suffix, the leading slash matters.
3. **Hard-reload the browser.** Ctrl+Shift+R / Cmd+Shift+R (or clear the
   site's cache) on every device/browser used to view the dashboard —
   including the mobile app's internal browser, which caches separately
   (fully close and reopen the Companion App if needed).
4. **Check the file is actually served.** Open
   `http://YOUR-HA-ADDRESS:8123/carnet_entretien/carnet-entretien-card.js`
   directly in a browser tab (adjust the address/port). You should see
   raw JavaScript. If you get a 404: the integration's static route
   failed to register — check step 5.
5. **Check the Home Assistant logs** (Settings → System → Logs) for any
   line mentioning `carnet_entretien` right after startup — in
   particular a failure to register the static path, or a missing file.
   If you installed manually, double-check every file listed in
   [§2](#2-installation) is present (a partial copy, e.g. forgetting the
   `www/` folder or `data/referentiel.json`, breaks things silently).
6. **Duplicate resource.** If you added the resource more than once
   (e.g. once manually and once by an older version's now-removed
   auto-registration), remove the duplicates — HA can get confused about
   which one to load, especially after an update. Keep exactly one entry
   pointing at the URL above.
7. **Still stuck?** Remove the resource entirely, hard-reload the
   browser, restart Home Assistant, then add the resource again from
   scratch (step-by-step as above). This clears any stale in-browser or
   in-HA state left over from an earlier attempt.

### 5. First use

1. Click **➕ Add** on the card.
2. Pick **🚗 Car** or **🏍️ Two-wheeler** (motorcycle / scooter / e-bike);
   this decides which maintenance catalog and which brand/model
   suggestions apply — the two never mix.
3. **Brand**: start typing, an autocomplete dropdown appears.
   You can also type a brand that isn't listed: free text is always
   accepted.
4. **Model**: the list filters by the chosen brand, same free-text
   fallback.
5. Fill in the engine/motor (optional — an instant Gemini-powered
   suggestion list appears once brand/model/year are set), year, current
   mileage, plate (optional), fuel/energy type, photo (optional).
6. Confirm: three generation steps run in sequence (manufacturer info →
   maintenance plan → known issues), 15 to 45 seconds depending on the
   Gemini API's load.
7. You land on the vehicle page with four tabs:
   - **🔧 Maintenance**: due items sorted by urgency, with a progress bar
     and a "✓ Done" button to log a service.
   - **⚠️ Known issues**: documented weak points for this exact model, by
     severity, with a banner reminding it's an AI summary, not certified
     manufacturer data.
   - **💶 Value**: an "Estimate now" button → a resale value curve over
     time, to re-run periodically (manually, or via automation using the
     `value_snapshot` service).
   - **📓 History**: the service log.

### 6. Automate with services

All services are visible under **Developer tools → Actions**, prefixed
`carnet_entretien.`. Examples:

**Weekly value estimate reminder** (`automations.yaml`):
```yaml
alias: Vehicle value estimate - weekly
trigger:
  - platform: time
    at: "08:00:00"
condition:
  - condition: time
    weekday: [mon]
action:
  - service: carnet_entretien.value_snapshot
    data:
      vehicle_id: "YOUR_VEHICLE_ID"
```

**Notify when an item becomes due** — use the
`sensor.<brand>_<model>_next_due_item` sensor directly, `statut`
attribute:
```yaml
alias: Vehicle maintenance alert
trigger:
  - platform: state
    entity_id: sensor.peugeot_308_prochaine_echeance
    attribute: statut
    to: "echue"
action:
  - service: notify.mobile_app_your_phone
    data:
      message: >
        Overdue item on the 308: {{ state_attr('sensor.peugeot_308_prochaine_echeance','km_restants') }} km overdue.
```

Each vehicle's `id` is visible in its sensors' attributes, or by clicking
the vehicle in the card and inspecting the corresponding device under
Settings → Devices.

### 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Card doesn't appear / "Custom element doesn't exist" | Lovelace resource missing, mistyped or cached | See the full checklist in [§4](#the-card-doesnt-appear--custom-element-doesnt-exist) |
| "no_model" when adding a vehicle | No Gemini key configured, or an invalid one | Set/check the key from the integration's Options |
| "rate_limited" / "Quota exceeded" | Daily Gemini quota reached on that model | Wait, or try again — the integration automatically falls back to other models |
| "timeout" | Gemini API slow or overloaded | Retry; the "↻ Regenerate" button re-issues the call |
| "truncated" | Response cut off by the token limit | Already mitigated with generous token budgets; if it persists, reduce the number of requested items in `gemini_client.py` |
| Hidden ("not applicable") items keep reappearing | Historic bug, fixed in v1.3.2 (a settings-save schema was silently rejecting the setting) | Update to the latest version |
| Text is in the wrong language after switching | Only the interface/catalog translate instantly; AI-generated content (notes, known issues, DIY...) keeps its original language until regenerated | Use "↻ Regenerate plan" / refresh known issues or recalls / a new DIY request |
| Entities missing after removing a vehicle | Expected, transient | They're removed from the registry automatically on removal |

### 9. Known limitations

- **Brand/model reference list**: deliberately curated, not exhaustive —
  extend it per [§7](#7-customize-the-brandmodel-reference-list), or
  replace it with a call to an open vehicle database if you want it fully
  automated.
- **Annual mileage estimate**: used to rank due items against each other
  (`utils.py`), based on the vehicle's mileage history; not very reliable
  until a few data points exist (falls back to registration-year-based
  estimate, then a flat default).
- **No automated tests** included in this project — consider adding some
  (pytest + `pytest-homeassistant-custom-component`) before a wide public
  release.
- **AI content is a summary, not certified data** — known issues, recalls
  and DIY guidance are Gemini's best synthesis of public information, not
  a manufacturer source; always double-check anything safety-related.

### 🤝 Contributing

Feedback, issues and pull requests are welcome.

### 📜 License

MIT — see [LICENSE](LICENSE).

---

<a id="français"></a>
## 🇫🇷 Français

**CARnet - Garage Log** est un carnet d'entretien intelligent pour
**voitures, motos, scooters et vélos électriques** dans Home Assistant.
Il s'appuie sur **Google Gemini** (un forfait gratuit est
disponible) pour générer et tenir à jour : un plan d'entretien basé sur un
catalogue fixe d'opérations par type de véhicule, les points de vigilance
connus sur le modèle précis, les rappels constructeur actifs, et une
estimation de valeur de revente dans le temps — le tout affiché sur une
carte Lovelace dédiée avec quatre thèmes visuels et une prise en charge
complète du français, de l'anglais, de l'allemand, de l'espagnol et de
l'italien.

Le stockage est 100 % local (aucun compte cloud, aucune télémétrie). La
carte est servie directement par l'intégration — rien à copier dans
`www/` — il suffit de l'enregistrer une fois comme ressource de tableau de
bord (voir [§4](#4-ajouter-la-carte-au-tableau-de-bord)). 

### 🌟 Bien plus qu'un carnet basique

Un tableur ou un carnet papier permet de noter ce que vous avez déjà fait.
CARnet est conçu pour faire la partie vraiment fastidieuse : déterminer
**ce qu'il faut faire, quand, pour combien, et comment** — pour votre
véhicule précis, pas un modèle générique.

- 🔍 **Un plan d'entretien construit sur une vraie recherche, pas un
  modèle générique.** Pour la marque/modèle/motorisation/année exacte que
  vous saisissez, Gemini recherche le programme d'entretien officiel
  constructeur et des sources garagistes/revues techniques pour décider
  quelles opérations du catalogue s'appliquent réellement et à quel
  intervalle — au lieu d'une règle générique "tous les 10 000 km"
  appliquée aveuglément à toutes les voitures.
- 🛠️ **Coût DIY et conseils pas à pas, générés à la demande.** Chaque
  échéance affiche un coût estimé des pièces seules à côté du tarif
  garage, et un bouton "comment le faire moi-même ?" génère une
  explication DIY détaillée et spécifique au modèle (outils, étapes,
  difficulté) — pas juste une case à cocher indiquant qu'une opération est
  due.
- 💶 **Coût estimé par opération**, prix garage et prix DIY côte à côte,
  pour décider à l'avance si une intervention vaut le coup de la faire
  soi-même.
- 🔔 **Notifications d'échéances**, pas seulement un tableau de bord qu'il
  faut penser à consulter — l'intégration déclenche une notification
  persistante Home Assistant (et peut alimenter vos propres automatisations
  / appels `notify.*`, voir [§6](#6-automatiser-avec-les-services)) dès
  qu'une échéance devient dépassée ou qu'un rappel au kilométrage est
  atteint.
- 🔗 **Kilométrage réel, pas une estimation saisie à la main.** Liez un
  capteur Home Assistant existant (boîtier OBD, intégration odomètre
  constructeur, `input_number`...) plutôt que de retaper le kilométrage à
  chaque fois — les échéances et les "km restants" se recalculent
  automatiquement à chaque mise à jour du capteur lié.
- 📈 **Une estimation de valeur de revente ancrée dans le marché actuel**,
  pas une courbe de décote statique — Gemini prend en compte la tendance
  du marché, le kilométrage par rapport à la moyenne du segment et l'état
  du véhicule pour produire une fourchette de prix avec un raisonnement
  écrit, suivable dans le temps.
- ⚠️ **Un inventaire des pannes les plus fréquemment rencontrées** sur ce
  modèle précis — les points faibles les plus souvent signalés par les
  autres propriétaires et les garagistes, avec gravité et coût de
  réparation indicatif — pour savoir à quoi s'attendre avant que ça ne
  devienne une mauvaise surprise coûteuse, ainsi que les rappels
  constructeur actifs recherchés à la création.

### ✨ Fonctionnalités

- 🚗🏍️🛵🚲 **Voitures, motos/scooters et vélos électriques**, chacun avec
  un catalogue d'entretien totalement séparé : une voiture ne voit jamais
  un entretien de moto, même comme "non applicable" — autocomplétion
  marque/modèle/motorisation (référentiel local + suggestions Gemini mises
  en cache), année, kilométrage, plaque, photo.
- 🛠️ **Catalogue d'entretien fixe par type de véhicule** (46 opérations
  pour une voiture, 26 pour une moto/scooter, 15 pour un vélo électrique) :
  vidange, tous les filtres, courroie/chaîne de distribution et
  d'accessoires comme entrées séparées, disques et plaquettes
  avant/arrière comme entrées séparées, batterie, climatisation, FAP/EGR,
  contrôle technique, révision constructeur, kit chaîne moto, diagnostic
  batterie de traction... L'IA ne décide que de l'applicabilité et des
  intervalles pour chaque entrée fixe — rien ne peut plus être oublié
  d'une génération à l'autre. Chaque échéance affiche : intervalle
  km/mois, coût estimé en garage, date prévisionnelle réelle, difficulté
  DIY et coût des pièces seules, avec une explication détaillée générée à
  la demande.
- ✏️ **Corrections manuelles à tout moment** : case applicable/non
  applicable par échéance, ajustement direct de la date ou du kilométrage
  d'échéance, ajout d'un entretien manquant sans régénérer tout le plan.
- ⚠️ **Points de vigilance & pannes connues** spécifiques au modèle précis,
  avec gravité, coût indicatif et types de sources cités.
- 🚨 **Rappels constructeur actifs**, recherchés par l'IA à la création,
  mutualisés entre véhicules identiques et rafraîchissables à la demande,
  avec un rappel de vérifier sur les canaux officiels.
- 💶 **Suivi de la valeur de revente** dans le temps, avec une fourchette
  de prix et un raisonnement détaillé (tendance marché, décote,
  kilométrage).
- 📆 **Historique d'entretien horodaté** : chaque échéance se déplie pour
  enregistrer une intervention (bouton "fait aujourd'hui", ou une date/km
  antérieurs), qui recalcule aussitôt les prochaines échéances.
- 🔗 **Kilométrage manuel ou lié à un capteur** existant de Home Assistant
  (odomètre constructeur, boîtier OBD, `input_number`...).
- 🎨 **4 thèmes visuels** : Grand tourisme cuir, Manufacture horlogère,
  Carbone et titane, Atelier vintage — choix persistant via un panneau de
  réglages dédié.
- 🌍 **Multilingue** : français, anglais, allemand, espagnol, italien —
  une seule langue pour toute l'installation (carte, noms du catalogue,
  texte généré par l'IA, notifications persistantes), choisie une fois à
  l'ajout de l'intégration (voir [§3](#3-configurer-lintégration)).
- 🚙 **Multi-véhicules** avec sélecteur rapide et vue d'ensemble en
  tuiles.
- 🔧 **Services Home Assistant** pour tout piloter en automatisation
  (`add_vehicle`, `update_mileage`, `log_maintenance`, `value_snapshot`,
  `set_mileage_source`...).

### 1. Pré-requis

- Home Assistant 2024.1 ou plus récent.
- (Optionnel mais recommandé) Une clé API Gemini gratuite — sans clé, vous
  pouvez toujours créer des véhicules et remplir le carnet à la main, mais
  sans génération automatique du plan, des points de vigilance ni de
  l'estimation de valeur. Pour l'obtenir :
  1. Allez sur [aistudio.google.com](https://aistudio.google.com) et
     connectez-vous avec un compte Google.
  2. Cliquez sur **Get API key** (menu de gauche) → **Create API key**.
  3. Choisissez un projet Google Cloud existant ou laissez-en créer un
     nouveau — aucune information de facturation n'est requise pour le
     forfait gratuit.
  4. Copiez la clé (elle commence par `AIza...`) et collez-la dans l'écran
     de configuration de l'intégration (voir
     [§3](#3-configurer-lintégration)). Le quota quotidien du forfait
     gratuit est généreux pour un usage personnel ; si vous l'atteignez
     malgré tout, l'intégration bascule automatiquement sur d'autres
     modèles Gemini (voir [§8](#8-dépannage)).
- HACS si vous voulez la voie "dépôt personnalisé" (l'installation
  manuelle fonctionne tout aussi bien, voir ci-dessous).

### 2. Installation

**Option A — HACS (dépôt personnalisé)**

1. Dans HACS → ⋮ (menu en haut à droite) → **Dépôts personnalisés**.
2. Collez l'URL de ce dépôt, catégorie **Intégration**.
3. Recherchez "CARnet - Garage Log" dans HACS, installez, puis
   **redémarrez Home Assistant**.

**Option B — Installation manuelle**

1. Copiez le dossier `custom_components/carnet_entretien/` tel quel dans
   `config/custom_components/` de votre installation Home Assistant (via
   Samba, SSH, ou l'add-on File Editor).
2. Vérifiez l'arborescence obtenue :
   ```
   config/
     custom_components/
       carnet_entretien/
         __init__.py
         config_flow.py
         const.py
         catalog_i18n.py
         gemini_client.py
         maintenance_catalog.py
         manifest.json
         sensor.py
         services.yaml
         storage.py
         utils.py
         strings.json
         translations/
         data/referentiel.json
         brand/icon.png, icon@2x.png
         www/carnet-entretien-card.js
   ```
3. **Redémarrez Home Assistant** (Paramètres → Système → Redémarrer).

### 3. Configurer l'intégration

1. **Paramètres → Appareils et services → Ajouter une intégration**.
2. Cherchez **CARnet - Garage Log**.
3. Renseignez votre clé Gemini si vous en avez une (champ optionnel,
   laissez vide sinon), et **choisissez la langue de contenu** (français,
   anglais, allemand, espagnol ou italien) — ce seul réglage pilote
   l'interface de la carte, les noms du catalogue, tout ce que Gemini
   génère, et les notifications persistantes.
4. Validez. Aucun appareil/entité n'apparaît encore : ils sont créés au
   fur et à mesure que vous ajoutez des véhicules via la carte.

La clé API comme la langue peuvent être modifiées ensuite depuis
**Paramètres → Appareils et services → CARnet - Garage Log →
Configurer** (les Options de l'intégration). Changer de langue ne traduit
pas rétroactivement le contenu déjà généré par Gemini pour un véhicule
existant (notes, points de vigilance, rappels, explications DIY,
estimation de revente) — celui-ci reste dans sa langue d'origine jusqu'à
sa prochaine régénération (bouton "↻ Regénérer le plan", rafraîchissement
des points de vigilance/rappels, ou nouvelle demande DIY). C'est
volontaire : changer de langue ne doit jamais consommer du quota IA sans
demande explicite.

### 4. Ajouter la carte au tableau de bord

**Étape manuelle, une seule fois** — contrairement à d'autres intégrations
similaires, la ressource JS de la carte n'est **pas** enregistrée
automatiquement : ce mécanisme (`add_extra_js_url`) s'est avéré peu
fiable sur certaines versions de Home Assistant (échec silencieux, rien
dans les journaux). L'ajout manuel via l'interface standard de HA
fonctionne de façon garantie, quelle que soit votre version :

1. **Paramètres → Tableaux de bord** → **⋮** (menu en haut à droite) →
   **Ressources**.
2. **Ajouter une ressource** :
   - URL : `/carnet_entretien/carnet-entretien-card.js`
   - Type de ressource : **Module JavaScript**
3. Enregistrer, puis **forcer un rechargement complet du cache du
   navigateur** (Ctrl+Maj+R / Cmd+Maj+R).
4. Ouvrez un tableau de bord → **Modifier le tableau de bord** →
   **Ajouter une carte** → cherchez **"CARnet - Garage Log"** dans la
   liste (ou choisissez "Manuel" et collez le YAML ci-dessous).
5. YAML minimal :
   ```yaml
   type: custom:carnet-entretien-card
   ```

Après une mise à jour de l'intégration, le contenu du fichier change mais
pas son URL : un simple rechargement du cache du navigateur suffit, pas
besoin de retoucher la ressource.

#### La carte n'apparaît pas / "Custom element doesn't exist"

C'est presque toujours la ressource ci-dessus manquante, mal orthographiée
ou mise en cache par le navigateur. Suivez cette liste dans l'ordre :

1. **La ressource est-elle bien enregistrée ?** Paramètres → Tableaux de
   bord → ⋮ → Ressources. Vous devez voir
   `/carnet_entretien/carnet-entretien-card.js` avec le type **Module
   JavaScript** (pas "CSS" ni "HTML"). Si elle est absente, ajoutez-la
   comme décrit ci-dessus.
2. **Une faute de frappe dans l'URL ?** Elle doit être exactement
   `/carnet_entretien/carnet-entretien-card.js` — pas de `www/`, pas de
   suffixe de version, le slash initial compte.
3. **Rechargez le cache du navigateur.** Ctrl+Maj+R / Cmd+Maj+R (ou videz
   le cache du site) sur chaque appareil/navigateur utilisé pour voir le
   tableau de bord — y compris le navigateur interne de l'app mobile, qui
   a son propre cache (fermez et rouvrez complètement l'app Companion si
   besoin).
4. **Vérifiez que le fichier est bien servi.** Ouvrez directement
   `http://ADRESSE-DE-VOTRE-HA:8123/carnet_entretien/carnet-entretien-card.js`
   dans un onglet de navigateur (adaptez l'adresse/le port). Vous devez
   voir du JavaScript brut. Si vous obtenez une erreur 404 : la route
   statique de l'intégration n'a pas pu s'enregistrer — voir l'étape 5.
5. **Consultez les journaux Home Assistant** (Paramètres → Système →
   Journaux) à la recherche d'une ligne mentionnant `carnet_entretien`
   juste après le démarrage — en particulier un échec d'enregistrement de
   la route statique, ou un fichier manquant. Si vous avez fait une
   installation manuelle, vérifiez que tous les fichiers listés au
   [§2](#2-installation) sont bien présents (une copie partielle, par
   exemple en oubliant le dossier `www/` ou `data/referentiel.json`, casse
   tout silencieusement).
6. **Ressource en double.** Si vous avez ajouté la ressource plus d'une
   fois (par exemple une fois à la main et une fois via
   l'auto-enregistrement d'une ancienne version, depuis retiré),
   supprimez les doublons — HA peut se tromper sur laquelle charger,
   surtout après une mise à jour. Ne gardez qu'une seule entrée pointant
   vers l'URL ci-dessus.
7. **Toujours bloqué ?** Supprimez complètement la ressource, rechargez le
   cache du navigateur, redémarrez Home Assistant, puis rajoutez la
   ressource depuis zéro (en suivant à nouveau les étapes ci-dessus). Cela
   efface tout état résiduel côté navigateur ou côté HA laissé par une
   tentative précédente.

### 5. Premier usage

1. Cliquez **➕ Ajouter** sur la carte.
2. Choisissez **🚗 Auto** ou **🏍️ 2 roues** (moto / scooter / vélo
   électrique) ; ce choix détermine le catalogue d'entretien et les
   suggestions marque/modèle applicables — les deux ne se mélangent
   jamais.
3. **Marque** : tapez les premières lettres, une liste déroulante
   d'autocomplétion apparaît. Vous pouvez
   aussi taper une marque absente de la liste : la saisie libre est
   toujours acceptée.
4. **Modèle** : la liste se filtre selon la marque choisie, même principe
   de saisie libre en repli.
5. Renseignez motorisation (facultatif — une suggestion instantanée via
   Gemini apparaît une fois marque/modèle/année remplis), année,
   kilométrage actuel, immatriculation (facultative), type de
   carburant/énergie, photo (facultative).
6. Validez : trois étapes de génération s'enchaînent (info constructeur →
   plan d'entretien → points de vigilance), 15 à 45 secondes selon la
   charge de l'API Gemini.
7. Vous arrivez sur la fiche véhicule avec quatre onglets :
   - **🔧 Entretien** : échéances triées par urgence, avec barre de
     progression et bouton "✓ Fait" pour enregistrer une intervention.
   - **⚠️ Points de vigilance** : pannes connues sur ce modèle précis, par
     gravité, avec un bandeau rappelant qu'il s'agit d'une synthèse IA,
     pas d'une donnée constructeur certifiée.
   - **💶 Valeur** : bouton "Estimer maintenant" → courbe de valeur de
     revente dans le temps, à relancer périodiquement (manuellement, ou
     via automatisation avec le service `value_snapshot`).
   - **📓 Historique** : journal des interventions.

### 6. Automatiser avec les services

Tous les services sont visibles dans **Outils de développement →
Actions**, préfixés `carnet_entretien.`. Exemples :

**Rappel hebdomadaire d'estimation de valeur** (`automations.yaml`) :
```yaml
alias: Estimation valeur véhicules - hebdo
trigger:
  - platform: time
    at: "08:00:00"
condition:
  - condition: time
    weekday: [mon]
action:
  - service: carnet_entretien.value_snapshot
    data:
      vehicle_id: "VOTRE_ID_VEHICULE"
```

**Notification quand une échéance est due** — utilisez directement le
capteur `sensor.<marque>_<modele>_prochaine_echeance`, attribut `statut` :
```yaml
alias: Alerte entretien véhicule
trigger:
  - platform: state
    entity_id: sensor.peugeot_308_prochaine_echeance
    attribute: statut
    to: "echue"
action:
  - service: notify.mobile_app_votre_telephone
    data:
      message: >
        Échéance dépassée sur la 308 : {{ state_attr('sensor.peugeot_308_prochaine_echeance','km_restants') }} km de retard.
```

L'`id` de chaque véhicule est visible dans les attributs de ses capteurs,
ou en cliquant sur le véhicule dans la carte puis en inspectant l'appareil
correspondant dans Paramètres → Appareils.

### 7. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| La carte n'apparaît pas / "Custom element doesn't exist" | Ressource Lovelace manquante, mal orthographiée ou mise en cache | Voir la liste complète au [§4](#la-carte-napparaît-pas--custom-element-doesnt-exist) |
| "no_model" à l'ajout d'un véhicule | Pas de clé Gemini configurée, ou clé invalide | Renseignez/vérifiez la clé dans les Options de l'intégration |
| "rate_limited" / "Quota dépassé" | Quota Gemini quotidien atteint sur ce modèle | Patientez, ou réessayez — l'intégration bascule automatiquement sur d'autres modèles |
| "timeout" | API Gemini lente ou surchargée | Réessayez ; le bouton "↻ Regénérer" relance l'appel |
| "truncated" | Réponse coupée par la limite de tokens | Déjà anticipé par des budgets de tokens généreux ; si ça persiste, réduisez le nombre d'items demandés dans `gemini_client.py` |
| Les entretiens masqués ("non applicables") réapparaissent | Bug historique, corrigé en v1.3.2 (un réglage était silencieusement rejeté à l'enregistrement) | Mettez à jour vers la dernière version |
| Le texte reste dans la mauvaise langue après changement | Seules l'interface et le catalogue se traduisent instantanément ; le contenu généré par l'IA (notes, points de vigilance, DIY...) garde sa langue d'origine jusqu'à régénération | Utilisez "↻ Regénérer le plan" / rafraîchissez les points de vigilance ou rappels / relancez une demande DIY |
| Capteurs manquants après suppression d'un véhicule | Normal, transitoire | Ils sont retirés du registre automatiquement au retrait |

### 9. Limites connues

- **Référentiel marques/modèles** : volontairement sélectif, pas
  exhaustif — étoffez-le selon [§7](#7-personnaliser-le-référentiel-marquesmodèles),
  ou remplacez-le par un appel à une base de données véhicules ouverte si
  vous voulez l'automatiser entièrement.
- **Estimation de kilométrage annuel** : utilisée pour classer les
  échéances entre elles (`utils.py`), basée sur l'historique de
  kilométrage du véhicule ; peu fiable tant que peu de points de mesure
  existent (repli sur une estimation basée sur l'année de mise en
  circulation, puis une valeur par défaut fixe).
- **Pas de tests automatisés** inclus dans ce projet — à envisager
  (pytest + `pytest-homeassistant-custom-component`) avant une diffusion
  publique large.
- **Le contenu IA est une synthèse, pas une donnée certifiée** — points
  de vigilance, rappels et conseils DIY sont la meilleure synthèse de
  Gemini à partir d'informations publiques, pas une source constructeur ;
  vérifiez toujours ce qui touche à la sécurité.

### 🤝 Contribuer

Les retours, issues et pull requests sont les bienvenus.

### 📜 Licence

MIT — voir [LICENSE](LICENSE).
