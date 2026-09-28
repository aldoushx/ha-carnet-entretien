"""Rappels saisonniers : contenu et logique de saison (module pur, sans
dépendance à Home Assistant, pour rester testable isolément).

Une notification persistante par véhicule est créée à chaque changement de
saison (voir __init__.py::_async_check_seasonal_reminders), avec une liste de
points à vérifier adaptée au type de véhicule et à la langue choisie.

Saisons "météorologiques" (mars-mai, juin-août, septembre-novembre,
décembre-février), inversées dans l'hémisphère sud.
"""
from __future__ import annotations

from datetime import date

SEASONS = ("spring", "summer", "autumn", "winter")

# Point à vérifier -> texte par langue (fr/en/de/es/it).
TIPS: dict[str, dict[str, str]] = {
    "wipers": {
        "fr": "Essuie-glaces : vérifier l'état des balais, les remplacer s'ils rayent ou broutent.",
        "en": "Wipers: check the blades and replace them if they streak or judder.",
        "de": "Scheibenwischer: Wischerblätter prüfen und bei Schlieren oder Rattern ersetzen.",
        "es": "Limpiaparabrisas: revisar las escobillas y cambiarlas si rayan o saltan.",
        "it": "Tergicristalli: controllare le spazzole e sostituirle se rigano o saltellano.",
    },
    "tires_rain": {
        "fr": "Pneus : profondeur des sculptures (3 mm minimum conseillés sur le mouillé) et pression.",
        "en": "Tyres: tread depth (3 mm minimum advised in the wet) and pressure.",
        "de": "Reifen: Profiltiefe (bei Nässe mindestens 3 mm empfohlen) und Luftdruck.",
        "es": "Neumáticos: profundidad del dibujo (mínimo 3 mm aconsejados en mojado) y presión.",
        "it": "Pneumatici: profondità del battistrada (minimo 3 mm consigliati sul bagnato) e pressione.",
    },
    "lights": {
        "fr": "Éclairage : tester feux et phares, remplacer les ampoules faibles (les jours raccourcissent).",
        "en": "Lighting: test all lights and replace dim bulbs (days are getting shorter).",
        "de": "Beleuchtung: Lichter testen und schwache Lampen ersetzen (die Tage werden kürzer).",
        "es": "Iluminación: probar luces y faros y cambiar las bombillas débiles (los días se acortan).",
        "it": "Illuminazione: provare luci e fari e sostituire le lampadine deboli (le giornate si accorciano).",
    },
    "battery_test": {
        "fr": "Batterie : faire tester la charge avant les premiers froids.",
        "en": "Battery: have its charge tested before the first cold snaps.",
        "de": "Batterie: Ladezustand vor den ersten Frösten testen lassen.",
        "es": "Batería: hacer comprobar la carga antes de los primeros fríos.",
        "it": "Batteria: far controllare la carica prima dei primi freddi.",
    },
    "washer_antifreeze": {
        "fr": "Lave-glace : passer à un liquide antigel.",
        "en": "Washer fluid: switch to an antifreeze mix.",
        "de": "Scheibenwaschflüssigkeit: auf Frostschutz umstellen.",
        "es": "Lavaparabrisas: cambiar a un líquido anticongelante.",
        "it": "Lavavetri: passare a un liquido antigelo.",
    },
    "tires_pressure_cold": {
        "fr": "Pneus : contrôler la pression (le froid la fait baisser) ; pneus hiver si votre région l'impose.",
        "en": "Tyres: check the pressure (cold lowers it); winter tyres where required.",
        "de": "Reifen: Luftdruck prüfen (Kälte senkt ihn); Winterreifen, wo vorgeschrieben.",
        "es": "Neumáticos: comprobar la presión (el frío la reduce); neumáticos de invierno si su zona lo exige.",
        "it": "Pneumatici: controllare la pressione (il freddo la abbassa); gomme invernali dove richieste.",
    },
    "moto_tires_pressure_cold": {
        "fr": "Pneus : contrôler la pression (le froid la fait baisser) et l'état de la gomme avant de rouler.",
        "en": "Tyres: check the pressure (cold lowers it) and the rubber's condition before riding.",
        "de": "Reifen: Luftdruck (Kälte senkt ihn) und Zustand des Gummis vor der Fahrt prüfen.",
        "es": "Neumáticos: comprobar la presión (el frío la reduce) y el estado de la goma antes de rodar.",
        "it": "Pneumatici: controllare la pressione (il freddo la abbassa) e lo stato della gomma prima di partire.",
    },
    "coolant_antifreeze": {
        "fr": "Liquide de refroidissement : vérifier le niveau et la protection antigel.",
        "en": "Coolant: check the level and the antifreeze protection.",
        "de": "Kühlflüssigkeit: Füllstand und Frostschutz prüfen.",
        "es": "Líquido refrigerante: comprobar el nivel y la protección anticongelante.",
        "it": "Liquido di raffreddamento: controllare livello e protezione antigelo.",
    },
    "washer_level": {
        "fr": "Lave-glace : niveau et protection antigel.",
        "en": "Washer fluid: level and antifreeze protection.",
        "de": "Scheibenwaschflüssigkeit: Füllstand und Frostschutz.",
        "es": "Lavaparabrisas: nivel y protección anticongelante.",
        "it": "Lavavetri: livello e protezione antigelo.",
    },
    "battery_cold": {
        "fr": "Batterie : le froid est son pire ennemi, la faire contrôler avant une panne de démarrage.",
        "en": "Battery: cold is its worst enemy, have it checked before a no-start.",
        "de": "Batterie: Kälte ist ihr größter Feind, vor einer Startpanne prüfen lassen.",
        "es": "Batería: el frío es su peor enemigo, hacerla revisar antes de quedarse sin arranque.",
        "it": "Batteria: il freddo è il suo peggior nemico, farla controllare prima di restare a piedi.",
    },
    "winter_kit": {
        "fr": "Kit d'hiver : grattoir, câbles de démarrage, couverture, lampe.",
        "en": "Winter kit: ice scraper, jump leads, blanket, torch.",
        "de": "Winterausrüstung: Eiskratzer, Starthilfekabel, Decke, Taschenlampe.",
        "es": "Kit de invierno: rasqueta, cables de arranque, manta, linterna.",
        "it": "Kit invernale: raschietto, cavi di avviamento, coperta, torcia.",
    },
    "summer_tires_swap": {
        "fr": "Pneus : repasser aux pneus été si des pneus hiver sont montés.",
        "en": "Tyres: switch back to summer tyres if winter ones are fitted.",
        "de": "Reifen: von Winter- auf Sommerreifen wechseln, falls montiert.",
        "es": "Neumáticos: volver a los de verano si hay montados los de invierno.",
        "it": "Pneumatici: tornare alle gomme estive se montate quelle invernali.",
    },
    "post_winter_check": {
        "fr": "Contrôle après l'hiver : traces de sel et de corrosion, freins, dessous de caisse.",
        "en": "Post-winter check: salt and corrosion marks, brakes, underbody.",
        "de": "Kontrolle nach dem Winter: Salz- und Rostspuren, Bremsen, Unterboden.",
        "es": "Revisión tras el invierno: restos de sal y corrosión, frenos, bajos.",
        "it": "Controllo dopo l'inverno: tracce di sale e corrosione, freni, sottoscocca.",
    },
    "ac_recheck": {
        "fr": "Climatisation : la remettre en route et vérifier qu'elle refroidit bien avant l'été.",
        "en": "Air conditioning: run it and check it cools properly before summer.",
        "de": "Klimaanlage: einschalten und vor dem Sommer prüfen, ob sie gut kühlt.",
        "es": "Aire acondicionado: ponerlo en marcha y comprobar que enfría bien antes del verano.",
        "it": "Climatizzatore: riattivarlo e verificare che raffreddi bene prima dell'estate.",
    },
    "pollen_filter": {
        "fr": "Filtre d'habitacle (pollen) : à remplacer s'il est encrassé.",
        "en": "Cabin (pollen) filter: replace it if clogged.",
        "de": "Innenraum-/Pollenfilter: bei Verschmutzung ersetzen.",
        "es": "Filtro de habitáculo (polen): cambiarlo si está sucio.",
        "it": "Filtro abitacolo (pollini): sostituirlo se intasato.",
    },
    "fluids_levels": {
        "fr": "Niveaux (huile, liquides) : à contrôler après une saison rude.",
        "en": "Levels (oil, fluids): check them after a harsh season.",
        "de": "Füllstände (Öl, Flüssigkeiten): nach einer harten Saison prüfen.",
        "es": "Niveles (aceite, líquidos): comprobarlos tras una estación dura.",
        "it": "Livelli (olio, liquidi): controllarli dopo una stagione dura.",
    },
    "ac_gas": {
        "fr": "Climatisation : faire contrôler le gaz avant les fortes chaleurs.",
        "en": "Air conditioning: have the refrigerant checked before the heat arrives.",
        "de": "Klimaanlage: Kältemittel vor der großen Hitze prüfen lassen.",
        "es": "Aire acondicionado: hacer revisar el gas antes de las olas de calor.",
        "it": "Climatizzatore: far controllare il gas prima del grande caldo.",
    },
    "tires_pressure_heat": {
        "fr": "Pneus : pression à vérifier à froid, surtout avant les longs trajets (la chaleur la fait varier).",
        "en": "Tyres: check the pressure cold, especially before long trips (heat makes it vary).",
        "de": "Reifen: Luftdruck kalt prüfen, besonders vor langen Fahrten (Hitze verändert ihn).",
        "es": "Neumáticos: comprobar la presión en frío, sobre todo antes de viajes largos (el calor la hace variar).",
        "it": "Pneumatici: controllare la pressione a freddo, soprattutto prima dei lunghi viaggi (il caldo la fa variare).",
    },
    "coolant_heat": {
        "fr": "Refroidissement : niveau du liquide et absence de fuite (risque de surchauffe).",
        "en": "Cooling: coolant level and no leaks (overheating risk).",
        "de": "Kühlung: Flüssigkeitsstand und keine Undichtigkeiten (Überhitzungsgefahr).",
        "es": "Refrigeración: nivel del líquido y ausencia de fugas (riesgo de sobrecalentamiento).",
        "it": "Raffreddamento: livello del liquido e assenza di perdite (rischio di surriscaldamento).",
    },
    "safety_kit_trip": {
        "fr": "Longs trajets : triangle, gilet, eau et trousse de secours à bord.",
        "en": "Long trips: warning triangle, hi-vis vest, water and first-aid kit on board.",
        "de": "Lange Fahrten: Warndreieck, Warnweste, Wasser und Verbandskasten an Bord.",
        "es": "Viajes largos: triángulo, chaleco, agua y botiquín a bordo.",
        "it": "Viaggi lunghi: triangolo, giubbotto, acqua e kit di pronto soccorso a bordo.",
    },
    "battery_heat": {
        "fr": "Batterie : la chaleur l'use aussi, la faire contrôler si elle faiblit.",
        "en": "Battery: heat wears it too, have it checked if it weakens.",
        "de": "Batterie: auch Hitze setzt ihr zu, bei Schwäche prüfen lassen.",
        "es": "Batería: el calor también la desgasta, hacerla revisar si flojea.",
        "it": "Batteria: anche il caldo la consuma, farla controllare se cala.",
    },
    "hybrid_range_cold": {
        "fr": "Hybride : une autonomie électrique réduite par le froid est normale.",
        "en": "Hybrid: reduced electric range in the cold is normal.",
        "de": "Hybrid: eine durch Kälte verringerte elektrische Reichweite ist normal.",
        "es": "Híbrido: una autonomía eléctrica reducida por el frío es normal.",
        "it": "Ibrido: un'autonomia elettrica ridotta dal freddo è normale.",
    },
    "coolant_dual": {
        "fr": "Hybride : deux circuits de refroidissement (moteur et électronique de puissance) à vérifier.",
        "en": "Hybrid: two cooling circuits (engine and power electronics) to check.",
        "de": "Hybrid: zwei Kühlkreisläufe (Motor und Leistungselektronik) prüfen.",
        "es": "Híbrido: dos circuitos de refrigeración (motor y electrónica de potencia) que revisar.",
        "it": "Ibrido: due circuiti di raffreddamento (motore ed elettronica di potenza) da controllare.",
    },
    "hybrid_hv_cooling": {
        "fr": "Hybride : grilles et entrées d'air de la batterie haute tension dégagées.",
        "en": "Hybrid: keep the high-voltage battery's vents and air intakes clear.",
        "de": "Hybrid: Lüftungsgitter und Lufteinlässe der Hochvoltbatterie freihalten.",
        "es": "Híbrido: mantener despejadas las rejillas y entradas de aire de la batería de alto voltaje.",
        "it": "Ibrido: tenere libere le griglie e le prese d'aria della batteria ad alta tensione.",
    },
    "battery12_check": {
        "fr": "Batterie 12 V : sa santé conditionne le démarrage du véhicule, à faire tester.",
        "en": "12 V battery: its health decides whether the vehicle starts, have it tested.",
        "de": "12-V-Batterie: ihr Zustand entscheidet über den Start des Fahrzeugs, testen lassen.",
        "es": "Batería de 12 V: su estado condiciona el arranque del vehículo, hacerla comprobar.",
        "it": "Batteria da 12 V: il suo stato condiziona l'avviamento del veicolo, farla testare.",
    },
    "ev_cold_charging": {
        "fr": "Recharge par grand froid : préchauffer le véhicule branché et éviter de laisser la batterie très déchargée.",
        "en": "Charging in deep cold: preheat while plugged in and avoid leaving the battery very low.",
        "de": "Laden bei starker Kälte: am Kabel vorheizen und die Batterie nicht stark entladen lassen.",
        "es": "Carga con mucho frío: precalentar con el vehículo enchufado y evitar dejar la batería muy descargada.",
        "it": "Ricarica con freddo intenso: preriscaldare con il veicolo collegato ed evitare batteria molto scarica.",
    },
    "charge_cable_check": {
        "fr": "Câble et prise de charge : état, humidité, corrosion des contacts.",
        "en": "Charging cable and socket: condition, moisture, contact corrosion.",
        "de": "Ladekabel und Ladebuchse: Zustand, Feuchtigkeit, Korrosion der Kontakte.",
        "es": "Cable y toma de carga: estado, humedad, corrosión de los contactos.",
        "it": "Cavo e presa di ricarica: stato, umidità, corrosione dei contatti.",
    },
    "ac_check_ev": {
        "fr": "Climatisation : à faire contrôler seulement si elle refroidit mal (pas de recharge de gaz systématique).",
        "en": "Air conditioning: have it checked only if it cools poorly (no routine refrigerant top-up).",
        "de": "Klimaanlage: nur prüfen lassen, wenn sie schlecht kühlt (kein routinemäßiges Nachfüllen).",
        "es": "Aire acondicionado: revisarlo solo si enfría mal (sin recarga de gas sistemática).",
        "it": "Climatizzatore: farlo controllare solo se raffredda male (nessuna ricarica di gas sistematica).",
    },
    "ev_fast_charge_heat": {
        "fr": "Éviter les charges rapides répétées par forte chaleur pour ménager la batterie.",
        "en": "Avoid repeated fast charging in high heat to spare the battery.",
        "de": "Wiederholtes Schnellladen bei großer Hitze vermeiden, um die Batterie zu schonen.",
        "es": "Evitar cargas rápidas repetidas con mucho calor para cuidar la batería.",
        "it": "Evitare ricariche rapide ripetute con il caldo forte per preservare la batteria.",
    },
    "moto_tires_wet": {
        "fr": "Pneus : profondeur des sculptures, pression et état des flancs (adhérence sur le mouillé).",
        "en": "Tyres: tread depth, pressure and sidewall condition (wet grip).",
        "de": "Reifen: Profiltiefe, Luftdruck und Zustand der Flanken (Grip bei Nässe).",
        "es": "Neumáticos: profundidad del dibujo, presión y estado de los flancos (agarre en mojado).",
        "it": "Pneumatici: profondità del battistrada, pressione e stato dei fianchi (aderenza sul bagnato).",
    },
    "chain_wet": {
        "fr": "Chaîne : nettoyer et graisser avant la saison des pluies.",
        "en": "Chain: clean and lubricate before the rainy season.",
        "de": "Kette: vor der Regenzeit reinigen und schmieren.",
        "es": "Cadena: limpiar y engrasar antes de la temporada de lluvias.",
        "it": "Catena: pulire e lubrificare prima della stagione delle piogge.",
    },
    "brake_pads": {
        "fr": "Plaquettes de frein : contrôler l'usure.",
        "en": "Brake pads: check the wear.",
        "de": "Bremsbeläge: Verschleiß prüfen.",
        "es": "Pastillas de freno: comprobar el desgaste.",
        "it": "Pastiglie dei freni: controllare l'usura.",
    },
    "moto_battery_maintainer": {
        "fr": "Batterie : brancher un chargeur d'entretien si le véhicule reste à l'arrêt.",
        "en": "Battery: connect a trickle charger if the vehicle stays parked.",
        "de": "Batterie: bei längerem Stillstand ein Erhaltungsladegerät anschließen.",
        "es": "Batería: conectar un cargador de mantenimiento si el vehículo permanece parado.",
        "it": "Batteria: collegare un mantenitore di carica se il veicolo resta fermo.",
    },
    "fuel_stabilizer": {
        "fr": "Carburant : faire le plein ou ajouter un stabilisant avant un long arrêt.",
        "en": "Fuel: fill the tank or add a stabiliser before a long storage.",
        "de": "Kraftstoff: vor längerer Stilllegung volltanken oder Stabilisator zugeben.",
        "es": "Combustible: llenar el depósito o añadir estabilizador antes de una parada larga.",
        "it": "Carburante: fare il pieno o aggiungere uno stabilizzante prima di una lunga sosta.",
    },
    "coolant_antifreeze_if_liquid": {
        "fr": "Refroidissement liquide : vérifier la protection antigel du liquide (si refroidissement par liquide).",
        "en": "Liquid cooling: check the coolant's antifreeze protection (if liquid-cooled).",
        "de": "Flüssigkeitskühlung: Frostschutz der Kühlflüssigkeit prüfen (bei Flüssigkeitskühlung).",
        "es": "Refrigeración líquida: comprobar la protección anticongelante (si es de refrigeración líquida).",
        "it": "Raffreddamento a liquido: controllare la protezione antigelo (se raffreddato a liquido).",
    },
    "moto_restart_battery": {
        "fr": "Remise en route : recharger la batterie et vérifier qu'elle tient la charge.",
        "en": "Restart: recharge the battery and check it holds its charge.",
        "de": "Wiederinbetriebnahme: Batterie laden und prüfen, ob sie die Ladung hält.",
        "es": "Puesta en marcha: recargar la batería y comprobar que mantiene la carga.",
        "it": "Rimessa in moto: ricaricare la batteria e verificare che tenga la carica.",
    },
    "moto_tires_age_pressure": {
        "fr": "Pneus : pression, âge (date DOT) et fissures après l'immobilisation.",
        "en": "Tyres: pressure, age (DOT date) and cracks after standing idle.",
        "de": "Reifen: Luftdruck, Alter (DOT-Datum) und Risse nach dem Stillstand.",
        "es": "Neumáticos: presión, edad (fecha DOT) y grietas tras la inmovilización.",
        "it": "Pneumatici: pressione, età (data DOT) e crepe dopo il fermo.",
    },
    "brake_fluid_2y": {
        "fr": "Liquide de frein : à renouveler tous les 2 ans environ.",
        "en": "Brake fluid: replace roughly every 2 years.",
        "de": "Bremsflüssigkeit: etwa alle 2 Jahre erneuern.",
        "es": "Líquido de frenos: renovar aproximadamente cada 2 años.",
        "it": "Liquido freni: sostituire circa ogni 2 anni.",
    },
    "chain_check": {
        "fr": "Chaîne : tension, usure, graissage.",
        "en": "Chain: tension, wear, lubrication.",
        "de": "Kette: Spannung, Verschleiß, Schmierung.",
        "es": "Cadena: tensión, desgaste, engrase.",
        "it": "Catena: tensione, usura, lubrificazione.",
    },
    "moto_cooling": {
        "fr": "Refroidissement : niveau, ventilateur et absence de fuite avant la chaleur.",
        "en": "Cooling: level, fan and no leaks before the heat.",
        "de": "Kühlung: Füllstand, Lüfter und keine Undichtigkeiten vor der Hitze.",
        "es": "Refrigeración: nivel, ventilador y ausencia de fugas antes del calor.",
        "it": "Raffreddamento: livello, ventola e assenza di perdite prima del caldo.",
    },
    "chain_lube": {
        "fr": "Chaîne : nettoyer et lubrifier.",
        "en": "Chain: clean and lubricate.",
        "de": "Kette: reinigen und schmieren.",
        "es": "Cadena: limpiar y lubricar.",
        "it": "Catena: pulire e lubrificare.",
    },
    "gear_equipment": {
        "fr": "Équipement : casque, gants et protections en bon état, adaptés à la chaleur.",
        "en": "Gear: helmet, gloves and protection in good condition, suited to the heat.",
        "de": "Ausrüstung: Helm, Handschuhe und Schutzkleidung in gutem Zustand und hitzetauglich.",
        "es": "Equipo: casco, guantes y protecciones en buen estado y adecuados al calor.",
        "it": "Equipaggiamento: casco, guanti e protezioni in buono stato e adatti al caldo.",
    },
    "scooter_belt_rollers": {
        "fr": "Scooter : courroie et galets de variateur (usure après les trajets courts de l'hiver).",
        "en": "Scooter: drive belt and variator rollers (wear after short winter trips).",
        "de": "Roller: Antriebsriemen und Variatorrollen (Verschleiß nach kurzen Winterfahrten).",
        "es": "Scooter: correa y rodillos del variador (desgaste tras los trayectos cortos del invierno).",
        "it": "Scooter: cinghia e rulli del variatore (usura dopo i tragitti brevi invernali).",
    },
    "bike_tires_wet": {
        "fr": "Pneus : pression et usure (crevaisons plus fréquentes sur sol mouillé).",
        "en": "Tyres: pressure and wear (punctures are more frequent on wet ground).",
        "de": "Reifen: Luftdruck und Verschleiß (auf nassem Boden häufiger Pannen).",
        "es": "Neumáticos: presión y desgaste (los pinchazos son más frecuentes en suelo mojado).",
        "it": "Pneumatici: pressione e usura (forature più frequenti sul bagnato).",
    },
    "bike_lights": {
        "fr": "Éclairage : feux avant et arrière, leur alimentation, catadioptres.",
        "en": "Lighting: front and rear lights, their power supply, reflectors.",
        "de": "Beleuchtung: Front- und Rücklicht, Stromversorgung, Reflektoren.",
        "es": "Iluminación: luces delantera y trasera, su alimentación, catadióptricos.",
        "it": "Illuminazione: luci anteriore e posteriore, alimentazione, catarifrangenti.",
    },
    "bike_brake_pads": {
        "fr": "Freins : usure des plaquettes ou patins.",
        "en": "Brakes: pad or shoe wear.",
        "de": "Bremsen: Verschleiß von Belägen oder Klötzen.",
        "es": "Frenos: desgaste de pastillas o zapatas.",
        "it": "Freni: usura di pastiglie o pattini.",
    },
    "bike_battery_storage": {
        "fr": "Batterie : si le vélo ne roule pas, la stocker entre 10 et 20 °C, chargée à 50–60 %, jamais vide.",
        "en": "Battery: if the bike isn't ridden, store it at 10–20 °C, 50–60 % charged, never empty.",
        "de": "Akku: wenn das Rad nicht genutzt wird, bei 10–20 °C und 50–60 % Ladung lagern, nie leer.",
        "es": "Batería: si la bici no se usa, guardarla entre 10 y 20 °C, cargada al 50–60 %, nunca vacía.",
        "it": "Batteria: se la bici non si usa, conservarla tra 10 e 20 °C, carica al 50–60 %, mai scarica.",
    },
    "bike_contacts_humidity": {
        "fr": "Contacts électriques : les protéger de l'humidité et de la boue.",
        "en": "Electrical contacts: protect them from moisture and mud.",
        "de": "Elektrische Kontakte: vor Feuchtigkeit und Schlamm schützen.",
        "es": "Contactos eléctricos: protegerlos de la humedad y el barro.",
        "it": "Contatti elettrici: proteggerli da umidità e fango.",
    },
    "bike_general_check": {
        "fr": "Contrôle général : chaîne, câbles, freins et pression des pneus.",
        "en": "General check: chain, cables, brakes and tyre pressure.",
        "de": "Allgemeine Kontrolle: Kette, Züge, Bremsen und Reifendruck.",
        "es": "Revisión general: cadena, cables, frenos y presión de los neumáticos.",
        "it": "Controllo generale: catena, cavi, freni e pressione dei pneumatici.",
    },
    "bike_electrical_connections": {
        "fr": "Connexions électriques : connecteurs, prise de charge, affichage.",
        "en": "Electrical connections: connectors, charging port, display.",
        "de": "Elektrische Verbindungen: Steckverbinder, Ladebuchse, Display.",
        "es": "Conexiones eléctricas: conectores, toma de carga, pantalla.",
        "it": "Connessioni elettriche: connettori, presa di ricarica, display.",
    },
    "bike_battery_sun": {
        "fr": "Batterie : ne pas la laisser au soleil ni dans un véhicule surchauffé.",
        "en": "Battery: don't leave it in the sun or in an overheated vehicle.",
        "de": "Akku: nicht in der Sonne oder in einem überhitzten Fahrzeug lassen.",
        "es": "Batería: no dejarla al sol ni en un vehículo recalentado.",
        "it": "Batteria: non lasciarla al sole né in un veicolo surriscaldato.",
    },
    "bike_tires_pressure": {
        "fr": "Pneus : pression à vérifier régulièrement (chaleur, charge).",
        "en": "Tyres: check the pressure regularly (heat, load).",
        "de": "Reifen: Luftdruck regelmäßig prüfen (Hitze, Beladung).",
        "es": "Neumáticos: comprobar la presión con regularidad (calor, carga).",
        "it": "Pneumatici: controllare regolarmente la pressione (caldo, carico).",
    },
}

