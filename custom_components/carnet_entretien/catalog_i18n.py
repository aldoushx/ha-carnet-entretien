"""Traductions des noms d'opérations du catalogue d'entretien fixe
(maintenance_catalog.py) et des libellés de catégorie, pour les langues
autres que le français (langue native du catalogue).

Structure : ITEM_NAMES[item_id][lang_code] -> nom traduit.
Le français n'est PAS dupliqué ici : le champ "name" de maintenance_catalog.py
fait déjà foi pour "fr" (fallback si une clé manque dans ITEM_NAMES).
"""
from __future__ import annotations

SUPPORTED_LANGUAGES = ["fr", "en", "de", "es", "it"]

LANGUAGE_NAMES = {
    "fr": "français",
    "en": "English",
    "de": "Deutsch",
    "es": "español",
    "it": "italiano",
}

# Libellés de catégorie (les clés "category" utilisées dans les catalogues :
# moteur, filtration, distribution, freinage, pneumatiques, electronique,
# autre, carrosserie, controle_technique, revision)
CATEGORY_LABELS = {
    "en": {
        "moteur": "Engine",
        "filtration": "Filters",
        "distribution": "Timing / drivetrain",
        "freinage": "Brakes",
        "pneumatiques": "Tires",
        "electronique": "Electrical / electronics",
        "autre": "Other",
        "carrosserie": "Bodywork",
        "controle_technique": "Roadworthiness inspection",
        "revision": "Scheduled service",
    },
    "de": {
        "moteur": "Motor",
        "filtration": "Filter",
        "distribution": "Steuerung / Antrieb",
        "freinage": "Bremsen",
        "pneumatiques": "Reifen",
        "electronique": "Elektrik / Elektronik",
        "autre": "Sonstiges",
        "carrosserie": "Karosserie",
        "controle_technique": "Hauptuntersuchung (TÜV)",
        "revision": "Herstellerwartung",
    },
    "es": {
        "moteur": "Motor",
        "filtration": "Filtros",
        "distribution": "Distribución / transmisión",
        "freinage": "Frenos",
        "pneumatiques": "Neumáticos",
        "electronique": "Eléctrico / electrónico",
        "autre": "Otros",
        "carrosserie": "Carrocería",
        "controle_technique": "Inspección técnica (ITV)",
        "revision": "Revisión periódica",
    },
    "it": {
        "moteur": "Motore",
        "filtration": "Filtri",
        "distribution": "Distribuzione / trasmissione",
        "freinage": "Freni",
        "pneumatiques": "Pneumatici",
        "electronique": "Elettrico / elettronico",
        "autre": "Altro",
        "carrosserie": "Carrozzeria",
        "controle_technique": "Revisione (controllo tecnico)",
        "revision": "Tagliando periodico",
    },
}

