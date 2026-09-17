"""Intégration Carnet d'entretien.

Structure calquée sur ha-millesime :
- stockage JSON local (storage.py)
- appels Gemini côté serveur (gemini_client.py)
- API websocket consommée par la carte Lovelace auto-servie (www/)
- services HA pour les automatisations (services.yaml)
"""
from __future__ import annotations

import json
import logging
from datetime import date, datetime
from pathlib import Path

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.entity_registry import async_entries_for_config_entry, async_get as async_get_entity_registry
from homeassistant.helpers.event import async_track_state_change_event

from .const import CONF_GEMINI_API_KEY, DOMAIN, SIGNAL_VEHICLES_UPDATED
from .gemini_client import GeminiClient, GeminiError
from .storage import CarnetStore
from .utils import compute_plan_status, estimate_annual_km

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

REFERENTIEL_PATH = Path(__file__).parent / "data" / "referentiel.json"
CARD_JS_PATH = Path(__file__).parent / "www" / "carnet-entretien-card.js"
CARD_URL = f"/{DOMAIN}/carnet-entretien-card.js"


def _load_referentiel_file() -> dict[str, list[str]]:
    """Lecture synchrone du JSON référentiel — à n'appeler que via
    hass.async_add_executor_job pour ne pas bloquer la boucle asyncio."""
    with open(REFERENTIEL_PATH, encoding="utf-8") as f:
        return json.load(f)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})

    store = CarnetStore(hass)
    await store.async_load()

    api_key = entry.options.get(CONF_GEMINI_API_KEY, entry.data.get(CONF_GEMINI_API_KEY, ""))
    session = async_get_clientsession(hass)
    gemini = GeminiClient(session, api_key)

    referentiel: dict[str, list[str]] = await hass.async_add_executor_job(_load_referentiel_file)

    hass.data[DOMAIN][entry.entry_id] = {
        "store": store,
        "gemini": gemini,
        "referentiel": referentiel,
        "mileage_unsubs": {},
    }

    entry.async_on_unload(entry.add_update_listener(_async_reload_on_options_update))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _async_register_websocket_api(hass, entry)
    _async_register_services(hass, entry)
    await _async_register_static_path(hass)

    for vehicle_id in list(store.vehicles.keys()):
        _async_sync_mileage_listener(hass, entry, vehicle_id)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        for unsub in hass.data[DOMAIN][entry.entry_id].get("mileage_unsubs", {}).values():
            unsub()
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return ok


async def _async_reload_on_options_update(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


# ---------------------------------------------------------------------------
# Liaison à un capteur de kilométrage existant dans HA
# ---------------------------------------------------------------------------


def _async_sync_mileage_listener(hass: HomeAssistant, entry: ConfigEntry, vehicle_id: str) -> None:
    """(Ré)abonne, ou désabonne, le véhicule aux changements d'état de son
    capteur de kilométrage lié, selon sa configuration actuelle en storage.
    """
    store: CarnetStore = hass.data[DOMAIN][entry.entry_id]["store"]
    unsubs: dict = hass.data[DOMAIN][entry.entry_id]["mileage_unsubs"]

    existing = unsubs.pop(vehicle_id, None)
    if existing:
        existing()

    vehicle = store.get_vehicle(vehicle_id)
    if not vehicle or vehicle.get("mileage_source") != "sensor":
        return
    entity_id = vehicle.get("mileage_sensor_entity_id")
    if not entity_id:
        return

    async def _on_state_change(event) -> None:
        new_state = event.data.get("new_state")
        if new_state is None or new_state.state in ("unknown", "unavailable"):
            return
        try:
            mileage = round(float(new_state.state))
        except (TypeError, ValueError):
            _LOGGER.warning("Capteur %s : état non numérique (%s)", entity_id, new_state.state)
            return
        current = store.get_vehicle(vehicle_id)
        if current is None or current.get("mileage") == mileage:
            return
        await store.async_update_mileage(vehicle_id, mileage)
        async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)

    unsubs[vehicle_id] = async_track_state_change_event(hass, [entity_id], _on_state_change)

    # Synchronise immédiatement sur l'état courant du capteur, si disponible.
    state = hass.states.get(entity_id)
    if state and state.state not in ("unknown", "unavailable"):
        try:
            mileage = round(float(state.state))
        except (TypeError, ValueError):
            return
        if vehicle.get("mileage") != mileage:
            hass.async_create_task(store.async_update_mileage(vehicle_id, mileage))


