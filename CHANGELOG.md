# Changelog

Historique des versions de l'intégration Carnet d'entretien.

## 🆕 Nouveautés v1.4.1

- **Choix de la langue déplacé à l'installation** : la langue de contenu
  (carte, catalogue, texte généré par l'IA, notifications) se choisit
  désormais **au même écran que la clé API Gemini**, lors de l'ajout de
  l'intégration (`config_flow`), et reste modifiable ensuite uniquement
  depuis **Paramètres → Appareils et services → CARnet - Garage Log →
  Configurer** (les Options). Le panneau Réglages de la carte n'affiche
  plus qu'un rappel en lecture seule de la langue active — il n'y a plus
  de sélecteur de langue cliquable dans la carte : l'entrée de
  configuration Home Assistant est désormais la seule source de vérité,
  synchronisée automatiquement dans le stockage de l'intégration à chaque
  démarrage.
- **Correctif** : `translations/en.json` contenait en réalité du texte
  français par erreur (bug latent, non signalé mais repéré durant ce
  travail) — corrigé, et utilisé comme base pour créer les nouvelles
  traductions `de.json`, `es.json` et `it.json` de l'écran de
  configuration/options (jusqu'ici seuls `fr.json` et `en.json`
  existaient pour cet écran).
- **README entièrement réécrit** : structure bilingue anglais d'abord,
  français ensuite (au lieu de français uniquement), avec une nouvelle
  section de dépannage détaillée dédiée au cas où la carte Lovelace
  n'apparaît pas après l'installation (ressource JS manquante, mal
  orthographiée, mise en cache — avec une checklist en 7 points).

## 🆕 Nouveautés v0.2

Suite à des retours d'usage sur un outil comparable, chaque échéance du
plan d'entretien et chaque estimation affichent maintenant :

- **💰 Coût estimé** par opération (`cost_estimate_eur`), pièces + main
  d'œuvre, tarif moyen constaté en France pour ce modèle.
- **📅 Date prévisionnelle réelle** (`prevu_vers`, format `MM/AAAA`) :
  calculée en convertissant le kilométrage restant via le **rythme
  kilométrique annuel réel du véhicule** (déduit de l'historique de
  kilométrage saisi), et non plus une simple estimation générique à
  12 000 km/an tant que peu de mesures existent.
- **⚠️ "Dépassé de : X km"** au lieu d'un simple "reste" négatif, avec
  mention "à faire dès que possible" — distinct visuellement d'une
  échéance encore à venir.
- **Opérations non applicables au véhicule précis** : Gemini vérifie
  l'équipement réel (ex : freins à tambours à l'arrière → pas de
  "Remplacement disques de frein arrière") et affiche l'opération grisée
  avec le motif, plutôt que de générer une échéance qui n'a pas de sens.
