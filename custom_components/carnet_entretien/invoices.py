"""Helpers pour le stockage sur disque des factures d'entretien.

Les fichiers eux-mêmes ne vivent JAMAIS dans le Store JSON (storage.py) —
seule leur métadonnée y est gardée. Voir le commentaire en tête de
storage.py, section "Factures", pour la raison (taille du Store,
limite de message websocket).

Emplacement : config/carnet_entretien_files/<vehicle_id>/ — volontairement
PAS sous www/ (servi publiquement, sans authentification, par Home
Assistant) : ces fichiers sont servis par une HomeAssistantView dédiée
(voir __init__.py::InvoiceView) qui exige une session authentifiée.

Convention de nommage du fichier stocké sur disque :
    {YYYY-MM-DD}_{slug-du-nom-original}_{id-court}.{extension}
    ex : 2026-09-26_facture-garage-dupont_9f2a7c.pdf

- La date en tête rend le dossier trivialement triable/parcourable dans un
  gestionnaire de fichiers, même en dehors de Home Assistant (sauvegarde,
  export vers le garagiste, etc.).
- Le "slug" garde une trace lisible du nom d'origine (utile pour
  reconnaître un fichier en le survolant) sans jamais faire confiance au
  nom fourni par le navigateur (caractères spéciaux, chemins, homonymes).
- L'id court garantit l'unicité même pour deux uploads le même jour avec un
  nom très proche, sans quoi le second écraserait silencieusement le
  premier.
"""
from __future__ import annotations

import re
import unicodedata
import uuid
from datetime import date
from pathlib import Path

from homeassistant.core import HomeAssistant

INVOICES_DIR_NAME = "carnet_entretien_files"

ALLOWED_MIME_EXTENSIONS: dict[str, str] = {
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/jpg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
    "image/heic": "heic",
}

# Une facture scannée/photographiée dépasse rarement 5 Mo ; 10 Mo laisse de
# la marge sans s'approcher de la limite par défaut d'un message websocket
# Home Assistant (le fichier voyage en base64, donc ~+33 % en transit).
MAX_INVOICE_SIZE_BYTES = 10 * 1024 * 1024


def slugify(text: str, max_len: int = 40) -> str:
    """"Facture Garage Dupont (2).pdf" -> "facture-garage-dupont-2"."""
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"\.[a-zA-Z0-9]{1,6}$", "", text)  # retire une éventuelle extension
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    text = text[:max_len].strip("-")
    return text or "document"


def build_stored_filename(original_filename: str, mime: str) -> str:
    ext = ALLOWED_MIME_EXTENSIONS.get(mime)
    if not ext:
        raise ValueError(f"Type de fichier non supporté : {mime}")
    day = date.today().isoformat()
    slug = slugify(original_filename)
    short_id = uuid.uuid4().hex[:6]
    return f"{day}_{slug}_{short_id}.{ext}"


def vehicle_invoice_dir(hass: HomeAssistant, vehicle_id: str, base_dir: str | None = None) -> Path:
    """Dossier des factures d'un véhicule.

    base_dir : dossier personnalisé choisi dans les réglages
    ("invoices_base_dir"), ou None/"" pour l'emplacement par défaut
    (config/carnet_entretien_files). Toujours un sous-dossier par véhicule,
    y compris en dossier personnalisé, pour ne pas mélanger les factures de
    plusieurs véhicules dans le même dossier partagé.
    """
    if base_dir:
        return Path(base_dir) / vehicle_id
    return Path(hass.config.path(INVOICES_DIR_NAME, vehicle_id))


def is_invoices_dir_allowed(hass: HomeAssistant, base_dir: str) -> bool:
    """Bloquant (I/O) : à appeler via hass.async_add_executor_job.

    Un dossier personnalisé doit être dans allowlist_external_dirs, la
    liste des chemins que Home Assistant s'autorise à lire/écrire en
    dehors de sa propre gestion (voir configuration.yaml ->
    allowlist_external_dirs, ou tout point de montage sous config/media,
    config/share). Sans ça, l'écriture échouerait silencieusement pour de
    bonnes raisons de sécurité — mieux vaut le signaler clairement à la
    saisie plutôt que de laisser échouer un envoi de facture plus tard.
    """
    return hass.config.is_allowed_path(base_dir)
