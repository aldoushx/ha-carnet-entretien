// Carte Lovelace "Carnet d'entretien" — thèmes visuels premium
// Custom element vanilla JS, sans dépendance externe, servi automatiquement
// par le composant (voir __init__.py: register_static_path + add_extra_js_url).
// Les couleurs sont pilotées par variables CSS (--ce-*) selon l'attribut
// data-theme posé sur <ha-card>, ce qui permet de changer de thème sans
// toucher au JS : voir le bloc THEMES en bas de fichier.

const DOMAIN = "carnet_entretien";
const CARNET_ICON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="96" height="96">
  <rect x="3" y="3" width="90" height="90" rx="20" fill="#392318"/>
  <rect x="9" y="9" width="78" height="78" rx="15" fill="none" stroke="#C59C35" stroke-width="2.4" stroke-dasharray="5,3"/>
  <text x="22" y="52" font-family="Georgia, 'Times New Roman', serif" font-weight="bold" font-size="44" fill="#F4E5C3">C</text>
  <text x="49" y="52" font-family="Georgia, 'Times New Roman', serif" font-weight="bold" font-size="44" fill="#D96B27">n</text>
  <path d="M 30 73 C 30 70 31.6 68.4 34.4 68 L 38.4 61.4 C 40 59 42.6 58 45.6 58 H 50.4 C 53.4 58 56 59 57.6 61.4 L 61.6 68 C 64.4 68.4 66 70 66 73 V 78 H 30 Z" fill="#F4E5C3"/>
  <circle cx="39" cy="78" r="4" fill="#392318"/>
  <circle cx="57" cy="78" r="4" fill="#392318"/>
