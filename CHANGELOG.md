# Changelog

Toutes les modifications notables de **CARnet - Garage Log**, depuis la
version 1.4.2. Une section par version : elle peut être collée telle quelle
dans la description d'une release GitHub (voir `docs/RELEASING.md`).

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [1.11.1] — Recherche IA des consommables ciblée

### Modifié
- **Recherche IA restreinte aux consommables cochés** : chaque ligne de
  l'onglet Références a maintenant une case à cocher « à inclure dans la
  recherche IA ». Le bouton ne recherche plus que ce qui est explicitement
  coché (y compris un libellé personnalisé), au lieu de laisser l'IA
  choisir elle-même sa liste — ce qui pouvait faire remonter des
  consommables non désirés tout en en oubliant d'autres. Cliquer sur une
  suggestion l'ajoute à la liste et la coche automatiquement.
- **Valeurs génériques plutôt que références fabricant** : le prompt
  demande désormais explicitement des caractéristiques et normes
  utilisables pour acheter un équivalent générique en magasin (viscosité et
  norme d'huile, dimensions de pneus, type et protection du liquide de
  refroidissement, capacité et ampérage de batterie...), plutôt qu'une
  référence catalogue propre à un équipementier.
- Le cache des suggestions tient maintenant compte des libellés
  explicitement demandés, plus seulement du véhicule.

## [1.11.0] — Dossier configurable et suggestions IA des consommables

### Ajouté
- **Dossier de stockage des factures configurable**, dans les réglages :
  un chemin absolu personnalisé (ex. un partage réseau monté dans Home
  Assistant), validé contre `allowlist_external_dirs` avant d'être
  enregistré. Vide = dossier par défaut (`config/carnet_entretien_files`).
  Les factures déjà envoyées ne sont pas déplacées automatiquement lors
  d'un changement de dossier.
- **Suggestion des références de consommables par IA** (bouton
  « ✨ Suggérer via IA » dans l'onglet Références) : propose des références
  adaptées à la marque, au modèle, à la motorisation et à l'énergie du
  véhicule (huile, pneus, liquides, bougies...), sur le même principe que
  la recherche de motorisation à la création d'un véhicule. Résultat mis
  en cache par véhicule/motorisation pour ne pas re-consommer de quota à
  chaque clic. Les suggestions s'ajoutent au brouillon sans écraser les
  lignes déjà saisies ni créer de doublon.

### Modifié
- PDF d'export : les colonnes **Garage** et **Coût** du tableau
  d'historique sont retirées, remplacées par une colonne **Commentaire**.
  Ces deux champs sont utilisables via le service Home Assistant
  `log_maintenance` (automatisations) mais n'ont aucun formulaire dans la
  carte : elles restaient donc presque toujours vides.

## [1.10.0] — Rappels saisonniers

### Ajouté
- **Rappels saisonniers** : une notification persistante par véhicule à
  chaque changement de saison (printemps, été, automne, hiver), avec une
  liste de points à vérifier adaptée au type de véhicule : voiture
  thermique, hybride, électrique, moto, scooter ou vélo électrique.
- Contenu disponible dans les 5 langues de l'intégration (fr, en, de, es, it).
- Interrupteur **Rappels saisonniers** dans les réglages de la carte,
  **activé par défaut**.
- Saisons météorologiques (mars-mai, juin-août, septembre-novembre,
  décembre-février), inversées automatiquement si la latitude de Home
  Assistant est dans l'hémisphère sud.
- Nouveau module `seasonal_reminders.py`.

### Notes de mise à jour
- Au premier redémarrage après la mise à jour, chaque véhicule reçoit la
  notification de la saison en cours.
- La notification n'est créée qu'une fois par saison : fermée, elle ne
  revient pas avant la saison suivante. Désactiver l'interrupteur retire les
  notifications en cours, et le réactiver en cours de saison les ramène.

## [1.9.0] — Références des consommables

### Ajouté
- Nouvel onglet **🛢️ Références** sur la fiche du véhicule : références
  exactes des consommables (type d'huile, pneus, filtres, liquide de
  refroidissement, etc.), en saisie libre libellé / valeur.
- Suggestions de libellés en un clic, selon le type de véhicule (voiture
  thermique ou électrique, moto, scooter, vélo électrique), traduites dans
  les 5 langues.
- Les références figurent sur la première page du PDF d'export.

### Corrigé
- PDF d'export : le texte saisi (intervention, garage, notes, références)
  est désormais échappé, un `&` ou un `<` pouvait faire échouer la
  génération.

## [1.8.0] — Export PDF

### Ajouté
- Bouton **📄 Générer un PDF** dans l'onglet Historique : page de garde,
  tableau chronologique de l'historique complet, puis les factures liées
  en annexe (PDF fusionnés tels quels, photos converties en pages PDF).
- Numéro de version de la carte affiché en bas de la page de réglages, pour
  vérifier qu'il s'agit bien de la dernière version, notamment dans l'app
  Companion où le cache est moins évident à vider.
- Nouveau module `history_pdf.py` et nouvelle vue HTTP authentifiée
  `/api/carnet_entretien/history_pdf/{vehicle_id}`.

### Modifié
- L'historique est trié explicitement par date décroissante (le plus récent
  en premier), et non plus par ordre de saisie inversé.

