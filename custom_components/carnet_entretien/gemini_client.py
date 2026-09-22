"""Client Gemini pour la génération du carnet d'entretien, des points de
vigilance et de l'estimation de valeur.

Conçu pour être robuste face aux erreurs d'API courantes :
- thinking désactivé sur les extractions structurées courtes
- budgets de sortie généreux (les réponses tronquées sont la cause n°1
  d'échec silencieux observée dans leur changelog)
- lecture de TOUTES les parties de la réponse, pas seulement la première
- tolérance aux ```json, aux préfixes parasites, au texte autour du JSON
- distinction claire des erreurs : no_model / timeout / truncated / parse_error / rate_limited
"""
from __future__ import annotations

import asyncio
import json
import logging
import re
from dataclasses import dataclass
from typing import Any

import aiohttp
import async_timeout

from .catalog_i18n import LANGUAGE_NAMES
from .const import GEMINI_MODEL_CANDIDATES, GEMINI_TIMEOUT
from .maintenance_catalog import CAR_CATALOG

_LOGGER = logging.getLogger(__name__)

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"
RATE_LIMIT_RETRY_DELAYS = (5, 15)  # secondes ; 2 re-tentatives sur le MÊME modèle avant de passer au suivant


def _language_instruction(language: str) -> str:
    """Ligne ajoutée en fin de prompt pour forcer la langue de réponse.

    Les prompts eux-mêmes restent écrits en français (langue native de
    l'intégration, aucune raison de tous les réécrire) : seule cette ligne
    change, dans une formulation en anglais — plus fiable pour orienter
    Gemini que d'essayer d'écrire l'instruction dans chaque langue cible.
    Sans effet si "fr" (déjà la langue par défaut des prompts).
    """
    if language == "fr" or language not in LANGUAGE_NAMES:
        return ""
    return (
        f"\n\nIMPORTANT: write every text field of your JSON response "
        f"(free-text explanations, notes, titles, descriptions...) exclusively "
        f"in {LANGUAGE_NAMES[language]}. Keep any field defined by the schema's "
        f"\"enum\" (fixed values such as difficulty/severity levels) in its "
        f"original form — only free text changes language."
    )


class GeminiError(Exception):
    """Erreur générique, avec un code stable pour l'UI."""

    def __init__(self, code: str, message: str = ""):
        super().__init__(message or code)
        self.code = code  # "no_model" | "timeout" | "truncated" | "parse_error" | "http_error"


@dataclass
class GeminiResult:
    data: Any
    tokens: int


