"""Client Gemini pour la génération du carnet d'entretien, des points de
vigilance et de l'estimation de valeur.

Reprend les leçons de robustesse de ha-millesime :
- thinking désactivé sur les extractions structurées courtes
- budgets de sortie généreux (les réponses tronquées sont la cause n°1
  d'échec silencieux observée dans leur changelog)
- lecture de TOUTES les parties de la réponse, pas seulement la première
- tolérance aux ```json, aux préfixes parasites, au texte autour du JSON
- distinction claire des erreurs : no_model / timeout / truncated / parse_error
"""
from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any

import aiohttp
import async_timeout

from .const import GEMINI_MODEL_CANDIDATES, GEMINI_TIMEOUT

_LOGGER = logging.getLogger(__name__)

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


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
                result = await self._call_model(model, parts, schema, max_output_tokens)
                self._working_model = model  # mémorise le modèle qui fonctionne
                return result
            except GeminiError as err:
                errors.append(f"{model} [{err.code}]: {err}")
                continue

        detail = " ; ".join(errors) if errors else "aucun modèle configuré"
        raise GeminiError("no_model", f"Tous les modèles Gemini ont échoué — {detail}")

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
                    if resp.status >= 400:
                        payload = await resp.text()
                        # Certains paramètres (ex: thinkingConfig) ne sont pas supportés par
                        # tous les modèles et renvoient parfois 500 plutôt que 400.
                        if resp.status in (400, 500):
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
        self, brand: str, model: str, motorisation: str, year: int, mileage: int
    ) -> GeminiResult:
        schema = {
            "type": "OBJECT",
            "properties": {
                "items": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "name": {"type": "STRING"},
                            "category": {
                                "type": "STRING",
                                "enum": [
                                    "moteur", "freinage", "pneumatiques", "distribution",
                                    "filtration", "carrosserie", "electronique",
                                    "controle_technique", "revision", "autre",
                                ],
                            },
                            "interval_km": {"type": "INTEGER"},
                            "interval_months": {"type": "INTEGER"},
                            "cost_estimate_eur": {"type": "NUMBER"},
                            "applicable": {"type": "BOOLEAN"},
                            "not_applicable_reason": {"type": "STRING"},
                            "notes": {"type": "STRING"},
                        },
                        "required": [
                            "name", "category", "interval_km", "interval_months",
                            "cost_estimate_eur", "applicable",
                        ],
                    },
                },
                "sources": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": ["items"],
        }
        prompt = f"""Tu es un expert en entretien automobile. Sur la base de la documentation
constructeur officielle (carnet/plan de maintenance) ET des revues techniques
indépendantes (type Revue Technique Automobile) pour ce véhicule précis —
croise mentalement ces deux types de sources et privilégie ce qui est
confirmé par les deux plutôt qu'une information isolée :

Marque : {brand}
Modèle : {model}
Motorisation : {motorisation or "non précisée"}
Année : {year}
Kilométrage actuel : {mileage} km

Génère le carnet d'entretien type de ce véhicule : la liste des opérations
périodiques (vidange, filtres, distribution/chaîne, freins, pneumatiques,
liquide de refroidissement, bougies, etc.), ET OBLIGATOIREMENT ces deux
échéances administratives/génériques :
- une entrée de catégorie "controle_technique" ("Contrôle technique") ;
- une entrée de catégorie "revision" ("Révision constructeur périodique").

Pour chaque opération, précise :
- son intervalle en kilomètres ET en mois (le plus contraignant des deux
  s'applique en pratique ; mets 0 pour celui qui ne s'applique pas, par
  exemple un remplacement de pneus n'a généralement pas d'intervalle en mois) ;
- un coût estimé en euros ("cost_estimate_eur", pièces + main d'œuvre, tarif
  moyen d'un garage en France) — donne toujours une valeur, même approximative ;
- "applicable" : false si cette opération concerne un équipement que CE
  véhicule précis n'a PAS (exemple typique : "Remplacement disques de frein
  arrière" doit être applicable=false si ce modèle/motorisation est équipé de
  freins à TAMBOURS à l'arrière et non de disques). Dans ce cas, renseigne
  "not_applicable_reason" en une phrase courte expliquant l'équipement réel.

IMPORTANT — cohérence factuelle : les caractéristiques techniques objectives
de ce véhicule (type de frein arrière disque/tambour, présence ou non d'une
courroie vs chaîne de distribution, etc.) sont des FAITS qui ne doivent pas
varier si on te repose la question pour le même véhicule. Si tu n'es pas
certain à 100% d'une caractéristique d'équipement précise, dis-le dans
"notes" ("non vérifié avec certitude") plutôt que d'affirmer tour à tour une
chose puis son contraire. Ne mentionne jamais un remplacement de disques ET
la présence de tambours pour le même essieu.

N'invente pas de valeurs si tu n'es pas raisonnablement confiant : utilise les
intervalles et coûts usuels de la catégorie de véhicule dans ce cas et
indique-le dans "notes". Limite-toi à 13 opérations maximum, les plus
pertinentes (inclus les opérations non applicables identifiées, ainsi que le
contrôle technique et la révision, qui comptent dans les 13). Renseigne
aussi "sources" : les types de documents sur lesquels tu t'es appuyé (ex :
"Programme d'entretien officiel {brand}", "Revue Technique Automobile (RTA)").
Réponds uniquement avec le JSON demandé, sans texte autour."""
        return await self._call(prompt, schema, max_output_tokens=4096)

    async def generate_known_issues(self, brand: str, model: str, motorisation: str, year: int) -> GeminiResult:
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
demandé, sans texte autour."""
        return await self._call(prompt, schema, max_output_tokens=3072)

    async def list_motorisations(self, brand: str, model: str, year: int) -> GeminiResult:
        schema = {"type": "ARRAY", "items": {"type": "STRING"}}
        prompt = f"""Liste les motorisations/versions commercialisées pour ce véhicule précis :