- **Sources citées** pour les points de vigilance (ex : *"Programme
  d'entretien officiel Renault, Revue Technique Automobile RTA B772…"*)
  et pour l'estimation de valeur (*"Estimation basée sur LaCentrale et
  Leboncoin, tenant compte de la décote ZFE et du kilométrage annuel
  par rapport à la moyenne du marché…"*) — affichées dans un encadré
  dédié sous chaque section, pour que vous sachiez toujours sur quoi
  s'appuie une affirmation générée par IA.

## 🆕 Nouveautés v0.3

- **Style "Grand Tourisme cuir"** : la carte a désormais sa propre identité
  visuelle (cuir cognac, surpiqûres crème en pointillés, noyer sombre),
  volontairement indépendante du thème clair/sombre de Home Assistant —
  esprit console d'habitacle plutôt qu'appli mobile. Les points de vigilance
  et la valeur de revente sont des **panneaux dépliables** (clic pour révéler
  le détail et la raison de l'estimation) plutôt que des onglets séparés, et
  chaque échéance d'entretien a désormais sa propre **jauge en ligne** — plus
  de traitement à part pour la vidange.
- **Kilométrage lié à un capteur** : bouton 🔗 à côté du champ kilométrage,
  sélecteur d'entité HA natif (`ha-entity-picker`) pour choisir n'importe quel
  capteur numérique existant (odomètre constructeur, traceur OBD/GPS,
  `input_number`...). Une fois lié, le kilométrage suit automatiquement les
  changements d'état du capteur — historique et échéances se recalculent
  tout seuls — et un bouton "Délier" permet de repasser en saisie manuelle à
  tout moment. Nouveau service : `carnet_entretien.set_mileage_source`.

## 🆕 Nouveautés v0.4

- **4 thèmes visuels au choix**, via le bouton ⚙️ en haut de la carte :
  *Grand tourisme cuir* (cognac/noyer, par défaut), *Manufacture horlogère*
  (navy/acier/rouge chirurgical), *Carbone et titane* (noir mat/cyan
  digital), *Atelier vintage* (ivoire/noyer/vert anglais, seul thème clair).
  Le thème change instantanément (toutes les couleurs — y compris les
  couleurs de statut des échéances — sont pilotées par variables CSS) et se
  mémorise côté serveur : le même thème s'affiche sur tous les appareils qui
  ouvrent le tableau de bord.
- **Sélecteur rapide de véhicule** : dès que vous avez plus d'un véhicule,
  une liste déroulante apparaît en haut de la fiche détail pour basculer
  d'un véhicule à l'autre sans repasser par la vue liste.

## 🆕 Nouveautés v0.5

- **Autocomplétion marque/modèle corrigée** : la version précédente
  s'appuyait sur `<datalist>` et perdait le focus du champ à chaque frappe
  (re-rendu complet de la carte). Remplacée par un vrai menu de suggestions
  maison qui se met à jour sans perturber la saisie — plusieurs propositions
  s'affichent au fur et à mesure que vous tapez, cliquables directement.
- **Photo du véhicule** : champ d'upload dans le formulaire d'ajout, et
  bouton "📷 Ajouter/Changer une photo" sur la fiche détail — upload direct
  depuis l'appareil qui affiche le tableau de bord (téléphone, tablette,
  ordinateur). L'image est redimensionnée et compressée **dans le
  navigateur** avant envoi (~480 px de large, JPEG qualité 72%) pour ne pas
  alourdir le fichier de stockage local ; comptez grossièrement 30 à 100 Ko
  par photo. Affichée en vignette sur les tuiles de la liste et en médaillon
  sur la fiche détail, avec un bouton "Retirer".
- Pour rappel, le bouton **➕ Ajouter** (création d'un véhicule) se trouve
  en haut à droite de la vue liste (écran d'accueil de la carte).

## 🆕 Nouveautés v0.6

- **Plaque d'immatriculation affichée** : le champ existait déjà dans le
  formulaire d'ajout mais n'était affiché nulle part — elle apparaît
  maintenant en petite puce sous le titre de la fiche véhicule et en rappel
  sur les tuiles de la liste.
- **Chaque échéance d'entretien est cliquable** : un clic sur une ligne
  déplie un formulaire avec la dernière intervention connue (date + km),
  une case à cocher **"Entretien fait aujourd'hui"** (pré-remplit
  automatiquement date du jour et kilométrage actuel du véhicule, champs
  verrouillés), ou une saisie manuelle libre de la date et du kilométrage
  de la dernière intervention. C'est cette date/ce kilométrage qui sert de
  base au calcul de la prochaine échéance (`due_km`/`due_date` dans
  `utils.py`) — plus besoin de passer par une boîte de dialogue système
  imprécise. Le service `carnet_entretien.log_maintenance` accepte
  désormais aussi un champ `date` optionnel.
- **v0.6.1** : la case "fait aujourd'hui" était ambiguë (fallait-il encore
  cliquer "Enregistrer" ?). Remplacée par un bouton d'action directe
  **"✓ Fait aujourd'hui (kilométrage actuel)"** qui enregistre immédiatement
  en un clic ; la saisie manuelle d'une date antérieure reste disponible
  juste en dessous, séparée visuellement ("ou une date antérieure").
- **v0.6.2 (correctif)** : `hass.http.register_static_path` a été retiré
  des versions récentes de Home Assistant (2024.7+) au profit de
  `async_register_static_paths` (asynchrone, via `StaticPathConfig`) ;
  `hass.components.frontend.add_extra_js_url` est lui aussi remplacé par un
  import direct. Corrigé dans `__init__.py` — si vous êtes sur une version
  de HA plus ancienne que 2024.7 et que cela pose problème, dites-le moi.
- **v0.6.2bis (correctif)** : la lecture du référentiel JSON au démarrage
  se faisait par un `open()` synchrone directement dans la boucle asyncio
  (bloquant, détecté par le garde-fou `homeassistant.util.loop`). Déplacée
  dans `hass.async_add_executor_job`.

## 🆕 Nouveautés v0.7

- **Autocomplétion de la motorisation** : une fois marque, modèle et année
  renseignés, le champ "Motorisation" propose désormais les versions
  réellement commercialisées (ex : "1.5 BlueHDi 130", "1.2 PureTech 130
  EAT8"), générées par Gemini et **mises en cache côté serveur** par
  combinaison marque/modèle/année (un seul appel IA par combinaison, jamais
  répété ensuite). Côté navigateur, la liste est récupérée une fois puis
  filtrée localement à chaque frappe — recherche instantanée, comme pour le
  référentiel marque/modèle. Le champ Année a été déplacé avant Motorisation
  dans le formulaire puisqu'il conditionne désormais la recherche. Sans clé
  Gemini configurée, le champ reste utilisable en saisie libre (simplement
  sans suggestions).

## 🆕 Nouveautés v0.8

- **Rappels constructeur actifs** : nouveau panneau "🚨 Rappels constructeur"
  (au-dessus des points de vigilance), généré par Gemini à la création du
  véhicule et rafraîchissable manuellement. Mutualisé par modèle (même
  cache que les points de vigilance) pour éviter de réinterroger l'IA à
  chaque véhicule identique. Chaque rappel affiche titre, référence,
  gravité, description, action requise et sources — avec un bandeau
  d'avertissement invitant à vérifier sur le site du constructeur ou
  rappel.conso.gouv.fr, car la synthèse IA n'est pas garantie exhaustive
  ni à jour en temps réel. Nouveau service : `carnet_entretien.refresh_recalls`.
- **Reconnaissance de plaque VIN à la création** : champ photo en tête du
  formulaire d'ajout — une photo de la plaque VIN/constructeur (sous le
  capot, montant de porte...) est envoyée à Gemini Vision, qui lit les
  informations visibles et/ou décode le VIN pour **préremplir
  automatiquement** marque, modèle, année et motorisation (chaque champ
  reste modifiable ensuite, avec un indicateur de confiance affiché).
  Nécessite une clé Gemini configurée ; sans clé, le formulaire reste
  utilisable en saisie manuelle classique.
- Le client Gemini interne a été généralisé pour supporter les appels
  multimodaux (texte + image), réutilisable pour de futures fonctions
  vision (`gemini_client._call_vision`).

## 🆕 Nouveautés v0.9

Passe de correctifs suite à un usage réel intensif :

- **`hacs.json` déplacé à la racine du dépôt** — il était par erreur dans
  `custom_components/carnet_entretien/`, ce qui empêchait purement et
  simplement HACS de détecter l'intégration à l'installation.
- **Nom de l'intégration** changé en "CARnet - Garage Log" (`manifest.json`,
  `hacs.json`), icône ajoutée (`icon.png` à la racine, + gabarits 256/512 px
  dans `brands/` pour une future soumission à `home-assistant/brands`).
- **Bug de cascade Gemini corrigé** : une erreur sur un modèle (timeout,
  réponse mal formée...) empêchait d'essayer les modèles suivants sauf pour
  les erreurs HTTP. Corrigé : tous les modèles candidats sont désormais
  systématiquement essayés, avec un message d'erreur agrégé en cas d'échec
  total. `gemini-1.5-flash` (déprécié chez Google) retiré de la liste des
  modèles essayés, remplacé par `gemini-2.5-flash-lite`.
- **Contrôle technique et révision constructeur garantis** dans le plan
  d'entretien : injectés automatiquement si l'IA les a omis
  (`utils.ensure_default_items`), avec la règle française réaliste pour le
  contrôle technique (1ère visite à 4 ans, puis tous les 2 ans — voir
  `first_interval_months` dans `utils.compute_item_status`).
- **Prompt renforcé** pour limiter les contradictions d'une génération à
  l'autre sur les caractéristiques factuelles du véhicule (ex : disques vs
  tambours à l'arrière) — un croisement multi-sources plus poussé (appels
  multiples réconciliés) reste une piste si cela ne suffit pas.
- **Notifications persistantes Home Assistant** créées/retirées
  automatiquement quand une échéance passe en statut "échue" (vérification
  au démarrage, après chaque mutation pertinente, et une fois par jour).
- **Bug d'affichage corrigé** : sur les échéances basées sur une durée
  (sans kilométrage), le prix s'affichait par erreur au bout de la jauge à
  la place du temps restant/dépassé.
- **VIN saisissable manuellement** (en plus de la photo), et **copie
  automatique dans le champ Immatriculation** si une plaque de circulation
  est détectée sur la photo ou saisie en même temps que le VIN.
- **Capture caméra directe** (`capture="environment"`) sur tous les champs
  photo — ouvre l'appareil photo directement depuis l'app Companion HA sur
  mobile plutôt qu'un sélecteur de fichiers générique.

## 🆕 Nouveautés v0.9.1

- **Re-tentative automatique sur quota Gemini (429)** : un dépassement de
  quota sur un modèle déclenche désormais jusqu'à 2 re-tentatives sur ce
  même modèle (délai croissant 5s/15s) avant de passer au modèle suivant —
  un dépassement de quota par minute se résorbe souvent tout seul en
  quelques secondes, inutile de basculer immédiatement vers un modèle
  potentiellement indisponible pour la clé. Nouveau code d'erreur dédié
  `rate_limited`.
- **Reconnaissance véhicule repensée** : le scan photo à la création vise
  maintenant une photo de la voiture (carrosserie, logos, plaque visibles),
  pas uniquement un gros plan de plaque — une plaque seule ne permet
  objectivement pas de déduire marque/modèle (aucune base publique ne fait
  cette correspondance), la fonction le signale désormais clairement au
  lieu de laisser les champs vides sans explication. La saisie manuelle du
  VIN a été retirée (trop contraignante à l'usage) ; la photo reste la
  seule voie assistée par IA, avec un texte d'aide invitant à cadrer plus
  large que la seule plaque.
- **Précision sur l'icône HACS** : `icon.png` à la racine du dépôt améliore
  l'affichage sur la page GitHub et dans le rendu du README, mais **HACS
  source l'icône affichée dans son interface depuis le dépôt
  `home-assistant/brands`**, pas depuis le dépôt lui-même — c'est normal
  qu'elle n'apparaisse pas encore dans HACS tant que cette PR séparée n'est
  pas soumise/mergée (voir `docs/RELEASING.md §7`, fichiers déjà préparés
  dans `brands/`).

## 🆕 Nouveautés v0.10 — refonte du plan d'entretien

Changement d'architecture majeur suite aux retours d'usage sur les oublis et
incohérences constatés (courroie d'accessoires manquante, disques/plaquettes
fusionnés, listes différentes à chaque régénération...) :

- **Reconnaissance photo/VIN/plaque entièrement retirée**. Retour au
  remplissage manuel marque/modèle/année, avec l'autocomplétion Gemini de
  la motorisation (déjà en place depuis la v0.7) comme seule assistance IA
  à la création.
- **Catalogue d'entretien codé en dur** (`maintenance_catalog.py`, ~28
  opérations) : vidange, tous les filtres, courroie de distribution **et**
  courroie d'accessoires séparément, disques **et** plaquettes avant/arrière
  comme entrées distinctes, batterie 12V, climatisation, FAP/EGR,
  embrayage, liquide de boîte, amortisseurs, rotules, cardans,
  échappement, essuie-glaces, contrôle technique, révision constructeur…
  L'IA ne décide plus QUELLES opérations existent (source des oublis) mais
  seulement, pour CHAQUE entrée fixe, si elle est applicable à ce véhicule
  précis et avec quel intervalle — rien ne peut plus disparaître d'une
  génération à l'autre.
- **Régénération non destructive** : les items ont désormais un id stable
  (celui du catalogue), donc régénérer le plan préserve les dates de
  dernière intervention, les bascules manuelles applicable/non-applicable,
  les ajustements d'échéance et les explications DIY déjà générées — ce
  qui disparaissait avant à chaque régénération.
- **Case à cocher applicable/non-applicable** sur chaque échéance,
  éditable manuellement à tout moment (contre les erreurs de génération
  IA, inévitables).
- **Ajustement manuel direct de l'échéance** (km et/ou date), en plus du
  calcul habituel basé sur la dernière intervention + intervalle.
- **Ajout d'un entretien manquant sans régénérer tout le plan** — bouton
  "+ Ajouter un entretien" en bas de la liste, formulaire nom/intervalles/
  coût, n'affecte aucun autre item.
- **Réglage "masquer les entretiens non applicables"** et **réglage
  "notifications d'échéances dépassées" (on/off)**, dans l'écran Réglages.
- **Difficulté DIY en deux temps** : dès la génération initiale, chaque
  échéance applicable reçoit un niveau de difficulté (facile/moyen/
  difficile/déconseillé) et un coût pièces estimé en DIY (peu de tokens
  supplémentaires). Un bouton "🔧 Comment le faire soi-même ?" génère à la
  demande — et met en cache — l'explication détaillée, l'outillage
  spécifique et le temps estimé (appel Gemini séparé, pour ne pas alourdir
  la génération initiale).
- Prompt de génération du plan encore renforcé : croisement mental
  documentation constructeur / revue technique indépendante, consigne
  explicite de cohérence factuelle (ex : ne jamais annoncer un
  remplacement de disques ET la présence de tambours sur le même essieu).

## 🎉 v1.0.0 — première version diffusable

Première version jugée prête pour une diffusion publique (au-delà d'un
usage personnel). Pas de nouvelle fonctionnalité par rapport à la v0.10 —
uniquement du polish autour de l'identité du projet et de son intégration
à l'écosystème HA/HACS :

- **Icône affichée dans Home Assistant** : ajout de
  `custom_components/carnet_entretien/brand/` (icon.png 256×256,
  icon@2x.png 512×512), le nouveau mécanisme d'icônes inline pour
  intégrations tierces introduit en Home Assistant 2026.3 — plus besoin de
  PR vers `home-assistant/brands` (qui n'accepte d'ailleurs plus les
  nouvelles intégrations tierces depuis ce changement). Voir
  `docs/RELEASING.md §7` pour le détail et une limite connue côté HACS.
- **Icône dans le titre de la carte Lovelace**, à la place de l'emoji 🚗
  générique.
- **Nom affiché harmonisé** partout : "CARnet - Garage Log" (carte,
  manifest, hacs.json, README).
- **Illustration d'en-tête `badge.svg`** dans le README, remplaçant le
  simple `icon.png`.
- **Toutes les références à ha-millesime retirées** du code et de la
  documentation (commentaires internes uniquement, aucun changement de
  comportement).
- **README recentré sur l'utilisateur final** : les liens vers
  `docs/IDEAS.md` (roadmap) et `docs/RELEASING.md` (workflow de
  publication, usage interne au mainteneur) ont été retirés du README
  public — les fichiers restent dans le dépôt mais ne sont plus mis en
  avant.

## 🛠️ v1.0.1 — correctifs

- **Notifications désactivées par défaut à l'installation.** Sans
  intervention enregistrée, toutes les échéances partaient "en retard"
  par rapport à une base zéro, générant une notification pour chaque
  entretien dès la création du premier véhicule. Les nouvelles
  installations démarrent maintenant avec les notifications désactivées ;
  activable à tout moment dans Réglages. **Les installations existantes**
  ayant déjà ce réglage enregistré ne sont pas affectées automatiquement —
  décochez-le manuellement dans Réglages si besoin.
- **Durcissement de l'enregistrement de la carte Lovelace** : si le
  fichier `www/carnet-entretien-card.js` venait à manquer ou si son
  enregistrement échouait pour une autre raison, toute l'intégration
  (services, capteurs, notifications) tombait avec lui. Désormais,
  seul le chargement de la carte est affecté en cas de problème — le
  reste continue de fonctionner — et l'erreur est journalisée clairement
  dans les logs HA (`carnet_entretien`) au lieu d'un simple "Custom
  element doesn't exist" côté navigateur, sans indication de cause.

## 🛠️ v1.0.2 — correctifs

- **Appareils fantômes non supprimables corrigés.** La suppression d'un
  véhicule ne retirait que ses entités, jamais l'appareil (device) associé
  — celui-ci restait visible dans Paramètres → Appareils, uniquement
  désactivable, jamais supprimable depuis l'UI. `_remove_vehicle` retire
  désormais explicitement le device en plus des entités. Un callback
  `async_remove_config_entry_device` a aussi été ajouté pour permettre de
  supprimer manuellement les appareils fantômes déjà créés par des
  versions antérieures (bouton "Supprimer" maintenant disponible dans
  Paramètres → Appareils → l'appareil concerné).
  Cela explique aussi les erreurs IA remontées sur un véhicule "déjà
  supprimé" : l'appareil fantôme restait référencé quelque part côté UI,
  et les requêtes générées pour son id de véhicule (qui n'existait plus
  côté stockage) échouaient normalement côté serveur.
- **Suppression d'un véhicule plus robuste côté carte** : une erreur lors
  de la suppression échouait silencieusement (aucun message, rendu figé) ;
  elle affiche maintenant une alerte explicite et resynchronise l'état.
- **Réglages** : retrait du texte "D'autres réglages arriveront ici".
  Ajout d'un réglage de **taille du texte** (boutons A−/A+, 80% à 140%
  par pas de 10%), qui redimensionne toute la carte proportionnellement.

## 🛠️ v1.0.3 — correctif majeur : le stockage survivait à la désinstallation

- **Le fichier de stockage local (`.storage/carnet_entretien_data`)
  n'était jamais purgé**, même en supprimant complètement l'intégration
  et en la désinstallant de HACS — ce fichier vit indépendamment du cycle
  de vie de la config entry. Conséquence directe : véhicules "supprimés"
  (y compris via suppression manuelle des appareils) qui réapparaissaient
  intégralement à la moindre réinstallation, échéances non validées
  comprises. Ajout du hook `async_remove_entry`, appelé par Home Assistant
  uniquement lors d'une suppression **définitive** de l'intégration (pas
  un simple rechargement), qui purge maintenant ce fichier.
  ⚠️ **Une fois cette version installée, un cycle complet
  suppression-de-l'intégration → réinstallation est nécessaire pour purger
  les données restées de la version précédente** — la mise à jour seule
  ne suffit pas, puisque le bug empêchait justement cette purge jusqu'ici.
- **Durcissement de `sensor.py`** : un enregistrement véhicule d'un ancien
  schéma de données (champ manquant) ne fait plus planter la création des
  capteurs des AUTRES véhicules, et n'interrompt plus tout le chargement
  de l'intégration — chaque véhicule est traité indépendamment, avec
  journalisation claire (`carnet_entretien`) en cas de souci sur l'un
  d'eux.

## 🛠️ v1.0.4 — la carte ne se chargeait toujours pas sur certaines versions de HA

- **`add_extra_js_url` retiré**, remplacé par un ajout manuel obligatoire
  de la ressource Lovelace (une fois, à l'installation — voir
  `docs/INSTALL.md §4`). Ce mécanisme d'enregistrement automatique de la
  carte s'est avéré peu fiable sur certaines versions récentes de Home
  Assistant : échec **silencieux**, aucune erreur journalisée, la route
  HTTP fonctionnait mais la ressource n'apparaissait jamais dans le
  tableau de bord. L'ajout manuel via Paramètres → Tableaux de bord →
  Ressources passe par l'UI standard de HA et fonctionne de façon
  garantie, quelle que soit la version.
- **`OptionsFlow` corrigé** : `config_entry` est devenu une propriété en
  lecture seule sur les versions récentes de HA, assignée automatiquement
  par le framework — notre `__init__` qui l'assignait manuellement (pattern
  historiquement standard) levait `AttributeError` à l'ouverture des
  réglages de l'intégration. Ne définit plus `__init__` du tout.

