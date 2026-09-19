# Changelog

Historique des versions de l'intégration Carnet d'entretien.

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

---

