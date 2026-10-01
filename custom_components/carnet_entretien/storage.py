"""Couche de persistance locale (JSON via homeassistant.helpers.storage.Store).

Toutes les données restent en local dans .storage/carnet_entretien_data,
aucune donnée n'est envoyée ailleurs qu'à
Gemini, et uniquement au moment d'une génération explicite.
"""
from __future__ import annotations

import time
import uuid
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import STORAGE_KEY, STORAGE_VERSION


def new_id() -> str:
    return uuid.uuid4().hex[:12]


def now_ts() -> float:
    return time.time()


DEFAULT_SETTINGS: dict[str, Any] = {
    "theme": "gt_cuir",
    "hide_not_applicable": True,
    "notifications_enabled": False,
    "font_scale": 1.0,
    "mileage_reminder_enabled": True,
    "mileage_reminder_days": 30,
    # Rappels saisonniers (une notification persistante par véhicule à chaque
    # changement de saison, voir seasonal_reminders.py) — activés par défaut.
    "seasonal_reminders_enabled": True,
    # Dossier de stockage des factures : "" = emplacement par défaut
    # (config/carnet_entretien_files), sinon chemin absolu personnalisé
    # (doit être dans allowlist_external_dirs, voir invoices.py).
    "invoices_base_dir": "",
    # Langue de l'ensemble de l'intégration (carte, catalogue d'entretien,
    # contenu généré par Gemini, notifications persistantes) — un seul
    # réglage pour toute l'installation, pas par utilisateur HA : le
    # contenu IA est mis en cache et partagé entre tous les viewers du
    # tableau de bord, donc une langue par viewer n'aurait pas de sens.
    "language": "fr",
}

DEFAULT_DATA: dict[str, Any] = {
    "vehicles": {},      # id -> vehicle dict
    "model_cache": {},   # "marque|modele|motorisation|annee" -> {known_issues, cached_at}
    "motorisation_cache": {},  # "marque|modele|annee" -> {"list": [...], "cached_at": ...}
    "consumables_cache": {},  # même type de clé (+motorisation) -> {"list": [...], "cached_at": ...}
    "ai_usage": {"date": "", "tokens": 0},
    "settings": dict(DEFAULT_SETTINGS),
}