## 🛠️ v1.0.5 — ajustements

- **Icône du titre de la carte doublée** (24px → 48px), trop petite pour
  être lisible.
- **Kilométrage annuel moyen** : se rabattait sur une constante fixe
  (12 000 km/an) pour tout véhicule n'ayant qu'un seul relevé de
  kilométrage (donc systématiquement juste après la création). Repli
  amélioré : kilométrage total actuel ÷ âge du véhicule (année de mise en
  circulation), nettement plus pertinent pour un véhicule d'occasion déjà
  roulé, disponible dès la création plutôt que d'attendre plusieurs
  relevés espacés d'au moins 30 jours.

## 🆕 v1.1.0

- **Icône remplacée partout** (page Intégrations, fiche HACS, coin de la
  carte Lovelace) par la nouvelle icône fournie, déjà au format natif
  48×48 — nette à l'échelle d'affichage réelle plutôt qu'agrandie depuis
  une source plus petite ou compressée depuis une plus grande.
- **Rappel périodique de mise à jour du kilométrage**, en plus du rappel
  d'échéances dépassées : notification persistante si le kilométrage d'un
  véhicule en saisie manuelle n'a pas été mis à jour depuis X jours
  (réglable, 30 jours par défaut, désactivable). Les véhicules liés à un
  capteur de kilométrage en sont naturellement exclus (ils se mettent à
  jour tout seuls). Vérifié au démarrage, une fois par jour, et après
  chaque mise à jour de kilométrage.
