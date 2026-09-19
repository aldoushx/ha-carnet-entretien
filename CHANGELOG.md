# Changelog

Historique des versions de l'intégration Carnet d'entretien.

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
- **README recentré sur l'utilisateur final** : les liens vers
  `docs/IDEAS.md` (roadmap) et `docs/RELEASING.md` (workflow de
  publication, usage interne au mainteneur) ont été retirés du README
  public — les fichiers restent dans le dépôt mais ne sont plus mis en
  avant.

---