_THERMAL: dict[str, list[str]] = {
    "autumn": ["wipers", "tires_rain", "lights", "battery_test", "washer_antifreeze"],
    "winter": ["tires_pressure_cold", "coolant_antifreeze", "washer_level", "battery_cold", "winter_kit"],
    "spring": ["summer_tires_swap", "post_winter_check", "ac_recheck", "pollen_filter", "fluids_levels"],
    "summer": ["ac_gas", "tires_pressure_heat", "coolant_heat", "safety_kit_trip", "battery_heat"],
}

SEASON_TIPS: dict[str, dict[str, list[str]]] = {
    "auto_thermal": _THERMAL,
    "auto_hybrid": {
        "autumn": _THERMAL["autumn"],
        "winter": _THERMAL["winter"] + ["hybrid_range_cold", "coolant_dual"],
        "spring": _THERMAL["spring"],
        "summer": _THERMAL["summer"] + ["hybrid_hv_cooling"],
    },
    "auto_electric": {
        "autumn": ["wipers", "tires_rain", "lights", "battery12_check"],
        "winter": ["tires_pressure_cold", "washer_level", "battery12_check", "ev_cold_charging", "winter_kit"],
        "spring": ["summer_tires_swap", "charge_cable_check", "pollen_filter", "post_winter_check"],
        "summer": ["ac_check_ev", "tires_pressure_heat", "ev_fast_charge_heat", "safety_kit_trip"],
    },
    "moto": {
        "autumn": ["moto_tires_wet", "lights", "chain_wet", "brake_pads"],
        "winter": ["moto_battery_maintainer", "fuel_stabilizer", "moto_tires_pressure_cold", "coolant_antifreeze_if_liquid"],
        "spring": ["moto_restart_battery", "moto_tires_age_pressure", "brake_fluid_2y", "chain_check", "fluids_levels"],
        "summer": ["moto_cooling", "tires_pressure_heat", "chain_lube", "gear_equipment"],
    },
    "scooter": {
        "autumn": ["moto_tires_wet", "lights", "brake_pads"],
        "winter": ["moto_battery_maintainer", "fuel_stabilizer", "moto_tires_pressure_cold", "coolant_antifreeze_if_liquid"],
        "spring": ["moto_restart_battery", "scooter_belt_rollers", "moto_tires_age_pressure", "brake_fluid_2y"],
        "summer": ["moto_cooling", "tires_pressure_heat", "gear_equipment"],
    },
    "velo_electrique": {
        "autumn": ["bike_tires_wet", "bike_lights", "bike_brake_pads"],
        "winter": ["bike_battery_storage", "bike_contacts_humidity", "chain_lube"],
        "spring": ["bike_general_check", "bike_electrical_connections"],
        "summer": ["bike_battery_sun", "bike_tires_pressure", "chain_lube"],
    },
}

