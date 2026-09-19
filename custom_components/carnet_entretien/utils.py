"""Calcul des échéances : transforme le plan d'entretien brut (intervalles)
en dates/km d'échéance concrets, en tenant compte du kilométrage actuel et
d'un kilométrage annuel moyen estimé à partir de l'historique du véhicule.

v0.10 : le plan est désormais toujours construit à partir du catalogue fixe
(voir maintenance_catalog.py + __init__.py::_refresh_plan) — la présence du
contrôle technique et de la révision constructeur est garantie par le
catalogue lui-même, plus besoin d'une fonction dédiée pour les injecter.
Ajout du support d'un ajustement manuel de l'échéance ("due_km_override" /
"due_date_override"), qui prime sur le calcul base+intervalle habituel.
"""
from __future__ import annotations

import calendar
import datetime
from typing import Any

from .const import SOON_DAYS_THRESHOLD, SOON_KM_THRESHOLD, STATUS_DUE, STATUS_OK, STATUS_SOON

DEFAULT_ANNUAL_KM = 12000
STATUS_NOT_APPLICABLE = "non_applicable"


def estimate_annual_km(vehicle: dict[str, Any]) -> int:
    """Kilométrage annuel moyen réel, déduit de l'historique de kilométrage
    du véhicule (au moins 2 points, sur au moins 30 jours). Repli sur une
    moyenne par défaut sinon.
    """
    history = vehicle.get("mileage_history") or []
    if len(history) < 2:
        return DEFAULT_ANNUAL_KM
    first, last = history[0], history[-1]
    days = (last["date"] - first["date"]) / 86400
    km = last["km"] - first["km"]
    if days < 30 or km <= 0:
        return DEFAULT_ANNUAL_KM
    return max(int(km / days * 365), 1000)


def _registration_date(vehicle: dict[str, Any]) -> datetime.date:
    year = vehicle.get("year") or datetime.date.today().year
    return datetime.date(int(year), 1, 1)


def _add_months(d: datetime.date, months: int) -> datetime.date:
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def compute_item_status(vehicle: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    """Retourne l'item enrichi avec due_km, due_date, km_restants,
    jours_restants, depasse_de_km, prevu_vers, statut.
    """
    if item.get("applicable") is False:
        return {**item, "statut": STATUS_NOT_APPLICABLE}

    current_km = vehicle.get("mileage", 0)
    annual_km = estimate_annual_km(vehicle)
    today = datetime.date.today()

    last_done_km = item.get("last_done_km")
    last_done_date_ts = item.get("last_done_date")

    interval_km = item.get("interval_km") or 0
    # Certaines échéances ont un premier intervalle différent des suivants
    # (ex : contrôle technique, 1ère visite à 4 ans puis tous les 2 ans).
    # "first_interval_months" ne s'applique que tant qu'aucune intervention
    # n'a encore été enregistrée pour cet item.
    if last_done_date_ts is None and item.get("first_interval_months"):
        interval_months = item["first_interval_months"]
    else:
        interval_months = item.get("interval_months") or 0

    base_km = last_done_km if last_done_km is not None else 0
    base_date = (
        datetime.date.fromtimestamp(last_done_date_ts) if last_done_date_ts else _registration_date(vehicle)
    )

    due_km = base_km + interval_km if interval_km else None
    due_date_from_months = _add_months(base_date, interval_months) if interval_months else None

    # Ajustement manuel de l'échéance (l'utilisateur peut corriger une
    # échéance générée qu'il sait erronée, sans attendre une régénération) :
    # prime sur le calcul base+intervalle ci-dessus s'il est renseigné.
    if item.get("due_km_override") is not None:
        due_km = item["due_km_override"]
    override_date_ts = item.get("due_date_override")
    due_date_from_months = (
        datetime.date.fromtimestamp(override_date_ts) if override_date_ts else due_date_from_months
    )

    km_restants = (due_km - current_km) if due_km is not None else None
    jours_restants_calendaires = (due_date_from_months - today).days if due_date_from_months else None

    # Jours restants "effectifs" : le plus contraignant entre l'échéance
    # calendaire déclarée et une projection du km restant au rythme réel du
    # véhicule. C'est ce qui permet une date prévisionnelle même sur une
    # échéance purement kilométrique (ex: pneus à 35 000 km sans équivalent
    # temps), et un tri cohérent entre échéances.
    km_projected_days = int(km_restants / annual_km * 365) if km_restants is not None and annual_km else None
    candidates = [d for d in (jours_restants_calendaires, km_projected_days) if d is not None]
    effective_days = min(candidates) if candidates else None

    prevu_vers = None
    if effective_days is not None:
        prevu_vers_date = today + datetime.timedelta(days=effective_days)
        prevu_vers = f"{prevu_vers_date.month:02d}/{prevu_vers_date.year}"

    statuses = []
    if km_restants is not None:
        statuses.append(
            STATUS_DUE if km_restants <= 0 else STATUS_SOON if km_restants <= SOON_KM_THRESHOLD else STATUS_OK
        )
    if jours_restants_calendaires is not None:
        statuses.append(
            STATUS_DUE if jours_restants_calendaires <= 0
            else STATUS_SOON if jours_restants_calendaires <= SOON_DAYS_THRESHOLD
            else STATUS_OK
        )
    order = {STATUS_DUE: 2, STATUS_SOON: 1, STATUS_OK: 0}
    statut = max(statuses, key=lambda s: order[s]) if statuses else STATUS_OK

    return {
        **item,
        "due_km": due_km,
        "due_date": due_date_from_months.isoformat() if due_date_from_months else None,
        "km_restants": km_restants,
        "depasse_de_km": abs(km_restants) if (km_restants is not None and km_restants < 0) else None,
        "jours_restants": jours_restants_calendaires,
        "prevu_vers": prevu_vers,
        "annual_km": annual_km,
        "statut": statut,
        "_effective_days": effective_days if effective_days is not None else 99999,
    }


def compute_plan_status(vehicle: dict[str, Any]) -> list[dict[str, Any]]:
    items = [compute_item_status(vehicle, item) for item in vehicle.get("maintenance_plan", [])]
    # Les opérations non applicables sont reléguées en fin de liste
    items.sort(key=lambda i: (i["statut"] == STATUS_NOT_APPLICABLE, i.get("_effective_days", 99999)))
    for i in items:
        i.pop("_effective_days", None)
    return items


def next_due_item(vehicle: dict[str, Any]) -> dict[str, Any] | None:
    items = [i for i in compute_plan_status(vehicle) if i["statut"] != STATUS_NOT_APPLICABLE]
    return items[0] if items else None