async def _async_register_static_path(hass: HomeAssistant) -> None:
    """Sert la carte Lovelace directement depuis le composant (rien à copier
    dans /www/) et l'enregistre comme ressource frontend, comme ha-millesime.

    Utilise l'API moderne (HA 2024.7+) : `register_static_path` (synchrone)
    a été retiré au profit de `async_register_static_paths`, et l'accès via
    `hass.components.frontend` est également déprécié au profit d'un import
    direct.
    """
    if hass.data[DOMAIN].get("_static_registered"):
        return
    hass.data[DOMAIN]["_static_registered"] = True

    await hass.http.async_register_static_paths(
        [StaticPathConfig(CARD_URL, str(CARD_JS_PATH), cache_headers=False)]
    )

    version = CARD_JS_PATH.stat().st_mtime_ns  # cache-busting à chaque modification du fichier
    add_extra_js_url(hass, f"{CARD_URL}?v={version}")


# ---------------------------------------------------------------------------
# Services HA (pour automatisations)
# ---------------------------------------------------------------------------


def _async_register_services(hass: HomeAssistant, entry: ConfigEntry) -> None:
    store: CarnetStore = hass.data[DOMAIN][entry.entry_id]["store"]
    gemini: GeminiClient = hass.data[DOMAIN][entry.entry_id]["gemini"]

    async def add_vehicle(call: ServiceCall) -> None:
        await _create_vehicle(hass, entry, store, gemini, dict(call.data))

    async def update_mileage(call: ServiceCall) -> None:
        await store.async_update_mileage(call.data["vehicle_id"], call.data["mileage"])
        async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)

    async def set_mileage_source(call: ServiceCall) -> None:
        await _set_mileage_source(
            hass, entry, store, call.data["vehicle_id"], call.data["source"], call.data.get("entity_id")
        )

    async def log_maintenance(call: ServiceCall) -> None:
        data = dict(call.data)
        vehicle_id = data.pop("vehicle_id")
        if isinstance(data.get("date"), str):
            data["date"] = datetime.combine(date.fromisoformat(data["date"]), datetime.min.time()).timestamp()
        await store.async_log_maintenance(vehicle_id, data)

    async def refresh_plan(call: ServiceCall) -> None:
        await _refresh_plan(store, gemini, call.data["vehicle_id"])

    async def refresh_known_issues(call: ServiceCall) -> None:
        await _refresh_known_issues(store, gemini, call.data["vehicle_id"])

    async def refresh_recalls(call: ServiceCall) -> None:
        await _refresh_recalls(store, gemini, call.data["vehicle_id"])
        async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)

    async def value_snapshot(call: ServiceCall) -> None:
        await _snapshot_value(store, gemini, call.data["vehicle_id"], call.data.get("condition", "correct"))

    async def remove_vehicle(call: ServiceCall) -> None:
        await _remove_vehicle(hass, entry, store, call.data["vehicle_id"])

    hass.services.async_register(DOMAIN, "add_vehicle", add_vehicle)
    hass.services.async_register(DOMAIN, "update_mileage", update_mileage)
    hass.services.async_register(DOMAIN, "set_mileage_source", set_mileage_source)
    hass.services.async_register(DOMAIN, "log_maintenance", log_maintenance)
    hass.services.async_register(DOMAIN, "refresh_plan", refresh_plan)
    hass.services.async_register(DOMAIN, "refresh_known_issues", refresh_known_issues)
    hass.services.async_register(DOMAIN, "refresh_recalls", refresh_recalls)
    hass.services.async_register(DOMAIN, "value_snapshot", value_snapshot)
    hass.services.async_register(DOMAIN, "remove_vehicle", remove_vehicle)


# ---------------------------------------------------------------------------
# Logique métier partagée entre services et websocket
# ---------------------------------------------------------------------------


