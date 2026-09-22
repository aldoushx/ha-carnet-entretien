"""Constantes pour l'intégration Carnet d'entretien."""

DOMAIN = "carnet_entretien"
STORAGE_VERSION = 1
STORAGE_KEY = f"{DOMAIN}_data"

CONF_GEMINI_API_KEY = "gemini_api_key"
# Langue de contenu de l'intégration (carte, catalogue, IA, notifications —
# voir catalog_i18n.py) : choisie à l'installation, au même endroit que la
# clé Gemini, modifiable ensuite via les Options de l'intégration. Distincte
# de la langue de l'interface Home Assistant elle-même (réglage natif HA,
# par profil utilisateur), qui reste inchangée par ce paramètre.
CONF_LANGUAGE = "language"

SIGNAL_VEHICLES_UPDATED = f"{DOMAIN}_vehicles_updated"

# Modèles Gemini essayés dans l'ordre, avec repli automatique en cas d'échec.
#
# v1.3.3 : gemini-2.0-flash retiré — Google a définitivement arrêté cette
# lignée, ce qui renvoyait systématiquement une erreur HTTP 404 traduite en
# "Modèle indisponible pour cette clé". Ce repli étant placé en 2ème
# position, il masquait l'éventuelle vraie cause d'un échec du modèle
# précédent (ex : quota dépassé sur gemini-2.5-flash) en faisant échouer
# toute la cascade sur un modèle qui n'existe plus, quelle que soit la clé.
# gemini-2.5-flash-lite est conservé (l'accès dépend de l'ancienneté de la
# clé/du projet Google AI Studio, donc pas fiable pour tout le monde), mais
# la lignée 3.x — actuelle au moment de cet ajout — est ajoutée en repli
# supplémentaire pour garantir qu'au moins un modèle réponde même si la
# lignée 2.5 devient elle aussi indisponible (accès limité ou quota) :
# 3.5 Flash-Lite / 3.1 Flash-Lite d'abord (rapides, économes, équivalents
# du 2.5 Flash-Lite), puis 3.8 Flash en tout dernier recours (plus capable
# mais plus coûteux) plutôt que d'échouer sans réponse utilisable.
#
# Si Google fait à nouveau évoluer sa gamme de modèles et que la cascade
# entière échoue de nouveau avec des erreurs "indisponible" (HTTP 404),
# c'est le signe qu'un ou plusieurs de ces identifiants doivent être mis à
# jour vers la génération alors courante.
GEMINI_MODEL_CANDIDATES = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
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