SEASON_TITLES: dict[str, dict[str, str]] = {
    "fr": {"spring": "🌸 Rappels de printemps", "summer": "☀️ Rappels d'été", "autumn": "🍂 Rappels d'automne", "winter": "❄️ Rappels d'hiver"},
    "en": {"spring": "🌸 Spring checklist", "summer": "☀️ Summer checklist", "autumn": "🍂 Autumn checklist", "winter": "❄️ Winter checklist"},
    "de": {"spring": "🌸 Frühjahrs-Check", "summer": "☀️ Sommer-Check", "autumn": "🍂 Herbst-Check", "winter": "❄️ Winter-Check"},
    "es": {"spring": "🌸 Revisión de primavera", "summer": "☀️ Revisión de verano", "autumn": "🍂 Revisión de otoño", "winter": "❄️ Revisión de invierno"},
    "it": {"spring": "🌸 Controlli di primavera", "summer": "☀️ Controlli d'estate", "autumn": "🍂 Controlli d'autunno", "winter": "❄️ Controlli d'inverno"},
}

INTRO: dict[str, str] = {
    "fr": "À vérifier pour cette saison :",
    "en": "Worth checking this season:",
    "de": "Für diese Jahreszeit prüfen:",
    "es": "Conviene revisar esta temporada:",
    "it": "Da controllare in questa stagione:",
}