def _extract_json(text: str) -> Any:
    """Nettoie une réponse Gemini et en extrait le JSON."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned.strip())
    cleaned = re.sub(r"```$", "", cleaned.strip())
    cleaned = re.sub(r"^(THOUGHT|REASONING)\s*:.*?\n", "", cleaned, flags=re.IGNORECASE)
    # Si du texte parasite entoure le JSON, on isole le premier bloc { ... } ou [ ... ]
    match = re.search(r"(\{.*\}|\[.*\])", cleaned, flags=re.DOTALL)
    if match:
        cleaned = match.group(1)
    return json.loads(cleaned)


class GeminiClient:
    def __init__(self, session: aiohttp.ClientSession, api_key: str) -> None:
        self._session = session
        self._api_key = api_key
        self._working_model: str | None = None

    async def _call(self, prompt: str, schema: dict[str, Any], max_output_tokens: int = 2048) -> GeminiResult:
        return await self._call_parts([{"text": prompt}], schema, max_output_tokens)

    async def _call_vision(
        self, prompt: str, image_b64: str, mime_type: str, schema: dict[str, Any], max_output_tokens: int = 512
    ) -> GeminiResult:
        parts = [{"text": prompt}, {"inlineData": {"mimeType": mime_type, "data": image_b64}}]
        return await self._call_parts(parts, schema, max_output_tokens)

    @staticmethod
    def parse_data_url(data_url: str) -> tuple[str, str]:
        """Découpe une data URL ('data:image/jpeg;base64,AAAA...') en (mime_type, base64)."""
        header, _, b64 = data_url.partition(",")
        mime = "image/jpeg"
        if header.startswith("data:") and ";base64" in header:
            mime = header[5 : header.index(";base64")]
        return mime, b64

    async def _call_parts(
        self, parts: list[dict[str, Any]], schema: dict[str, Any], max_output_tokens: int = 2048
    ) -> GeminiResult:
        if not self._api_key:
            raise GeminiError("no_model", "Aucune clé Gemini configurée")

        models_to_try = [self._working_model] if self._working_model else []
        models_to_try += [m for m in GEMINI_MODEL_CANDIDATES if m != self._working_model]

        # Contrairement à la version précédente, on essaie TOUS les modèles
        # candidats quel que soit le type d'erreur rencontré (y compris
        # timeout/truncated/parse_error) : un incident sur un modèle donné
        # (quota, réponse mal formée sur ce cas précis...) ne doit jamais
        # empêcher d'essayer les suivants. On agrège les erreurs pour un
        # message final exploitable plutôt que de ne montrer que la
        # dernière (souvent trompeuse, ex: un modèle retiré en fin de liste
        # masquant un vrai dépassement de quota sur le premier).
        errors: list[str] = []
        for model in models_to_try:
            if not model:
                continue
            try:
                result = await self._call_model_with_retry(model, parts, schema, max_output_tokens)
                self._working_model = model  # mémorise le modèle qui fonctionne
                return result
            except GeminiError as err:
                errors.append(f"{model} [{err.code}]: {err}")
                continue

        detail = " ; ".join(errors) if errors else "aucun modèle configuré"
        raise GeminiError("no_model", f"Tous les modèles Gemini ont échoué — {detail}")

    async def _call_model_with_retry(
        self, model: str, parts: list[dict[str, Any]], schema: dict[str, Any], max_output_tokens: int
    ) -> GeminiResult:
        """Comme _call_model, mais re-tente avec un délai croissant en cas de
        429 (quota) ou d'erreur serveur transitoire (503 surchargé, etc.) sur
        CE modèle précis avant d'abandonner — ces deux cas se résolvent
        souvent tout seuls en quelques secondes, pas la peine de passer
        directement à un autre modèle potentiellement indisponible pour la clé.
        """
        last_err: GeminiError | None = None
        for attempt, delay in enumerate((0, *RATE_LIMIT_RETRY_DELAYS)):
            if delay:
                _LOGGER.debug("Erreur transitoire sur %s, nouvelle tentative dans %ss", model, delay)
                await asyncio.sleep(delay)
            try:
                return await self._call_model(model, parts, schema, max_output_tokens)
            except GeminiError as err:
                last_err = err
                if err.code not in ("rate_limited", "server_error"):
                    raise
                continue
        raise last_err

    async def _call_model(
        self, model: str, parts: list[dict[str, Any]], schema: dict[str, Any], max_output_tokens: int
    ) -> GeminiResult:
        url = f"{API_BASE}/{model}:generateContent?key={self._api_key}"
        body = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": max_output_tokens,
                "responseMimeType": "application/json",
                "responseSchema": schema,
                "thinkingConfig": {"thinkingBudget": 0},
            },
        }
        try:
            async with async_timeout.timeout(GEMINI_TIMEOUT):
                async with self._session.post(url, json=body) as resp:
                    if resp.status == 404:
                        raise GeminiError("http_error", f"Modèle {model} indisponible pour cette clé")
                    if resp.status == 429:
                        retry_after = resp.headers.get("Retry-After")
                        raise GeminiError(
                            "rate_limited",
                            f"Quota dépassé sur {model}" + (f" (retry-after {retry_after}s)" if retry_after else ""),
                        )
                    if resp.status >= 500:
                        # 503 (surcharge) et autres erreurs serveur : transitoires par
                        # nature, la même stratégie de re-tentative que le 429 s'applique.
                        payload = await resp.text()
                        raise GeminiError("server_error", f"Erreur {resp.status} sur {model}: {payload[:200]}")
                    if resp.status >= 400:
                        payload = await resp.text()
                        if resp.status == 400:
                            raise GeminiError("http_error", f"Erreur {resp.status} sur {model}: {payload[:200]}")
                        raise GeminiError("http_error", f"Erreur {resp.status} sur {model}")
                    data = await resp.json()
        except TimeoutError as exc:
            raise GeminiError("timeout", f"Délai dépassé sur {model}") from exc

        candidates = data.get("candidates") or []
        if not candidates:
            raise GeminiError("parse_error", "Réponse vide")

        candidate = candidates[0]
        finish_reason = candidate.get("finishReason")
        parts = candidate.get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts if p.get("text") and not p.get("thought"))

        usage = data.get("usageMetadata", {})
        tokens = usage.get("totalTokenCount", 0)

        if finish_reason == "MAX_TOKENS" and not text.strip():
            raise GeminiError("truncated", "Réponse coupée avant tout contenu utilisable")

        if not text.strip():
            raise GeminiError("parse_error", "Aucun texte exploitable dans la réponse")

        try:
            parsed = _extract_json(text)
        except (json.JSONDecodeError, ValueError) as exc:
            if finish_reason == "MAX_TOKENS":
                raise GeminiError("truncated", "Réponse coupée en plein JSON") from exc
            raise GeminiError("parse_error", f"JSON illisible: {exc}") from exc

        return GeminiResult(data=parsed, tokens=tokens)

    # ---------------- Fonctions métier ----------------

    async def generate_maintenance_plan(
        self, brand: str, model: str, motorisation: str, year: int, mileage: int,
        fuel_type: str = "", catalog: list[dict] | None = None, vehicle_kind_label: str = "véhicule",
        language: str = "fr",
    ) -> GeminiResult:
        catalog = catalog if catalog is not None else CAR_CATALOG
        catalog_lines = "\n".join(
            f'- "{it["id"]}" : {it["name"]} (défaut : {it["default_interval_km"]} km / '
            f'{it["default_interval_months"]} mois)'
            for it in catalog
        )
        schema = {
            "type": "OBJECT",
            "properties": {
                "items": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "catalog_id": {"type": "STRING"},
                            "applicable": {"type": "BOOLEAN"},
                            "interval_km": {"type": "INTEGER"},
                            "interval_months": {"type": "INTEGER"},
                            "cost_estimate_eur": {"type": "NUMBER"},
                            "diy_difficulty": {
                                "type": "STRING",
                                "enum": ["facile", "moyen", "difficile", "non_recommande"],
                            },
                            "diy_cost_estimate_eur": {"type": "NUMBER"},
                            "not_applicable_reason": {"type": "STRING"},
                            "notes": {"type": "STRING"},
                        },
                        "required": ["catalog_id", "applicable"],
                    },
                },
                "sources": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": ["items"],
        }
        prompt = f"""Tu es un expert en entretien de {vehicle_kind_label}s. Sur la base de la