- **Catalogue étendu à 45 opérations** (contre 28) : ajout de tout
  l'entretien spécifique hybride (HEV/PHEV — filtre ventilation batterie
  HT, refroidissement inverter, diagnostic SoH), 100% électrique (BEV —
  réducteur, refroidissement batterie de traction, graissage étriers,
  cartouche dessiccante), GPL (filtres phase gazeuse/liquide, jeu aux
  soupapes, inspection réglementaire du réservoir) et quelques compléments
  thermiques qui manquaient (AdBlue, additif FAP/Eolys, ponts et boîte de
  transfert 4x4, géométrie des trains, réglage freins à tambour).
- **Sélecteur de carburant/énergie** à la création du véhicule (Essence /
  Diesel / Électrique / Hybride / GPL), avant le champ Motorisation —
  optionnel mais fortement recommandé : affine à la fois les suggestions
  de motorisation et la génération du plan (l'IA n'a plus à deviner le
  type d'énergie depuis le seul libellé de motorisation, ce qui limite le
  risque d'erreurs d'applicabilité sur les entrées thermiques vs
  électriques).
- **"Masquer les entretiens non applicables" coché par défaut** à
  l'installation — avec 45 opérations dont beaucoup ne concernent qu'un
  type d'énergie donné, la plupart des véhicules ont désormais une bonne
  proportion d'entrées non applicables ; les masquer par défaut rend la
  liste lisible dès le départ (reste décochable dans Réglages).

