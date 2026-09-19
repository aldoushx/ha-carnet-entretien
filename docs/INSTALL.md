# Guide d'installation et d'utilisation détaillé

[← Retour au README](../README.md)

## 1. Pré-requis

- Home Assistant 2024.1 ou plus récent.
- (Optionnel mais recommandé) Une clé API Gemini gratuite sur
  [aistudio.google.com](https://aistudio.google.com) — sans clé, vous
  pouvez toujours créer des véhicules et remplir le carnet à la main, mais
  sans génération automatique du plan, des points de vigilance ni de
  l'estimation de valeur.
- HACS installé si vous voulez la voie "dépôt personnalisé" (sinon,
  installation manuelle, tout aussi simple).

---

## 2. Installation

### Option A — HACS (dépôt personnalisé)

1. Poussez ce dossier tel quel dans un nouveau dépôt GitHub public
   (structure attendue : `custom_components/carnet_entretien/...` à la
   racine du dépôt, comme ici).
2. Dans HACS → ⋮ (menu en haut à droite) → **Dépôts personnalisés**.
3. Collez l'URL de votre dépôt, catégorie **Intégration**.
4. Recherchez "Carnet d'entretien" dans HACS, installez, puis
   **redémarrez Home Assistant**.

### Option B — Installation manuelle

1. Copiez le dossier `custom_components/carnet_entretien/` tel quel dans
   `config/custom_components/` de votre installation Home Assistant
   (via Samba, SSH, ou l'add-on File Editor).
2. Vérifiez l'arborescence obtenue :
   ```
   config/
     custom_components/
       carnet_entretien/
         __init__.py
         config_flow.py
         const.py
         gemini_client.py
         manifest.json
         sensor.py
         services.yaml
         storage.py
         utils.py
         strings.json
         translations/
         data/referentiel.json
         www/carnet-entretien-card.js
   ```
3. **Redémarrez Home Assistant** (Paramètres → Système → Redémarrer).

---

## 3. Configuration de l'intégration

1. **Paramètres → Appareils et services → Ajouter une intégration**.
2. Cherchez **Carnet d'entretien**.
3. Renseignez votre clé Gemini si vous en avez une (champ optionnel,
   laissez vide sinon — vous pourrez l'ajouter plus tard via ⚙️ sur
   l'intégration, dans les Options).
4. Validez. Aucun appareil/entité n'apparaît encore : ils sont créés au
   fur et à mesure que vous ajoutez des véhicules via la carte.

---

## 4. Ajouter la carte au tableau de bord

La ressource JS est **enregistrée automatiquement** au démarrage de
Home Assistant (comme pour ha-millesime) — vous n'avez rien à déclarer
dans Paramètres → Tableaux de bord → Ressources.

1. Ouvrez un tableau de bord → **Modifier le tableau de bord** →
   **Ajouter une carte** → cherchez **"Carnet d'entretien"** dans la
   liste (ou choisissez "Manuel" et collez le YAML ci-dessous).
2. YAML minimal :
   ```yaml
   type: custom:carnet-entretien-card
   ```

Si la carte n'apparaît pas dans la liste après installation, forcez un
rechargement complet du cache du navigateur (Ctrl+Maj+R / Cmd+Maj+R),
la ressource porte un paramètre de version basé sur la date de
modification du fichier pour éviter le cache normalement, mais certains
navigateurs mobiles sont plus agressifs.

---

## 5. Premier usage

1. Cliquez **➕ Ajouter** sur la carte.
2. **Marque** : tapez les premières lettres, une liste déroulante
   d'autocomplétion apparaît (référentiel local, éditable — voir §7).
   Vous pouvez aussi taper une marque absente de la liste : la saisie
   libre est toujours acceptée.
3. **Modèle** : la liste se filtre selon la marque choisie, même
   principe de saisie libre en repli.
4. Renseignez motorisation (facultatif), année, kilométrage actuel,
   immatriculation (facultatif).
5. Validez : trois étapes de génération s'enchaînent (info constructeur
   → plan d'entretien → points de vigilance), 15 à 45 secondes selon
   la charge de l'API Gemini.
6. Vous arrivez sur la fiche véhicule avec 4 onglets :
   - **🔧 Entretien** : échéances triées par urgence, avec barre de
     progression et bouton "✓ Fait" pour enregistrer une intervention.
   - **⚠️ Points de vigilance** : pannes connues sur ce modèle précis,
     par gravité, avec bandeau d'avertissement (synthèse IA, pas une
     donnée constructeur certifiée).
   - **💶 Valeur** : bouton "Estimer maintenant" → courbe de valeur de
     revente dans le temps, à relancer périodiquement (manuellement, ou
     via automatisation avec le service `value_snapshot`).
   - **📓 Historique** : journal des interventions.

---

## 6. Automatiser avec les services

Tous les services sont visibles dans **Outils de développement →
Actions**, préfixés `carnet_entretien.`. Exemples :

**Rappel hebdomadaire d'estimation de valeur** (`automations.yaml`) :
```yaml
alias: Estimation valeur véhicules - hebdo
trigger:
  - platform: time
    at: "08:00:00"
condition:
  - condition: time
    weekday: [mon]
action:
  - service: carnet_entretien.value_snapshot
    data:
      vehicle_id: "VOTRE_ID_VEHICULE"
```

**Notification quand une échéance est due** — utilisez directement le
capteur `sensor.<marque>_<modele>_prochaine_echeance`, attribut `statut` :
```yaml
alias: Alerte entretien véhicule
trigger:
  - platform: state
    entity_id: sensor.peugeot_308_prochaine_echeance
    attribute: statut
    to: "echue"
action:
  - service: notify.mobile_app_votre_telephone
    data:
      message: >
        Échéance dépassée sur la 308 : {{ state_attr('sensor.peugeot_308_prochaine_echeance','km_restants') }} km de retard.
```

L'`id` de chaque véhicule est visible dans les attributs de ses capteurs
ou en interrogeant le websocket `carnet_entretien/get_vehicles` depuis
Outils de développement → WebSocket (si vous avez cet outil), ou plus
simplement en cliquant sur le véhicule dans la carte puis en inspectant
l'appareil correspondant dans Paramètres → Appareils.

---

## 7. Personnaliser le référentiel marques/modèles

Le fichier `custom_components/carnet_entretien/data/referentiel.json`
contient une liste volontairement compacte (marques les plus courantes
en France). Pour l'enrichir :

```json
{
  "VotreMarque": ["Modèle A", "Modèle B"],
  "Peugeot": ["208", "2008", "308", "...", "Nouveau modèle"]
}
```

Redémarrez Home Assistant après modification (le fichier est chargé une
fois au démarrage de l'intégration). La saisie libre reste toujours
possible même pour un modèle absent du fichier.

---

## 8. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| "no_model" à l'ajout d'un véhicule | Pas de clé Gemini configurée, ou clé invalide | Renseignez/vérifiez la clé dans Options de l'intégration |
| "timeout" | API Gemini lente ou surchargée | Réessayez ; le bouton "↻ Regénérer" relance l'appel |
| "truncated" | Réponse coupée par la limite de tokens | Déjà anticipé par des budgets larges (3072 tokens) ; si ça persiste, réduisez le nombre d'items demandés dans `gemini_client.py` |
| La carte n'apparaît pas | Cache navigateur | Rechargement forcé (Ctrl+Maj+R) |
| Capteurs manquants après suppression d'un véhicule | Normal transitoire | Ils sont retirés du registre automatiquement au retrait |

---

## 9. Limites connues / pistes d'amélioration

- **Référentiel marques/modèles minimal** : à étoffer selon vos besoins
  (voir §7), ou à remplacer par un appel à une base ouverte type
  data.gouv.fr / API immatriculation si vous voulez l'automatiser.
- **Estimation de kilométrage annuel** : utilisée pour classer les
  échéances entre elles (`utils.py`), basée sur l'historique de
  kilométrage du véhicule ; peu fiable tant que peu de points de mesure
  existent (valeur par défaut 12 000 km/an en attendant).
- **Pas de scan de carte grise / photo** (contrairement au scan
  d'étiquette de ha-millesime) : pourrait être ajouté en réutilisant le
  même pattern (image en base64 envoyée à Gemini Vision) si utile.
- **Suppression d'entités** : gérée via le registre HA ; à tester
  spécifiquement sur votre version de Home Assistant, les API de
  registre évoluent parfois d'une version à l'autre.
- **Pas de tests automatisés** inclus dans ce squelette — à ajouter
  (pytest + `pytest-homeassistant-custom-component`) avant toute
  publication HACS large.

---

## 10. Licence

MIT — voir [LICENSE](LICENSE).
