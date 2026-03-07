# 🐍 CodeAcademy — Plateforme de Formation Python

## Installation

```bash
npm install
npm install vite@5 --save-dev   # si erreur crypto.hash
npm run dev
```

## Où placer vos fichiers de cours

Copiez vos notebooks (.ipynb) et fichiers (.md) dans :

```
public/courses/python/
├── debutant/          ← 17 notebooks (01_Introduction.ipynb, etc.)
├── intermediaire/     ← 11 notebooks
├── avance/            ← 11 fichiers
├── examens/           ← 7 fichiers .md
└── corrections/
    ├── projets/
    │   ├── 01_Projet_debutant/
    │   ├── 02_Projets_intermediaires/
    │   └── 03_Projet_avance/
    └── examens/       ← 6 notebooks CORRECTION
```

## Système de verrouillage

- Le **1er cours** de chaque module est **gratuit** (accessible sans code)
- Tous les autres cours sont **verrouillés**
- Bouton "Débloquer" en haut → code **** → tout est débloqué

## Configuration

Modifier `src/data/courseData.js` pour changer le code d'accès ou la liste des cours.
"# PythonAcademy" 