Marque : {brand}
Modèle : {model}
Année : {year}

Donne la liste des motorisations disponibles cette année-là (essence,
diesel, hybride, électrique), sous la forme habituelle du marché français
(ex : "1.5 BlueHDi 130", "1.2 PureTech 130 EAT8", "2.0 HDi 150"). Maximum
20 entrées, sans doublons. Si tu n'es pas certain de l'année exacte,
donne les motorisations de la génération commercialisée à cette période.
Réponds uniquement avec le JSON demandé (tableau de chaînes), sans texte
autour."""
        return await self._call(prompt, schema, max_output_tokens=1024)

    async def check_recalls(self, brand: str, model: str, motorisation: str, year: int) -> GeminiResult:
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
uniquement avec le JSON demandé, sans texte autour."""
        return await self._call(prompt, schema, max_output_tokens=2048)

    async def decode_vin_plate(self, image_data_url: str) -> GeminiResult:
        mime_type, image_b64 = self.parse_data_url(image_data_url)
        schema = {
            "type": "OBJECT",
            "properties": {
                "vin": {"type": "STRING"},
                "brand": {"type": "STRING"},
                "model": {"type": "STRING"},
                "year": {"type": "INTEGER"},
                "motorisation": {"type": "STRING"},
                "plate": {"type": "STRING"},
                "confidence": {"type": "STRING", "enum": ["haute", "moyenne", "faible"]},
            },
            "required": ["confidence"],
        }
        prompt = """Tu analyses une photo qui montre soit la plaque VIN / plaque
constructeur d'un véhicule (généralement sous le capot, dans le coffre, ou
sur le montant de porte côté conducteur), soit sa plaque d'immatriculation
(arrière ou avant), soit les deux. Lis directement les informations
visibles si présentes (marque, type/modèle, motorisation, date de première
mise en circulation, immatriculation au format plaque française ou
étrangère), et/ou décode le numéro VIN (17 caractères) s'il est lisible :
le WMI (3 premiers caractères) identifie le constructeur, le 10e caractère
encode l'année-modèle. Si une immatriculation (plaque de circulation, PAS
le VIN) est visible sur la photo, renseigne-la dans "plate". Ne renseigne
un champ que si tu es raisonnablement confiant de sa valeur ; laisse-le
vide sinon. Indique ton niveau de confiance global dans "confidence".
Réponds uniquement avec le JSON demandé, sans texte autour."""
        return await self._call_vision(prompt, image_b64, mime_type, schema, max_output_tokens=512)

    async def decode_vin_text(self, vin: str) -> GeminiResult:
        schema = {
            "type": "OBJECT",
            "properties": {
                "brand": {"type": "STRING"},
                "model": {"type": "STRING"},
                "year": {"type": "INTEGER"},
                "motorisation": {"type": "STRING"},
                "confidence": {"type": "STRING", "enum": ["haute", "moyenne", "faible"]},
            },
            "required": ["confidence"],
        }
        prompt = f"""Décode ce numéro VIN (numéro d'identification du véhicule) :
{vin.strip().upper()}

Le WMI (3 premiers caractères) identifie le constructeur et souvent le
pays/l'usine. Le 10e caractère encode généralement l'année-modèle (norme
historique, avec un cycle qui se répète tous les 30 ans — utilise le
contexte, par exemple si le VIN semble ancien ou récent, pour choisir le
bon cycle). Le modèle précis et la motorisation ne sont pas toujours
déductibles avec certitude d'un simple VIN sans base constructeur dédiée :
ne renseigne "model"/"motorisation" que si tu es raisonnablement confiant,
laisse vide sinon. Indique ton niveau de confiance global dans
"confidence". Réponds uniquement avec le JSON demandé, sans texte autour."""
        return await self._call(prompt, schema, max_output_tokens=256)

    async def estimate_resale_value(
        self,
        brand: str,
        model: str,
        motorisation: str,
        year: int,
        mileage: int,
        annual_km: int,
        condition: str = "correct",
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
autour."""
        return await self._call(prompt, schema, max_output_tokens=768)
