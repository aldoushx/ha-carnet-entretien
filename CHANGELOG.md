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

---