# Noms d'opérations, un sous-dict par item_id du catalogue
ITEM_NAMES: dict[str, dict[str, str]] = {
    # ---------------------------------------------------------------
    # CAR_CATALOG
    # ---------------------------------------------------------------
    "vidange_huile": {
        "en": "Engine oil change + oil filter",
        "de": "Motorölwechsel + Ölfilter",
        "es": "Cambio de aceite de motor + filtro de aceite",
        "it": "Cambio olio motore + filtro olio",
    },
    "filtre_air": {
        "en": "Air filter",
        "de": "Luftfilter",
        "es": "Filtro de aire",
        "it": "Filtro dell'aria",
    },
    "filtre_carburant": {
        "en": "Fuel filter",
        "de": "Kraftstofffilter",
        "es": "Filtro de combustible",
        "it": "Filtro del carburante",
    },
    "filtre_habitacle": {
        "en": "Cabin (pollen) filter",
        "de": "Innenraumfilter (Pollenfilter)",
        "es": "Filtro de habitáculo (polen)",
        "it": "Filtro abitacolo (antipolline)",
    },
    "bougies_allumage": {
        "en": "Spark plugs (petrol)",
        "de": "Zündkerzen (Benziner)",
        "es": "Bujías de encendido (gasolina)",
        "it": "Candele di accensione (benzina)",
    },
    "bougies_prechauffage": {
        "en": "Glow plugs (diesel)",
        "de": "Glühkerzen (Diesel)",
        "es": "Bujías de precalentamiento (diésel)",
        "it": "Candelette di preriscaldo (diesel)",
    },
    "courroie_distribution": {
        "en": "Timing belt (+ tensioner rollers, water pump)",
        "de": "Zahnriemen (+ Spannrollen, Wasserpumpe)",
        "es": "Correa de distribución (+ rodillos tensores, bomba de agua)",
        "it": "Cinghia di distribuzione (+ rulli tendicinghia, pompa acqua)",
    },
    "chaine_distribution": {
        "en": "Timing chain (wear/tension check)",
        "de": "Steuerkette (Verschleiß-/Spannungskontrolle)",
        "es": "Cadena de distribución (control de desgaste/tensión)",
        "it": "Catena di distribuzione (controllo usura/tensione)",
    },
    "courroie_accessoires": {
        "en": "Accessory (serpentine) belt",
        "de": "Keilrippenriemen (Nebenaggregate)",
        "es": "Correa de accesorios (poli-V)",
        "it": "Cinghia servizi (poly-V)",
    },
    "liquide_refroidissement": {
        "en": "Coolant",
        "de": "Kühlflüssigkeit",
        "es": "Líquido refrigerante",
        "it": "Liquido di raffreddamento",
    },
    "liquide_frein": {
        "en": "Brake fluid",
        "de": "Bremsflüssigkeit",
        "es": "Líquido de frenos",
        "it": "Liquido freni",
    },
    "disques_avant": {
        "en": "Front brake discs",
        "de": "Bremsscheiben vorne",
        "es": "Discos de freno delanteros",
        "it": "Dischi freno anteriori",
    },
    "plaquettes_avant": {
        "en": "Front brake pads",
        "de": "Bremsbeläge vorne",
        "es": "Pastillas de freno delanteras",
        "it": "Pastiglie freno anteriori",
    },
    "disques_arriere": {
        "en": "Rear brake discs",
        "de": "Bremsscheiben hinten",
        "es": "Discos de freno traseros",
        "it": "Dischi freno posteriori",
    },
    "plaquettes_machoires_arriere": {
        "en": "Rear brake pads or shoes",
        "de": "Bremsbeläge oder Bremsbacken hinten",
        "es": "Pastillas o zapatas de freno traseras",
        "it": "Pastiglie o ganasce freno posteriori",
    },
    "pneus_avant": {
        "en": "Front tires",
        "de": "Reifen vorne",
        "es": "Neumáticos delanteros",
        "it": "Pneumatici anteriori",
    },
    "pneus_arriere": {
        "en": "Rear tires",
        "de": "Reifen hinten",
        "es": "Neumáticos traseros",
        "it": "Pneumatici posteriori",
    },
    "batterie_12v": {
        "en": "12V battery check / replacement",
        "de": "12V-Batterie prüfen / ersetzen",
        "es": "Control / sustitución de la batería de 12V",
        "it": "Controllo / sostituzione batteria 12V",
    },
    "clim_recharge": {
        "en": "A/C refrigerant check / recharge",
        "de": "Klimaanlage prüfen / Kältemittel nachfüllen",
        "es": "Control / recarga del fluido del aire acondicionado",
        "it": "Controllo / ricarica del gas del climatizzatore",
    },
    "fap_egr": {
        "en": "DPF / EGR valve check (diesel)",
        "de": "Kontrolle Dieselpartikelfilter / AGR-Ventil (Diesel)",
        "es": "Control del filtro de partículas / válvula EGR (diésel)",
        "it": "Controllo FAP / valvola EGR (diesel)",
    },
    "amortisseurs": {
        "en": "Shock absorbers check / replacement",
        "de": "Stoßdämpfer prüfen / ersetzen",
        "es": "Control / sustitución de amortiguadores",
        "it": "Controllo / sostituzione ammortizzatori",
    },
    "rotules_biellettes": {
        "en": "Steering ball joints and tie rods check",
        "de": "Kontrolle Spurstangenköpfe und Koppelstangen",
        "es": "Control de rótulas y bieletas de dirección",
        "it": "Controllo giunti sferici e tiranti dello sterzo",
    },
    "embrayage": {
        "en": "Clutch check / replacement (manual gearbox)",
        "de": "Kupplung prüfen / ersetzen (Schaltgetriebe)",
        "es": "Control / sustitución del embrague (caja manual)",
        "it": "Controllo / sostituzione frizione (cambio manuale)",
    },
    "liquide_boite": {
        "en": "Gearbox fluid",
        "de": "Getriebeöl",
        "es": "Aceite de la caja de cambios",
        "it": "Olio del cambio",
    },
    "direction_assistee": {
        "en": "Power steering fluid (if hydraulic)",
        "de": "Servolenkungsflüssigkeit (bei Hydrauliklenkung)",
        "es": "Líquido de dirección asistida (si es hidráulica)",
        "it": "Liquido servosterzo (se idraulico)",
    },
    "cardans": {
        "en": "CV joint boots / driveshaft joints check",
        "de": "Kontrolle Antriebswellenmanschetten / Gelenke",
        "es": "Control de fuelles / juntas homocinéticas",
        "it": "Controllo cuffie / giunti dei semiassi",
    },
    "echappement": {
        "en": "Exhaust system check",
        "de": "Kontrolle der Abgasanlage",
        "es": "Control de la línea de escape",
        "it": "Controllo impianto di scarico",
    },
    "essuie_glaces": {
        "en": "Wiper blades",
        "de": "Scheibenwischerblätter",
        "es": "Escobillas del limpiaparabrisas",
        "it": "Spazzole tergicristallo",
    },
    "controle_technique": {
        "en": "Roadworthiness inspection",
        "de": "Hauptuntersuchung (TÜV)",
        "es": "Inspección técnica de vehículos (ITV)",
        "it": "Revisione periodica",
    },
    "revision_constructeur": {
        "en": "Scheduled manufacturer service",
        "de": "Periodische Herstellerinspektion",
        "es": "Revisión periódica del fabricante",
        "it": "Tagliando periodico del costruttore",
    },
    "adblue": {
        "en": "AdBlue top-up (SCR, diesel)",
        "de": "AdBlue nachfüllen (SCR, Diesel)",
        "es": "Rellenado de AdBlue (SCR, diésel)",
        "it": "Rabbocco AdBlue (SCR, diesel)",
    },
    "additif_fap_eolys": {
        "en": "DPF additive (Eolys)",
        "de": "Partikelfilter-Additiv (Eolys)",
        "es": "Aditivo del filtro de partículas (Eolys)",
        "it": "Additivo FAP (Eolys)",
    },
    "vidange_ponts_boite_transfert": {
        "en": "Differential and transfer case fluid change (4x4/AWD)",
        "de": "Ölwechsel Achsgetriebe und Verteilergetriebe (4x4/AWD)",
        "es": "Cambio de aceite de diferenciales y caja de transferencia (4x4/AWD)",
        "it": "Cambio olio differenziali e scatola di trasferimento (4x4/AWD)",
    },
    "geometrie_parallelisme": {
        "en": "Wheel alignment check and adjustment",
        "de": "Achsvermessung und Einstellung",
        "es": "Control y ajuste de la geometría/alineación",
        "it": "Controllo e regolazione dell'assetto (convergenza)",
    },
    "reglage_freins_tambour": {
        "en": "Drum brake cleaning and adjustment",
        "de": "Trommelbremsen reinigen und einstellen",
        "es": "Limpieza y ajuste de frenos de tambor",
        "it": "Pulizia e regolazione freni a tamburo",
    },
    "filtre_ventilation_batterie_ht": {
        "en": "HV battery ventilation filter",
        "de": "Lüftungsfilter der Hochvoltbatterie",
        "es": "Filtro de ventilación de la batería de alta tensión",
        "it": "Filtro di ventilazione della batteria ad alta tensione",
    },
    "liquide_refroidissement_inverter": {
        "en": "Inverter/converter coolant",
        "de": "Kühlflüssigkeit Wechselrichter/Konverter",
        "es": "Refrigerante del inversor/convertidor",
        "it": "Liquido di raffreddamento dell'inverter/convertitore",
    },
    "diagnostic_soh_batterie_traction": {
        "en": "Traction battery state-of-health (SoH) diagnostic",
        "de": "Gesundheitszustand (SoH) der Antriebsbatterie prüfen",
        "es": "Diagnóstico del estado de salud (SoH) de la batería de tracción",
        "it": "Diagnosi dello stato di salute (SoH) della batteria di trazione",
    },
    "vidange_reducteur_electrique": {
        "en": "Electric reduction gear / transmission oil change",
        "de": "Ölwechsel Untersetzungsgetriebe / elektrischer Antrieb",
        "es": "Cambio de aceite del reductor / transmisión eléctrica",
        "it": "Cambio olio del riduttore / trasmissione elettrica",
    },
    "liquide_refroidissement_batterie_traction": {
        "en": "Traction battery coolant",
        "de": "Kühlflüssigkeit der Antriebsbatterie",
        "es": "Refrigerante de la batería de tracción",
        "it": "Liquido di raffreddamento della batteria di trazione",
    },
    "graissage_etriers_frein": {
        "en": "Brake caliper cleaning and greasing (slide pins)",
        "de": "Bremssättel reinigen und Führungsbolzen schmieren",
        "es": "Limpieza y engrase de las pinzas de freno (guías)",
        "it": "Pulizia e ingrassaggio delle pinze freno (perni guida)",
    },
    "cartouche_dessiccante_batterie": {
        "en": "Battery cooling circuit desiccant cartridge",
        "de": "Trockenmittelpatrone im Batteriekühlkreislauf",
        "es": "Cartucho desecante del circuito de refrigeración de la batería",
        "it": "Cartuccia essiccante del circuito di raffreddamento della batteria",
    },
    "filtre_gpl_gazeux": {
        "en": "LPG filter (gas phase)",
        "de": "Autogasfilter (Gasphase)",
        "es": "Filtro de GLP (fase gaseosa)",
        "it": "Filtro GPL (fase gassosa)",
    },
    "filtre_gpl_liquide": {
        "en": "LPG filter (liquid phase)",
        "de": "Autogasfilter (Flüssigphase)",
        "es": "Filtro de GLP (fase líquida)",
        "it": "Filtro GPL (fase liquida)",
    },
    "jeu_soupapes_gpl": {
        "en": "Valve clearance check and adjustment",
        "de": "Ventilspiel prüfen und einstellen",
        "es": "Control y ajuste de la holgura de válvulas",
        "it": "Controllo e regolazione del gioco valvole",
    },
    "controle_reservoir_gpl": {
        "en": "Statutory inspection of LPG tank, lines and valve",
        "de": "Vorgeschriebene Prüfung von Autogastank, Leitungen und Ventil",
        "es": "Inspección reglamentaria del depósito de GLP, tuberías y válvula",
        "it": "Ispezione regolamentare del serbatoio GPL, tubazioni e valvola",
    },

    # ---------------------------------------------------------------
    # MOTORIZED_TWO_WHEELER_CATALOG
    # ---------------------------------------------------------------
    "vidange_huile_moto": {
        "en": "Engine oil change + oil filter",
        "de": "Motorölwechsel + Ölfilter",
        "es": "Cambio de aceite de motor + filtro de aceite",
        "it": "Cambio olio motore + filtro olio",
    },
    "filtre_air_moto": {
        "en": "Air filter",
        "de": "Luftfilter",
        "es": "Filtro de aire",
        "it": "Filtro dell'aria",
    },
    "bougies_moto": {
        "en": "Spark plug(s)",
        "de": "Zündkerze(n)",
        "es": "Bujía(s) de encendido",
        "it": "Candela/e di accensione",
    },
    "filtre_essence_moto": {
        "en": "Fuel filter",
        "de": "Kraftstofffilter",
        "es": "Filtro de gasolina",
        "it": "Filtro benzina",
    },
    "jeu_soupapes_moto": {
        "en": "Valve clearance check and adjustment",
        "de": "Ventilspiel prüfen und einstellen",
        "es": "Control y ajuste de la holgura de válvulas",
        "it": "Controllo e regolazione del gioco valvole",
    },
    "liquide_refroidissement_moto": {
        "en": "Coolant (if liquid-cooled)",
        "de": "Kühlflüssigkeit (bei Flüssigkeitskühlung)",
        "es": "Líquido refrigerante (si es refrigeración líquida)",
        "it": "Liquido di raffreddamento (se raffreddato a liquido)",
    },
    "kit_chaine": {
        "en": "Chain kit (chain + sprocket + rear sprocket)",
        "de": "Kettensatz (Kette + Ritzel + Kettenrad)",
        "es": "Kit de transmisión (cadena + piñón + corona)",
        "it": "Kit trasmissione (catena + pignone + corona)",
    },
    "reglage_graissage_chaine": {
        "en": "Chain tension adjustment and lubrication",
        "de": "Kette einstellen und schmieren",
        "es": "Ajuste de tensión y engrase de la cadena",
        "it": "Regolazione tensione e lubrificazione catena",
    },
    "courroie_transmission_scooter": {
        "en": "Drive belt (CVT scooter)",
        "de": "Antriebsriemen (Variomatik-Roller)",
        "es": "Correa de transmisión (scooter con variador)",
        "it": "Cinghia di trasmissione (scooter con variatore)",
    },
    "galets_variateur": {
        "en": "Variator rollers and pulley (CVT scooter)",
        "de": "Variorollen und Variomatik (CVT-Roller)",
        "es": "Rodillos y variador (scooter CVT)",
        "it": "Rulli e variatore (scooter CVT)",
    },
    "embrayage_moto": {
        "en": "Clutch check / adjustment",
        "de": "Kupplung prüfen / einstellen",
        "es": "Control / ajuste del embrague",
        "it": "Controllo / regolazione frizione",
    },
    "liquide_frein_moto": {
        "en": "Brake fluid",
        "de": "Bremsflüssigkeit",
        "es": "Líquido de frenos",
        "it": "Liquido freni",
    },
    "plaquettes_avant_moto": {
        "en": "Front brake pads",
        "de": "Bremsbeläge vorne",
        "es": "Pastillas de freno delanteras",
        "it": "Pastiglie freno anteriori",
    },
    "plaquettes_arriere_moto": {
        "en": "Rear brake pads",
        "de": "Bremsbeläge hinten",
        "es": "Pastillas de freno traseras",
        "it": "Pastiglie freno posteriori",
    },
    "disque_avant_moto": {
        "en": "Front brake disc(s) (wear)",
        "de": "Bremsscheibe(n) vorne (Verschleiß)",
        "es": "Disco(s) de freno delantero(s) (desgaste)",
        "it": "Disco/i freno anteriore/i (usura)",
    },
    "disque_arriere_moto": {
        "en": "Rear brake disc (wear)",
        "de": "Bremsscheibe hinten (Verschleiß)",
        "es": "Disco de freno trasero (desgaste)",
        "it": "Disco freno posteriore (usura)",
    },
    "pneu_avant_moto": {
        "en": "Front tire",
        "de": "Reifen vorne",
        "es": "Neumático delantero",
        "it": "Pneumatico anteriore",
    },
    "pneu_arriere_moto": {
        "en": "Rear tire",
        "de": "Reifen hinten",
        "es": "Neumático trasero",
        "it": "Pneumatico posteriore",
    },
    "huile_fourche": {
        "en": "Fork oil + seals",
        "de": "Gabelöl + Simmerringe",
        "es": "Aceite de horquilla + retenes",
        "it": "Olio forcella + paraoli",
    },
    "amortisseur_moto": {
        "en": "Rear shock absorber check / adjustment / replacement",
        "de": "Hinterradfederbein prüfen / einstellen / ersetzen",
        "es": "Control / ajuste / sustitución del amortiguador trasero",
        "it": "Controllo / regolazione / sostituzione ammortizzatore posteriore",
    },
    "roulements_roue_moto": {
        "en": "Wheel bearings play check",
        "de": "Radlagerspiel prüfen",
        "es": "Control de juego de los rodamientos de rueda",
        "it": "Controllo gioco cuscinetti ruota",
    },
    "roulement_colonne_direction": {
        "en": "Steering head bearing check",
        "de": "Lenkkopflager prüfen",
        "es": "Control del rodamiento de la columna de dirección",
        "it": "Controllo cuscinetto del cannotto di sterzo",
    },
    "batterie_12v_moto": {
        "en": "Battery check / replacement",
        "de": "Batterie prüfen / ersetzen",
        "es": "Control / sustitución de la batería",
        "it": "Controllo / sostituzione batteria",
    },
    "graissage_articulations_moto": {
        "en": "Side stand and chassis linkage lubrication",
        "de": "Seitenständer und Fahrwerksgelenke schmieren",
        "es": "Engrase del caballete lateral y articulaciones del chasis",
        "it": "Ingrassaggio cavalletto laterale e snodi del telaio",
    },
    "controle_technique_moto": {
        "en": "Roadworthiness inspection",
        "de": "Hauptuntersuchung (TÜV)",
        "es": "Inspección técnica de vehículos (ITV)",
        "it": "Revisione periodica",
    },
    "revision_constructeur_moto": {
        "en": "Scheduled manufacturer service",
        "de": "Periodische Herstellerinspektion",
        "es": "Revisión periódica del fabricante",
        "it": "Tagliando periodico del costruttore",
    },

    # ---------------------------------------------------------------
    # EBIKE_CATALOG
    # ---------------------------------------------------------------
    "reglage_chaine_ebike": {
        "en": "Chain check, tension adjustment and lubrication",
        "de": "Kette prüfen, spannen und schmieren",
        "es": "Control, tensado y lubricación de la cadena",
        "it": "Controllo, tensionamento e lubrificazione della catena",
    },
    "remplacement_chaine_ebike": {
        "en": "Chain replacement (worn drivetrain kit)",
        "de": "Kette ersetzen (verschlissener Antriebsstrang)",
        "es": "Sustitución de la cadena (kit de transmisión desgastado)",
        "it": "Sostituzione catena (kit trasmissione usurato)",
    },
    "reglage_derailleur_ebike": {
        "en": "Derailleur adjustment",
        "de": "Schaltwerk einstellen",
        "es": "Ajuste de los desviadores",
        "it": "Regolazione dei deragliatori",
    },
    "plaquettes_avant_ebike": {
        "en": "Front brake pads/blocks",
        "de": "Bremsbeläge/-klötze vorne",
        "es": "Pastillas/zapatas de freno delanteras",
        "it": "Pastiglie/pattini freno anteriori",
    },
    "plaquettes_arriere_ebike": {
        "en": "Rear brake pads/blocks",
        "de": "Bremsbeläge/-klötze hinten",
        "es": "Pastillas/zapatas de freno traseras",
        "it": "Pastiglie/pattini freno posteriori",
    },
    "disques_frein_ebike": {
        "en": "Brake discs (wear)",
        "de": "Bremsscheiben (Verschleiß)",
        "es": "Discos de freno (desgaste)",
        "it": "Dischi freno (usura)",
    },
    "pneu_avant_ebike": {
        "en": "Front tire (wear and pressure)",
        "de": "Reifen vorne (Verschleiß und Luftdruck)",
        "es": "Neumático delantero (desgaste y presión)",
        "it": "Pneumatico anteriore (usura e pressione)",
    },
    "pneu_arriere_ebike": {
        "en": "Rear tire (wear and pressure)",
        "de": "Reifen hinten (Verschleiß und Luftdruck)",
        "es": "Neumático trasero (desgaste y presión)",
        "it": "Pneumatico posteriore (usura e pressione)",
    },
    "diagnostic_soh_batterie_ebike": {
        "en": "Battery state-of-health (SoH) diagnostic",
        "de": "Gesundheitszustand (SoH) der Batterie prüfen",
        "es": "Diagnóstico del estado de salud (SoH) de la batería",
        "it": "Diagnosi dello stato di salute (SoH) della batteria",
    },
    "connecteurs_etancheite_ebike": {
        "en": "Electrical connectors and seal check",
        "de": "Steckverbinder und Dichtigkeit prüfen",
        "es": "Control de conectores eléctricos y estanqueidad",
        "it": "Controllo connettori elettrici e tenuta stagna",
    },
    "moteur_assistance_ebike": {
        "en": "Drive motor/sensor check (noise, play)",
        "de": "Antriebsmotor/Sensor prüfen (Geräusche, Spiel)",
        "es": "Control del motor/sensor de asistencia (ruido, holgura)",
        "it": "Controllo motore/sensore di assistenza (rumore, gioco)",
    },
    "firmware_ebike": {
        "en": "Drive system firmware update",
        "de": "Firmware-Update des Antriebssystems",
        "es": "Actualización del firmware del sistema de asistencia",
        "it": "Aggiornamento firmware del sistema di assistenza",
    },
    "roulements_ebike": {
        "en": "Bearings check and greasing (headset, bottom bracket, wheels)",
        "de": "Lager prüfen und schmieren (Steuersatz, Tretlager, Räder)",
        "es": "Control y engrase de rodamientos (dirección, pedalier, ruedas)",
        "it": "Controllo e ingrassaggio cuscinetti (sterzo, movimento centrale, ruote)",
    },
    "visserie_ebike": {
        "en": "Torque check on bolts (stem, seatpost, fasteners)",
        "de": "Anzugsdrehmomente prüfen (Vorbau, Sattelstütze, Schrauben)",
        "es": "Control del par de apriete (potencia, tija de sillín, tornillería)",
        "it": "Controllo coppie di serraggio (attacco manubrio, reggisella, bulloneria)",
    },
    "fourche_ebike": {
        "en": "Suspension fork check / service (if equipped)",
        "de": "Federgabel prüfen / warten (falls vorhanden)",
        "es": "Control / mantenimiento de la horquilla (si es suspendida)",
        "it": "Controllo / manutenzione forcella (se ammortizzata)",
    },
}