## 🆕 v1.2.0 — prise en charge des deux-roues

- **Moto, scooter et vélo électrique**, en plus des voitures : sélecteur
  🚗 Auto / 🏍️ 2 roues en tête du formulaire d'ajout, avec sous-choix du
  type pour les 2 roues. Trois catalogues d'entretien totalement
  distincts (`CAR_CATALOG` 46 entrées, `MOTORIZED_TWO_WHEELER_CATALOG`
  moto/scooter 26 entrées, `EBIKE_CATALOG` vélo électrique 15 entrées) —
  chaque véhicule ne pioche que dans son propre catalogue, donc aucun
  risque qu'une entrée "chaîne de transmission" apparaisse, même en non
  applicable, sur la fiche d'une voiture : c'est structurellement
  impossible plutôt que filtré a posteriori.
  Catalogue moto/scooter : vidange, kit chaîne ou courroie/galets
  (scooter CVT), freins avant/arrière séparés, fourche, amortisseur,
  contrôle technique (règles françaises 2 roues), etc. Catalogue vélo
  électrique : chaîne, freins, diagnostic santé batterie (SoH),
  connecteurs, firmware d'assistance, roulements, etc.
- **Pneus avant et arrière dissociés** dans les trois catalogues (voiture
  et vélo électrique — la moto l'était déjà) : ils s'usent et se
  remplacent rarement en même temps.
  ⚠️ Ce changement d'identifiant fait perdre la date de dernière
  intervention de l'ancien item "Pneumatiques (jeu complet)" au prochain
  renouvellement du plan — à ressaisir une fois pour les véhicules
  existants.
- **Icônes différenciées par type de véhicule** (🚗/🏍️/🛵/🚲) sur les
  tuiles et la fiche détail.
- **Robustesse de la génération IA améliorée** : re-tentative automatique
  aussi sur erreur 503 (surcharge serveur transitoire), pas seulement sur
  429 (quota).
- **Erreur de génération DIY affichée proprement** : un encart inline
  avec message clair et bouton "🔄 Réessayer", à la place d'une alerte
  système bloquante qui n'invitait pas explicitement à relancer.
- **Icône vectorielle (`icon.svg`)** ajoutée à la racine du dépôt, nette à
  n'importe quelle taille d'affichage — utilisée pour le README et
  inlinée directement dans le titre de la carte (remplace l'ancien PNG
  encodé en base64, plus lourd et moins net). Les fichiers
  `brand/icon.png` (48×48) et `brand/icon@2x.png` (96×96) ont aussi été
  mis à jour avec la nouvelle version, à leur taille native plutôt que
  surdimensionnés.

## 🛠️ v1.2.1 — autocomplétion motorisation adaptée par type de véhicule

- `vehicle_type`/`two_wheeler_type` transitent désormais jusqu'à
  `list_motorisations` (jusqu'ici seule la génération du plan les
  recevait) : le prompt et les exemples fournis à l'IA changent selon le
  type de véhicule plutôt qu'un format voiture générique appliqué à tout.
  - **Moto/scooter** : exemples au format du marché moto français, avec
    distinction explicite pleine puissance / bridée 35kW compatible
    permis A2 (ex : "MT-07 ABS" vs "MT-07 35kW (A2)").
  - **Vélo électrique** : le champ devient "Moteur d'assistance" plutôt
    que "Motorisation", suggestions au format moteur d'assistance (ex :
    "Bosch Performance Line CX 85Nm", "Shimano EP8").
  - **Voiture** : inchangé.
