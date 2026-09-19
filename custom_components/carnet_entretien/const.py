"""Constantes pour l'intégration Carnet d'entretien."""

DOMAIN = "carnet_entretien"
STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}_data"

CONF_GEMINI_API_KEY = "gemini_api_key"

SIGNAL_VEHICLES_UPDATED = f"{DOMAIN}_vehicles_updated"

# Modèles Gemini essayés dans l'ordre (repli automatique comme ha-millesime).
# gemini-1.5-flash a été retiré : Google a sunset la lignée 1.5 sur de
# nombreuses clés, ce qui provoquait une erreur "modèle indisponible"
# systématique en fin de cascade (masquant l'erreur réelle des modèles
# précédents). gemini-2.5-flash-lite ajouté comme repli plus économe, donc
# moins sujet aux quotas journaliers que 2.5-flash/2.0-flash.
GEMINI_MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
]
GEMINI_TIMEOUT = 45  # secondes
GEMINI_FREE_TIER_DAILY_BUDGET = 1_000_000  # tokens, ajustable

# Catégories d'entretien standard (utilisées pour l'icône/couleur côté carte)
CATEGORY_ICONS = {
    "moteur": "mdi:engine",
    "freinage": "mdi:car-brake-alert",
    "pneumatiques": "mdi:tire",
    "distribution": "mdi:cog",
    "filtration": "mdi:air-filter",
    "carrosserie": "mdi:car",
    "electronique": "mdi:chip",
    "controle_technique": "mdi:clipboard-check",
    "revision": "mdi:car-wrench",
    "autre": "mdi:wrench",
}

SEVERITY_ORDER = {"securite": 3, "majeur": 2, "mineur": 1}

# Statut d'une échéance calculée
STATUS_OK = "ok"
STATUS_SOON = "bientot"
STATUS_DUE = "echue"

# Seuils par défaut pour le statut "bientôt" (peuvent devenir des options)
SOON_KM_THRESHOLD = 1000
SOON_DAYS_THRESHOLD = 30