documentation constructeur officielle (carnet/plan de maintenance) ET des
revues techniques indépendantes pour ce {vehicle_kind_label} précis — croise
mentalement ces deux types de sources et privilégie ce qui est confirmé par
les deux plutôt qu'une information isolée :

Marque : {brand}
Modèle : {model}
Motorisation : {motorisation or "non précisée"}
Type de carburant/énergie : {fuel_type or "non précisé — déduis-le de la motorisation si possible"}
Année : {year}
Kilométrage actuel : {mileage} km

Voici un catalogue FIXE de {len(catalog)} opérations d'entretien possibles
pour ce type de {vehicle_kind_label}. Tu dois renvoyer un objet pour CHACUNE
d'entre elles, sans exception, en reprenant exactement son "catalog_id" :

{catalog_lines}

Pour chaque entrée :
- "applicable" : false si cette opération concerne un équipement que CE
  véhicule précis n'a PAS. Le type de carburant/énergie ci-dessus est un
  critère de tri de premier ordre : sur un véhicule 100% électrique (BEV),
  toutes les entrées liées au moteur thermique (vidange, bougies,
  distribution, FAP/EGR, AdBlue, embrayage, GPL...) doivent être
  applicable=false, et à l'inverse les entrées spécifiques électrique
  (réducteur, refroidissement batterie de traction, diagnostic SoH...)
  s'appliquent. Sur un hybride, les deux familles thermique ET hybride
  s'appliquent en général (sauf exception du modèle). Sur un GPL, les
  entrées GPL s'ajoutent aux entrées thermiques standards. Applique le même
  principe pour l'équipement mécanique (exemple typique : "disques_arriere"
  doit être applicable=false ET "plaquettes_machoires_arriere" doit rester
  applicable=true si ce modèle/motorisation est équipé de freins à TAMBOURS
  à l'arrière — les deux entrées ne s'excluent pas forcément, décide
  indépendamment pour chacune). Dans tous les cas de non-applicabilité,
  renseigne "not_applicable_reason" en une phrase courte expliquant pourquoi.
  De même, "chaine_distribution" et "courroie_distribution" sont mutuellement
  exclusives sur un même véhicule thermique : une seule des deux doit être
  applicable (et les deux sont non applicables sur un BEV).