</svg>`;

const I18N = {
  fr: {
    settings_language_readonly_note: "définie à l'installation de l'intégration ou dans ses Options (Paramètres → Appareils et services → CARnet → Configurer).",
    status_ok: "OK",
    status_soon: "Bientôt",
    status_due: "Échue",
    status_not_applicable: "Non applicable",
    severity_minor: "Mineur",
    severity_major: "Majeur",
    severity_safety: "Sécurité",
    diy_easy: "🟢 Facile en DIY",
    diy_medium: "🟠 Moyen en DIY",
    diy_hard: "🔴 Difficile en DIY",
    diy_not_recommended: "⛔ Déconseillé en DIY",
    settings_btn_title: "Réglages",
    back_btn: "← Retour",
    add_vehicle_btn: "➕ Ajouter",
    empty_vehicle_list: "Aucun véhicule pour l'instant. Ajoutez-en un avec « ➕ Ajouter ».",
    plan_not_generated: "Plan non généré",
    section_upcoming_maintenance: "Entretien à prévoir",
    settings_theme_section: "Thème visuel",
    theme_active_badge: "✓ actif",
    settings_notifications_section: "Notifications & affichage",
    setting_notification_desc: "Notification persistante HA quand une échéance est dépassée",
    setting_hide_na_desc: "Masquer les entretiens non applicables dans la liste",
    setting_mileage_reminder_desc: "Rappel périodique de mise à jour du kilométrage",
    setting_mileage_reminder_every: "tous les",
    setting_mileage_reminder_days_unit: "jours",
    settings_font_size_section: "Taille du texte",
    settings_language_section: "Langue",
    form_vehicle_type_label: "Type de véhicule",
    form_vehicle_type_auto: "🚗 Auto",
    form_vehicle_type_two_wheeler: "🏍️ 2 roues",
    form_two_wheeler_type_label: "Type de 2 roues",
    form_two_wheeler_moto: "Moto",
    form_two_wheeler_scooter: "Scooter",
    form_two_wheeler_ebike: "Vélo électrique",
    form_brand_label: "Marque",
    form_brand_placeholder_moto: "Ex : Yamaha",
    form_brand_placeholder_auto: "Ex : Peugeot",
    form_model_label: "Modèle",
    form_model_placeholder_moto: "Ex : MT-07",
    form_model_placeholder_auto: "Ex : 308",
    form_year_label: "Année",
    form_fuel_label: "Carburant / énergie",
    form_fuel_hint: "(optionnel — affine les suggestions et la génération)",
    form_fuel_unspecified: "Non précisé",
    fuel_petrol: "Essence",
    fuel_diesel: "Diesel",
    fuel_electric: "Électrique",
    fuel_hybrid: "Hybride (HEV/PHEV)",
    fuel_lpg: "GPL",
    form_motor_assist_label: "Moteur d'assistance",
    form_motorisation_label: "Motorisation",
    form_motorisation_hint: "(optionnel — suggestions une fois marque/modèle/année remplis)",
    form_motorisation_placeholder_ebike: "Ex : Bosch Performance Line CX",
    form_motorisation_placeholder_moto: "Ex : MT-07 ABS",
    form_motorisation_placeholder_auto: "Ex : 1.5 BlueHDi 130",
    form_mileage_label: "Kilométrage",
    form_plate_label: "Immatriculation",
    form_optional_short: "(opt.)",
    form_plate_placeholder: "AB-123-CD",
    form_photo_label: "Photo",
    form_optional: "(optionnel)",
    form_submit_btn: "Générer le carnet d'entretien",
    photo_change_btn: "Changer une photo",
    photo_add_btn: "Ajouter une photo",
    photo_remove_btn: "Retirer",
    tab_maintenance: "🔧 Entretien",
    tab_history: "📓 Historique",
    mileage_linked_to: "lié à {entity}",
    mileage_unlink_btn: "Délier",
    mileage_label_colon: "Kilométrage :",
    mileage_update_btn: "Mettre à jour",
    mileage_link_sensor_hint: "Lier un capteur existant (odomètre constructeur, OBD, input_number…) :",
    mileage_link_confirm_btn: "Lier",
    cancel_btn: "Annuler",
    mileage_link_sensor_title: "Lier un capteur existant",
    panel_recalls_title: "🚨 Rappels constructeur",
    recalls_active_one: "{n} actif",
    recalls_active_other: "{n} actifs",
    recalls_none_known: "aucun connu",
    disclaimer_recalls: "Synthèse IA, non exhaustive — vérifiez systématiquement sur le site du constructeur ou rappel.conso.gouv.fr avant toute décision.",
    recalls_empty: "Aucun rappel identifié pour ce véhicule.",
    sources_label: "📚 Sources :",
    recalls_last_check: "Dernière vérification : {date}",
    recalls_refresh_btn: "↻ Vérifier à nouveau",
    panel_vigilance_title: "⚠️ Points de vigilance",
    vigilance_count_one: "{n} point",
    vigilance_count_other: "{n} points",
    disclaimer_vigilance: "Synthèse IA à partir de retours d'expérience courants — à titre indicatif, ne remplace pas un diagnostic professionnel.",
    vigilance_typical_occurrence: "Apparaît généralement : {x}",
    vigilance_empty: "Aucun point recensé pour l'instant.",
    vigilance_cost_estimate: "💰 Coût indicatif : {x}",
    sources_data_label: "📚 Source des données :",
    vigilance_refresh_btn: "↻ Regénérer",
    panel_value_title: "💶 Valeur estimée",
    value_range: "Fourchette : {min} – {max}",
    sources_trend_label: "📚 Sources & tendance :",
    value_empty: "Aucune estimation pour l'instant.",
    value_estimate_btn: "💶 Estimer maintenant",
    plan_empty: "Aucun plan généré.",
    plan_generate_btn: "Générer",
    plan_regenerate_btn: "↻ Regénérer le plan",
    plan_annual_km: "📊 ~{km}/an",
    plan_hidden_count: "{n} entretien(s) non applicable(s) masqué(s) (réglages).",
    plan_add_item_btn: "+ Ajouter un entretien",
    item_not_applicable_badge: "non applicable",
    item_not_applicable_default_reason: "Ne concerne pas ce véhicule.",
    item_overdue_label: "⚠️ à faire dès que possible",
    overdue_days_label: "-{n} j",
    days_remaining_label: "{n} j",
    cost_garage_suffix: "(garage)",
    cost_diy_parts_suffix: "(pièces DIY)",
    item_applicable_checkbox: "Applicable à mon véhicule",
    item_remove_custom_btn: "Retirer cet entretien ajouté manuellement",
    section_last_intervention: "dernière intervention",
    last_done_unset: "non renseignée (calcul basé sur la mise en circulation)",
    done_today_btn: "✓ Fait aujourd'hui ({km})",
    section_earlier_date: "ou une date antérieure",
    label_intervention_date: "Date de l'intervention",
    generic_mileage_label: "Kilométrage",
    log_save_btn: "Enregistrer cette date",
    section_set_due_directly: "ou fixer l'échéance directement",
    due_km_label: "Échéance (km)",
    due_date_label: "Échéance (date)",
    override_save_btn: "Appliquer cet ajustement",
    section_diy: "bricolage (DIY)",
    diy_generating: "🔎 Génération de l'explication…",
    diy_estimated_time: "⏱️ Temps estimé : ~{min} min",
    diy_tools_needed: "🧰 Outillage spécifique : {tools}",
    diy_generation_failed: "⚠️ Échec de la génération : {err}",
    diy_retry_btn: "🔄 Réessayer",
    diy_generate_btn: "🔧 Comment le faire soi-même ?",
    history_add_btn: "+ Ajouter une intervention",
    history_default_item_name: "Intervention",
    history_empty: "Aucune intervention enregistrée.",
    new_item_name_label: "Nom de l'entretien",
    new_item_name_placeholder: "Ex : Remplacement rotule de direction",
    new_item_interval_km_label: "Intervalle (km)",
    new_item_interval_months_label: "Intervalle (mois)",
    new_item_cost_label: "Coût estimé (€, optionnel)",
    new_item_save_btn: "Ajouter",
    mileage_sensor_picker_label: "Capteur de kilométrage",
    mileage_sensor_fallback_placeholder: "sensor.mon_capteur_km",
    loading_step_search_manufacturer_info: "Recherche des informations constructeur…",
    loading_step_generate_plan: "Génération du plan d'entretien…",
    loading_step_analyze_known_feedback: "Analyse des retours d'expérience connus…",
    loading_check_recalls: "Vérification des rappels constructeur…",
    loading_regenerate_plan: "Régénération du plan d'entretien…",
    loading_analyze_feedback: "Analyse des retours d'expérience…",
    loading_value_estimate: "Estimation de la valeur de revente…",
    error_generation_prefix: "Erreur lors de la génération : {msg}",
    error_generic_prefix: "Erreur : {msg}",
    error_delete_prefix: "Erreur lors de la suppression : {msg}",
    error_setting_save_failed: "Le réglage n'a pas pu être enregistré et a été annulé : {msg}",
    confirm_remove_plan_item: "Retirer cet entretien du plan ?",
    confirm_remove_vehicle: "Supprimer ce véhicule et toutes ses données ?",
    alert_choose_sensor: "Choisissez un capteur avant de valider.",
    alert_invalid_date_km: "Merci de renseigner une date et un kilométrage valides.",
    alert_missing_item_name: "Donnez un nom à cet entretien.",
    prompt_intervention_done: "Intervention réalisée :",
    prompt_mileage: "Kilométrage :",
  },
  en: {
    settings_language_readonly_note: "set when the integration is installed, or from its Options (Settings → Devices & services → CARnet → Configure).",
    status_ok: "OK",
    status_soon: "Soon",
    status_due: "Overdue",
    status_not_applicable: "Not applicable",
    severity_minor: "Minor",
    severity_major: "Major",
    severity_safety: "Safety",
    diy_easy: "🟢 Easy DIY",
    diy_medium: "🟠 Moderate DIY",
    diy_hard: "🔴 Hard DIY",
    diy_not_recommended: "⛔ DIY not recommended",
    settings_btn_title: "Settings",
    back_btn: "← Back",
    add_vehicle_btn: "➕ Add",
    empty_vehicle_list: "No vehicle yet. Add one with « ➕ Add ».",
    plan_not_generated: "Plan not generated",
    section_upcoming_maintenance: "Upcoming maintenance",
    settings_theme_section: "Visual theme",
    theme_active_badge: "✓ active",
    settings_notifications_section: "Notifications & display",
    setting_notification_desc: "Persistent HA notification when a due date is overdue",
    setting_hide_na_desc: "Hide non-applicable maintenance items in the list",
    setting_mileage_reminder_desc: "Periodic reminder to update mileage",
    setting_mileage_reminder_every: "every",
    setting_mileage_reminder_days_unit: "days",
    settings_font_size_section: "Text size",
    settings_language_section: "Language",
    form_vehicle_type_label: "Vehicle type",
    form_vehicle_type_auto: "🚗 Car",
    form_vehicle_type_two_wheeler: "🏍️ Two-wheeler",
    form_two_wheeler_type_label: "Two-wheeler type",
    form_two_wheeler_moto: "Motorcycle",
    form_two_wheeler_scooter: "Scooter",
    form_two_wheeler_ebike: "Electric bike",
    form_brand_label: "Brand",
    form_brand_placeholder_moto: "E.g. Yamaha",
    form_brand_placeholder_auto: "E.g. Peugeot",
    form_model_label: "Model",
    form_model_placeholder_moto: "E.g. MT-07",
    form_model_placeholder_auto: "E.g. 308",
    form_year_label: "Year",
    form_fuel_label: "Fuel / energy",
    form_fuel_hint: "(optional — refines suggestions and generation)",
    form_fuel_unspecified: "Not specified",
    fuel_petrol: "Petrol",
    fuel_diesel: "Diesel",
    fuel_electric: "Electric",
    fuel_hybrid: "Hybrid (HEV/PHEV)",
    fuel_lpg: "LPG",
    form_motor_assist_label: "Assist motor",
    form_motorisation_label: "Engine",
    form_motorisation_hint: "(optional — suggestions once brand/model/year are filled in)",
    form_motorisation_placeholder_ebike: "E.g. Bosch Performance Line CX",
    form_motorisation_placeholder_moto: "E.g. MT-07 ABS",
    form_motorisation_placeholder_auto: "E.g. 1.5 BlueHDi 130",
    form_mileage_label: "Mileage",
    form_plate_label: "License plate",
    form_optional_short: "(opt.)",
    form_plate_placeholder: "AB-123-CD",
    form_photo_label: "Photo",
    form_optional: "(optional)",
    form_submit_btn: "Generate maintenance log",
    photo_change_btn: "Change photo",
    photo_add_btn: "Add photo",
    photo_remove_btn: "Remove",
    tab_maintenance: "🔧 Maintenance",
    tab_history: "📓 History",
    mileage_linked_to: "linked to {entity}",
    mileage_unlink_btn: "Unlink",
    mileage_label_colon: "Mileage:",
    mileage_update_btn: "Update",
    mileage_link_sensor_hint: "Link an existing sensor (manufacturer odometer, OBD, input_number…):",
    mileage_link_confirm_btn: "Link",
    cancel_btn: "Cancel",
    mileage_link_sensor_title: "Link an existing sensor",
    panel_recalls_title: "🚨 Manufacturer recalls",
    recalls_active_one: "{n} active",
    recalls_active_other: "{n} active",
    recalls_none_known: "none known",
    disclaimer_recalls: "AI summary, not exhaustive — always check the manufacturer's website before making a decision.",
    recalls_empty: "No recall identified for this vehicle.",
    sources_label: "📚 Sources:",
    recalls_last_check: "Last check: {date}",
    recalls_refresh_btn: "↻ Check again",
    panel_vigilance_title: "⚠️ Points to watch",
    vigilance_count_one: "{n} point",
    vigilance_count_other: "{n} points",
    disclaimer_vigilance: "AI summary based on common user feedback — for guidance only, does not replace a professional diagnosis.",
    vigilance_typical_occurrence: "Usually appears: {x}",
    vigilance_empty: "No point identified so far.",
    vigilance_cost_estimate: "💰 Estimated cost: {x}",
    sources_data_label: "📚 Data source:",
    vigilance_refresh_btn: "↻ Regenerate",
    panel_value_title: "💶 Estimated value",
    value_range: "Range: {min} – {max}",
    sources_trend_label: "📚 Sources & trend:",
    value_empty: "No estimate yet.",
    value_estimate_btn: "💶 Estimate now",
    plan_empty: "No plan generated.",
    plan_generate_btn: "Generate",
    plan_regenerate_btn: "↻ Regenerate plan",
    plan_annual_km: "📊 ~{km}/year",
    plan_hidden_count: "{n} non-applicable item(s) hidden (settings).",
    plan_add_item_btn: "+ Add a maintenance item",
    item_not_applicable_badge: "not applicable",
    item_not_applicable_default_reason: "Does not apply to this vehicle.",
    item_overdue_label: "⚠️ to do as soon as possible",
    overdue_days_label: "-{n} d",
    days_remaining_label: "{n} d",
    cost_garage_suffix: "(garage)",
    cost_diy_parts_suffix: "(DIY parts)",
    item_applicable_checkbox: "Applies to my vehicle",
    item_remove_custom_btn: "Remove this manually added item",
    section_last_intervention: "last service",
    last_done_unset: "not recorded (estimated from first registration)",
    done_today_btn: "✓ Done today ({km})",
    section_earlier_date: "or an earlier date",
    label_intervention_date: "Service date",
    generic_mileage_label: "Mileage",
    log_save_btn: "Save this date",
    section_set_due_directly: "or set the due date directly",
    due_km_label: "Due (km)",
    due_date_label: "Due (date)",
    override_save_btn: "Apply this adjustment",
    section_diy: "DIY",
    diy_generating: "🔎 Generating explanation…",
    diy_estimated_time: "⏱️ Estimated time: ~{min} min",
    diy_tools_needed: "🧰 Specific tools: {tools}",
    diy_generation_failed: "⚠️ Generation failed: {err}",
    diy_retry_btn: "🔄 Retry",
    diy_generate_btn: "🔧 How do I do it myself?",
    history_add_btn: "+ Add a service",
    history_default_item_name: "Service",
    history_empty: "No service recorded.",
    new_item_name_label: "Item name",
    new_item_name_placeholder: "E.g. Steering ball joint replacement",
    new_item_interval_km_label: "Interval (km)",
    new_item_interval_months_label: "Interval (months)",
    new_item_cost_label: "Estimated cost (€, optional)",
    new_item_save_btn: "Add",
    mileage_sensor_picker_label: "Mileage sensor",
    mileage_sensor_fallback_placeholder: "sensor.my_mileage_sensor",
    loading_step_search_manufacturer_info: "Looking up manufacturer information…",
    loading_step_generate_plan: "Generating maintenance plan…",
    loading_step_analyze_known_feedback: "Analyzing known feedback…",
    loading_check_recalls: "Checking manufacturer recalls…",
    loading_regenerate_plan: "Regenerating maintenance plan…",
    loading_analyze_feedback: "Analyzing feedback…",
    loading_value_estimate: "Estimating resale value…",
    error_generation_prefix: "Error during generation: {msg}",
    error_generic_prefix: "Error: {msg}",
    error_delete_prefix: "Error while deleting: {msg}",
    error_setting_save_failed: "The setting could not be saved and was reverted: {msg}",
    confirm_remove_plan_item: "Remove this item from the plan?",
    confirm_remove_vehicle: "Delete this vehicle and all its data?",
    alert_choose_sensor: "Choose a sensor before confirming.",
    alert_invalid_date_km: "Please enter a valid date and mileage.",
    alert_missing_item_name: "Give this item a name.",
    prompt_intervention_done: "Service performed:",
    prompt_mileage: "Mileage:",
  },
  de: {
    settings_language_readonly_note: "bei der Installation der Integration festgelegt oder über ihre Optionen (Einstellungen → Geräte & Dienste → CARnet → Konfigurieren).",
    status_ok: "OK",
    status_soon: "Bald fällig",
    status_due: "Überfällig",
    status_not_applicable: "Nicht zutreffend",
    severity_minor: "Gering",
    severity_major: "Schwerwiegend",
    severity_safety: "Sicherheit",
    diy_easy: "🟢 Einfach in Eigenregie",
    diy_medium: "🟠 Mittel in Eigenregie",
    diy_hard: "🔴 Schwierig in Eigenregie",
    diy_not_recommended: "⛔ Nicht für Eigenregie empfohlen",
    settings_btn_title: "Einstellungen",
    back_btn: "← Zurück",
    add_vehicle_btn: "➕ Hinzufügen",
    empty_vehicle_list: "Noch kein Fahrzeug. Fügen Sie eines über « ➕ Hinzufügen » hinzu.",
    plan_not_generated: "Plan nicht erstellt",
    section_upcoming_maintenance: "Anstehende Wartungen",
    settings_theme_section: "Visuelles Thema",
    theme_active_badge: "✓ aktiv",
    settings_notifications_section: "Benachrichtigungen & Anzeige",
    setting_notification_desc: "Dauerhafte HA-Benachrichtigung bei überfälligem Termin",
    setting_hide_na_desc: "Nicht zutreffende Wartungen in der Liste ausblenden",
    setting_mileage_reminder_desc: "Regelmäßige Erinnerung zur Aktualisierung des Kilometerstands",
    setting_mileage_reminder_every: "alle",
    setting_mileage_reminder_days_unit: "Tage",
    settings_font_size_section: "Textgröße",
    settings_language_section: "Sprache",
    form_vehicle_type_label: "Fahrzeugtyp",
    form_vehicle_type_auto: "🚗 Auto",
    form_vehicle_type_two_wheeler: "🏍️ Zweirad",
    form_two_wheeler_type_label: "Zweiradtyp",
    form_two_wheeler_moto: "Motorrad",
    form_two_wheeler_scooter: "Roller",
    form_two_wheeler_ebike: "E-Bike",
    form_brand_label: "Marke",
    form_brand_placeholder_moto: "Z. B. Yamaha",
    form_brand_placeholder_auto: "Z. B. Peugeot",
    form_model_label: "Modell",
    form_model_placeholder_moto: "Z. B. MT-07",
    form_model_placeholder_auto: "Z. B. 308",
    form_year_label: "Baujahr",
    form_fuel_label: "Kraftstoff / Energie",
    form_fuel_hint: "(optional — verfeinert Vorschläge und Generierung)",
    form_fuel_unspecified: "Nicht angegeben",
    fuel_petrol: "Benzin",
    fuel_diesel: "Diesel",
    fuel_electric: "Elektrisch",
    fuel_hybrid: "Hybrid (HEV/PHEV)",
    fuel_lpg: "Autogas (LPG)",
    form_motor_assist_label: "Motorunterstützung",
    form_motorisation_label: "Motorisierung",
    form_motorisation_hint: "(optional — Vorschläge sobald Marke/Modell/Baujahr ausgefüllt sind)",
    form_motorisation_placeholder_ebike: "Z. B. Bosch Performance Line CX",
    form_motorisation_placeholder_moto: "Z. B. MT-07 ABS",
    form_motorisation_placeholder_auto: "Z. B. 1.5 BlueHDi 130",
    form_mileage_label: "Kilometerstand",
    form_plate_label: "Kennzeichen",
    form_optional_short: "(opt.)",
    form_plate_placeholder: "AB-123-CD",
    form_photo_label: "Foto",
    form_optional: "(optional)",
    form_submit_btn: "Wartungsheft erstellen",
    photo_change_btn: "Foto ändern",
    photo_add_btn: "Foto hinzufügen",
    photo_remove_btn: "Entfernen",
    tab_maintenance: "🔧 Wartung",
    tab_history: "📓 Verlauf",
    mileage_linked_to: "verknüpft mit {entity}",
    mileage_unlink_btn: "Trennen",
    mileage_label_colon: "Kilometerstand:",
    mileage_update_btn: "Aktualisieren",
    mileage_link_sensor_hint: "Einen vorhandenen Sensor verknüpfen (Werksstandtacho, OBD, input_number…):",
    mileage_link_confirm_btn: "Verknüpfen",
    cancel_btn: "Abbrechen",
    mileage_link_sensor_title: "Einen vorhandenen Sensor verknüpfen",
    panel_recalls_title: "🚨 Herstellerrückrufe",
    recalls_active_one: "{n} aktiv",
    recalls_active_other: "{n} aktiv",
    recalls_none_known: "keine bekannt",
    disclaimer_recalls: "KI-Zusammenfassung, nicht erschöpfend — prüfen Sie vor jeder Entscheidung systematisch die Website des Herstellers.",
    recalls_empty: "Kein Rückruf für dieses Fahrzeug bekannt.",
    sources_label: "📚 Quellen:",
    recalls_last_check: "Letzte Prüfung: {date}",
    recalls_refresh_btn: "↻ Erneut prüfen",
    panel_vigilance_title: "⚠️ Beobachtungspunkte",
    vigilance_count_one: "{n} Punkt",
    vigilance_count_other: "{n} Punkte",
    disclaimer_vigilance: "KI-Zusammenfassung auf Basis häufiger Erfahrungsberichte — dient nur zur Orientierung und ersetzt keine professionelle Diagnose.",
    vigilance_typical_occurrence: "Tritt meist auf: {x}",
    vigilance_empty: "Bisher kein Punkt erfasst.",
    vigilance_cost_estimate: "💰 Geschätzte Kosten: {x}",
    sources_data_label: "📚 Datenquelle:",
    vigilance_refresh_btn: "↻ Neu generieren",
    panel_value_title: "💶 Geschätzter Wert",
    value_range: "Spanne: {min} – {max}",
    sources_trend_label: "📚 Quellen & Trend:",
    value_empty: "Noch keine Schätzung.",
    value_estimate_btn: "💶 Jetzt schätzen",
    plan_empty: "Kein Plan erstellt.",
    plan_generate_btn: "Erstellen",
    plan_regenerate_btn: "↻ Plan neu erstellen",
    plan_annual_km: "📊 ~{km}/Jahr",
    plan_hidden_count: "{n} nicht zutreffende Wartung(en) ausgeblendet (Einstellungen).",
    plan_add_item_btn: "+ Wartung hinzufügen",
    item_not_applicable_badge: "nicht zutreffend",
    item_not_applicable_default_reason: "Betrifft dieses Fahrzeug nicht.",
    item_overdue_label: "⚠️ so bald wie möglich erledigen",
    overdue_days_label: "-{n} T",
    days_remaining_label: "{n} T",
    cost_garage_suffix: "(Werkstatt)",
    cost_diy_parts_suffix: "(Teile für Eigenregie)",
    item_applicable_checkbox: "Trifft auf mein Fahrzeug zu",
    item_remove_custom_btn: "Diese manuell hinzugefügte Wartung entfernen",
    section_last_intervention: "letzte Durchführung",
    last_done_unset: "nicht erfasst (berechnet ab Erstzulassung)",
    done_today_btn: "✓ Heute erledigt ({km})",
    section_earlier_date: "oder ein früheres Datum",
    label_intervention_date: "Datum der Durchführung",
    generic_mileage_label: "Kilometerstand",
    log_save_btn: "Dieses Datum speichern",
    section_set_due_directly: "oder Fälligkeit direkt festlegen",
    due_km_label: "Fällig bei (km)",
    due_date_label: "Fällig am (Datum)",
    override_save_btn: "Diese Anpassung anwenden",
    section_diy: "Eigenregie (DIY)",
    diy_generating: "🔎 Erklärung wird erstellt…",
    diy_estimated_time: "⏱️ Geschätzte Dauer: ~{min} Min.",
    diy_tools_needed: "🧰 Spezialwerkzeug: {tools}",
    diy_generation_failed: "⚠️ Erstellung fehlgeschlagen: {err}",
    diy_retry_btn: "🔄 Erneut versuchen",
    diy_generate_btn: "🔧 Wie mache ich das selbst?",
    history_add_btn: "+ Durchführung hinzufügen",
    history_default_item_name: "Durchführung",
    history_empty: "Keine Durchführung erfasst.",
    new_item_name_label: "Name der Wartung",
    new_item_name_placeholder: "Z. B. Austausch Spurstangenkopf",
    new_item_interval_km_label: "Intervall (km)",
    new_item_interval_months_label: "Intervall (Monate)",
    new_item_cost_label: "Geschätzte Kosten (€, optional)",
    new_item_save_btn: "Hinzufügen",
    mileage_sensor_picker_label: "Kilometerstand-Sensor",
    mileage_sensor_fallback_placeholder: "sensor.mein_km_sensor",
    loading_step_search_manufacturer_info: "Herstellerinformationen werden gesucht…",
    loading_step_generate_plan: "Wartungsplan wird erstellt…",
    loading_step_analyze_known_feedback: "Bekannte Erfahrungsberichte werden analysiert…",
    loading_check_recalls: "Herstellerrückrufe werden geprüft…",
    loading_regenerate_plan: "Wartungsplan wird neu erstellt…",
    loading_analyze_feedback: "Erfahrungsberichte werden analysiert…",
    loading_value_estimate: "Wiederverkaufswert wird geschätzt…",
    error_generation_prefix: "Fehler bei der Erstellung: {msg}",
    error_generic_prefix: "Fehler: {msg}",
    error_delete_prefix: "Fehler beim Löschen: {msg}",
    error_setting_save_failed: "Die Einstellung konnte nicht gespeichert werden und wurde zurückgesetzt: {msg}",
    confirm_remove_plan_item: "Diese Wartung aus dem Plan entfernen?",
    confirm_remove_vehicle: "Dieses Fahrzeug und alle zugehörigen Daten löschen?",
    alert_choose_sensor: "Bitte wählen Sie vor dem Bestätigen einen Sensor aus.",
    alert_invalid_date_km: "Bitte geben Sie ein gültiges Datum und einen gültigen Kilometerstand ein.",
    alert_missing_item_name: "Geben Sie dieser Wartung einen Namen.",
    prompt_intervention_done: "Durchgeführte Wartung:",
    prompt_mileage: "Kilometerstand:",
  },
  es: {
    settings_language_readonly_note: "se define al instalar la integración, o desde sus Opciones (Ajustes → Dispositivos y servicios → CARnet → Configurar).",
    status_ok: "OK",
    status_soon: "Próximamente",
    status_due: "Vencida",
    status_not_applicable: "No aplicable",
    severity_minor: "Menor",
    severity_major: "Mayor",
    severity_safety: "Seguridad",
    diy_easy: "🟢 Fácil de hacer uno mismo",
    diy_medium: "🟠 Dificultad media",
    diy_hard: "🔴 Difícil de hacer uno mismo",
    diy_not_recommended: "⛔ No recomendado hacerlo uno mismo",
    settings_btn_title: "Ajustes",
    back_btn: "← Volver",
    add_vehicle_btn: "➕ Añadir",
    empty_vehicle_list: "Aún no hay ningún vehículo. Añade uno con « ➕ Añadir ».",
    plan_not_generated: "Plan no generado",
    section_upcoming_maintenance: "Mantenimiento previsto",
    settings_theme_section: "Tema visual",
    theme_active_badge: "✓ activo",
    settings_notifications_section: "Notificaciones y visualización",
    setting_notification_desc: "Notificación persistente de HA cuando se supera una fecha límite",
    setting_hide_na_desc: "Ocultar en la lista los mantenimientos no aplicables",
    setting_mileage_reminder_desc: "Recordatorio periódico para actualizar el kilometraje",
    setting_mileage_reminder_every: "cada",
    setting_mileage_reminder_days_unit: "días",
    settings_font_size_section: "Tamaño del texto",
    settings_language_section: "Idioma",
    form_vehicle_type_label: "Tipo de vehículo",
    form_vehicle_type_auto: "🚗 Coche",
    form_vehicle_type_two_wheeler: "🏍️ 2 ruedas",
    form_two_wheeler_type_label: "Tipo de 2 ruedas",
    form_two_wheeler_moto: "Moto",
    form_two_wheeler_scooter: "Scooter",
    form_two_wheeler_ebike: "Bicicleta eléctrica",
    form_brand_label: "Marca",
    form_brand_placeholder_moto: "Ej.: Yamaha",
    form_brand_placeholder_auto: "Ej.: Peugeot",
    form_model_label: "Modelo",
    form_model_placeholder_moto: "Ej.: MT-07",
    form_model_placeholder_auto: "Ej.: 308",
    form_year_label: "Año",
    form_fuel_label: "Combustible / energía",
    form_fuel_hint: "(opcional — mejora las sugerencias y la generación)",
    form_fuel_unspecified: "No especificado",
    fuel_petrol: "Gasolina",
    fuel_diesel: "Diésel",
    fuel_electric: "Eléctrico",
    fuel_hybrid: "Híbrido (HEV/PHEV)",
    fuel_lpg: "GLP",
    form_motor_assist_label: "Motor de asistencia",
    form_motorisation_label: "Motorización",
    form_motorisation_hint: "(opcional — sugerencias una vez completados marca/modelo/año)",
    form_motorisation_placeholder_ebike: "Ej.: Bosch Performance Line CX",
    form_motorisation_placeholder_moto: "Ej.: MT-07 ABS",
    form_motorisation_placeholder_auto: "Ej.: 1.5 BlueHDi 130",
    form_mileage_label: "Kilometraje",
    form_plate_label: "Matrícula",
    form_optional_short: "(opc.)",
    form_plate_placeholder: "AB-123-CD",
    form_photo_label: "Foto",
    form_optional: "(opcional)",
    form_submit_btn: "Generar el cuaderno de mantenimiento",
    photo_change_btn: "Cambiar foto",
    photo_add_btn: "Añadir foto",
    photo_remove_btn: "Quitar",
    tab_maintenance: "🔧 Mantenimiento",
    tab_history: "📓 Historial",
    mileage_linked_to: "vinculado a {entity}",
    mileage_unlink_btn: "Desvincular",
    mileage_label_colon: "Kilometraje:",
    mileage_update_btn: "Actualizar",
    mileage_link_sensor_hint: "Vincular un sensor existente (odómetro de fábrica, OBD, input_number…):",
    mileage_link_confirm_btn: "Vincular",
    cancel_btn: "Cancelar",
    mileage_link_sensor_title: "Vincular un sensor existente",
    panel_recalls_title: "🚨 Llamadas a revisión del fabricante",
    recalls_active_one: "{n} activa",
    recalls_active_other: "{n} activas",
    recalls_none_known: "ninguna conocida",
    disclaimer_recalls: "Resumen generado por IA, no exhaustivo — verifique siempre en el sitio del fabricante antes de tomar cualquier decisión.",
    recalls_empty: "No se ha identificado ninguna llamada a revisión para este vehículo.",
    sources_label: "📚 Fuentes:",
    recalls_last_check: "Última verificación: {date}",
    recalls_refresh_btn: "↻ Verificar de nuevo",
    panel_vigilance_title: "⚠️ Puntos de atención",
    vigilance_count_one: "{n} punto",
    vigilance_count_other: "{n} puntos",
    disclaimer_vigilance: "Resumen de IA basado en experiencias frecuentes de otros usuarios — solo a título informativo, no sustituye un diagnóstico profesional.",
    vigilance_typical_occurrence: "Suele aparecer: {x}",
    vigilance_empty: "Ningún punto identificado por el momento.",
    vigilance_cost_estimate: "💰 Coste orientativo: {x}",
    sources_data_label: "📚 Fuente de los datos:",
    vigilance_refresh_btn: "↻ Regenerar",
    panel_value_title: "💶 Valor estimado",
    value_range: "Rango: {min} – {max}",
    sources_trend_label: "📚 Fuentes y tendencia:",
    value_empty: "Aún no hay ninguna estimación.",
    value_estimate_btn: "💶 Estimar ahora",
    plan_empty: "No se ha generado ningún plan.",
    plan_generate_btn: "Generar",
    plan_regenerate_btn: "↻ Regenerar el plan",
    plan_annual_km: "📊 ~{km}/año",
    plan_hidden_count: "{n} mantenimiento(s) no aplicable(s) oculto(s) (ajustes).",
    plan_add_item_btn: "+ Añadir un mantenimiento",
    item_not_applicable_badge: "no aplicable",
    item_not_applicable_default_reason: "No corresponde a este vehículo.",
    item_overdue_label: "⚠️ hacerlo cuanto antes",
    overdue_days_label: "-{n} d",
    days_remaining_label: "{n} d",
    cost_garage_suffix: "(taller)",
    cost_diy_parts_suffix: "(piezas para hacerlo uno mismo)",
    item_applicable_checkbox: "Se aplica a mi vehículo",
    item_remove_custom_btn: "Quitar este mantenimiento añadido manualmente",
    section_last_intervention: "última intervención",
    last_done_unset: "sin registrar (calculado a partir de la primera matriculación)",
    done_today_btn: "✓ Hecho hoy ({km})",
    section_earlier_date: "o una fecha anterior",
    label_intervention_date: "Fecha de la intervención",
    generic_mileage_label: "Kilometraje",
    log_save_btn: "Guardar esta fecha",
    section_set_due_directly: "o fijar el vencimiento directamente",
    due_km_label: "Vencimiento (km)",
    due_date_label: "Vencimiento (fecha)",
    override_save_btn: "Aplicar este ajuste",
    section_diy: "hazlo tú mismo (DIY)",
    diy_generating: "🔎 Generando la explicación…",
    diy_estimated_time: "⏱️ Tiempo estimado: ~{min} min",
    diy_tools_needed: "🧰 Herramientas específicas: {tools}",
    diy_generation_failed: "⚠️ Error al generar: {err}",
    diy_retry_btn: "🔄 Reintentar",
    diy_generate_btn: "🔧 ¿Cómo hacerlo uno mismo?",
    history_add_btn: "+ Añadir una intervención",
    history_default_item_name: "Intervención",
    history_empty: "No se ha registrado ninguna intervención.",
    new_item_name_label: "Nombre del mantenimiento",
    new_item_name_placeholder: "Ej.: Sustitución de la rótula de dirección",
    new_item_interval_km_label: "Intervalo (km)",
    new_item_interval_months_label: "Intervalo (meses)",
    new_item_cost_label: "Coste estimado (€, opcional)",
    new_item_save_btn: "Añadir",
    mileage_sensor_picker_label: "Sensor de kilometraje",
    mileage_sensor_fallback_placeholder: "sensor.mi_sensor_km",
    loading_step_search_manufacturer_info: "Buscando información del fabricante…",
    loading_step_generate_plan: "Generando el plan de mantenimiento…",
    loading_step_analyze_known_feedback: "Analizando experiencias conocidas…",
    loading_check_recalls: "Verificando llamadas a revisión del fabricante…",
    loading_regenerate_plan: "Regenerando el plan de mantenimiento…",
    loading_analyze_feedback: "Analizando experiencias de otros usuarios…",
    loading_value_estimate: "Estimando el valor de reventa…",
    error_generation_prefix: "Error durante la generación: {msg}",
    error_generic_prefix: "Error: {msg}",
    error_delete_prefix: "Error al eliminar: {msg}",
    error_setting_save_failed: "El ajuste no se pudo guardar y se ha revertido: {msg}",
    confirm_remove_plan_item: "¿Quitar este mantenimiento del plan?",
    confirm_remove_vehicle: "¿Eliminar este vehículo y todos sus datos?",
    alert_choose_sensor: "Elija un sensor antes de confirmar.",
    alert_invalid_date_km: "Indique una fecha y un kilometraje válidos.",
    alert_missing_item_name: "Ponga un nombre a este mantenimiento.",
    prompt_intervention_done: "Intervención realizada:",
    prompt_mileage: "Kilometraje:",
  },
  it: {
    settings_language_readonly_note: "impostata all'installazione dell'integrazione, oppure dalle sue Opzioni (Impostazioni → Dispositivi e servizi → CARnet → Configura).",
    status_ok: "OK",
    status_soon: "In arrivo",
    status_due: "Scaduta",
    status_not_applicable: "Non applicabile",
    severity_minor: "Minore",
    severity_major: "Maggiore",
    severity_safety: "Sicurezza",
    diy_easy: "🟢 Facile fai da te",
    diy_medium: "🟠 Difficoltà media",
    diy_hard: "🔴 Difficile fai da te",
    diy_not_recommended: "⛔ Sconsigliato fai da te",
    settings_btn_title: "Impostazioni",
    back_btn: "← Indietro",
    add_vehicle_btn: "➕ Aggiungi",
    empty_vehicle_list: "Nessun veicolo per ora. Aggiungine uno con « ➕ Aggiungi ».",
    plan_not_generated: "Piano non generato",
    section_upcoming_maintenance: "Manutenzioni da programmare",
    settings_theme_section: "Tema visivo",
    theme_active_badge: "✓ attivo",
    settings_notifications_section: "Notifiche e visualizzazione",
    setting_notification_desc: "Notifica persistente HA quando una scadenza è superata",
    setting_hide_na_desc: "Nascondi nell'elenco gli interventi non applicabili",
    setting_mileage_reminder_desc: "Promemoria periodico per aggiornare il chilometraggio",
    setting_mileage_reminder_every: "ogni",
    setting_mileage_reminder_days_unit: "giorni",
    settings_font_size_section: "Dimensione del testo",
    settings_language_section: "Lingua",
    form_vehicle_type_label: "Tipo di veicolo",
    form_vehicle_type_auto: "🚗 Auto",
    form_vehicle_type_two_wheeler: "🏍️ Due ruote",
    form_two_wheeler_type_label: "Tipo di due ruote",
    form_two_wheeler_moto: "Moto",
    form_two_wheeler_scooter: "Scooter",
    form_two_wheeler_ebike: "Bicicletta elettrica",
    form_brand_label: "Marca",
    form_brand_placeholder_moto: "Es.: Yamaha",
    form_brand_placeholder_auto: "Es.: Peugeot",
    form_model_label: "Modello",
    form_model_placeholder_moto: "Es.: MT-07",
    form_model_placeholder_auto: "Es.: 308",
    form_year_label: "Anno",
    form_fuel_label: "Carburante / energia",
    form_fuel_hint: "(opzionale — affina i suggerimenti e la generazione)",
    form_fuel_unspecified: "Non specificato",
    fuel_petrol: "Benzina",
    fuel_diesel: "Diesel",
    fuel_electric: "Elettrico",
    fuel_hybrid: "Ibrido (HEV/PHEV)",
    fuel_lpg: "GPL",
    form_motor_assist_label: "Motore di assistenza",
    form_motorisation_label: "Motorizzazione",
    form_motorisation_hint: "(opzionale — suggerimenti una volta compilati marca/modello/anno)",
    form_motorisation_placeholder_ebike: "Es.: Bosch Performance Line CX",
    form_motorisation_placeholder_moto: "Es.: MT-07 ABS",
    form_motorisation_placeholder_auto: "Es.: 1.5 BlueHDi 130",
    form_mileage_label: "Chilometraggio",
    form_plate_label: "Targa",
    form_optional_short: "(opz.)",
    form_plate_placeholder: "AB-123-CD",
    form_photo_label: "Foto",
    form_optional: "(opzionale)",
    form_submit_btn: "Genera il libretto di manutenzione",
    photo_change_btn: "Cambia foto",
    photo_add_btn: "Aggiungi foto",
    photo_remove_btn: "Rimuovi",
    tab_maintenance: "🔧 Manutenzione",
    tab_history: "📓 Cronologia",
    mileage_linked_to: "collegato a {entity}",
    mileage_unlink_btn: "Scollega",
    mileage_label_colon: "Chilometraggio:",
    mileage_update_btn: "Aggiorna",
    mileage_link_sensor_hint: "Collega un sensore esistente (contachilometri di fabbrica, OBD, input_number…):",
    mileage_link_confirm_btn: "Collega",
    cancel_btn: "Annulla",
    mileage_link_sensor_title: "Collega un sensore esistente",
    panel_recalls_title: "🚨 Richiami del costruttore",
    recalls_active_one: "{n} attivo",
    recalls_active_other: "{n} attivi",
    recalls_none_known: "nessuno noto",
    disclaimer_recalls: "Sintesi generata dall'IA, non esaustiva — verificate sempre sul sito del costruttore prima di ogni decisione.",
    recalls_empty: "Nessun richiamo individuato per questo veicolo.",
    sources_label: "📚 Fonti:",
    recalls_last_check: "Ultima verifica: {date}",
    recalls_refresh_btn: "↻ Verifica di nuovo",
    panel_vigilance_title: "⚠️ Punti di attenzione",
    vigilance_count_one: "{n} punto",
    vigilance_count_other: "{n} punti",
    disclaimer_vigilance: "Sintesi IA basata su esperienze comuni riportate dagli utenti — a solo titolo indicativo, non sostituisce una diagnosi professionale.",
    vigilance_typical_occurrence: "Compare generalmente: {x}",
    vigilance_empty: "Nessun punto rilevato per ora.",
    vigilance_cost_estimate: "💰 Costo indicativo: {x}",
    sources_data_label: "📚 Fonte dei dati:",
    vigilance_refresh_btn: "↻ Rigenera",
    panel_value_title: "💶 Valore stimato",
    value_range: "Intervallo: {min} – {max}",
    sources_trend_label: "📚 Fonti e tendenza:",
    value_empty: "Nessuna stima per ora.",
    value_estimate_btn: "💶 Stima ora",
    plan_empty: "Nessun piano generato.",
    plan_generate_btn: "Genera",
    plan_regenerate_btn: "↻ Rigenera il piano",
    plan_annual_km: "📊 ~{km}/anno",
    plan_hidden_count: "{n} intervento/i non applicabile/i nascosto/i (impostazioni).",
    plan_add_item_btn: "+ Aggiungi un intervento",
    item_not_applicable_badge: "non applicabile",
    item_not_applicable_default_reason: "Non riguarda questo veicolo.",
    item_overdue_label: "⚠️ da fare il prima possibile",
    overdue_days_label: "-{n} gg",
    days_remaining_label: "{n} gg",
    cost_garage_suffix: "(officina)",
    cost_diy_parts_suffix: "(ricambi fai da te)",
    item_applicable_checkbox: "Applicabile al mio veicolo",
    item_remove_custom_btn: "Rimuovi questo intervento aggiunto manualmente",
    section_last_intervention: "ultimo intervento",
    last_done_unset: "non registrato (calcolato dalla data di prima immatricolazione)",
    done_today_btn: "✓ Fatto oggi ({km})",
    section_earlier_date: "oppure una data precedente",
    label_intervention_date: "Data dell'intervento",
    generic_mileage_label: "Chilometraggio",
    log_save_btn: "Salva questa data",
    section_set_due_directly: "oppure imposta direttamente la scadenza",
    due_km_label: "Scadenza (km)",
    due_date_label: "Scadenza (data)",
    override_save_btn: "Applica questa modifica",
    section_diy: "fai da te (DIY)",
    diy_generating: "🔎 Generazione della spiegazione…",
    diy_estimated_time: "⏱️ Tempo stimato: ~{min} min",
    diy_tools_needed: "🧰 Attrezzi specifici: {tools}",
    diy_generation_failed: "⚠️ Generazione non riuscita: {err}",
    diy_retry_btn: "🔄 Riprova",
    diy_generate_btn: "🔧 Come farlo da soli?",
    history_add_btn: "+ Aggiungi un intervento",
    history_default_item_name: "Intervento",
    history_empty: "Nessun intervento registrato.",
    new_item_name_label: "Nome dell'intervento",
    new_item_name_placeholder: "Es.: Sostituzione testina dello sterzo",
    new_item_interval_km_label: "Intervallo (km)",
    new_item_interval_months_label: "Intervallo (mesi)",
    new_item_cost_label: "Costo stimato (€, opzionale)",
    new_item_save_btn: "Aggiungi",
    mileage_sensor_picker_label: "Sensore di chilometraggio",
    mileage_sensor_fallback_placeholder: "sensor.mio_sensore_km",
    loading_step_search_manufacturer_info: "Ricerca delle informazioni del costruttore…",
    loading_step_generate_plan: "Generazione del piano di manutenzione…",
    loading_step_analyze_known_feedback: "Analisi delle esperienze note…",
    loading_check_recalls: "Verifica dei richiami del costruttore…",
    loading_regenerate_plan: "Rigenerazione del piano di manutenzione…",
    loading_analyze_feedback: "Analisi delle esperienze degli utenti…",
    loading_value_estimate: "Stima del valore di rivendita…",
    error_generation_prefix: "Errore durante la generazione: {msg}",
    error_generic_prefix: "Errore: {msg}",
    error_delete_prefix: "Errore durante l'eliminazione: {msg}",
    error_setting_save_failed: "Impossibile salvare l'impostazione, è stata ripristinata: {msg}",
    confirm_remove_plan_item: "Rimuovere questo intervento dal piano?",
    confirm_remove_vehicle: "Eliminare questo veicolo e tutti i suoi dati?",
    alert_choose_sensor: "Scegliete un sensore prima di confermare.",
    alert_invalid_date_km: "Inserite una data e un chilometraggio validi.",
    alert_missing_item_name: "Assegnate un nome a questo intervento.",
    prompt_intervention_done: "Intervento eseguito:",
    prompt_mileage: "Chilometraggio:",
  },
};

// Correspondance code backend -> clé de traduction (les valeurs "ok", "bientot",
// "mineur", "facile"... viennent du backend et ne sont jamais affichées telles
// quelles : elles sont toujours passées à this._t() via ces tables).
const STATUS_LABEL_KEY = { ok: "status_ok", bientot: "status_soon", echue: "status_due", non_applicable: "status_not_applicable" };
const SEVERITY_LABEL_KEY = { mineur: "severity_minor", majeur: "severity_major", securite: "severity_safety" };
const DIY_LABEL_KEY = { facile: "diy_easy", moyen: "diy_medium", difficile: "diy_hard", non_recommande: "diy_not_recommended" };
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
const LANGUAGES_META = [
  { id: "fr", name: "Français", flag: "🇫🇷" },
  { id: "en", name: "English", flag: "🇬🇧" },
  { id: "de", name: "Deutsch", flag: "🇩🇪" },
  { id: "es", name: "Español", flag: "🇪🇸" },
  { id: "it", name: "Italiano", flag: "🇮🇹" },
];
const VALID_LANG_IDS = LANGUAGES_META.map((l) => l.id);

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
    this._addForm = { vehicle_type: "auto", two_wheeler_type: "moto", brand: "", model: "", fuel_type: "", motorisation: "", year: "", mileage: "", plate: "", photo: "" };
    this._brandOptions = [];
    this._modelOptions = [];
    this._mileageSourceEditing = false;
    this._pendingSensorEntity = "";
    this._theme = "gt_cuir";
    this._settings = { hide_not_applicable: true, notifications_enabled: true, font_scale: 1, mileage_reminder_enabled: true, mileage_reminder_days: 30, language: "fr" };
    this._motorisationKey = null;
    this._motorisationFullList = null;
    this._diyLoading = {}; // { [itemId]: bool } — état de chargement de l'explication DIY
    this._diyError = {}; // { [itemId]: message } — dernière erreur de génération DIY, pour affichage inline
    // _render() reconstruit tout le innerHTML du shadow DOM à chaque appel
    // (mise à jour de kilométrage, bascule applicable/non applicable,
    // enregistrement d'une intervention, génération DIY...). Sans état
    // explicite, chaque <details> d'entretien perd son ouverture à chaque
    // rafraîchissement : l'encart qu'on vient de dérouler se réenroule tout
    // seul (typiquement pendant une requête DIY), obligeant à le rechercher
    // plus haut dans la liste pour le rouvrir. On mémorise donc ici les
    // entretiens actuellement dépliés pour reproduire l'attribut "open" à
    // chaque rendu, quelle que soit l'action qui l'a déclenché.
    this._expandedItemIds = new Set();
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

  // Traduit une clé I18N dans la langue actuellement choisie (réglage
  // "language", français par défaut), avec repli sur le français puis sur
  // la clé elle-même (entre crochets) si elle est introuvable, pour ne
  // jamais planter le rendu à cause d'une clé oubliée.
  _t(key, vars) {
    const lang = (this._settings && this._settings.language && I18N[this._settings.language]) ? this._settings.language : "fr";
    let str = I18N[lang][key];
    if (str === undefined) str = I18N.fr[key];
    if (str === undefined) return `[${key}]`;
    if (vars) {
      str = str.replace(/\{(\w+)\}/g, (m, name) => (name in vars ? String(vars[name]) : m));
    }
    return str;
  }

  _statusLabel(status) {
    const key = STATUS_LABEL_KEY[status];
    return key ? this._t(key) : status;
  }

  _severityLabel(severity) {
    const key = SEVERITY_LABEL_KEY[severity];
    return key ? this._t(key) : severity;
  }

  _diyLabel(difficulty) {
    const key = DIY_LABEL_KEY[difficulty];
    return key ? this._t(key) : difficulty;
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
    this._loadingMsg = this._t("loading_step_search_manufacturer_info");
    this._render();
    const steps = [
      this._t("loading_step_search_manufacturer_info"),
      this._t("loading_step_generate_plan"),
      this._t("loading_step_analyze_known_feedback"),
      this._t("loading_check_recalls"),
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
          fuel_type: f.fuel_type,
          vehicle_type: f.vehicle_type,
          two_wheeler_type: f.vehicle_type === "deux_roues" ? f.two_wheeler_type : "",
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
      this._addForm = { vehicle_type: "auto", two_wheeler_type: "moto", brand: "", model: "", fuel_type: "", motorisation: "", year: "", mileage: "", plate: "", photo: "" };
    } catch (err) {
      alert(this._t("error_generation_prefix", { msg: err.message || err.code || err }));
    } finally {
      clearInterval(timer);
      this._loading = false;
      this._render();
    }
  }

  async _searchBrand(query) {
    const f = this._addForm;
    const res = await this._ws({
      type: "search_referentiel",
      data: { query, vehicle_type: f.vehicle_type, two_wheeler_type: f.vehicle_type === "deux_roues" ? f.two_wheeler_type : "" },
    });
    this._brandOptions = res.results || [];
    this._renderSuggestions("brand", this._brandOptions);
  }

  async _searchModel(brand, query) {
    const f = this._addForm;
    const res = await this._ws({
      type: "search_referentiel",
      data: { brand, query, vehicle_type: f.vehicle_type, two_wheeler_type: f.vehicle_type === "deux_roues" ? f.two_wheeler_type : "" },
    });
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
    const key = `${f.brand}|${f.model}|${f.year}|${f.fuel_type}|${f.vehicle_type}|${f.two_wheeler_type}`;
    if (this._motorisationKey !== key) {
      this._motorisationKey = key;
      this._motorisationFullList = null;
      this._renderSuggestions("motorisation", []);
      try {
        const res = await this._ws({
          type: "search_motorisations",
          data: {
            brand: f.brand, model: f.model, year: parseInt(f.year, 10), fuel_type: f.fuel_type,
            vehicle_type: f.vehicle_type, two_wheeler_type: f.vehicle_type === "deux_roues" ? f.two_wheeler_type : "",
            query: "",
          },
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
    this._loadingMsg = this._t("loading_regenerate_plan");
    this._render();
    try {
      await this._ws({ type: "refresh_plan", data: { vehicle_id: vehicleId } });
      await this._fetchVehicles();
    } catch (err) {
      alert(this._t("error_generic_prefix", { msg: err.message || err.code || err }));
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
    if (!confirm(this._t("confirm_remove_plan_item"))) return;
    await this._ws({ type: "remove_plan_item", data: { vehicle_id: vehicleId, item_id: itemId } });
    await this._fetchVehicles();
  }

  async _generateDiyExplanation(vehicleId, itemId) {
    this._diyLoading[itemId] = true;
    delete this._diyError[itemId];
    this._render();
    try {
      await this._ws({ type: "generate_diy_explanation", data: { vehicle_id: vehicleId, item_id: itemId } });
      await this._fetchVehicles();
    } catch (err) {
      this._diyError[itemId] = err.message || err.code || String(err);
    } finally {
      delete this._diyLoading[itemId];
      this._render();
    }
  }

  async _refreshKnownIssues(vehicleId) {
    this._loading = true;
    this._loadingMsg = this._t("loading_analyze_feedback");
    this._render();
    try {
      await this._ws({ type: "refresh_known_issues", data: { vehicle_id: vehicleId } });
      await this._fetchVehicles();
    } catch (err) {
      alert(this._t("error_generic_prefix", { msg: err.message || err.code || err }));
    } finally {
      this._loading = false;
      this._render();
    }
  }

  async _refreshRecalls(vehicleId) {
    this._loading = true;
    this._loadingMsg = this._t("loading_check_recalls");
    this._render();
    try {
      await this._ws({ type: "refresh_recalls", data: { vehicle_id: vehicleId } });
      await this._fetchVehicles();
    } catch (err) {
      alert(this._t("error_generic_prefix", { msg: err.message || err.code || err }));
    } finally {
      this._loading = false;
      this._render();
    }
  }

  async _valueSnapshot(vehicleId) {
    this._loading = true;
    this._loadingMsg = this._t("loading_value_estimate");
    this._render();
    try {
      await this._ws({ type: "value_snapshot", data: { vehicle_id: vehicleId, condition: "correct" } });
      await this._fetchVehicles();
    } catch (err) {
      alert(this._t("error_generic_prefix", { msg: err.message || err.code || err }));
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
    if (!confirm(this._t("confirm_remove_vehicle"))) return;
    try {
      await this._ws({ type: "remove_vehicle", data: { vehicle_id: vehicleId } });
      this._view = "list";
      this._selectedId = null;
      await this._fetchVehicles();
    } catch (err) {
      alert(this._t("error_delete_prefix", { msg: err.message || err.code || err }));
      await this._fetchVehicles();
    }
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
    const previous = this._settings[key];
    this._settings = { ...this._settings, [key]: value };
    this._render();
    try {
      await this._ws({ type: "set_settings", data: { [key]: value } });
    } catch (e) {
      // Si l'enregistrement échoue côté serveur, la valeur affichée
      // localement ne doit pas mentir : on revient à l'ancienne valeur et on
      // prévient clairement, plutôt que de laisser un réglage "appliqué" à
      // l'écran mais jamais persisté (c'était la cause du bug où le
      // masquage des entretiens non applicables se réinitialisait tout
      // seul — voir CHANGELOG v1.3.2).
      this._settings = { ...this._settings, [key]: previous };
      this._render();
      console.error("carnet_entretien: échec de l'enregistrement du réglage", key, value, e);
      alert(this._t("error_setting_save_failed", { msg: e.message || e.code || String(e) }));
    }
  }

  // ---------------------------------------------------------------- render

  _render() {
    if (!this.shadowRoot) return;
    // La liste des entretiens est triée par échéance la plus proche : la
    // position d'un item peut donc bouger d'un rendu à l'autre (ex : après
    // avoir enregistré une intervention, son échéance recule et l'item
    // change de place). On restaure la position de défilement pour éviter
    // l'impression déroutante que la liste "saute" ou que des entretiens
    // masqués/cochés réapparaissent ailleurs.
    const prevBody = this.shadowRoot.querySelector(".body");
    const prevScrollTop = prevBody ? prevBody.scrollTop : 0;
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
        ? `<button class="btn ghost" id="back-btn">${this._t("back_btn")}</button>`
        : this._view === "list"
        ? `<button class="btn primary" id="add-btn">${this._t("add_vehicle_btn")}</button>`
        : `<button class="btn ghost" id="back-btn">${this._t("back_btn")}</button>`;

    this.shadowRoot.innerHTML = `
      <style>${STYLE}</style>
      <ha-card data-theme="${this._theme}" style="font-size:${this._settings.font_scale || 1}em;">
        <div class="header">
          <div class="title">${CARNET_ICON_SVG} CARnet - Garage Log</div>
          <div class="header-actions">
            ${showSettingsBtn ? `<button class="btn ghost icon" id="settings-btn" title="${this._t("settings_btn_title")}">⚙️</button>` : ""}
            ${primaryBtn}
          </div>
        </div>
        ${this._loading ? `<div class="loading"><div class="spinner"></div>${this._loadingMsg}</div>` : ""}
        <div class="body">${content}</div>
      </ha-card>
    `;
    this._bindEvents();
    const nextBody = this.shadowRoot.querySelector(".body");
    if (nextBody && prevScrollTop) nextBody.scrollTop = prevScrollTop;
  }

  _renderList() {
    if (!this._vehicles.length) {
      return `<div class="empty">${this._t("empty_vehicle_list")}</div>`;
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
            <div class="tile-title">${v.photo ? "" : vehicleEmoji(v) + " "}${esc(v.brand)} ${esc(v.model)}</div>
            <div class="tile-sub">${v.year} · ${fmtKm(v.mileage)}${v.plate ? ` · ${esc(v.plate.toUpperCase())}` : ""}</div>
            ${
              next
                ? `<div class="tile-next">${CATEGORY_EMOJI[next.category] || "🔩"} ${esc(next.name)} — ${this._statusLabel(next.statut)}</div>`
                : `<div class="tile-next muted">${this._t("plan_not_generated")}</div>`
            }
          </div>`;
        })
        .join("")}
    </div>`;
  }

  _renderSettings() {
    const lang = this._settings.language || "fr";
    return `
      <p class="section-label">${this._t("settings_theme_section")}</p>
      <div class="theme-grid">
        ${THEMES_META.map(
          (t) => `
          <div class="theme-card ${this._theme === t.id ? "active" : ""}" data-theme-id="${t.id}">
            <div class="theme-card-head">
              <span>${t.icon} ${esc(t.name)}</span>
              ${this._theme === t.id ? `<span class="accent small">${this._t("theme_active_badge")}</span>` : ""}
            </div>
            <div class="swatches">
              ${t.swatches.map((c) => `<span style="background:${c}"></span>`).join("")}
            </div>
          </div>`
        ).join("")}
      </div>
      <p class="section-label">${this._t("settings_language_section")}</p>
      <div class="muted small" style="margin-bottom:10px;">
        ${(() => {
          const current = LANGUAGES_META.find((l) => l.id === lang) || LANGUAGES_META[0];
          return `${current.flag} ${esc(current.name)} — ${this._t("settings_language_readonly_note")}`;
        })()}
      </div>
      <p class="section-label">${this._t("settings_notifications_section")}</p>
      <label class="checkbox-row" style="margin-bottom:10px;">
        <input type="checkbox" id="setting-notifications" ${this._settings.notifications_enabled ? "checked" : ""} />
        ${this._t("setting_notification_desc")}
      </label>
      <label class="checkbox-row">
        <input type="checkbox" id="setting-hide-na" ${this._settings.hide_not_applicable ? "checked" : ""} />
        ${this._t("setting_hide_na_desc")}
      </label>
      <label class="checkbox-row" style="margin-top:10px;">
        <input type="checkbox" id="setting-mileage-reminder" ${this._settings.mileage_reminder_enabled ? "checked" : ""} />
        ${this._t("setting_mileage_reminder_desc")}
      </label>
      <div class="mileage-reminder-days-row" style="${this._settings.mileage_reminder_enabled ? "" : "display:none;"}">
        <span class="muted small">${this._t("setting_mileage_reminder_every")}</span>
        <input type="number" id="setting-mileage-reminder-days" value="${this._settings.mileage_reminder_days ?? 30}" min="1" max="365" />
        <span class="muted small">${this._t("setting_mileage_reminder_days_unit")}</span>
      </div>
      <p class="section-label">${this._t("settings_font_size_section")}</p>
      <div class="font-size-row">
        <button class="btn small ghost" id="font-decrease-btn" ${this._settings.font_scale <= 0.8 ? "disabled" : ""}>A−</button>
        <span class="mono small">${Math.round((this._settings.font_scale || 1) * 100)}%</span>
        <button class="btn small ghost" id="font-increase-btn" ${this._settings.font_scale >= 1.4 ? "disabled" : ""}>A+</button>
      </div>
    `;
  }

  _renderAddForm() {
    const f = this._addForm;
    const isTwoWheeler = f.vehicle_type === "deux_roues";
    return `
      <form id="add-form" class="form">
        <label>${this._t("form_vehicle_type_label")}</label>
        <div class="vehicle-type-toggle">
          <button type="button" class="btn ${!isTwoWheeler ? "primary" : "ghost"} vehicle-type-btn" data-vehicle-type="auto">${this._t("form_vehicle_type_auto")}</button>
          <button type="button" class="btn ${isTwoWheeler ? "primary" : "ghost"} vehicle-type-btn" data-vehicle-type="deux_roues">${this._t("form_vehicle_type_two_wheeler")}</button>
        </div>
        ${
          isTwoWheeler
            ? `<label>${this._t("form_two_wheeler_type_label")}
                <select id="f-two-wheeler-type">
                  <option value="moto" ${f.two_wheeler_type === "moto" ? "selected" : ""}>${this._t("form_two_wheeler_moto")}</option>
                  <option value="scooter" ${f.two_wheeler_type === "scooter" ? "selected" : ""}>${this._t("form_two_wheeler_scooter")}</option>
                  <option value="velo_electrique" ${f.two_wheeler_type === "velo_electrique" ? "selected" : ""}>${this._t("form_two_wheeler_ebike")}</option>
                </select>
              </label>`
            : ""
        }
        <label>${this._t("form_brand_label")}
          <div class="autocomplete">
            <input id="f-brand" value="${esc(f.brand)}" placeholder="${isTwoWheeler ? this._t("form_brand_placeholder_moto") : this._t("form_brand_placeholder_auto")}" autocomplete="off" />
            <div class="suggestions" id="brand-suggestions"></div>
          </div>
        </label>
        <label>${this._t("form_model_label")}
          <div class="autocomplete">
            <input id="f-model" value="${esc(f.model)}" placeholder="${isTwoWheeler ? this._t("form_model_placeholder_moto") : this._t("form_model_placeholder_auto")}" autocomplete="off" />
            <div class="suggestions" id="model-suggestions"></div>
          </div>
        </label>
        <label>${this._t("form_year_label")}
          <input type="number" id="f-year" value="${esc(f.year)}" min="1970" max="2100" />
        </label>
        <label>${this._t("form_fuel_label")} <span class="muted">${this._t("form_fuel_hint")}</span>
          <select id="f-fuel-type">
            <option value="" ${f.fuel_type === "" ? "selected" : ""}>${this._t("form_fuel_unspecified")}</option>
            <option value="Essence" ${f.fuel_type === "Essence" ? "selected" : ""}>${this._t("fuel_petrol")}</option>
            <option value="Diesel" ${f.fuel_type === "Diesel" ? "selected" : ""}>${this._t("fuel_diesel")}</option>
            <option value="Électrique" ${f.fuel_type === "Électrique" ? "selected" : ""}>${this._t("fuel_electric")}</option>
            <option value="Hybride" ${f.fuel_type === "Hybride" ? "selected" : ""}>${this._t("fuel_hybrid")}</option>
            <option value="GPL" ${f.fuel_type === "GPL" ? "selected" : ""}>${this._t("fuel_lpg")}</option>
          </select>
        </label>
        <label>${f.two_wheeler_type === "velo_electrique" && isTwoWheeler ? this._t("form_motor_assist_label") : this._t("form_motorisation_label")} <span class="muted">${this._t("form_motorisation_hint")}</span>
          <div class="autocomplete">
            <input id="f-motorisation" value="${esc(f.motorisation)}" placeholder="${f.two_wheeler_type === "velo_electrique" && isTwoWheeler ? this._t("form_motorisation_placeholder_ebike") : isTwoWheeler ? this._t("form_motorisation_placeholder_moto") : this._t("form_motorisation_placeholder_auto")}" autocomplete="off" />
            <div class="suggestions" id="motorisation-suggestions"></div>
          </div>
        </label>
        <div class="row-2">
          <label>${this._t("form_mileage_label")}
            <input type="number" id="f-mileage" value="${esc(f.mileage)}" min="0" />
          </label>
          <label>${this._t("form_plate_label")} <span class="muted">${this._t("form_optional_short")}</span>
            <input id="f-plate" value="${esc(f.plate)}" placeholder="${this._t("form_plate_placeholder")}" />
          </label>
        </div>
        <label>${this._t("form_photo_label")} <span class="muted">${this._t("form_optional")}</span>
          <input type="file" id="f-photo" accept="image/*" capture="environment" />
        </label>
        <img id="add-photo-preview" class="photo-preview" style="display:${f.photo ? "block" : "none"};" src="${f.photo || ""}" />
        <button type="submit" class="btn primary full">${this._t("form_submit_btn")}</button>
      </form>
    `;
  }

  _renderDetail(v) {
    const tabs = [
      ["entretien", this._t("tab_maintenance")],
      ["historique", this._t("tab_history")],
    ];
    return `
      <div class="detail-header">
        <div class="detail-header-main">
          ${
            v.photo
              ? `<img class="vehicle-photo" src="${v.photo}" alt="" />`
              : `<div class="vehicle-photo placeholder">${vehicleEmoji(v)}</div>`
          }
          <div>
            <div class="detail-title">${esc(v.brand)} ${esc(v.model)} <span class="muted">(${v.year})</span></div>
            <div class="muted small">${esc(v.motorisation || "")}${v.fuel_type ? ` · ${esc(v.fuel_type)}` : ""}</div>
            ${v.plate ? `<div class="plate-chip mono">${esc(v.plate.toUpperCase())}</div>` : ""}
            <div class="photo-controls">
              <label class="link-btn">
                📷 ${v.photo ? this._t("photo_change_btn") : this._t("photo_add_btn")}
                <input type="file" id="photo-input" accept="image/*" capture="environment" style="display:none;" />
              </label>
              ${v.photo ? `<button class="link-btn" id="remove-photo-btn">${this._t("photo_remove_btn")}</button>` : ""}
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
          <span class="muted small">${this._t("mileage_linked_to", { entity: esc(v.mileage_sensor_entity_id || "") })}</span>
          <button class="btn small ghost" id="unlink-sensor-btn">${this._t("mileage_unlink_btn")}</button>
        </div>`;
    }
    if (this._mileageSourceEditing) {
      return `
        <div class="mileage-row">
          <span>${this._t("mileage_label_colon")}</span>
          <input type="number" id="mileage-input" value="${v.mileage}" min="0" />
          <button class="btn small" id="mileage-btn">${this._t("mileage_update_btn")}</button>
        </div>
        <div class="sensor-link-box">
          <div class="muted small" style="margin-bottom:6px;">${this._t("mileage_link_sensor_hint")}</div>
          <div id="entity-picker-slot"></div>
          <div class="row-2" style="margin-top:8px;">
            <button class="btn small primary" id="confirm-link-btn">${this._t("mileage_link_confirm_btn")}</button>
            <button class="btn small ghost" id="cancel-link-btn">${this._t("cancel_btn")}</button>
          </div>
        </div>`;
    }
    return `
      <div class="mileage-row">
        <span>${this._t("mileage_label_colon")}</span>
        <input type="number" id="mileage-input" value="${v.mileage}" min="0" />
        <button class="btn small" id="mileage-btn">${this._t("mileage_update_btn")}</button>
        <button class="btn small ghost" id="link-sensor-btn" title="${this._t("mileage_link_sensor_title")}">🔗</button>
      </div>`;
  }

  _renderTabEntretien(v) {
    return `
      ${this._renderRecallsPanel(v)}
      ${this._renderVigilancePanel(v)}
      ${this._renderValeurPanel(v)}
      <p class="section-label">${this._t("section_upcoming_maintenance")}</p>
      ${this._renderPlanList(v)}
    `;
  }

  _renderRecallsPanel(v) {
    const recalls = v.recalls || [];
    return `
      <details class="panel">
        <summary>
          <span>${this._t("panel_recalls_title")}</span>
          <span class="small" style="${recalls.length ? "color:var(--ce-danger-text);font-weight:600;" : "color:var(--ce-text-muted);"}">
            ${recalls.length ? this._t(recalls.length > 1 ? "recalls_active_other" : "recalls_active_one", { n: recalls.length }) : this._t("recalls_none_known")}
          </span>
        </summary>
        <div class="panel-body">
          <div class="disclaimer">${this._t("disclaimer_recalls")}</div>
          ${
            recalls.length
              ? `<div class="issue-list">
                  ${recalls
                    .map(
                      (r) => `
                    <div class="issue-item">
                      <div class="issue-head">
                        <span>🚨 ${esc(r.title)}</span>
                        <span class="status-chip" style="background:${severityVar(r.severity)}">${this._severityLabel(r.severity)}</span>
                      </div>
                      ${r.reference || r.date ? `<div class="muted small">${[r.reference, r.date].filter(Boolean).map(esc).join(" · ")}</div>` : ""}
                      <div class="small">${esc(r.description || "")}</div>
                      ${r.action_required ? `<div class="muted small">➡️ ${esc(r.action_required)}</div>` : ""}
                    </div>`
                    )
                    .join("")}
                </div>`
              : `<div class="empty small">${this._t("recalls_empty")}</div>`
          }
          ${
            v.recalls_sources
              ? `<div class="sources-box"><b>${this._t("sources_label")}</b> <span class="muted small">${esc(v.recalls_sources)}</span></div>`
              : ""
          }
          ${
            v.recalls_checked_at
              ? `<div class="muted small" style="margin-top:6px;">${this._t("recalls_last_check", { date: fmtDate(v.recalls_checked_at) })}</div>`
              : ""
          }
          <button class="btn small ghost full" id="refresh-recalls-btn">${this._t("recalls_refresh_btn")}</button>
        </div>
      </details>
    `;
  }

  _renderVigilancePanel(v) {
    const issues = v.known_issues || [];
    return `
      <details class="panel">
        <summary>
          <span>${this._t("panel_vigilance_title")}</span>
          <span class="muted small">${issues.length ? this._t(issues.length > 1 ? "vigilance_count_other" : "vigilance_count_one", { n: issues.length }) : "—"}</span>
        </summary>
        <div class="panel-body">
          <div class="disclaimer">${this._t("disclaimer_vigilance")}</div>
          ${
            issues.length
              ? `<div class="issue-list">
                  ${issues
                    .map(
                      (it) => `
                    <div class="issue-item">
                      <div class="issue-head">
                        <span>${CATEGORY_EMOJI[it.category] || "🔩"} ${esc(it.title)}</span>
                        <span class="status-chip" style="background:${severityVar(it.severity)}">${this._severityLabel(it.severity)}</span>
                      </div>
                      ${it.typical_occurrence ? `<div class="muted small">${this._t("vigilance_typical_occurrence", { x: esc(it.typical_occurrence) })}</div>` : ""}
                      <div class="small">${esc(it.description || "")}</div>
                      ${it.cost_estimate ? `<div class="muted small">${this._t("vigilance_cost_estimate", { x: esc(it.cost_estimate) })}</div>` : ""}
                    </div>`
                    )
                    .join("")}
                </div>`
              : `<div class="empty small">${this._t("vigilance_empty")}</div>`
          }
          ${
            v.known_issues_sources
              ? `<div class="sources-box"><b>${this._t("sources_data_label")}</b> <span class="muted small">${esc(v.known_issues_sources)}</span></div>`
              : ""
          }
          <button class="btn small ghost full" id="refresh-issues-btn">${this._t("vigilance_refresh_btn")}</button>
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
          <span>${this._t("panel_value_title")}</span>
          <span class="mono accent small">${last ? fmtEur(last.value_avg) : "—"}</span>
        </summary>
        <div class="panel-body">
          ${
            last
              ? `<div class="value-range small muted">${this._t("value_range", { min: fmtEur(last.value_min), max: fmtEur(last.value_max) })}</div>
                 ${history.length > 1 ? renderValueChart(history) : ""}
                 ${
                   last.sources_tendance
                     ? `<div class="sources-box"><b>${this._t("sources_trend_label")}</b> <span class="muted small">${esc(last.sources_tendance)}</span></div>`
                     : ""
                 }`
              : `<div class="empty small">${this._t("value_empty")}</div>`
          }
          <button class="btn small primary full" id="snapshot-btn">${this._t("value_estimate_btn")}</button>
        </div>
      </details>
    `;
  }

  _renderPlanList(v) {
    const allItems = v.maintenance_plan || [];
    if (!allItems.length) {
      return `<div class="empty">${this._t("plan_empty")} <button class="btn small" id="refresh-plan-btn">${this._t("plan_generate_btn")}</button></div>`;
    }
    const items = this._settings.hide_not_applicable
      ? allItems.filter((it) => it.statut !== "non_applicable")
      : allItems;
    const annualKm = allItems.find((it) => it.annual_km)?.annual_km;
    const hiddenCount = allItems.length - items.length;
    return `
      <div class="toolbar">
        <button class="btn small ghost" id="refresh-plan-btn">${this._t("plan_regenerate_btn")}</button>
        ${annualKm ? `<span class="muted small">${this._t("plan_annual_km", { km: fmtKm(annualKm) })}</span>` : ""}
      </div>
      ${hiddenCount ? `<div class="muted small" style="margin-bottom:8px;">${this._t("plan_hidden_count", { n: hiddenCount })}</div>` : ""}
      <div class="plan-list">
        ${items.map((it) => this._renderPlanRow(it, v)).join("")}
      </div>
      <button class="btn small ghost full" id="add-item-btn" style="margin-top:10px;">${this._t("plan_add_item_btn")}</button>
      <div id="add-item-form" class="add-item-form" style="display:none;"></div>
    `;
  }

  _renderPlanRow(it, v) {
    const isNA = it.statut === "non_applicable";
    const applicableChecked = it.applicable !== false;
    const diyBadge = !isNA && it.diy_difficulty ? `<span class="diy-badge diy-${it.diy_difficulty}">${this._diyLabel(it.diy_difficulty)}</span>` : "";

    let summaryBody = "";
    if (isNA) {
      summaryBody = `
        <div class="plan-row-head">
          <span>${CATEGORY_EMOJI[it.category] || "🔩"} ${esc(it.name)}</span>
          <span class="muted small">${this._t("item_not_applicable_badge")}</span>
        </div>
        <div class="muted small">${esc(it.not_applicable_reason) || this._t("item_not_applicable_default_reason")}</div>`;
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
        rightLabel = it.depasse_de_km != null ? `-${fmtKm(it.depasse_de_km)}` : it.jours_restants != null ? this._t("overdue_days_label", { n: Math.abs(it.jours_restants) }) : "⚠️";
      } else if (it.km_restants != null) {
        rightLabel = fmtKm(it.km_restants);
      } else if (it.jours_restants != null) {
        rightLabel = this._t("days_remaining_label", { n: it.jours_restants });
      }
      summaryBody = `
        <div class="plan-row-head">
          <span>${CATEGORY_EMOJI[it.category] || "🔩"} ${esc(it.name)} ${diyBadge}</span>
          <span class="mono small" style="color:${overdue ? "var(--ce-danger-text)" : "var(--ce-text-muted)"}">${rightLabel}</span>
        </div>
        <div class="bar"><div class="bar-fill" style="width:${pct}%;background:${color}"></div></div>
        <div class="plan-row-meta muted small">
          ${it.prevu_vers && !overdue ? `📅 ${esc(it.prevu_vers)}` : overdue ? this._t("item_overdue_label") : ""}
          ${it.cost_estimate_eur != null ? ` · 💰 ${fmtEur(it.cost_estimate_eur)} ${this._t("cost_garage_suffix")}` : ""}
          ${it.diy_cost_estimate_eur != null ? ` · 🔧 ${fmtEur(it.diy_cost_estimate_eur)} ${this._t("cost_diy_parts_suffix")}` : ""}
        </div>`;
    }

    const isOpen = this._expandedItemIds.has(it.id);
    return `
      <details class="plan-row ${isNA ? "na" : ""}" data-item-id="${it.id}" ${isOpen ? "open" : ""}>
        <summary class="plan-row-summary">${summaryBody}</summary>
        <div class="plan-row-edit">
          <label class="checkbox-row">
            <input type="checkbox" class="applicable-cb" data-item-id="${it.id}" ${applicableChecked ? "checked" : ""} />
            ${this._t("item_applicable_checkbox")}
          </label>
          ${it.custom ? `<button class="link-btn" id="remove-item-${it.id}" data-item-id="${it.id}" style="margin-top:4px;">${this._t("item_remove_custom_btn")}</button>` : ""}

          ${
            !isNA
              ? `
          <div class="edit-divider"><span>${this._t("section_last_intervention")}</span></div>
          <div class="muted small" style="margin-bottom:10px;">
            🔧 ${it.last_done_date ? `<b>${fmtDate(it.last_done_date)}</b> — <b>${fmtKm(it.last_done_km)}</b>` : this._t("last_done_unset")}
          </div>
          <button class="btn primary full done-today-btn" data-item-id="${it.id}" data-item-name="${esc(it.name)}">${this._t("done_today_btn", { km: fmtKm(v.mileage) })}</button>
          <div class="edit-divider"><span>${this._t("section_earlier_date")}</span></div>
          <div class="row-2">
            <label>${this._t("label_intervention_date")}
              <input type="date" class="log-date-input" data-item-id="${it.id}" value="${it.last_done_date ? isoDateFromUnix(it.last_done_date) : todayIso()}" max="${todayIso()}" />
            </label>
            <label>${this._t("generic_mileage_label")}
              <input type="number" class="log-km-input" data-item-id="${it.id}" value="${it.last_done_km ?? v.mileage}" min="0" />
            </label>
          </div>
          <button class="btn small ghost full log-save-btn" data-item-id="${it.id}" data-item-name="${esc(it.name)}">${this._t("log_save_btn")}</button>

          <div class="edit-divider"><span>${this._t("section_set_due_directly")}</span></div>
          <div class="row-2">
            <label>${this._t("due_km_label")}
              <input type="number" class="override-km-input" data-item-id="${it.id}" value="${it.due_km_override ?? ""}" placeholder="${it.due_km ?? ""}" min="0" />
            </label>
            <label>${this._t("due_date_label")}
              <input type="date" class="override-date-input" data-item-id="${it.id}" value="${it.due_date_override ? isoDateFromUnix(it.due_date_override) : ""}" />
            </label>
          </div>
          <button class="btn small ghost full override-save-btn" data-item-id="${it.id}">${this._t("override_save_btn")}</button>

          <div class="edit-divider"><span>${this._t("section_diy")}</span></div>
          ${this._renderDiySection(it)}
          `
              : ""
          }
        </div>
      </details>`;
  }

  _renderDiySection(it) {
    if (this._diyLoading[it.id]) {
      return `<div class="muted small">${this._t("diy_generating")}</div>`;
    }
    if (it.diy_explanation) {
      return `
        <div class="diy-box">
          ${it.diy_safety_warning ? `<div class="diy-warning">⚠️ ${esc(it.diy_safety_warning)}</div>` : ""}
          <div class="small">${esc(it.diy_explanation)}</div>
          ${it.diy_estimated_time_minutes ? `<div class="muted small" style="margin-top:6px;">${this._t("diy_estimated_time", { min: it.diy_estimated_time_minutes })}</div>` : ""}
          ${
            it.diy_tools_needed && it.diy_tools_needed.length
              ? `<div class="muted small">${this._t("diy_tools_needed", { tools: it.diy_tools_needed.map(esc).join(", ") })}</div>`
              : ""
          }
        </div>`;
    }
    const error = this._diyError[it.id];
    if (error) {
      return `
        <div class="diy-box">
          <div class="diy-warning">${this._t("diy_generation_failed", { err: esc(error) })}</div>
          <button class="btn small primary full diy-generate-btn" data-item-id="${it.id}">${this._t("diy_retry_btn")}</button>
        </div>`;
    }
    return `<button class="btn small ghost full diy-generate-btn" data-item-id="${it.id}">${this._t("diy_generate_btn")}</button>`;
  }

  _renderTabHistorique(v) {
    const log = (v.maintenance_log || []).slice().reverse();
    return `
      <div class="toolbar"><button class="btn small ghost" id="add-log-btn">${this._t("history_add_btn")}</button></div>
      ${
        log.length
          ? `<div class="log-list">${log
              .map(
                (l) => `
            <div class="log-item">
              <div><b>${esc(l.item_name) || this._t("history_default_item_name")}</b> — ${fmtKm(l.km)}</div>
              <div class="muted small">${new Date(l.date * 1000).toLocaleDateString("fr-FR")}${l.garage ? " · " + esc(l.garage) : ""}${l.cost ? " · " + l.cost + " €" : ""}</div>
              ${l.notes ? `<div class="small">${esc(l.notes)}</div>` : ""}
            </div>`
              )
              .join("")}</div>`
          : `<div class="empty">${this._t("history_empty")}</div>`
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

    root.querySelectorAll(".theme-card[data-theme-id]").forEach((el) =>
      el.addEventListener("click", () => this._selectTheme(el.dataset.themeId))
    );
    // Pas de bascule cliquable pour la langue depuis v1.4.1 : c'est un
    // réglage d'installation (voir config_flow.py), affiché en lecture
    // seule ici avec une note expliquant où le changer.
    root.getElementById("setting-notifications")?.addEventListener("change", (e) => this._updateSetting("notifications_enabled", e.target.checked));
    root.getElementById("setting-hide-na")?.addEventListener("change", (e) => this._updateSetting("hide_not_applicable", e.target.checked));
    root.getElementById("setting-mileage-reminder")?.addEventListener("change", (e) => this._updateSetting("mileage_reminder_enabled", e.target.checked));
    root.getElementById("setting-mileage-reminder-days")?.addEventListener("change", (e) => {
      const days = Math.max(1, Math.min(365, parseInt(e.target.value, 10) || 30));
      this._updateSetting("mileage_reminder_days", days);
    });
    root.getElementById("font-decrease-btn")?.addEventListener("click", () => {
      const next = Math.max(0.8, Math.round(((this._settings.font_scale || 1) - 0.1) * 10) / 10);
      this._updateSetting("font_scale", next);
    });
    root.getElementById("font-increase-btn")?.addEventListener("click", () => {
      const next = Math.min(1.4, Math.round(((this._settings.font_scale || 1) + 0.1) * 10) / 10);
      this._updateSetting("font_scale", next);
    });

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
      root.querySelectorAll(".vehicle-type-btn").forEach((btn) =>
        btn.addEventListener("click", () => {
          if (this._addForm.vehicle_type === btn.dataset.vehicleType) return;
          this._addForm.vehicle_type = btn.dataset.vehicleType;
          // Le référentiel marque/modèle est séparé par catégorie (auto /
          // moto / scooter / vélo électrique) : une marque de moto ne doit
          // jamais rester sélectionnée après bascule vers "Auto", et
          // inversement — on réinitialise donc marque/modèle/motorisation.
          this._addForm.brand = "";
          this._addForm.model = "";
          this._addForm.motorisation = "";
          this._motorisationKey = null; // le type change le contexte : on relance la recherche au prochain focus
          this._render();
        })
      );
      root.getElementById("f-two-wheeler-type")?.addEventListener("change", (e) => {
        if (this._addForm.two_wheeler_type === e.target.value) return;
        this._addForm.two_wheeler_type = e.target.value;
        this._addForm.brand = "";
        this._addForm.model = "";
        this._addForm.motorisation = "";
        this._motorisationKey = null;
        this._render();
      });

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
      root.getElementById("f-fuel-type").addEventListener("change", (e) => {
        this._addForm.fuel_type = e.target.value;
        this._motorisationKey = null; // le carburant a changé : on relance la recherche au prochain focus
      });

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
        alert(this._t("alert_choose_sensor"));
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
          alert(this._t("alert_invalid_date_km"));
          return;
        }
        const dateTs = Math.floor(new Date(dateInput.value + "T12:00:00").getTime() / 1000);
        this._logMaintenance(this._selectedId, { item_id: itemId, item_name: itemName, km, date: dateTs });
      })
    );

    // Mémorise l'ouverture/fermeture manuelle de chaque encart d'entretien
    // pour la reproduire au prochain _render() (voir _expandedItemIds dans
    // le constructeur) — sans ça, toute action (case à cocher, log d'une
    // intervention, génération DIY...) referme l'encart en cours de lecture.
    root.querySelectorAll("details.plan-row").forEach((el) => {
      el.addEventListener("toggle", () => {
        if (el.open) this._expandedItemIds.add(el.dataset.itemId);
        else this._expandedItemIds.delete(el.dataset.itemId);
      });
    });

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
            <label>${this._t("new_item_name_label")}<input type="text" id="new-item-name" placeholder="${this._t("new_item_name_placeholder")}" /></label>
            <div class="row-2">
              <label>${this._t("new_item_interval_km_label")}<input type="number" id="new-item-km" min="0" value="0" /></label>
              <label>${this._t("new_item_interval_months_label")}<input type="number" id="new-item-months" min="0" value="0" /></label>
            </div>
            <label>${this._t("new_item_cost_label")}<input type="number" id="new-item-cost" min="0" /></label>
            <button class="btn small primary full" id="new-item-save-btn" style="margin-top:8px;">${this._t("new_item_save_btn")}</button>
          </div>`;
        root.getElementById("new-item-save-btn").addEventListener("click", () => {
          const name = root.getElementById("new-item-name").value.trim();
          if (!name) {
            alert(this._t("alert_missing_item_name"));
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
      const item_name = prompt(this._t("prompt_intervention_done"));
      if (!item_name) return;
      const km = prompt(this._t("prompt_mileage"), this._selectedVehicle.mileage);
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
      picker.label = this._t("mileage_sensor_picker_label");
      picker.style.display = "block";
      picker.style.width = "100%";
      picker.addEventListener("value-changed", (e) => {
        this._pendingSensorEntity = e.detail.value;
      });
      slot.appendChild(picker);
    } else {
      slot.innerHTML = `<input type="text" id="sensor-entity-fallback" placeholder="${this._t("mileage_sensor_fallback_placeholder")}" value="${esc(this._pendingSensorEntity || "")}" />`;
      slot.querySelector("#sensor-entity-fallback").addEventListener("input", (e) => {
        this._pendingSensorEntity = e.target.value;
      });
    }
  }
}

// ---------------------------------------------------------------- helpers

function vehicleEmoji(v) {
  if (v.vehicle_type === "deux_roues") {
    if (v.two_wheeler_type === "velo_electrique") return "🚲";
    if (v.two_wheeler_type === "scooter") return "🛵";
    return "🏍️";
  }
  return "🚗";
}

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
  .title { font-family: var(--ce-font-header); font-size: 1.2em; font-weight: 600; letter-spacing:0.2px; color: var(--ce-text); display:flex; align-items:center; gap:8px; }
  .title-icon, .title svg { width:48px; height:48px; border-radius:10px; flex-shrink:0; }
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
  .font-size-row { display:flex; align-items:center; gap:12px; }
  .font-size-row .btn:disabled { opacity:0.4; cursor:default; }
  .vehicle-type-toggle { display:flex; gap:8px; margin-bottom:4px; }
  .vehicle-type-toggle .btn { flex:1; }
  .mileage-reminder-days-row { display:flex; align-items:center; gap:8px; margin-top:8px; }
  .mileage-reminder-days-row input { width:70px; padding:6px 8px; border-radius:8px; border:1px solid var(--ce-border); background: var(--ce-surface); color: var(--ce-text); }

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