_NORTH_BY_MONTH = {12: "winter", 1: "winter", 2: "winter", 3: "spring", 4: "spring", 5: "spring",
                   6: "summer", 7: "summer", 8: "summer", 9: "autumn", 10: "autumn", 11: "autumn"}
_OPPOSITE = {"winter": "summer", "summer": "winter", "spring": "autumn", "autumn": "spring"}


def current_season(today: date, latitude: float | None) -> tuple[str, str]:
    """Renvoie (saison, clé) — la clé (ex. "2026-winter") identifie une
    occurrence précise de saison et reste stable tout au long de celle-ci,
    même quand elle chevauche deux années civiles (hiver au nord, été au
    sud), pour ne notifier qu'une fois par saison."""
    south = latitude is not None and latitude < 0
    season = _NORTH_BY_MONTH[today.month]
    if south:
        season = _OPPOSITE[season]
    wraps = season == ("summer" if south else "winter")
    year = today.year - 1 if wraps and today.month <= 2 else today.year
    return season, f"{year}-{season}"


def vehicle_kind(vehicle: dict) -> str:
    """auto_thermal | auto_hybrid | auto_electric | moto | scooter | velo_electrique"""
    if vehicle.get("vehicle_type") == "deux_roues":
        return vehicle.get("two_wheeler_type") or "moto"
    fuel = (vehicle.get("fuel_type") or "").lower()
    if "hybri" in fuel or "ibrid" in fuel:
        return "auto_hybrid"
    if "lectri" in fuel or "elettr" in fuel or fuel == "electric":
        return "auto_electric"
    return "auto_thermal"


def build_seasonal_message(kind: str, season: str, lang: str, label: str) -> tuple[str, str]:
    """(titre, corps markdown) de la notification saisonnière."""
    lang = lang if lang in INTRO else "fr"
    tips = SEASON_TIPS.get(kind, SEASON_TIPS["auto_thermal"])[season]
    lines = "\n".join(f"- {TIPS[t][lang]}" for t in tips)
    return SEASON_TITLES[lang][season], f"**{label}**\n\n{INTRO[lang]}\n\n{lines}"