- Clé de cache des suggestions étendue en conséquence (le même
  marque/modèle/année ne partage plus son cache entre une recherche auto
  et une recherche moto, par exemple).

## 🛠️ v1.3.0 — l'encart d'un entretien ne se referme plus tout seul, référentiel marque/modèle enrichi

- **Correctif : un entretien déplié se repliait automatiquement**, par
  exemple juste après avoir cliqué sur "🔧 Comment le faire soi-même ?",
  obligeant à le rechercher plus haut dans la liste pour lire le conseil
  généré. Cause : chaque action (case "Applicable", enregistrement d'une
  intervention, génération DIY, ajustement d'échéance...) recharge les
  véhicules et reconstruit entièrement l'affichage, ce qui réinitialisait
  systématiquement tous les encarts `<details>` à l'état fermé — la carte
  ne gardait aucune mémoire de ce que l'utilisateur avait ouvert. La carte
  mémorise désormais quels entretiens sont dépliés et reproduit cet état à
  chaque rafraîchissement, quelle que soit l'action qui l'a déclenché.
  Cette même reconstruction complète de la liste (qui se retrie aussi par
  échéance la plus proche) est le mécanisme le plus probable derrière les
  signalements d'entretiens "masqués qui réapparaissent" ou de case à
  cocher "qui se décoche" après une action : l'encart concerné se
  refermait et la liste se retriait au même instant, donnant l'impression
  qu'un autre réglage venait de changer alors que la donnée réelle,
  elle, était correcte. La position de défilement de la liste est
  également restaurée après chaque rafraîchissement, pour éviter que la
  vue ne "saute" en haut de la liste à chaque action.
- **Référentiel marque/modèle enrichi et séparé par catégorie de
  véhicule** : le fichier `data/referentiel.json` ne comportait qu'une
  vingtaine de marques automobiles et aucune marque de deux-roues, alors
  qu'il est partagé par toutes les catégories depuis l'ajout du support
  moto/scooter/vélo électrique.
  - Ajout d'une soixantaine de marques automobiles supplémentaires
    (généralistes, premium et sportives) et enrichissement des gammes de
    modèles déjà présentes.
  - Ajout de catalogues marque/modèle dédiés pour les **motos** (18
    marques), les **scooters** (11 marques) et les **vélos électriques**
    (20 marques).
  - Le référentiel est désormais structuré par catégorie
    (`{"auto": {...}, "moto": {...}, "scooter": {...}, "velo_electrique":
    {...}}`) et la recherche marque/modèle (`search_referentiel`) filtre
    sur la catégorie du véhicule en cours de création : les suggestions
    d'une moto n'incluent plus jamais de marques automobiles, et
    inversement, à l'image de ce qui existait déjà pour les catalogues
    d'entretien.
  - Changer de type de véhicule ou de sous-type (auto ↔ 2 roues, moto ↔
    scooter ↔ vélo électrique) au formulaire d'ajout réinitialise
    désormais marque/modèle/motorisation, pour éviter de garder
    sélectionnée une marque qui n'existe plus dans la nouvelle catégorie.

## 🔍 v1.3.1 — logs de diagnostic pour le bug résiduel "entretiens masqués qui réapparaissent"

Version purement diagnostique : aucun changement de comportement, juste des
traces supplémentaires pour identifier précisément où l'état "applicable"
d'un entretien change de façon inattendue, dans le cas où le correctif de
la v1.3.0 (encart qui ne se referme plus, position de liste conservée) ne
suffirait pas à faire disparaître le symptôme pour de bon.

- **Logs HA (`_LOGGER.debug`)**, préfixés `[carnet_entretien DEBUG]` :
  - `get_vehicles` : à chaque rafraîchissement, l'état `applicable` /
    `applicable_override` / `statut` de tous les entretiens du plan, tel
    qu'envoyé à la carte.
  - `set_item_applicable` : le plan complet juste avant et juste après une
    bascule de case à cocher, pour repérer si un item *autre* que celui
    cliqué change lui aussi.
  - `log_maintenance` : l'item concerné avant/après l'enregistrement d'une
    intervention, plus l'état `applicable` de tout le plan après coup.
- **Logs navigateur (`console.debug`)**, préfixés `[CARnet DEBUG]`,
  filtrables dans la console (F12 → Console → filtre "CARnet DEBUG") :
  état du plan du véhicule sélectionné juste avant et juste après chaque
  bascule de case ou enregistrement d'intervention, avec le réglage
  `hide_not_applicable` en vigueur à cet instant.
- Objectif : comparer l'état stocké côté serveur (logs HA) et l'état reçu
  côté carte (logs navigateur) au moment précis où le symptôme apparaît,
  pour savoir s'il s'agit d'une vraie perte de donnée côté stockage ou
  d'un problème d'affichage/timing côté carte.

## 🛠️ v1.3.2 — correctif définitif : "entretiens masqués qui réapparaissent"

Cause identifiée grâce aux logs de diagnostic ajoutés en v1.3.1 (retirés
dans cette version, le nécessaire ayant été trouvé) : ce n'était ni un bug
d'affichage, ni un problème de tri de liste, mais un rejet silencieux côté
serveur.

- **Cause réelle** : le schéma de validation de la commande websocket
  `set_settings` ne déclarait que la clé `theme` comme acceptée. Or c'est
  cette même commande qui enregistre *tous* les réglages de la carte —
  y compris **le masquage des entretiens non applicables**
  (`hide_not_applicable`), les notifications, l'échelle de police et le
  rappel de kilométrage. Toute tentative d'enregistrer un réglage autre
  que le thème échouait donc systématiquement côté serveur avec l'erreur
  `extra keys not allowed`, visible uniquement dans la console développeur
  du navigateur — jamais signalée à l'écran.
  - La carte appliquait pourtant le changement **localement** dès le clic
    (affichage optimiste), donnant l'impression que ça avait fonctionné.
  - Mais rien n'était réellement enregistré : au rechargement suivant —
    déclenché par n'importe quelle action sur le plan (cocher/décocher un
    entretien, enregistrer une intervention...) — le réglage repartait de
    sa dernière valeur réellement sauvegardée, et les entretiens non
    applicables, jusque-là masqués, redevenaient visibles avec leur case
    "Applicable" logiquement décochée. C'est ce qui donnait l'impression
    trompeuse qu'un entretien "réapparaissait" et qu'une case "se
    décochait toute seule", alors qu'aucune donnée d'entretien n'était
    réellement perdue ni modifiée — seul le réglage d'affichage du
    masquage ne survivait jamais à l'enregistrement.