### Notes de mise à jour
- Nouvelles dépendances Python déclarées dans `manifest.json` : `reportlab`,
  `pypdf` et `Pillow`. Home Assistant les installe automatiquement : le
  premier redémarrage peut être plus long que d'habitude.

## [1.7.1] — Prise de photo directe

### Corrigé
- Le bouton « Prendre une photo » des factures ouvrait Google Photos et non
  l'appareil photo dans l'app Companion Android (l'attribut HTML `capture`
  n'y est pas respecté). La carte ouvre maintenant un flux caméra en direct
  intégré (plein écran, bouton de déclenchement, annulation).
- Repli automatique sur l'ancien sélecteur de fichier si l'accès direct à la
  caméra est indisponible (refus d'autorisation, ou Home Assistant servi en
  `http://` : `getUserMedia` exige un contexte sécurisé HTTPS).

## [1.7.0] — Corrections de la v1.6

### Ajouté
- Suppression d'une intervention de l'historique (icône 🗑️), avec recalcul
  de la prochaine échéance de l'entretien concerné à partir de ce qu'il
  reste dans l'historique.
- Lien d'une facture existante à une intervention déjà enregistrée, depuis
  l'onglet Historique (« 🧾 Lier une facture existante »).
- Boutons distincts « 📷 Prendre une photo » et « 📎 Importer un fichier »
  dans l'onglet Factures.

### Modifié
- Les deux thèmes « Home Assistant clair » et « Home Assistant nuit »
  étaient un doublon exact (tous deux suivent le thème courant de Home
  Assistant) : ils sont fusionnés en un seul thème **Home Assistant (thème
  courant)**. Le choix précédent est migré automatiquement.

### Corrigé
- Ouverture d'une facture : erreur `401: Unauthorized`. Les fichiers sont
  maintenant récupérés par une requête authentifiée (`fetchWithAuth`) puis
  ouverts dans un onglet, avec repli sur un téléchargement si le
  navigateur bloque l'ouverture.
- La prochaine échéance d'un entretien se basait sur la dernière intervention
  saisie et non sur la plus récente : elle est maintenant recalculée à partir
  de l'entrée la plus récente de l'historique (ce qui corrige aussi la saisie
  a posteriori d'une date antérieure).

## [1.6.0] — Factures

### Ajouté
- Nouvel onglet **🧾 Factures** par véhicule : envoi de PDF ou d'images,
  intitulé facultatif, suppression.
- Fichiers stockés sur disque, un dossier par véhicule
  (`config/carnet_entretien_files/<véhicule>/`), nommés
  `AAAA-MM-JJ_nom-du-fichier_id.ext`, limités à 10 Mo. Seule la métadonnée
  est conservée dans le stockage de l'intégration.
- Fichiers servis par une vue HTTP authentifiée
  (`/api/carnet_entretien/invoice/{id}`) et non par un chemin statique
  public.
- Liaison d'une ou plusieurs factures à une intervention, à sa saisie
  (formulaire simple et « entretiens multiples »), avec affichage en puces
  dans l'historique et possibilité de délier.
- Nouveau module `invoices.py`, nouvelles commandes websocket
  `add_invoice`, `remove_invoice` et `set_log_entry_invoices`.

### Modifié
- Supprimer une facture la détache des interventions qui la référençaient ;
  supprimer un véhicule supprime son dossier de factures.

### Corrigé
- Les thèmes « Home Assistant » introduits en 1.5.0 n'étaient pas acceptés
  par la validation du backend et ne pouvaient pas être enregistrés.

## [1.5.0] — Thèmes, commentaires et entretiens multiples

### Ajouté
- Deux thèmes graphiques « Home Assistant » (clair et nuit), reprenant les
  variables de couleur du thème Home Assistant actif (fusionnés en un seul
  en 1.7.0).
- Champ **commentaire** facultatif sur chaque intervention (par exemple
  « essuie-glaces vérifiés », « pneu avant remplacé après crevaison »),
  saisissable dans tous les formulaires d'enregistrement et affiché dans
  l'historique.
- **Entretiens multiples** : mode de sélection pour cocher plusieurs
  échéances réalisées lors d'un même passage au garage et les enregistrer en
  une fois, avec une date, un kilométrage et un commentaire communs.

## [1.4.2] — Version de départ

Point de départ de ce changelog. Pour l'historique antérieur, voir les
tags et les releases du dépôt.