# Chaînes utilisées par les notifications persistantes HA (__init__.py :
# _async_check_overdue_notifications / _async_check_mileage_reminders),
# seules chaînes ni saisies par l'utilisateur ni générées par Gemini — donc
# traduites statiquement ici comme le reste du texte fixe de l'intégration.
# Le français est inclus (contrairement à ITEM_NAMES) car ces chaînes ne
# proviennent d'aucun autre fichier source à utiliser comme repli.
NOTIF_STRINGS = {
    "fr": {
        "generic_ai_fallback_note": "Non couvert par la génération IA — valeurs génériques du catalogue.",
        "vehicle_fallback": "Véhicule",
        "overdue_km": "{km} km de dépassement",
        "overdue_days": "{days} j de retard",
        "overdue_generic": "échéance dépassée",
        "overdue_title": "🔧 Entretien à faire",
        "overdue_body": (
            "**{label}** — {item}\n\n{detail}. Ouvrez la carte Carnet d'entretien "
            "pour enregistrer l'intervention une fois réalisée."
        ),
        "mileage_title": "📏 Mettre à jour le kilométrage",
        "mileage_body": (
            "Le kilométrage de **{label}** n'a pas été mis à jour depuis {days} jours "
            "(rappel réglé sur {period} j). Une valeur à jour améliore la précision "
            "des échéances et de la date prévisionnelle."
        ),
    },
    "en": {
        "generic_ai_fallback_note": "Not covered by the AI generation — generic catalog values.",
        "vehicle_fallback": "Vehicle",
        "overdue_km": "{km} km overdue",
        "overdue_days": "{days} days overdue",
        "overdue_generic": "due date passed",
        "overdue_title": "🔧 Maintenance due",
        "overdue_body": (
            "**{label}** — {item}\n\n{detail}. Open the Garage Log card to log the "
            "service once it's done."
        ),
        "mileage_title": "📏 Update the mileage",
        "mileage_body": (
            "The mileage for **{label}** hasn't been updated in {days} days "
            "(reminder set to {period} days). A current value improves the accuracy "
            "of due dates and forecasts."
        ),
    },
    "de": {
        "generic_ai_fallback_note": "Nicht von der KI-Generierung abgedeckt — generische Katalogwerte.",
        "vehicle_fallback": "Fahrzeug",
        "overdue_km": "{km} km überfällig",
        "overdue_days": "{days} Tage überfällig",
        "overdue_generic": "Termin überschritten",
        "overdue_title": "🔧 Wartung fällig",
        "overdue_body": (
            "**{label}** — {item}\n\n{detail}. Öffnen Sie die CARnet-Karte, um die "
            "Arbeit nach der Durchführung zu erfassen."
        ),
        "mileage_title": "📏 Kilometerstand aktualisieren",
        "mileage_body": (
            "Der Kilometerstand von **{label}** wurde seit {days} Tagen nicht "
            "aktualisiert (Erinnerung auf {period} Tage eingestellt). Ein aktueller "
            "Wert verbessert die Genauigkeit der Termine und Prognosen."
        ),
    },
    "es": {
        "generic_ai_fallback_note": "No cubierto por la generación de la IA — valores genéricos del catálogo.",
        "vehicle_fallback": "Vehículo",
        "overdue_km": "{km} km de retraso",
        "overdue_days": "{days} días de retraso",
        "overdue_generic": "plazo superado",
        "overdue_title": "🔧 Mantenimiento pendiente",
        "overdue_body": (
            "**{label}** — {item}\n\n{detail}. Abre la tarjeta CARnet para "
            "registrar la intervención una vez realizada."
        ),
        "mileage_title": "📏 Actualizar el kilometraje",
        "mileage_body": (
            "El kilometraje de **{label}** no se ha actualizado desde hace {days} "
            "días (recordatorio configurado a {period} días). Un valor actualizado "
            "mejora la precisión de los plazos y la fecha prevista."
        ),
    },
    "it": {
        "generic_ai_fallback_note": "Non coperto dalla generazione IA — valori generici del catalogo.",
        "vehicle_fallback": "Veicolo",
        "overdue_km": "{km} km di ritardo",
        "overdue_days": "{days} giorni di ritardo",
        "overdue_generic": "scadenza superata",
        "overdue_title": "🔧 Manutenzione da fare",
        "overdue_body": (
            "**{label}** — {item}\n\n{detail}. Apri la scheda CARnet per registrare "
            "l'intervento una volta effettuato."
        ),
        "mileage_title": "📏 Aggiorna il chilometraggio",
        "mileage_body": (
            "Il chilometraggio di **{label}** non viene aggiornato da {days} giorni "
            "(promemoria impostato su {period} giorni). Un valore aggiornato migliora "
            "la precisione delle scadenze e della data prevista."
        ),
    },
}