- Si applicable : ajuste "interval_km"/"interval_months" par rapport aux
  valeurs par défaut du catalogue si tu as une information plus précise pour
  CE véhicule (sinon reprends les valeurs par défaut) ; mets 0 pour
  l'intervalle qui ne s'applique pas (ex : les pneus n'ont pas d'intervalle
  en mois) ; "cost_estimate_eur" : coût moyen constaté en France en garage
  (pièces + main d'œuvre) ; "diy_difficulty" : niveau de difficulté à
  réaliser soi-même (facile/moyen/difficile/non_recommande — non_recommande
  si ça touche à la sécurité et nécessite un outillage/une expertise
  spécifique, ex : distribution, circuit haute tension) ; "diy_cost_estimate_eur" :
  coût des seules pièces si fait soi-même (sans main d'œuvre).
- Si non applicable : "interval_km"/"interval_months"/coûts peuvent être 0,
  seul "not_applicable_reason" compte.

IMPORTANT — cohérence factuelle : les caractéristiques techniques objectives
de ce véhicule (type de frein arrière disque/tambour, présence ou non d'une
courroie vs chaîne de distribution, type d'énergie, etc.) sont des FAITS qui
ne doivent pas varier si on te repose la question pour le même véhicule. Si
tu n'es pas certain à 100% d'une caractéristique d'équipement précise,
dis-le dans "notes" ("non vérifié avec certitude") plutôt que d'affirmer
tour à tour une chose puis son contraire.

N'invente pas de valeurs si tu n'es pas raisonnablement confiant : reprends
alors les valeurs par défaut du catalogue et indique-le dans "notes".
Renseigne aussi "sources" : les types de documents sur lesquels tu t'es
appuyé (ex : "Programme d'entretien officiel {brand}", "Revue Technique
Automobile (RTA)"). Réponds uniquement avec le JSON demandé (un objet par
catalog_id, tous présents), sans texte autour.""" + _language_instruction(language)
        return await self._call(prompt, schema, max_output_tokens=12288)

    async def generate_known_issues(
        self, brand: str, model: str, motorisation: str, year: int, language: str = "fr"
    ) -> GeminiResult:
        schema = {
            "type": "OBJECT",
            "properties": {
                "sources_summary": {"type": "STRING"},
                "issues": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "title": {"type": "STRING"},
                            "category": {
                                "type": "STRING",
                                "enum": [
                                    "moteur", "boite_de_vitesses", "electronique", "carrosserie",
                                    "suspension", "freinage", "climatisation", "autre",
                                ],
                            },
                            "severity": {"type": "STRING", "enum": ["mineur", "majeur", "securite"]},
                            "typical_occurrence": {"type": "STRING"},
                            "description": {"type": "STRING"},
                            "cost_estimate": {"type": "STRING"},
                        },
                        "required": ["title", "category", "severity", "description"],
                    },
                },
            },
            "required": ["sources_summary", "issues"],
        }
        prompt = f"""Tu es un mécanicien expérimenté. Pour ce véhicule :

Marque : {brand}
Modèle : {model}
Motorisation : {motorisation or "non précisée"}
Année : {year}

Liste les points de vigilance et pannes réputées sur ce modèle précis,
d'après les retours d'expérience courants (documentation constructeur,
revues techniques automobiles, forums spécialisés, garages, associations
de propriétaires). Pour chaque point : un titre court, une catégorie, une
gravité (mineur = confort, majeur = fonctionnel, securite = urgent), à quel
kilométrage ou âge cela apparaît typiquement ("typical_occurrence", ex:
"après 150 000 km" ou "sur les premières années de commercialisation"),
une description en 1-2 phrases, et un coût indicatif de réparation.
Limite-toi aux 8 points les plus significatifs et les plus consensuels.

Renseigne aussi "sources_summary" : 1 à 3 phrases nommant le TYPE de
documentation sur lequel tu t'appuies pour CE modèle précis (ex: "Programme
d'entretien officiel {brand}", "Revue Technique Automobile", "retours de
forums de propriétaires spécialisés"), pour que l'utilisateur sache d'où
vient l'information. Sois honnête : si tu n'as pas d'information fiable et
spécifique à ce modèle, renvoie une liste "issues" vide et dis-le dans
"sources_summary" plutôt que d'inventer. Réponds uniquement avec le JSON
demandé, sans texte autour.""" + _language_instruction(language)
        return await self._call(prompt, schema, max_output_tokens=3072)

    async def list_motorisations(
        self, brand: str, model: str, year: int, fuel_type: str = "",
        vehicle_type: str = "auto", two_wheeler_type: str = "",
    ) -> GeminiResult:
        schema = {"type": "ARRAY", "items": {"type": "STRING"}}
        fuel_line = (
            f"Ne liste QUE les motorisations correspondant à l'énergie suivante : {fuel_type}.\n"
            if fuel_type
            else ""
        )

        if vehicle_type == "deux_roues" and two_wheeler_type == "velo_electrique":
            what = "moteurs d'assistance électrique"
            examples = '"Bosch Performance Line CX 85Nm", "Shimano EP8", "Brose Drive S Mag"'
            extra = (
                "Le terme \"motorisation\" désigne ici le moteur d'assistance électrique "
                "(marque + gamme + couple en Nm), pas une motorisation au sens automobile."
            )
        elif vehicle_type == "deux_roues":
            what = "motorisations/versions"
            examples = '"MT-07 ABS", "MT-07 35kW (A2)", "125 XMAX", "CB500F A2"'
            extra = (
                "Distingue bien, quand c'est pertinent, la version pleine puissance de la "
                "version bridée 35kW compatible permis A2 — une même moto existe souvent "
                "dans les deux, ce sont deux entrées différentes sur le marché français."
            )
        else:
            what = "motorisations/versions"
            examples = '"1.5 BlueHDi 130", "1.2 PureTech 130 EAT8", "2.0 HDi 150"'
            extra = ""

        prompt = f"""Liste les {what} commercialisées pour ce véhicule précis :

Marque : {brand}
Modèle : {model}
Année : {year}
{fuel_line}
Donne la liste des {what} disponibles cette année-là, sous la forme
habituelle du marché français (ex : {examples}). {extra}
Maximum 20 entrées, sans doublons. Si tu n'es pas certain de l'année
exacte, donne les {what} de la génération commercialisée à cette période.
Réponds uniquement avec le JSON demandé (tableau de chaînes), sans texte
autour."""
        return await self._call(prompt, schema, max_output_tokens=1024)

    async def check_recalls(
        self, brand: str, model: str, motorisation: str, year: int, language: str = "fr"
    ) -> GeminiResult:
        schema = {
            "type": "OBJECT",
            "properties": {
                "recalls": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "title": {"type": "STRING"},
                            "reference": {"type": "STRING"},
                            "date": {"type": "STRING"},
                            "severity": {"type": "STRING", "enum": ["mineur", "majeur", "securite"]},
                            "description": {"type": "STRING"},
                            "action_required": {"type": "STRING"},
                        },
                        "required": ["title", "severity", "description"],
                    },
                },
                "sources": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": ["recalls"],
        }
        prompt = f"""Tu es un expert en sécurité automobile. Pour ce véhicule précis :

Marque : {brand}
Modèle : {model}
Motorisation : {motorisation or "non précisée"}
Année : {year}

Liste les campagnes de rappel (recalls) constructeur notables et documentées
pour ce modèle/motorisation/année, en France ou au niveau européen
(sécurité, freinage, airbag, moteur, direction, incendie, etc.). Pour
chacune : un titre court, la référence officielle si connue, la date
approximative, une gravité (mineur = confort, majeur = fonctionnel,
securite = sécurité active/passive), une description en 1-2 phrases, et
l'action requise (ex : "contrôle en concession", "remplacement pièce").
Ne liste QUE des rappels dont tu es raisonnablement confiant qu'ils ont
réellement existé pour ce modèle précis — si tu n'as pas d'information
fiable et spécifique, renvoie une liste "recalls" vide plutôt que
d'inventer. Renseigne "sources" (types de documents/bases consultés, ex :
"Base de rappels constructeur {brand}", "rappel.conso.gouv.fr"). Réponds
uniquement avec le JSON demandé, sans texte autour.""" + _language_instruction(language)
        return await self._call(prompt, schema, max_output_tokens=2048)

    async def explain_diy_operation(
        self, item_name: str, category: str, brand: str, model: str, motorisation: str, year: int,
        language: str = "fr",
    ) -> GeminiResult:
        """Génération à la demande (2e temps, sur clic) : explication détaillée
        pour réaliser une opération soi-même — appelée séparément de la
        génération du plan pour ne pas alourdir l'appel initial.
        """
        schema = {
            "type": "OBJECT",
            "properties": {
                "explanation": {"type": "STRING"},
                "tools_needed": {"type": "ARRAY", "items": {"type": "STRING"}},
                "estimated_time_minutes": {"type": "INTEGER"},
                "safety_warning": {"type": "STRING"},
            },
            "required": ["explanation", "tools_needed", "estimated_time_minutes"],
        }
        prompt = f"""Un particulier bricoleur envisage de réaliser lui-même cette
opération d'entretien :

Opération : {item_name} (catégorie : {category})
Véhicule : {brand} {model} {motorisation or ""} ({year})

Explique en 3-4 phrases pourquoi c'est facile ou difficile à faire soi-même
sur ce véhicule précis (accessibilité des pièces, outillage spécifique
requis, risque d'erreur, particularité connue de ce modèle si pertinente).
Liste l'outillage spécifique nécessaire dans "tools_needed" (outils
courants comme "clé à cliquet" sous-entendus, ne liste que le spécifique :
ex "outil de calage distribution", "valve de recharge clim R134a"). Donne
une estimation réaliste du temps total en minutes pour un bricoleur amateur
expérimenté (pas un professionnel) dans "estimated_time_minutes". Si
l'opération présente un risque de sécurité notable si mal réalisée (freinage,
direction, distribution...), ajoute un avertissement court dans
"safety_warning", sinon laisse ce champ vide. Réponds uniquement avec le
JSON demandé, sans texte autour.""" + _language_instruction(language)
        return await self._call(prompt, schema, max_output_tokens=1024)

    async def estimate_resale_value(
        self,
        brand: str,
        model: str,
        motorisation: str,
        year: int,
        mileage: int,
        annual_km: int,
        condition: str = "correct",
        language: str = "fr",
    ) -> GeminiResult:
        schema = {
            "type": "OBJECT",
            "properties": {
                "value_min": {"type": "NUMBER"},
                "value_avg": {"type": "NUMBER"},
                "value_max": {"type": "NUMBER"},
                "currency": {"type": "STRING"},
                "sources_tendance": {"type": "STRING"},
            },
            "required": ["value_min", "value_avg", "value_max", "currency", "sources_tendance"],
        }
        prompt = f"""Tu es un expert en cote automobile du marché de l'occasion (France).

Marque : {brand}
Modèle : {model}
Motorisation : {motorisation or "non précisée"}
Année : {year}
Kilométrage : {mileage} km (≈ {annual_km} km/an en moyenne depuis la mise en service)
État général déclaré : {condition}

Estime une fourchette de prix de revente réaliste sur le marché de
l'occasion actuel (particulier à particulier), en euros, en te basant sur la
décote typique de ce modèle selon l'âge et le kilométrage.

Renseigne aussi "sources_tendance" : 2-3 phrases qui nomment les plateformes
ou types de sources sur lesquelles tu t'appuies (ex: LaCentrale, Leboncoin,
Argus) et qui expliquent la tendance actuelle du marché pour ce modèle
(effet du kilométrage annuel par rapport à la moyenne, décote liée aux ZFE
pour un diesel/essence ancien le cas échéant, cote de la motorisation ou de
la finition, etc.). Réponds uniquement avec le JSON demandé, sans texte
autour.""" + _language_instruction(language)
        return await self._call(prompt, schema, max_output_tokens=768)