async def _create_vehicle(hass: HomeAssistant, entry: ConfigEntry, store: CarnetStore, gemini: GeminiClient, data: dict) -> dict:
    vehicle = await store.async_add_vehicle(
        {
            "brand": data["brand"],
            "model": data["model"],
            "motorisation": data.get("motorisation", ""),
            "year": int(data["year"]),
            "mileage": int(data["mileage"]),
            "plate": data.get("plate", ""),
            "photo": data.get("photo") or None,
        }
    )
    vehicle_id = vehicle["id"]

    if data.get("mileage_source") == "sensor" and data.get("mileage_sensor_entity_id"):
        await store.async_set_mileage_source(vehicle_id, "sensor", data["mileage_sensor_entity_id"])
        _async_sync_mileage_listener(hass, entry, vehicle_id)

    errors = {}
    try:
        await _refresh_plan(store, gemini, vehicle_id)
    except GeminiError as err:
        errors["plan"] = err.code
    try:
        await _refresh_known_issues(store, gemini, vehicle_id)
    except GeminiError as err:
        errors["known_issues"] = err.code
    try:
        await _refresh_recalls(store, gemini, vehicle_id)
    except GeminiError as err:
        errors["recalls"] = err.code

    async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)
    result = dict(store.get_vehicle(vehicle_id))
    if errors:
        result["_ai_errors"] = errors
    return result


async def _refresh_plan(store: CarnetStore, gemini: GeminiClient, vehicle_id: str) -> None:
    vehicle = store.get_vehicle(vehicle_id)
    if not vehicle:
        raise ValueError("Véhicule inconnu")
    result = await gemini.generate_maintenance_plan(
        vehicle["brand"], vehicle["model"], vehicle.get("motorisation", ""),
        vehicle["year"], vehicle.get("mileage", 0),
    )
    plan = [{"id": f"item_{i}", **item} for i, item in enumerate(result.data)]
    await store.async_set_plan(vehicle_id, plan)
    await store.async_add_token_usage(result.tokens)


async def _refresh_known_issues(store: CarnetStore, gemini: GeminiClient, vehicle_id: str) -> None:
    vehicle = store.get_vehicle(vehicle_id)
    if not vehicle:
        raise ValueError("Véhicule inconnu")

    # Mutualisation par modèle : on ne réinterroge pas Gemini si un véhicule
    # identique (marque+modèle+motorisation+année) a déjà été analysé.
    cache_key = store.model_cache_key(
        vehicle["brand"], vehicle["model"], vehicle.get("motorisation", ""), vehicle["year"]
    )
    cached = store.get_model_cache(cache_key)
    if cached:
        await store.async_set_known_issues(
            vehicle_id, cached["known_issues"], cached.get("sources_summary", "")
        )
        return

    result = await gemini.generate_known_issues(
        vehicle["brand"], vehicle["model"], vehicle.get("motorisation", ""), vehicle["year"]
    )
    sources_summary = result.data.get("sources_summary", "")
    issues = [{"id": f"issue_{i}", **issue} for i, issue in enumerate(result.data.get("issues", []))]
    await store.async_set_known_issues(vehicle_id, issues, sources_summary)
    await store.async_set_model_cache(cache_key, issues, sources_summary)
    await store.async_add_token_usage(result.tokens)


async def _refresh_recalls(store: CarnetStore, gemini: GeminiClient, vehicle_id: str) -> None:
    vehicle = store.get_vehicle(vehicle_id)
    if not vehicle:
        raise ValueError("Véhicule inconnu")

    # Mutualisation par modèle, même clé que les points de vigilance : un
    # rappel constructeur concerne le modèle, pas un exemplaire précis.
    cache_key = store.model_cache_key(
        vehicle["brand"], vehicle["model"], vehicle.get("motorisation", ""), vehicle["year"]
    )
    cached = store.get_recalls_cache(cache_key)
    if cached:
        await store.async_set_recalls(vehicle_id, cached["recalls"], cached.get("recalls_sources", ""))
        return

    result = await gemini.check_recalls(
        vehicle["brand"], vehicle["model"], vehicle.get("motorisation", ""), vehicle["year"]
    )
    sources_summary = ", ".join(result.data.get("sources", [])) if isinstance(result.data.get("sources"), list) else str(result.data.get("sources", ""))
    recalls = [{"id": f"recall_{i}", **r} for i, r in enumerate(result.data.get("recalls", []))]
    await store.async_set_recalls(vehicle_id, recalls, sources_summary)
    await store.async_set_recalls_cache(cache_key, recalls, sources_summary)
    await store.async_add_token_usage(result.tokens)