class CarnetStore:
    """Wrapper autour du Store HA, avec cache mémoire et helpers métier."""

    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
        self.data: dict[str, Any] = dict(DEFAULT_DATA)

    async def async_load(self) -> None:
        stored = await self._store.async_load()
        if stored:
            # fusion défensive : garde les clés par défaut si absentes (upgrade)
            merged = dict(DEFAULT_DATA)
            merged.update(stored)
            # "settings" mérite une fusion clé par clé (pas un simple écrasement) :
            # sinon un stockage antérieur à v0.10 (sans hide_not_applicable /
            # notifications_enabled) perdrait ces nouveaux réglages par défaut.
            merged["settings"] = {**DEFAULT_SETTINGS, **(stored.get("settings") or {})}
            # Migration v1.6.0 -> v1.7.0 : les thèmes "ha_light" et "ha_dark"
            # étaient un doublon exact (même rendu, car tous deux suivaient déjà
            # le thème HA courant) — fusionnés en un seul "ha_native".
            if merged["settings"].get("theme") in ("ha_light", "ha_dark"):
                merged["settings"]["theme"] = "ha_native"
            self.data = merged
        else:
            self.data = {
                "vehicles": {},
                "model_cache": {},
                "motorisation_cache": {},
                "consumables_cache": {},
                "ai_usage": {"date": "", "tokens": 0},
                "settings": dict(DEFAULT_SETTINGS),
            }

    async def async_save(self) -> None:
        await self._store.async_save(self.data)

    # ---------- Véhicules ----------

    @property
    def vehicles(self) -> dict[str, Any]:
        return self.data["vehicles"]

    def get_vehicle(self, vehicle_id: str) -> dict[str, Any] | None:
        return self.vehicles.get(vehicle_id)

    async def async_add_vehicle(self, vehicle: dict[str, Any]) -> dict[str, Any]:
        vehicle_id = new_id()
        vehicle = {
            "id": vehicle_id,
            "created_at": now_ts(),
            "mileage_history": [{"date": now_ts(), "km": vehicle.get("mileage", 0)}],
            "maintenance_plan": [],
            "maintenance_plan_sources": "",
            "known_issues": [],
            "known_issues_sources": "",
            "recalls": [],
            "recalls_sources": "",
            "recalls_checked_at": None,
            "value_history": [],
            "maintenance_log": [],
            "mileage_source": "manual",
            "mileage_sensor_entity_id": None,
            "photo": None,
            "fuel_type": "",
            "vehicle_type": "auto",
            "two_wheeler_type": "",
            "invoices": [],  # [{id, stored_filename, original_filename, mime, size, uploaded_at, label}]
            "consumables": [],  # [{id, label, value}] références des consommables (huile, pneus...)
            **vehicle,
        }
        vehicle["id"] = vehicle_id  # au cas où **vehicle contenait déjà "id"
        self.vehicles[vehicle_id] = vehicle
        await self.async_save()
        return vehicle

    async def async_update_vehicle(self, vehicle_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        vehicle.update(patch)
        await self.async_save()
        return vehicle

    async def async_remove_vehicle(self, vehicle_id: str) -> bool:
        if vehicle_id in self.vehicles:
            del self.vehicles[vehicle_id]
            await self.async_save()
            return True
        return False

    async def async_update_mileage(self, vehicle_id: str, mileage: int) -> dict[str, Any] | None:
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        vehicle["mileage"] = mileage
        vehicle.setdefault("mileage_history", []).append({"date": now_ts(), "km": mileage})
        await self.async_save()
        return vehicle

    async def async_set_mileage_source(
        self, vehicle_id: str, source: str, entity_id: str | None
    ) -> dict[str, Any] | None:
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        vehicle["mileage_source"] = source  # "manual" | "sensor"
        vehicle["mileage_sensor_entity_id"] = entity_id if source == "sensor" else None
        await self.async_save()
        return vehicle

    async def async_set_photo(self, vehicle_id: str, photo: str | None) -> dict[str, Any] | None:
        """photo : data URL base64 (déjà compressée côté navigateur) ou None pour retirer."""
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        vehicle["photo"] = photo
        await self.async_save()
        return vehicle

    async def async_set_seasonal_notified(self, vehicle_id: str, key: str | None) -> None:
        """Mémorise la saison (ex. "2026-autumn") pour laquelle la notification
        saisonnière a déjà été émise, afin de n'en créer qu'une par saison ;
        None l'efface (rappels désactivés : ils reviendront à la réactivation)."""
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle or vehicle.get("seasonal_notified") == key:
            return
        vehicle["seasonal_notified"] = key
        await self.async_save()

    async def async_set_consumables(self, vehicle_id: str, consumables: list[dict[str, Any]]) -> dict[str, Any] | None:
        """Remplace la liste des références de consommables du véhicule
        (huile, pneus, filtres...) : saisie libre libellé/valeur, le client
        envoie toujours la liste complète."""
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        cleaned = []
        for c in consumables:
            label = (c.get("label") or "").strip()
            value = (c.get("value") or "").strip()
            if not label and not value:
                continue  # ligne vide : ignorée
            cleaned.append({"id": c.get("id") or new_id(), "label": label[:80], "value": value[:300]})
        vehicle["consumables"] = cleaned
        await self.async_save()
        return vehicle

    # ---------- Factures ----------
    # Contrairement à la photo véhicule (data URL en base64 dans ce même
    # JSON), les factures sont écrites sur disque par __init__.py — seule
    # leur métadonnée vit ici, sinon ce fichier grossirait sans limite et
    # serait relu/réécrit en entier à chaque sauvegarde. Voir invoices.py.

    async def async_add_invoice(self, vehicle_id: str, invoice: dict[str, Any]) -> dict[str, Any] | None:
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        invoice = {"id": new_id(), "uploaded_at": now_ts(), **invoice}
        vehicle.setdefault("invoices", []).append(invoice)
        await self.async_save()
        return invoice

    async def async_remove_invoice(self, vehicle_id: str, invoice_id: str) -> dict[str, Any] | None:
        """Retire la métadonnée et renvoie l'entrée retirée (pour que l'appelant
        supprime le fichier correspondant sur disque) — et détache cette
        facture de toute échéance d'entretien qui la référençait, pour ne
        jamais laisser un lien mort dans l'historique.
        """
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        invoices = vehicle.get("invoices", [])
        removed = next((i for i in invoices if i.get("id") == invoice_id), None)
        if removed is None:
            return None
        vehicle["invoices"] = [i for i in invoices if i.get("id") != invoice_id]
        for entry in vehicle.get("maintenance_log", []):
            if invoice_id in (entry.get("invoice_ids") or []):
                entry["invoice_ids"] = [i for i in entry["invoice_ids"] if i != invoice_id]
        await self.async_save()
        return removed

    async def async_set_log_entry_invoices(
        self, vehicle_id: str, entry_id: str, invoice_ids: list[str]
    ) -> dict[str, Any] | None:
        """Lie/délie des factures existantes à une intervention déjà enregistrée
        (depuis l'onglet Historique) — remplace la liste, ne l'additionne pas.
        """
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        for entry in vehicle.get("maintenance_log", []):
            if entry.get("id") == entry_id:
                entry["invoice_ids"] = invoice_ids
                await self.async_save()
                return entry
        return None

    async def async_set_plan(
        self, vehicle_id: str, plan: list[dict[str, Any]], sources_summary: str = ""
    ) -> None:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is not None:
            vehicle["maintenance_plan"] = plan
            vehicle["maintenance_plan_sources"] = sources_summary
            await self.async_save()

    async def async_update_plan_item(
        self, vehicle_id: str, item_id: str, patch: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Modifie un item existant du plan en place (bascule
        applicable/non applicable, ajustement manuel d'échéance, mise en
        cache d'une explication DIY générée à la demande...) sans toucher
        aux autres items ni régénérer quoi que ce soit.
        """
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is None:
            return None
        for item in vehicle.get("maintenance_plan", []):
            if item.get("id") == item_id:
                item.update(patch)
                await self.async_save()
                return item
        return None

    async def async_add_plan_item(self, vehicle_id: str, item: dict[str, Any]) -> dict[str, Any] | None:
        """Ajoute un item personnalisé au plan sans toucher aux autres —
        permet de compléter une échéance oubliée sans perdre les dates de
        dernière intervention déjà enregistrées sur le reste du plan.
        """
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is None:
            return None
        item = {"id": f"custom_{new_id()}", "applicable": True, "custom": True, **item}
        vehicle.setdefault("maintenance_plan", []).append(item)
        await self.async_save()
        return item

    async def async_remove_plan_item(self, vehicle_id: str, item_id: str) -> bool:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is None:
            return False
        plan = vehicle.get("maintenance_plan", [])
        new_plan = [i for i in plan if i.get("id") != item_id]
        if len(new_plan) == len(plan):
            return False
        vehicle["maintenance_plan"] = new_plan
        await self.async_save()
        return True

    async def async_set_known_issues(
        self, vehicle_id: str, issues: list[dict[str, Any]], sources_summary: str = ""
    ) -> None:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is not None:
            vehicle["known_issues"] = issues
            vehicle["known_issues_sources"] = sources_summary
            await self.async_save()

    async def async_set_recalls(
        self, vehicle_id: str, recalls: list[dict[str, Any]], sources_summary: str = ""
    ) -> None:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is not None:
            vehicle["recalls"] = recalls
            vehicle["recalls_sources"] = sources_summary
            vehicle["recalls_checked_at"] = now_ts()
            await self.async_save()

    async def async_add_value_snapshot(self, vehicle_id: str, snapshot: dict[str, Any]) -> None:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is not None:
            vehicle.setdefault("value_history", []).append(snapshot)
            await self.async_save()

    async def async_log_maintenance(self, vehicle_id: str, entry: dict[str, Any]) -> dict[str, Any] | None:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is None:
            return None
        entry = {"id": new_id(), "date": now_ts(), **entry}
        vehicle.setdefault("maintenance_log", []).append(entry)
        item_id = entry.get("item_id")
        if item_id:
            self._recompute_last_done(vehicle, item_id)
        await self.async_save()
        return entry

    async def async_remove_log_entry(self, vehicle_id: str, entry_id: str) -> dict[str, Any] | None:
        """Supprime une intervention de l'historique (erreur de saisie...) et
        redérive l'échéance du plan correspondante à partir de ce qu'il reste
        dans l'historique — sans quoi une échéance supprimée par erreur
        continuerait à afficher "fait le ..." comme si de rien n'était.
        """
        vehicle = self.vehicles.get(vehicle_id)
        if not vehicle:
            return None
        log = vehicle.get("maintenance_log", [])
        removed = next((e for e in log if e.get("id") == entry_id), None)
        if removed is None:
            return None
        vehicle["maintenance_log"] = [e for e in log if e.get("id") != entry_id]
        item_id = removed.get("item_id")
        if item_id:
            self._recompute_last_done(vehicle, item_id)
        await self.async_save()
        return removed

    def _recompute_last_done(self, vehicle: dict[str, Any], item_id: str) -> None:
        """Redérive last_done_km/last_done_date d'une échéance du plan à
        partir de l'entrée la plus récente de l'historique qui lui est
        rattachée — plutôt que de se contenter d'écraser avec "la dernière
        entrée saisie", ce qui serait incorrect après une suppression, ou
        après la saisie a posteriori d'une date antérieure à celle déjà
        enregistrée.
        """
        item = next((i for i in vehicle.get("maintenance_plan", []) if i.get("id") == item_id), None)
        if item is None:
            return
        matching = [e for e in vehicle.get("maintenance_log", []) if e.get("item_id") == item_id]
        if not matching:
            item["last_done_km"] = None
            item["last_done_date"] = None
            return
        best = max(matching, key=lambda e: (e.get("date") or 0, e.get("km") or 0))
        item["last_done_km"] = best.get("km")
        item["last_done_date"] = best.get("date")

    # ---------- Cache modèle (points de vigilance mutualisés) ----------

    def model_cache_key(self, brand: str, model: str, motorisation: str, year: int, language: str = "fr") -> str:
        # "language" fait partie de la clé : les points de vigilance et
        # rappels constructeur mis en cache sont du texte généré par Gemini
        # dans une langue donnée — un changement de langue ne doit jamais
        # resservir un texte en français à un utilisateur qui vient de
        # basculer en anglais (ou l'inverse). Chaque langue a son propre
        # cache par modèle, ce qui reste cohérent avec l'objectif du cache
        # (mutualiser entre véhicules identiques) tout en couvrant le cas
        # multilingue.
        return (
            f"{brand.strip().lower()}|{model.strip().lower()}|{(motorisation or '').strip().lower()}"
            f"|{year}|{language}"
        )

    def get_model_cache(self, key: str) -> dict[str, Any] | None:
        return self.data["model_cache"].get(key)

    async def async_set_model_cache(
        self, key: str, known_issues: list[dict[str, Any]], sources_summary: str = ""
    ) -> None:
        self.data["model_cache"][key] = {
            "known_issues": known_issues,
            "sources_summary": sources_summary,
            "cached_at": now_ts(),
        }
        await self.async_save()

    def get_recalls_cache(self, key: str) -> dict[str, Any] | None:
        entry = self.data["model_cache"].get(key)
        return entry if entry and "recalls" in entry else None

    async def async_set_recalls_cache(
        self, key: str, recalls: list[dict[str, Any]], sources_summary: str = ""
    ) -> None:
        entry = self.data["model_cache"].setdefault(key, {})
        entry["recalls"] = recalls
        entry["recalls_sources"] = sources_summary
        entry["recalls_cached_at"] = now_ts()
        await self.async_save()

    # ---------- Cache des motorisations (autocomplétion du champ "version") ----------

    def motorisation_cache_key(
        self, brand: str, model: str, year: int, fuel_type: str = "",
        vehicle_type: str = "auto", two_wheeler_type: str = "",
    ) -> str:
        return (
            f"{brand.strip().lower()}|{model.strip().lower()}|{year}|{fuel_type.strip().lower()}"
            f"|{vehicle_type}|{two_wheeler_type}"
        )

    def get_motorisation_cache(self, key: str) -> list[str] | None:
        entry = self.data["motorisation_cache"].get(key)
        return entry["list"] if entry else None

    async def async_set_motorisation_cache(self, key: str, motorisations: list[str]) -> None:
        self.data["motorisation_cache"][key] = {"list": motorisations, "cached_at": now_ts()}
        await self.async_save()

    # ---------- Cache des suggestions de consommables (onglet Références) ----------

    def consumables_cache_key(
        self, brand: str, model: str, year: int, motorisation: str = "", fuel_type: str = "",
        vehicle_type: str = "auto", two_wheeler_type: str = "", labels: list[str] | None = None,
    ) -> str:
        # Le résultat dépend maintenant des libellés explicitement demandés
        # (voir __init__.py::ws_suggest_consumables) : ils font partie de la
        # clé, triés pour que l'ordre de sélection ne change pas le cache.
        labels_part = "|".join(sorted((l or "").strip().lower() for l in (labels or [])))
        return (
            f"{brand.strip().lower()}|{model.strip().lower()}|{year}|{motorisation.strip().lower()}"
            f"|{fuel_type.strip().lower()}|{vehicle_type}|{two_wheeler_type}|{labels_part}"
        )

    def get_consumables_cache(self, key: str) -> list[dict[str, str]] | None:
        entry = self.data["consumables_cache"].get(key)
        return entry["list"] if entry else None

    async def async_set_consumables_cache(self, key: str, items: list[dict[str, str]]) -> None:
        self.data["consumables_cache"][key] = {"list": items, "cached_at": now_ts()}
        await self.async_save()

    # ---------- Réglages (thème visuel, etc.) ----------

    def get_settings(self) -> dict[str, Any]:
        settings = self.data.setdefault("settings", dict(DEFAULT_SETTINGS))
        for key, value in DEFAULT_SETTINGS.items():
            settings.setdefault(key, value)
        return settings

    async def async_set_settings(self, patch: dict[str, Any]) -> dict[str, Any]:
        settings = self.get_settings()
        settings.update(patch)
        await self.async_save()
        return settings

    # ---------- Suivi tokens IA (budget quotidien Gemini) ----------

    async def async_add_token_usage(self, tokens: int) -> None:
        import datetime

        today = datetime.date.today().isoformat()
        usage = self.data.setdefault("ai_usage", {"date": today, "tokens": 0})
        if usage.get("date") != today:
            usage["date"] = today
            usage["tokens"] = 0
        usage["tokens"] += tokens
        await self.async_save()
