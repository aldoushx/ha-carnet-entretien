<p align="center"><img src="icon.png" width="96" height="96" alt="Icône CARnet - Garage Log" /></p>

# 🚗 CARnet - Garage Log — Home Assistant

**Carnet d'entretien automobile intelligent pour Home Assistant**, généré et
tenu à jour par **Google Gemini** : plan d'entretien constructeur, points de
vigilance connus, estimation de valeur de revente, et une carte Lovelace
dédiée avec quatre thèmes visuels au choix.

![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?logo=homeassistantcommunitystore&logoColor=white)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-41BDF5?logo=home-assistant&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-0.9.0-orange)

Architecture inspirée de [ha-millesime](https://github.com/Redsklns/ha-millesime)
(cave à vin gérée par IA) : stockage 100 % local, carte Lovelace auto-servie
(rien à copier dans `www/`), IA optionnelle avec repli manuel si aucune clé
n'est configurée.

> **État du projet** : fonctionnel et testé sur une instance personnelle,
> encore jeune (v0.7) — voir [CHANGELOG.md](CHANGELOG.md) pour l'historique
> et [Limites connues](docs/INSTALL.md#9-limites-connues--pistes-damélioration)
> avant un usage en production.

<!-- 📸 Capture d'écran de la carte à ajouter ici -->

## ✨ Fonctionnalités

- 🔍 **Ajout d'un véhicule en 30 secondes** : marque, modèle et motorisation
  avec autocomplétion intelligente (référentiel local + suggestions Gemini
  mises en cache), année, kilométrage, plaque, photo.
- 🛠️ **Plan d'entretien généré par IA** à partir de la documentation
  constructeur : chaque échéance avec intervalle km/mois, coût estimé,
  date prévisionnelle réelle (calculée sur le rythme kilométrique annuel du
  véhicule), et détection automatique des opérations non applicables
  (ex : pas de disques de frein arrière sur un véhicule à tambours).
- ⚠️ **Points de vigilance & pannes connues** spécifiques au modèle, avec
  gravité, coût indicatif et sources citées.
- 🚨 **Rappels constructeur actifs** recherchés par IA à la création,
  mutualisés par modèle et rafraîchissables, avec sources et avertissement
  à vérifier sur les canaux officiels.
- 🪪 **Reconnaissance de plaque VIN** à la création : une photo suffit à
  préremplir marque/modèle/année/motorisation (Gemini Vision).
- 💶 **Suivi de la valeur de revente** dans le temps, avec fourchette et
  raisonnement détaillé (tendance marché, décote, kilométrage).
- 📆 **Historique d'entretien horodaté** : chaque échéance se déplie pour
  enregistrer une intervention (bouton "fait aujourd'hui" ou date/km
  antérieurs), qui recalcule aussitôt les prochaines échéances.
- 🔗 **Kilométrage manuel ou lié à un capteur** existant de Home Assistant
  (odomètre constructeur, traceur OBD, `input_number`...).
- 🎨 **4 thèmes visuels** : Grand tourisme cuir, Manufacture horlogère,
  Carbone et titane, Atelier vintage — choix persistant via un panneau de
  réglages dédié.
- 🚙 **Multi-véhicules** avec sélecteur rapide et vue d'ensemble en tuiles.
- 🔧 **Services HA** pour tout piloter en automatisation (`add_vehicle`,
  `update_mileage`, `log_maintenance`, `value_snapshot`, `set_mileage_source`...).

## 🚀 Installation rapide

```text
HACS → ⋮ → Dépôts personnalisés → coller l'URL de ce dépôt → Intégration
→ Installer → redémarrer Home Assistant
→ Paramètres → Appareils et services → Ajouter une intégration → « Carnet d'entretien »
```

Guide complet, pas à pas, avec dépannage : **[docs/INSTALL.md](docs/INSTALL.md)**.

## 🔑 Clé Gemini

Optionnelle mais recommandée pour la génération automatique (plan, points de
vigilance, valeur, autocomplétion motorisation). Clé gratuite sur
[aistudio.google.com](https://aistudio.google.com). Sans clé, l'intégration
reste utilisable en saisie 100 % manuelle.

## 📄 Documentation

- [Guide d'installation et d'utilisation détaillé](docs/INSTALL.md)
- [Changelog](CHANGELOG.md)
- [Idées de fonctionnalités à venir](docs/IDEAS.md)
- [Publier des mises à jour via GitHub + HACS](docs/RELEASING.md)

## 🤝 Contribuer

Les retours, issues et pull requests sont les bienvenus — c'est un projet
jeune, taillé pour évoluer avec l'usage réel. Avant de proposer une
fonctionnalité, un coup d'œil à [docs/IDEAS.md](docs/IDEAS.md) pour voir si
elle y figure déjà.

## 📜 Licence

MIT — voir [LICENSE](LICENSE).