- **Correctif** : le schéma accepte désormais explicitement les cinq
  réglages existants (`hide_not_applicable`, `notifications_enabled`,
  `font_scale`, `mileage_reminder_enabled`, `mileage_reminder_days`), avec
  le bon type/validateur pour chacun.
- **Filet de sécurité ajouté en prime** : si un enregistrement de réglage
  échoue malgré tout à l'avenir (ex. panne réseau), la carte annule
  maintenant proprement l'affichage optimiste et montre une alerte
  explicite au lieu de laisser un réglage affiché comme actif sans jamais
  l'avoir réellement été.
- Les logs de diagnostic temporaires ajoutés en v1.3.1 (logs HA et
  console navigateur préfixés "DEBUG") sont retirés, la cause étant
  identifiée avec certitude.

## 🛠️ v1.3.3 — la génération DIY échouait sur tous les modèles Gemini (modèle 2.0 Flash arrêté par Google)

Signalé avec le message "Tous les modèles Gemini ont échoué — gemini-2.5-flash
[rate_limited]: Quota dépassé... ; gemini-2.0-flash [http_error]: Modèle
indisponible pour cette clé ; gemini-2.5-flash-lite [http_error]: Modèle
indisponible pour cette clé" lors d'une demande d'explication DIY (mais le
souci touchait potentiellement toutes les générations IA : plan, points de
vigilance, rappels, revente).

