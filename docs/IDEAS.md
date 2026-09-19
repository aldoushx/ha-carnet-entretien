# Idées de fonctionnalités à venir

[← Retour au README](../README.md)

Pistes d'évolution inspirées d'applications de référence en gestion
automobile (Fuelio, Drivvo, Simply Auto, myCarfax, CARFAX Canada...).
Celles non cochées sont de simples propositions à discuter/prioriser en
issue avant tout développement.

## ✅ Déjà implémenté

- **Vérification des rappels constructeur actifs** *(v0.8)* — panneau
  dédié, généré par IA, mutualisé par modèle.
- **Reconnaissance photo de plaque VIN** *(v0.8)* — préremplissage du
  formulaire d'ajout via Gemini Vision.

## À venir (non implémenté)

### 1. Suivi carburant & consommation
*Inspiré de Fuelio, Drivvo.*
Journal des pleins (litres, prix/L, plein complet ou non) → consommation
moyenne (L/100 km) calculée automatiquement, courbe de tendance, coût par
km roulé. Se combine naturellement avec l'historique de kilométrage déjà
suivi par le carnet.

### 2. Tableau de bord "coût total de possession"
*Inspiré des rapports Drivvo/Fuelio.*
Cumul entretien + carburant (si #1 implémenté) + assurance saisie
manuellement − décote (déjà suivie) = coût réel par kilomètre parcouru,
utile pour comparer plusieurs véhicules ou décider d'une revente.

### 3. Échéances administratives (assurance, contrôle technique, Crit'Air)
*Inspiré des rappels myCarfax/aCar.*
Un type d'échéance "document" à côté de l'entretien mécanique : date
d'expiration d'assurance, prochain contrôle technique, vignette Crit'Air —
avec upload photo du document, sur le même modèle que la photo véhicule
déjà en place.

### 4. Multi-conducteurs / partage du véhicule
*Inspiré de Simply Auto "family sharing".*
Associer une intervention ou un relevé de kilométrage à un conducteur du
foyer, utile pour les véhicules partagés — qui a fait le plein, qui a
conduit récemment.

### 5. Export PDF du carnet d'entretien
*Le carnet papier traditionnel, numérisé.*
Génération d'un PDF présentable (historique complet, plan, points de
vigilance) — utile à imprimer ou à joindre à une annonce de vente, en
partant du même style visuel (cuir/thème choisi) que la carte.

### 6. Rappel saisonnier pneus été/hiver
*Inspiré des rappels saisonniers d'aCar.*
Une échéance "spéciale" déclenchée par date calendaire (pas km) pour le
changement de pneus, avec un texte adapté à la région si la géolocalisation
HA est disponible.

### 7. Historique de devis comparés
*Inspiré des comparateurs de devis des plateformes de réparation.*
Pour une grosse réparation à venir, enregistrer plusieurs devis reçus
(garage, montant, date) avant de choisir — conservés dans l'historique une
fois l'intervention réalisée.

### 8. Partage en lecture seule du carnet (façon rapport Carfax)
Générer un lien (ou export) consultable par un acheteur potentiel sans accès
à l'instance Home Assistant complète — transparence à la revente, à
l'image d'un rapport d'historique véhicule.

---

Une suggestion à ajouter ? Ouvrez une issue plutôt qu'une pull request
directe pour en discuter d'abord — certaines de ces pistes (le PDF, le
multi-conducteurs) changent la structure de données et méritent d'être
cadrées avant implémentation.
