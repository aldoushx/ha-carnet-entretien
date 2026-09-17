"""Couche de persistance locale (JSON via homeassistant.helpers.storage.Store).

Toutes les données restent en local dans .storage/carnet_entretien_data,
à l'image de ha-millesime : aucune donnée n'est envoyée ailleurs qu'à
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


DEFAULT_DATA: dict[str, Any] = {
    "vehicles": {},      # id -> vehicle dict
    "model_cache": {},   # "marque|modele|motorisation|annee" -> {known_issues, cached_at}
    "motorisation_cache": {},  # "marque|modele|annee" -> {"list": [...], "cached_at": ...}
    "ai_usage": {"date": "", "tokens": 0},
    "settings": {"theme": "gt_cuir"},
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
            self.data = merged
        else:
            self.data = {
                "vehicles": {},
                "model_cache": {},
                "motorisation_cache": {},
                "ai_usage": {"date": "", "tokens": 0},
                "settings": {"theme": "gt_cuir"},
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

    async def async_set_plan(self, vehicle_id: str, plan: list[dict[str, Any]]) -> None:
        vehicle = self.vehicles.get(vehicle_id)
        if vehicle is not None:
            vehicle["maintenance_plan"] = plan
            await self.async_save()

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
        # Met à jour l'échéance correspondante du plan, si liée par item_id
        item_id = entry.get("item_id")
        if item_id:
            for item in vehicle.get("maintenance_plan", []):
                if item.get("id") == item_id:
                    item["last_done_km"] = entry.get("km")
                    item["last_done_date"] = entry.get("date")
                    break
        await self.async_save()
        return entry

    # ---------- Cache modèle (points de vigilance mutualisés) ----------

    def model_cache_key(self, brand: str, model: str, motorisation: str, year: int) -> str:
        return f"{brand.strip().lower()}|{model.strip().lower()}|{(motorisation or '').strip().lower()}|{year}"

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

    def motorisation_cache_key(self, brand: str, model: str, year: int) -> str:
        return f"{brand.strip().lower()}|{model.strip().lower()}|{year}"

    def get_motorisation_cache(self, key: str) -> list[str] | None:
        entry = self.data["motorisation_cache"].get(key)
        return entry["list"] if entry else None

    async def async_set_motorisation_cache(self, key: str, motorisations: list[str]) -> None:
        self.data["motorisation_cache"][key] = {"list": motorisations, "cached_at": now_ts()}
        await self.async_save()

    # ---------- Réglages (thème visuel, etc.) ----------

    def get_settings(self) -> dict[str, Any]:
        return self.data.setdefault("settings", {"theme": "gt_cuir"})

    async def async_set_settings(self, patch: dict[str, Any]) -> dict[str, Any]:
        settings = self.data.setdefault("settings", {"theme": "gt_cuir"})
        settings.update(patch)
        await self.async_save()
        return settings

    # ---------- Suivi tokens IA (comme le budget quotidien Gemini de ha-millesime) ----------

    async def async_add_token_usage(self, tokens: int) -> None:
        import datetime

        today = datetime.date.today().isoformat()
        usage = self.data.setdefault("ai_usage", {"date": today, "tokens": 0})
        if usage.get("date") != today:
            usage["date"] = today
            usage["tokens"] = 0
        usage["tokens"] += tokens
        await self.async_save()
