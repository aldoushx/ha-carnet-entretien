"""Capteurs HA : un jeu de 3 capteurs par véhicule, créés/retirés dynamiquement
quand des véhicules sont ajoutés/supprimés via la carte ou les services.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SIGNAL_VEHICLES_UPDATED
from .storage import CarnetStore
from .utils import next_due_item

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    store: CarnetStore = hass.data[DOMAIN][entry.entry_id]["store"]
    known_ids: set[str] = set()

    @callback
    def _sync_entities() -> None:
        new_entities = []
        for vehicle_id, vehicle in store.vehicles.items():
            if vehicle_id in known_ids:
                continue
            try:
                known_ids.add(vehicle_id)
                new_entities += [
                    NextMaintenanceSensor(store, vehicle_id),
                    MileageSensor(store, vehicle_id),
                    ResaleValueSensor(store, vehicle_id),
                ]
            except Exception:  # noqa: BLE001 - un véhicule mal formé ne doit jamais bloquer les autres
                _LOGGER.exception("Impossible de créer les capteurs pour le véhicule %s", vehicle_id)
        # Les suppressions passent par le registre d'entités (retrait explicite),
        # gérées dans __init__.py au moment de remove_vehicle.
        if new_entities:
            async_add_entities(new_entities)

    _sync_entities()
    entry.async_on_unload(async_dispatcher_connect(hass, SIGNAL_VEHICLES_UPDATED, _sync_entities))


class _VehicleSensorBase(SensorEntity):
    _attr_should_poll = False

    def __init__(self, store: CarnetStore, vehicle_id: str, suffix: str, name_suffix: str) -> None:
        self._store = store
        self._vehicle_id = vehicle_id
        self._attr_unique_id = f"{DOMAIN}_{vehicle_id}_{suffix}"
        self._name_suffix = name_suffix

    @property
    def _vehicle(self) -> dict[str, Any] | None:
        return self._store.vehicles.get(self._vehicle_id)

    @property
    def available(self) -> bool:
        return self._vehicle is not None

    @property
    def name(self) -> str:
        v = self._vehicle
        label = f"{v.get('brand', '?')} {v.get('model', '?')}" if v else self._vehicle_id
        return f"{label} - {self._name_suffix}"

    @property
    def device_info(self):
        v = self._vehicle
        if not v:
            return None
        return {
            "identifiers": {(DOMAIN, self._vehicle_id)},
            "name": f"{v.get('brand', '?')} {v.get('model', '?')} ({v.get('year', '?')})",
            "manufacturer": v.get("brand", "?"),
            "model": v.get("model", "?"),
        }


class NextMaintenanceSensor(_VehicleSensorBase):
    _attr_icon = "mdi:wrench-clock"

    def __init__(self, store: CarnetStore, vehicle_id: str) -> None:
        super().__init__(store, vehicle_id, "next_maintenance", "Prochaine échéance")

    @property
    def native_value(self) -> str | None:
        v = self._vehicle
        item = next_due_item(v) if v else None
        return item["name"] if item else "Aucune"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        v = self._vehicle
        item = next_due_item(v) if v else None
        if not item:
            return {}
        return {
            "statut": item["statut"],
            "km_restants": item["km_restants"],
            "jours_restants": item["jours_restants"],
            "due_km": item["due_km"],
            "due_date": item["due_date"],
            "prevu_vers": item.get("prevu_vers"),
            "depasse_de_km": item.get("depasse_de_km"),
            "cout_estime_eur": item.get("cost_estimate_eur"),
            "km_annuel_moyen": item.get("annual_km"),
            "categorie": item.get("category"),
        }


class MileageSensor(_VehicleSensorBase):
    _attr_icon = "mdi:counter"
    _attr_native_unit_of_measurement = "km"

    def __init__(self, store: CarnetStore, vehicle_id: str) -> None:
        super().__init__(store, vehicle_id, "mileage", "Kilométrage")

    @property
    def native_value(self) -> int | None:
        v = self._vehicle
        return v.get("mileage") if v else None


class ResaleValueSensor(_VehicleSensorBase):
    _attr_icon = "mdi:cash"
    _attr_native_unit_of_measurement = "EUR"

    def __init__(self, store: CarnetStore, vehicle_id: str) -> None:
        super().__init__(store, vehicle_id, "resale_value", "Valeur estimée")

    @property
    def native_value(self) -> float | None:
        v = self._vehicle
        history = v.get("value_history") if v else None
        return history[-1]["value_avg"] if history else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        v = self._vehicle
        history = v.get("value_history") if v else None
        if not history:
            return {}
        last = history[-1]
        return {
            "value_min": last.get("value_min"),
            "value_max": last.get("value_max"),
            "km_lors_estimation": last.get("km"),
            "date": last.get("date"),
        }