async def _snapshot_value(store: CarnetStore, gemini: GeminiClient, vehicle_id: str, condition: str) -> dict:
    vehicle = store.get_vehicle(vehicle_id)
    if not vehicle:
        raise ValueError("Véhicule inconnu")
    result = await gemini.estimate_resale_value(
        vehicle["brand"], vehicle["model"], vehicle.get("motorisation", ""),
        vehicle["year"], vehicle.get("mileage", 0), estimate_annual_km(vehicle), condition,
    )
    snapshot = {
        "date": __import__("time").time(),
        "km": vehicle.get("mileage", 0),
        **result.data,
    }
    await store.async_add_value_snapshot(vehicle_id, snapshot)
    await store.async_add_token_usage(result.tokens)
    return snapshot


async def _remove_vehicle(hass: HomeAssistant, entry: ConfigEntry, store: CarnetStore, vehicle_id: str) -> None:
    registry = async_get_entity_registry(hass)
    for reg_entry in async_entries_for_config_entry(registry, entry.entry_id):
        if reg_entry.unique_id.startswith(f"{DOMAIN}_{vehicle_id}_"):
            registry.async_remove(reg_entry.entity_id)
    unsubs: dict = hass.data[DOMAIN][entry.entry_id]["mileage_unsubs"]
    unsub = unsubs.pop(vehicle_id, None)
    if unsub:
        unsub()
    await store.async_remove_vehicle(vehicle_id)
    async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)


async def _set_mileage_source(
    hass: HomeAssistant, entry: ConfigEntry, store: CarnetStore, vehicle_id: str, source: str, entity_id: str | None
) -> dict | None:
    vehicle = await store.async_set_mileage_source(vehicle_id, source, entity_id)
    _async_sync_mileage_listener(hass, entry, vehicle_id)
    async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)
    return vehicle


# ---------------------------------------------------------------------------
# API websocket consommée par la carte
# ---------------------------------------------------------------------------


def _serialize_vehicle(vehicle: dict) -> dict:
    v = dict(vehicle)
    v["maintenance_plan"] = compute_plan_status(vehicle)
    return v