- **Cause** : `gemini-2.0-flash`, deuxième modèle de la cascade de repli,
  a été **définitivement arrêté par Google** — l'appel renvoie
  systématiquement une erreur HTTP 404, traduite par l'intégration en
  "Modèle indisponible pour cette clé". Placé en position intermédiaire,
  il faisait échouer toute la cascade dès que le premier modèle
  (`gemini-2.5-flash`) était temporairement à quota, empêchant le repli
  d'atteindre un modèle réellement disponible.
- **Correctif** : `gemini-2.0-flash` retiré de la liste. La cascade
  inclut désormais, dans l'ordre : `gemini-2.5-flash`,
  `gemini-2.5-flash-lite`, puis en repli supplémentaire les modèles de la
  génération courante `gemini-3.5-flash-lite`, `gemini-3.1-flash-lite` et
  `gemini-3.8-flash` (ce dernier plus capable mais plus coûteux, utilisé
  seulement si tout le reste échoue) — de quoi absorber un quota
  temporairement dépassé sur un modèle sans faire échouer toute la
  génération.
- Aucune action requise après la mise à jour : la cascade se réajuste
  automatiquement au prochain appel IA (génération de plan, DIY, points
  de vigilance, rappels, estimation de revente).

## 🌍 v1.4.0 — intégration multilingue (français, anglais, allemand, espagnol, italien)

Un seul réglage de langue pour toute l'installation (Réglages de la carte,
à côté du thème visuel) — pas un réglage par utilisateur HA : le contenu
généré par l'IA est mis en cache et partagé entre tous les viewers du
tableau de bord, donc une langue par personne n'aurait pas de sens.
Couvre tout ce qui est visible par l'utilisateur :

- **Interface de la carte** : 160 chaînes traduites (boutons, labels,
  formulaire d'ajout de véhicule, écran Réglages, statuts, badges DIY,
  messages de confirmation/erreur, étapes de chargement...) dans les 5
  langues. Nouveau sélecteur de langue dans Réglages (drapeaux
  🇫🇷🇬🇧🇩🇪🇪🇸🇮🇹), au même endroit que le sélecteur de thème.
- **Catalogue d'entretien** : les noms des 87 opérations (auto, moto/
  scooter, vélo électrique) sont traduits en anglais/allemand/espagnol/
  italien (`catalog_i18n.py`, nouveau fichier) et affichés dans la langue
  choisie — le français du catalogue source (`maintenance_catalog.py`)
  n'est pas dupliqué, c'est la référence utilisée telle quelle pour "fr".
- **Contenu généré par Gemini** : plan d'entretien (notes, raisons de non-
  applicabilité), points de vigilance, rappels constructeur, explications
  DIY et estimation de revente sont désormais demandés dans la langue
  choisie. Le cache par modèle (points de vigilance/rappels, mutualisé
  entre véhicules identiques) inclut maintenant la langue dans sa clé,
  pour ne jamais resservir un texte dans la mauvaise langue après un
  changement de réglage.
- **Notifications persistantes HA** (échéance dépassée, rappel de
  kilométrage) traduites, y compris le nom de l'entretien concerné.
- **Important** : changer de langue traduit instantanément l'interface et
  les noms d'opérations du catalogue (statiques), mais le contenu déjà
  généré par l'IA pour un véhicule existant (notes, points de vigilance,
  rappels, explications DIY, estimation de revente) reste dans la langue
  où il a été généré jusqu'à sa prochaine régénération (boutons
  "↻ Regénérer le plan" / rafraîchir les points de vigilance ou rappels /
  nouvelle demande DIY) — ce n'est régénéré automatiquement pour aucun
  véhicule existant afin de ne pas consommer de quota IA sans demande
  explicite.
- L'écran de configuration Home Assistant (ajout de l'intégration,
  options) suit toujours la langue du profil HA de chaque utilisateur
  (mécanisme natif HA, actuellement FR/EN) — c'est un réglage séparé de
  celui-ci, propre à Home Assistant, non couvert par ce changement.

---

