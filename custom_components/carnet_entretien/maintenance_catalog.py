"""Catalogue codé en dur de toutes les opérations d'entretien possibles
sur un véhicule courant.

Architecture v0.10 : plutôt que de laisser l'IA générer librement la liste
des opérations (source d'oublis et d'incohérences constatés en usage réel :
courroie d'accessoires ou contrôle de batterie oubliés, disques et
plaquettes fusionnés en une seule ligne...), le rôle de l'IA se limite
désormais à trancher, POUR CHAQUE entrée de ce catalogue fixe, si elle est
applicable à un véhicule précis et à en ajuster les intervalles/coûts. Rien
ne peut plus être oublié : une opération non pertinente est marquée
"non applicable" avec un motif plutôt que d'être simplement absente.

Chaque entrée :
- id : identifiant stable, ne change jamais (sert à faire persister les
  dates de dernière intervention d'une régénération à l'autre, et les
  ajustements manuels de l'utilisateur) ;
- name / category : affichage ;
- default_interval_km / default_interval_months : valeurs de repli si
  l'IA ne peut pas se prononcer ou si l'intégration tourne sans clé Gemini
  (mode manuel) — volontairement prudentes/génériques, à ajuster par
  véhicule via l'IA ou manuellement ;
- first_interval_months : optionnel, pour les échéances dont la première
  occurrence diffère des suivantes (ex : contrôle technique).
"""
from __future__ import annotations

from typing import Any

MAINTENANCE_CATALOG: list[dict[str, Any]] = [
    {"id": "vidange_huile", "name": "Vidange moteur + filtre à huile", "category": "moteur",
     "default_interval_km": 15000, "default_interval_months": 12},
    {"id": "filtre_air", "name": "Filtre à air", "category": "filtration",
     "default_interval_km": 30000, "default_interval_months": 24},
    {"id": "filtre_carburant", "name": "Filtre à carburant", "category": "filtration",
     "default_interval_km": 40000, "default_interval_months": 36},
    {"id": "filtre_habitacle", "name": "Filtre d'habitacle (pollen)", "category": "filtration",
     "default_interval_km": 15000, "default_interval_months": 12},
    {"id": "bougies_allumage", "name": "Bougies d'allumage (essence)", "category": "moteur",
     "default_interval_km": 60000, "default_interval_months": 48},
    {"id": "bougies_prechauffage", "name": "Bougies de préchauffage (diesel)", "category": "moteur",
     "default_interval_km": 100000, "default_interval_months": 84},
    {"id": "courroie_distribution", "name": "Courroie de distribution (+ galets, pompe à eau)",
     "category": "distribution", "default_interval_km": 120000, "default_interval_months": 60},
    {"id": "chaine_distribution", "name": "Chaîne de distribution (contrôle usure/tension)",
     "category": "distribution", "default_interval_km": 150000, "default_interval_months": 120},
    {"id": "courroie_accessoires", "name": "Courroie d'accessoires (serpentine)", "category": "distribution",
     "default_interval_km": 80000, "default_interval_months": 60},
    {"id": "liquide_refroidissement", "name": "Liquide de refroidissement", "category": "moteur",
     "default_interval_km": 60000, "default_interval_months": 48},
    {"id": "liquide_frein", "name": "Liquide de frein", "category": "freinage",
     "default_interval_km": 0, "default_interval_months": 24},
    {"id": "disques_avant", "name": "Disques de frein avant", "category": "freinage",
     "default_interval_km": 60000, "default_interval_months": 0},
    {"id": "plaquettes_avant", "name": "Plaquettes de frein avant", "category": "freinage",
     "default_interval_km": 30000, "default_interval_months": 0},
    {"id": "disques_arriere", "name": "Disques de frein arrière", "category": "freinage",
     "default_interval_km": 70000, "default_interval_months": 0},
    {"id": "plaquettes_machoires_arriere", "name": "Plaquettes ou mâchoires de frein arrière",
     "category": "freinage", "default_interval_km": 40000, "default_interval_months": 0},
    {"id": "pneus", "name": "Pneumatiques (jeu complet)", "category": "pneumatiques",
     "default_interval_km": 40000, "default_interval_months": 0},
    {"id": "batterie_12v", "name": "Contrôle / remplacement batterie 12V", "category": "electronique",
     "default_interval_km": 0, "default_interval_months": 48},
    {"id": "clim_recharge", "name": "Contrôle / recharge fluide climatisation", "category": "autre",
     "default_interval_km": 0, "default_interval_months": 24},
    {"id": "fap_egr", "name": "Contrôle FAP / vanne EGR (diesel)", "category": "moteur",
     "default_interval_km": 0, "default_interval_months": 24},
    {"id": "amortisseurs", "name": "Contrôle / remplacement amortisseurs", "category": "autre",
     "default_interval_km": 80000, "default_interval_months": 0},
    {"id": "rotules_biellettes", "name": "Contrôle rotules et biellettes de direction", "category": "autre",
     "default_interval_km": 0, "default_interval_months": 24},
    {"id": "embrayage", "name": "Contrôle / remplacement embrayage (boîte manuelle)", "category": "autre",
     "default_interval_km": 120000, "default_interval_months": 0},
    {"id": "liquide_boite", "name": "Liquide de boîte de vitesses", "category": "autre",
     "default_interval_km": 80000, "default_interval_months": 0},
    {"id": "direction_assistee", "name": "Liquide de direction assistée (si hydraulique)", "category": "autre",
     "default_interval_km": 0, "default_interval_months": 60},
    {"id": "cardans", "name": "Contrôle soufflets / joints de cardan", "category": "autre",
     "default_interval_km": 0, "default_interval_months": 24},
    {"id": "echappement", "name": "Contrôle ligne d'échappement", "category": "autre",
     "default_interval_km": 0, "default_interval_months": 24},
    {"id": "essuie_glaces", "name": "Balais d'essuie-glace", "category": "carrosserie",
     "default_interval_km": 0, "default_interval_months": 12},
    {"id": "controle_technique", "name": "Contrôle technique", "category": "controle_technique",
     "default_interval_km": 0, "default_interval_months": 24, "first_interval_months": 48},
    {"id": "revision_constructeur", "name": "Révision constructeur périodique", "category": "revision",
     "default_interval_km": 15000, "default_interval_months": 12},
]

CATALOG_BY_ID: dict[str, dict[str, Any]] = {item["id"]: item for item in MAINTENANCE_CATALOG}
