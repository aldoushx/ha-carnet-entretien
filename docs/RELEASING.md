# De ce dossier à un dépôt GitHub avec mises à jour via HACS

[← Retour au README](../README.md)

Ce tuto couvre tout le cycle : création du dépôt, première release, puis
le workflow que vous répéterez à chaque nouvelle version que je vous
fournis. Dépôt cible : **https://github.com/aldoushx/ha-carnet-entretien**

---

## 0. Pré-requis

- `git` installé sur votre machine.
- Le dépôt GitHub `aldoushx/ha-carnet-entretien` déjà créé (vide, sans
  README auto-généré si possible, pour éviter un conflit à la première
  synchronisation).
- Optionnel mais pratique : [GitHub CLI](https://cli.github.com/) (`gh`),
  pour créer les releases en une commande plutôt que depuis l'interface web.

---

## 1. Préparer le dossier local

Vous devez avoir exactement cette structure à la racine (c'est déjà le cas
dans l'archive fournie) :

```
ha-carnet-entretien/
  hacs.json                 ← DOIT être à la racine, pas ailleurs
  README.md
  LICENSE
  CHANGELOG.md
  icon.png                  ← icône pour le README / la page GitHub (repli)
  icon.svg                  ← version vectorielle, à privilégier
  badge.svg                 ← illustration d'en-tête du README
  docs/
  custom_components/
    carnet_entretien/
      manifest.json          ← la version ("version": "x.y.z") vit ici
      brand/                 ← icône affichée DANS Home Assistant (§7)
        icon.png
        icon@2x.png
      __init__.py
      ...
```

Vérifiez notamment que `hacs.json` est bien au même niveau que le dossier
`custom_components/`, pas dedans (c'est l'erreur qui vous bloquait).

---

## 2. Initialiser le dépôt Git local

Dans le dossier extrait de l'archive :

```bash
cd ha-carnet-entretien
git init
git add .
git commit -m "Version initiale — 1.0.0"
```

Si vous n'avez pas encore configuré Git sur cette machine :

```bash
git config --global user.name "Votre nom"
git config --global user.email "votre@email.com"
```

---

## 3. Lier au dépôt GitHub et pousser

```bash
git branch -M main
git remote add origin https://github.com/aldoushx/ha-carnet-entretien.git
git push -u origin main
```

Si GitHub demande une authentification : utilisez un
[token d'accès personnel](https://github.com/settings/tokens) (classic,
scope `repo`) comme mot de passe, ou configurez `gh auth login` si vous
utilisez GitHub CLI.

À ce stade, tous les fichiers sont visibles sur GitHub mais **HACS ne
détecte pas encore de mise à jour disponible** : il lui faut une *release*
taguée.

---

## 4. Créer la première release

Le tag doit correspondre à la version du `manifest.json`
(`custom_components/carnet_entretien/manifest.json`, champ `"version"`),
précédé de `v`. Actuellement : **`v1.0.0`**.

### Option A — Interface GitHub

1. Sur la page du dépôt → **Releases** (colonne de droite) → **Create a
   new release** (ou **Draft a new release**).
2. **Choose a tag** → tapez `v1.0.0` → **Create new tag on publish**.
3. **Release title** : `v1.0.0`.
4. **Description** : collez le contenu de la section correspondante de
   `CHANGELOG.md`.
5. **Publish release**.

### Option B — GitHub CLI

```bash
gh release create v1.0.0 --title "v1.0.0" --notes-file CHANGELOG.md
```

(`--notes-file CHANGELOG.md` colle tout le changelog ; pour ne coller que
la section de cette version, extrayez-la dans un fichier temporaire avant,
ou utilisez `--notes "..."` directement.)

---

## 5. Ajouter le dépôt dans HACS (première fois)

1. Home Assistant → **HACS** → menu **⋮** (en haut à droite) →
   **Dépôts personnalisés**.
2. URL : `https://github.com/aldoushx/ha-carnet-entretien`
   Catégorie : **Intégration**.
3. **Ajouter**.
4. Recherchez **"CARnet - Garage Log"** dans HACS → **Télécharger** →
   redémarrez Home Assistant.

Une fois que vous soumettrez éventuellement le dépôt à l'annuaire officiel
HACS (facultatif, processus de validation à part), cette étape 5 ne sera
plus nécessaire pour les autres utilisateurs — mais reste nécessaire pour
vous tant que ce n'est qu'un dépôt personnalisé.

---

## 6. Workflow de mise à jour (à chaque nouvelle version que je vous donne)

À chaque fois que je vous fournis une archive mise à jour :

```bash
# 1. Remplacez les fichiers modifiés dans votre dossier local
#    (copier/écraser depuis la nouvelle archive)

# 2. Vérifiez que le numéro de version a bien changé
grep version custom_components/carnet_entretien/manifest.json

# 3. Committez et poussez
git add .
git commit -m "v0.9.1 — description courte du changement"
git push

# 4. Créez la release correspondante
gh release create v0.9.1 --title "v0.9.1" --notes "Voir CHANGELOG.md"
#    (ou via l'interface GitHub, comme à l'étape 4)
```

**C'est l'étape 4 (la release taguée) qui déclenche la détection par
HACS** — un simple `git push` sans release ne suffit pas à faire
apparaître une mise à jour dans l'interface HACS. Une fois la release
publiée :

5. Dans Home Assistant → **HACS** → l'intégration affiche un badge de
   mise à jour → **Mettre à jour** → redémarrer Home Assistant.

---

## 7. Icône du dépôt et de l'intégration

Trois fichiers, trois usages différents :

**`icon.svg`** (vectoriel) sert au README/à la page GitHub du dépôt — net à
n'importe quelle taille d'affichage, à privilégier partout où le format est
accepté (GitHub le rend nativement dans le README via `<img>`). `icon.png`
reste présent à la racine en repli pour les contextes qui n'acceptent pas
le SVG.

**`custom_components/carnet_entretien/brand/`** (`icon.png` 48×48 et
`icon@2x.png` 96×96 — tailles volontairement natives plutôt que
surdimensionnées, pour un rendu net sans mise à l'échelle à ces
résolutions précises d'affichage dans HA) est le mécanisme qui affiche
réellement l'icône dans Home Assistant, depuis la version **2026.3** :
les intégrations personnalisées peuvent désormais embarquer leurs propres
images de marque directement dans ce dossier, servies via
`/api/brands/integration/carnet_entretien/icon.png`. Plus besoin de PR
vers `home-assistant/brands` (ce dépôt n'accepte d'ailleurs plus les
nouvelles soumissions d'intégrations tierces depuis ce changement) — rien
à faire de plus, l'icône est incluse dans chaque release comme n'importe
quel autre fichier. Le SVG n'est pas utilisable ici : ce mécanisme HA
attend des PNG.

Cette icône s'affiche correctement dans Paramètres → Appareils et
services, sur la page de l'intégration et sur les fiches d'appareils.
**Limite connue** : la vignette dans la **liste de HACS elle-même** peut
continuer à afficher "icon not available" même quand tout le reste
fonctionne — HACS a un bug ouvert (interface encore basée sur l'ancien
CDN `brands.home-assistant.io` plutôt que sur le nouveau proxy local) qui
ne dépend pas de ce dépôt et devrait se résoudre avec une future mise à
jour du frontend HACS.

---

## 8. Bonnes pratiques pour la suite

- Toujours bumper `version` dans `manifest.json` avant de tagger — HACS
  s'en sert pour savoir qu'une mise à jour existe.
- Une entrée `CHANGELOG.md` par version (déjà en place) : réutilisable
  telle quelle comme description de release.
- Convention de tag : `vMAJOR.MINOR.PATCH` (semver), toujours avec le `v`
  devant, cohérent avec `manifest.json` sans le `v`.
- Si une mise à jour ne remonte pas dans HACS après une release : forcez
  un **"Redécouvrir"** depuis HACS (menu ⋮ → Redécouvrir), ou vérifiez que
  le tag correspond bien à une *release* publiée (pas juste un tag Git nu
  — HACS lit les releases, pas les tags seuls, sauf configuration
  spécifique).