def _async_register_websocket_api(hass: HomeAssistant, entry: ConfigEntry) -> None:
    store: CarnetStore = hass.data[DOMAIN][entry.entry_id]["store"]
    gemini: GeminiClient = hass.data[DOMAIN][entry.entry_id]["gemini"]
    referentiel: dict[str, list[str]] = hass.data[DOMAIN][entry.entry_id]["referentiel"]

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/get_vehicles"})
    @websocket_api.async_response
    async def ws_get_vehicles(hass, connection, msg):
        vehicles = [_serialize_vehicle(v) for v in store.vehicles.values()]
        connection.send_result(msg["id"], {"vehicles": vehicles, "settings": store.get_settings()})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/search_referentiel",
            vol.Optional("brand"): str,
            vol.Optional("query", default=""): str,
        }
    )
    @websocket_api.async_response
    async def ws_search_referentiel(hass, connection, msg):
        query = msg["query"].strip().lower()
        if msg.get("brand"):
            models = referentiel.get(msg["brand"], [])
            results = [m for m in models if query in m.lower()] if query else models
            connection.send_result(msg["id"], {"results": results})
        else:
            brands = list(referentiel.keys())
            results = [b for b in brands if query in b.lower()] if query else brands
            connection.send_result(msg["id"], {"results": results})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/search_motorisations",
            vol.Required("brand"): str,
            vol.Required("model"): str,
            vol.Required("year"): int,
            vol.Optional("query", default=""): str,
        }
    )
    @websocket_api.async_response
    async def ws_search_motorisations(hass, connection, msg):
        key = store.motorisation_cache_key(msg["brand"], msg["model"], msg["year"])
        options = store.get_motorisation_cache(key)
        if options is None:
            try:
                result = await gemini.list_motorisations(msg["brand"], msg["model"], msg["year"])
                options = [str(o) for o in result.data]
                await store.async_set_motorisation_cache(key, options)
                await store.async_add_token_usage(result.tokens)
            except GeminiError:
                # Pas de clé configurée, ou échec ponctuel : champ libre, pas de suggestion.
                options = []
        query = msg["query"].strip().lower()
        results = [o for o in options if query in o.lower()] if query else options
        connection.send_result(msg["id"], {"results": results})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/add_vehicle",
            vol.Required("brand"): str,
            vol.Required("model"): str,
            vol.Optional("motorisation", default=""): str,
            vol.Required("year"): int,
            vol.Required("mileage"): int,
            vol.Optional("plate", default=""): str,
            vol.Optional("mileage_source"): vol.In(["manual", "sensor"]),
            vol.Optional("mileage_sensor_entity_id"): str,
            vol.Optional("photo"): str,
        }
    )
    @websocket_api.async_response
    async def ws_add_vehicle(hass, connection, msg):
        data = {k: v for k, v in msg.items() if k not in ("id", "type")}
        try:
            vehicle = await _create_vehicle(hass, entry, store, gemini, data)
            connection.send_result(msg["id"], {"vehicle": _serialize_vehicle(vehicle)})
        except GeminiError as err:
            connection.send_error(msg["id"], err.code, str(err))

    @websocket_api.websocket_command(
        {vol.Required("type"): f"{DOMAIN}/remove_vehicle", vol.Required("vehicle_id"): str}
    )
    @websocket_api.async_response
    async def ws_remove_vehicle(hass, connection, msg):
        await _remove_vehicle(hass, entry, store, msg["vehicle_id"])
        connection.send_result(msg["id"], {"ok": True})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/update_mileage",
            vol.Required("vehicle_id"): str,
            vol.Required("mileage"): int,
        }
    )
    @websocket_api.async_response
    async def ws_update_mileage(hass, connection, msg):
        vehicle = await store.async_update_mileage(msg["vehicle_id"], msg["mileage"])
        async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)
        connection.send_result(msg["id"], {"vehicle": _serialize_vehicle(vehicle) if vehicle else None})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/set_mileage_source",
            vol.Required("vehicle_id"): str,
            vol.Required("source"): vol.In(["manual", "sensor"]),
            vol.Optional("entity_id"): str,
        }
    )
    @websocket_api.async_response
    async def ws_set_mileage_source(hass, connection, msg):
        vehicle = await _set_mileage_source(
            hass, entry, store, msg["vehicle_id"], msg["source"], msg.get("entity_id")
        )
        connection.send_result(msg["id"], {"vehicle": _serialize_vehicle(vehicle) if vehicle else None})

    @websocket_api.websocket_command(
        {vol.Required("type"): f"{DOMAIN}/refresh_plan", vol.Required("vehicle_id"): str}
    )
    @websocket_api.async_response
    async def ws_refresh_plan(hass, connection, msg):
        try:
            await _refresh_plan(store, gemini, msg["vehicle_id"])
            connection.send_result(msg["id"], {"vehicle": _serialize_vehicle(store.get_vehicle(msg["vehicle_id"]))})
        except GeminiError as err:
            connection.send_error(msg["id"], err.code, str(err))

    @websocket_api.websocket_command(
        {vol.Required("type"): f"{DOMAIN}/refresh_known_issues", vol.Required("vehicle_id"): str}
    )
    @websocket_api.async_response
    async def ws_refresh_known_issues(hass, connection, msg):
        try:
            await _refresh_known_issues(store, gemini, msg["vehicle_id"])
            connection.send_result(msg["id"], {"vehicle": _serialize_vehicle(store.get_vehicle(msg["vehicle_id"]))})
        except GeminiError as err:
            connection.send_error(msg["id"], err.code, str(err))

    @websocket_api.websocket_command(
        {vol.Required("type"): f"{DOMAIN}/refresh_recalls", vol.Required("vehicle_id"): str}
    )
    @websocket_api.async_response
    async def ws_refresh_recalls(hass, connection, msg):
        try:
            await _refresh_recalls(store, gemini, msg["vehicle_id"])
            connection.send_result(msg["id"], {"vehicle": _serialize_vehicle(store.get_vehicle(msg["vehicle_id"]))})
        except GeminiError as err:
            connection.send_error(msg["id"], err.code, str(err))

    @websocket_api.websocket_command(
        {vol.Required("type"): f"{DOMAIN}/decode_vin_photo", vol.Required("photo"): str}
    )
    @websocket_api.async_response
    async def ws_decode_vin_photo(hass, connection, msg):
        try:
            result = await gemini.decode_vin_plate(msg["photo"])
            await store.async_add_token_usage(result.tokens)
            connection.send_result(msg["id"], result.data)
        except GeminiError as err:
            connection.send_error(msg["id"], err.code, str(err))

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/value_snapshot",
            vol.Required("vehicle_id"): str,
            vol.Optional("condition", default="correct"): str,
        }
    )
    @websocket_api.async_response
    async def ws_value_snapshot(hass, connection, msg):
        try:
            snapshot = await _snapshot_value(store, gemini, msg["vehicle_id"], msg["condition"])
            connection.send_result(msg["id"], {"snapshot": snapshot})
        except GeminiError as err:
            connection.send_error(msg["id"], err.code, str(err))

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/log_maintenance",
            vol.Required("vehicle_id"): str,
            vol.Optional("item_id"): str,
            vol.Required("item_name"): str,
            vol.Required("km"): int,
            vol.Optional("date"): vol.Coerce(float),
            vol.Optional("cost"): vol.Coerce(float),
            vol.Optional("garage"): str,
            vol.Optional("notes"): str,
        }
    )
    @websocket_api.async_response
    async def ws_log_maintenance(hass, connection, msg):
        msg_id = msg.pop("id")
        msg.pop("type")
        vehicle_id = msg.pop("vehicle_id")
        entry_data = await store.async_log_maintenance(vehicle_id, msg)
        async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)
        connection.send_result(msg_id, {"entry": entry_data})

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/ai_usage"})
    @websocket_api.async_response
    async def ws_ai_usage(hass, connection, msg):
        connection.send_result(msg["id"], store.data.get("ai_usage", {}))

    @websocket_api.websocket_command({vol.Required("type"): f"{DOMAIN}/get_settings"})
    @websocket_api.async_response
    async def ws_get_settings(hass, connection, msg):
        connection.send_result(msg["id"], {"settings": store.get_settings()})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/set_settings",
            vol.Optional("theme"): vol.In(["gt_cuir", "horlogerie", "carbone", "vintage"]),
        }
    )
    @websocket_api.async_response
    async def ws_set_settings(hass, connection, msg):
        patch = {k: v for k, v in msg.items() if k not in ("id", "type")}
        settings = await store.async_set_settings(patch)
        async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)
        connection.send_result(msg["id"], {"settings": settings})

    @websocket_api.websocket_command(
        {
            vol.Required("type"): f"{DOMAIN}/set_photo",
            vol.Required("vehicle_id"): str,
            vol.Optional("photo"): vol.Any(str, None),
        }
    )
    @websocket_api.async_response
    async def ws_set_photo(hass, connection, msg):
        vehicle = await store.async_set_photo(msg["vehicle_id"], msg.get("photo"))
        async_dispatcher_send(hass, SIGNAL_VEHICLES_UPDATED)
        connection.send_result(msg["id"], {"vehicle": _serialize_vehicle(vehicle) if vehicle else None})

    for handler in (
        ws_get_vehicles, ws_search_referentiel, ws_search_motorisations, ws_add_vehicle, ws_remove_vehicle,
        ws_update_mileage, ws_set_mileage_source, ws_refresh_plan, ws_refresh_known_issues,
        ws_refresh_recalls, ws_decode_vin_photo,
        ws_value_snapshot, ws_log_maintenance, ws_ai_usage, ws_get_settings, ws_set_settings,
        ws_set_photo,
    ):
        websocket_api.async_register_command(hass, handler)
