"""Catalogues codés en dur de toutes les opérations d'entretien possibles,
un catalogue distinct par grande famille de véhicule.

Architecture v0.10 : plutôt que de laisser l'IA générer librement la liste
des opérations (source d'oublis et d'incohérences constatés en usage réel :
courroie d'accessoires ou contrôle de batterie oubliés, disques et
plaquettes fusionnés en une seule ligne...), le rôle de l'IA se limite
désormais à trancher, POUR CHAQUE entrée du catalogue fixe correspondant au
véhicule, si elle est applicable et à en ajuster les intervalles/coûts.

v1.2 : un véhicule est soit une voiture (CAR_CATALOG), soit un deux-roues
motorisé — moto/scooter (MOTORIZED_TWO_WHEELER_CATALOG), soit un vélo à
assistance électrique (EBIKE_CATALOG). Chaque véhicule ne pioche JAMAIS que
dans un seul catalogue : une voiture n'a donc structurellement aucune chance
de se voir proposer une entrée "chaîne de transmission" même non applicable,
et inversement — pas besoin de filtrage supplémentaire, c'est une propriété
de la génération elle-même.

Chaque entrée :
- id : identifiant stable, ne change jamais (sert à faire persister les
  dates de dernière intervention d'une régénération à l'autre, et les
  ajustements manuels de l'utilisateur) — unique PAR catalogue, pas besoin
  d'être unique entre catalogues puisqu'un véhicule ne mélange jamais deux
  catalogues ;
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

# ---------------------------------------------------------------------------
# Voitures (45 entrées : thermique, hybride, électrique, GPL)
# ---------------------------------------------------------------------------

CAR_CATALOG: list[dict[str, Any]] = [
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
    {"id": "pneus_avant", "name": "Pneumatiques avant", "category": "pneumatiques",
     "default_interval_km": 40000, "default_interval_months": 0},
    {"id": "pneus_arriere", "name": "Pneumatiques arrière", "category": "pneumatiques",
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

    # ---- Thermique : compléments (4x4, SCR/FAP, trains, tambours) ----
    {"id": "adblue", "name": "Appoint AdBlue (SCR, diesel)", "category": "moteur",
     "default_interval_km": 0, "default_interval_months": 6},
    {"id": "additif_fap_eolys", "name": "Additif FAP (Eolys)", "category": "moteur",
     "default_interval_km": 60000, "default_interval_months": 0},
    {"id": "vidange_ponts_boite_transfert", "name": "Vidange des ponts et boîte de transfert (4x4/AWD)",
     "category": "autre", "default_interval_km": 60000, "default_interval_months": 48},
    {"id": "geometrie_parallelisme", "name": "Contrôle et réglage de la géométrie des trains",
     "category": "pneumatiques", "default_interval_km": 20000, "default_interval_months": 24},
    {"id": "reglage_freins_tambour", "name": "Dépoussiérage et réglage des freins à tambour",
     "category": "freinage", "default_interval_km": 20000, "default_interval_months": 0},

    # ---- Hybride (HEV/PHEV) ----
    {"id": "filtre_ventilation_batterie_ht", "name": "Filtre de ventilation de la batterie HT",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 24},
    {"id": "liquide_refroidissement_inverter", "name": "Liquide de refroidissement de l'inverter/convertisseur",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 60},
    {"id": "diagnostic_soh_batterie_traction", "name": "Diagnostic de santé de la batterie de traction (SoH)",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 24},

    # ---- 100 % électrique (BEV) ----
    {"id": "vidange_reducteur_electrique", "name": "Vidange de l'huile du réducteur / transmission électrique",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 60},
    {"id": "liquide_refroidissement_batterie_traction", "name": "Liquide de refroidissement de la batterie de traction",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 60},
    {"id": "graissage_etriers_frein", "name": "Nettoyage et graissage des étriers de frein (colonnettes)",
     "category": "freinage", "default_interval_km": 0, "default_interval_months": 24},
    {"id": "cartouche_dessiccante_batterie", "name": "Cartouche dessiccante du circuit de refroidissement batterie",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 60},

    # ---- GPL ----
    {"id": "filtre_gpl_gazeux", "name": "Filtre GPL (phase gazeuse)", "category": "filtration",
     "default_interval_km": 20000, "default_interval_months": 0},
    {"id": "filtre_gpl_liquide", "name": "Filtre GPL (phase liquide)", "category": "filtration",
     "default_interval_km": 20000, "default_interval_months": 0},
    {"id": "jeu_soupapes_gpl", "name": "Contrôle et réglage du jeu aux soupapes", "category": "moteur",
     "default_interval_km": 40000, "default_interval_months": 0},
    {"id": "controle_reservoir_gpl", "name": "Inspection réglementaire du réservoir GPL, canalisations et soupape",
     "category": "autre", "default_interval_km": 0, "default_interval_months": 120},
]

# ---------------------------------------------------------------------------
# Deux-roues motorisés : moto et scooter (thermique ou électrique)
# ---------------------------------------------------------------------------

MOTORIZED_TWO_WHEELER_CATALOG: list[dict[str, Any]] = [
    {"id": "vidange_huile_moto", "name": "Vidange moteur + filtre à huile", "category": "moteur",
     "default_interval_km": 6000, "default_interval_months": 12},
    {"id": "filtre_air_moto", "name": "Filtre à air", "category": "filtration",
     "default_interval_km": 12000, "default_interval_months": 24},
    {"id": "bougies_moto", "name": "Bougie(s) d'allumage", "category": "moteur",
     "default_interval_km": 12000, "default_interval_months": 24},
    {"id": "filtre_essence_moto", "name": "Filtre à essence", "category": "filtration",
     "default_interval_km": 20000, "default_interval_months": 0},
    {"id": "jeu_soupapes_moto", "name": "Contrôle et réglage du jeu aux soupapes", "category": "moteur",
     "default_interval_km": 20000, "default_interval_months": 24},
    {"id": "liquide_refroidissement_moto", "name": "Liquide de refroidissement (si refroidi par liquide)",
     "category": "moteur", "default_interval_km": 0, "default_interval_months": 24},
    {"id": "kit_chaine", "name": "Kit chaîne (chaîne + pignon + couronne)", "category": "distribution",
     "default_interval_km": 20000, "default_interval_months": 0},
    {"id": "reglage_graissage_chaine", "name": "Réglage tension et graissage de la chaîne", "category": "distribution",
     "default_interval_km": 600, "default_interval_months": 0},
    {"id": "courroie_transmission_scooter", "name": "Courroie de transmission (scooter à variateur)",
     "category": "distribution", "default_interval_km": 15000, "default_interval_months": 0},
    {"id": "galets_variateur", "name": "Galets et variateur (scooter CVT)", "category": "distribution",
     "default_interval_km": 15000, "default_interval_months": 0},
    {"id": "embrayage_moto", "name": "Contrôle / réglage embrayage", "category": "autre",
     "default_interval_km": 20000, "default_interval_months": 0},
    {"id": "liquide_frein_moto", "name": "Liquide de frein", "category": "freinage",
     "default_interval_km": 0, "default_interval_months": 24},
    {"id": "plaquettes_avant_moto", "name": "Plaquettes de frein avant", "category": "freinage",
     "default_interval_km": 12000, "default_interval_months": 0},
    {"id": "plaquettes_arriere_moto", "name": "Plaquettes de frein arrière", "category": "freinage",
     "default_interval_km": 15000, "default_interval_months": 0},
    {"id": "disque_avant_moto", "name": "Disque(s) de frein avant (usure)", "category": "freinage",
     "default_interval_km": 30000, "default_interval_months": 0},
    {"id": "disque_arriere_moto", "name": "Disque de frein arrière (usure)", "category": "freinage",
     "default_interval_km": 30000, "default_interval_months": 0},
    {"id": "pneu_avant_moto", "name": "Pneu avant", "category": "pneumatiques",
     "default_interval_km": 10000, "default_interval_months": 0},
    {"id": "pneu_arriere_moto", "name": "Pneu arrière", "category": "pneumatiques",
     "default_interval_km": 8000, "default_interval_months": 0},
    {"id": "huile_fourche", "name": "Huile de fourche + joints spi", "category": "autre",
     "default_interval_km": 20000, "default_interval_months": 36},
    {"id": "amortisseur_moto", "name": "Contrôle / réglage / remplacement amortisseur arrière",
     "category": "autre", "default_interval_km": 30000, "default_interval_months": 0},
    {"id": "roulements_roue_moto", "name": "Contrôle jeu des roulements de roue", "category": "autre",
     "default_interval_km": 20000, "default_interval_months": 24},
    {"id": "roulement_colonne_direction", "name": "Contrôle roulement de colonne de direction",
     "category": "autre", "default_interval_km": 20000, "default_interval_months": 24},
    {"id": "batterie_12v_moto", "name": "Contrôle / remplacement batterie", "category": "electronique",
     "default_interval_km": 0, "default_interval_months": 36},
    {"id": "graissage_articulations_moto", "name": "Graissage béquille et articulations châssis",
     "category": "autre", "default_interval_km": 6000, "default_interval_months": 12},
    {"id": "controle_technique_moto", "name": "Contrôle technique", "category": "controle_technique",
     "default_interval_km": 0, "default_interval_months": 24, "first_interval_months": 48},
    {"id": "revision_constructeur_moto", "name": "Révision constructeur périodique", "category": "revision",
     "default_interval_km": 6000, "default_interval_months": 12},
]

# ---------------------------------------------------------------------------
# Vélo à assistance électrique
# ---------------------------------------------------------------------------

EBIKE_CATALOG: list[dict[str, Any]] = [
    {"id": "reglage_chaine_ebike", "name": "Contrôle, tension et lubrification de la chaîne",
     "category": "distribution", "default_interval_km": 500, "default_interval_months": 3},
    {"id": "remplacement_chaine_ebike", "name": "Remplacement chaîne (kit transmission usé)",
     "category": "distribution", "default_interval_km": 3000, "default_interval_months": 0},
    {"id": "reglage_derailleur_ebike", "name": "Réglage des dérailleurs", "category": "distribution",
     "default_interval_km": 1000, "default_interval_months": 12},
    {"id": "plaquettes_avant_ebike", "name": "Plaquettes/patins de frein avant", "category": "freinage",
     "default_interval_km": 1500, "default_interval_months": 0},
    {"id": "plaquettes_arriere_ebike", "name": "Plaquettes/patins de frein arrière", "category": "freinage",
     "default_interval_km": 1500, "default_interval_months": 0},
    {"id": "disques_frein_ebike", "name": "Disques de frein (usure)", "category": "freinage",
     "default_interval_km": 5000, "default_interval_months": 0},
    {"id": "pneu_avant_ebike", "name": "Pneu avant (usure et pression)", "category": "pneumatiques",
     "default_interval_km": 3000, "default_interval_months": 0},
    {"id": "pneu_arriere_ebike", "name": "Pneu arrière (usure et pression)", "category": "pneumatiques",
     "default_interval_km": 3000, "default_interval_months": 0},
    {"id": "diagnostic_soh_batterie_ebike", "name": "Diagnostic de santé de la batterie (SoH)",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 12},
    {"id": "connecteurs_etancheite_ebike", "name": "Contrôle des connecteurs électriques et étanchéité",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 12},
    {"id": "moteur_assistance_ebike", "name": "Contrôle moteur/capteur d'assistance (bruit, jeu)",
     "category": "electronique", "default_interval_km": 0, "default_interval_months": 12},
    {"id": "firmware_ebike", "name": "Mise à jour firmware système d'assistance", "category": "electronique",
     "default_interval_km": 0, "default_interval_months": 12},
    {"id": "roulements_ebike", "name": "Contrôle et graissage roulements (direction, pédalier, roues)",
     "category": "autre", "default_interval_km": 3000, "default_interval_months": 12},
    {"id": "visserie_ebike", "name": "Contrôle couple de serrage (potence, tige de selle, visserie)",
     "category": "autre", "default_interval_km": 0, "default_interval_months": 6},
    {"id": "fourche_ebike", "name": "Contrôle / entretien fourche (si suspendue)", "category": "autre",
     "default_interval_km": 0, "default_interval_months": 12},
]

# Rétrocompatibilité : ancien nom utilisé avant l'introduction des deux-roues
MAINTENANCE_CATALOG = CAR_CATALOG

CATALOG_BY_ID: dict[str, dict[str, Any]] = {item["id"]: item for item in CAR_CATALOG}
MOTORIZED_TWO_WHEELER_CATALOG_BY_ID: dict[str, dict[str, Any]] = {
    item["id"]: item for item in MOTORIZED_TWO_WHEELER_CATALOG
}
EBIKE_CATALOG_BY_ID: dict[str, dict[str, Any]] = {item["id"]: item for item in EBIKE_CATALOG}


def get_catalog(vehicle_type: str, two_wheeler_type: str = "") -> list[dict[str, Any]]:
    """Retourne le catalogue applicable à ce véhicule.

    vehicle_type : "auto" (défaut) | "deux_roues"
    two_wheeler_type (si deux_roues) : "moto" | "scooter" | "velo_electrique"
    """
    if vehicle_type == "deux_roues":
        if two_wheeler_type == "velo_electrique":
            return EBIKE_CATALOG
        return MOTORIZED_TWO_WHEELER_CATALOG  # moto et scooter partagent le même catalogue
    return CAR_CATALOG


def get_catalog_by_id(vehicle_type: str, two_wheeler_type: str = "") -> dict[str, dict[str, Any]]:
    catalog = get_catalog(vehicle_type, two_wheeler_type)
    return {item["id"]: item for item in catalog}
