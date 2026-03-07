export const UNLOCK_CODE = "Python24";

const BASE = "/courses/python";

export const formations = [
  {
    id: "python",
    title: "Python",
    subtitle: "De débutant à expert",
    description: "Maîtrisez Python de A à Z avec des cours progressifs, des exercices pratiques et des projets concrets.",
    available: true,
    levels: ["debutant", "intermediaire", "avance"],
  },
  {
    id: "machine-learning",
    title: "Machine Learning",
    subtitle: "Intelligence Artificielle & Data Science",
    description: "Apprenez les fondamentaux du Machine Learning, du Deep Learning et de la Data Science.",
    available: false,
  },
];

export const pythonLevels = [
  { id: "debutant",      title: "Débutant",       subtitle: "Les fondamentaux de Python",   folder: "debutant",      image: "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=700&q=80" },
  { id: "intermediaire", title: "Intermédiaire",  subtitle: "Concepts avancés & modules",   folder: "intermediaire", image: "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=700&q=80" },
  { id: "avance",        title: "Avancé",          subtitle: "Maîtrise & performance",       folder: "avance",        image: "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=700&q=80" },
  { id: "examens",       title: "Examens",         subtitle: "Testez vos connaissances",     folder: "examens",       image: "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=700&q=80" },
  { id: "corrections",   title: "Corrections",     subtitle: "Projets & examens corrigés",   folder: "corrections",   image: "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=700&q=80" },
];

export const debutantCourses = [
  { id: 1,  filename: "01_Introduction.ipynb",                 title: "Introduction",                  duration: "30 min" },
  { id: 2,  filename: "02_Variables et types de donnees.ipynb", title: "Variables et types de données", duration: "45 min" },
  { id: 3,  filename: "03_Operations et expressions.ipynb",     title: "Opérations et expressions",     duration: "40 min" },
  { id: 4,  filename: "04_Les conditions.ipynb",                title: "Les conditions",                duration: "35 min" },
  { id: 5,  filename: "05_Structure match_case.ipynb",          title: "Structure match/case",          duration: "30 min" },
  { id: 6,  filename: "06_Les boucles.ipynb",                   title: "Les boucles",                   duration: "45 min" },
  { id: 7,  filename: "07_Les listes.ipynb",                    title: "Les listes",                    duration: "50 min" },
  { id: 8,  filename: "08_Les tuples.ipynb",                    title: "Les tuples",                    duration: "30 min" },
  { id: 9,  filename: "09_Les ensembles.ipynb",                 title: "Les ensembles",                 duration: "35 min" },
  { id: 10, filename: "10_Les dictionnaires.ipynb",             title: "Les dictionnaires",             duration: "45 min" },
  { id: 11, filename: "11_Gestion des fichiers.ipynb",          title: "Gestion des fichiers",          duration: "40 min" },
  { id: 12, filename: "12_Les fonctions.ipynb",                 title: "Les fonctions",                 duration: "50 min" },
  { id: 13, filename: "13_Docstrings.ipynb",                    title: "Docstrings",                    duration: "25 min" },
  { id: 14, filename: "14_Structurer son code.ipynb",           title: "Structurer son code",           duration: "35 min" },
  { id: 15, filename: "15_PEP8.ipynb",                          title: "PEP8",                          duration: "30 min" },
  { id: 16, filename: "16_Les modules de base.ipynb",           title: "Les modules de base",           duration: "40 min" },
  { id: 17, filename: "17_Projet.ipynb",                        title: "Projet",                        duration: "60 min" },
];

export const intermediaireCourses = [
  { id: 1,  filename: "01_POO.ipynb",                        title: "Programmation Orientée Objet",  duration: "60 min" },
  { id: 2,  filename: "02_Programmation_fonctionnelle.ipynb", title: "Programmation fonctionnelle",   duration: "45 min" },
  { id: 3,  filename: "03_Gerer les exceptions.ipynb",       title: "Gérer les exceptions",          duration: "35 min" },
  { id: 4,  filename: "04_Portee des variables.ipynb",       title: "Portée des variables",          duration: "30 min" },
  { id: 5,  filename: "05_Recursivite.ipynb",                title: "Récursivité",                   duration: "45 min" },
  { id: 6,  filename: "06_Module collections.ipynb",         title: "Module collections",            duration: "40 min" },
  { id: 7,  filename: "07_Module itertools.ipynb",           title: "Module itertools",              duration: "35 min" },
  { id: 8,  filename: "08_Module Logging.ipynb",             title: "Module Logging",                duration: "30 min" },
  { id: 9,  filename: "09_Module re.ipynb",                  title: "Module re (Regex)",             duration: "45 min" },
  { id: 10, filename: "10_Module_resquests.ipynb",           title: "Module requests",               duration: "40 min" },
  { id: 11, filename: "12_Projets.ipynb",                    title: "Projets",                       duration: "90 min" },
];

export const avanceCourses = [
  { id: 1,  filename: "01_Tests_unitaires.ipynb",          title: "Tests unitaires",           duration: "45 min" },
  { id: 2,  filename: "02_Decorateurs.ipynb",              title: "Décorateurs",               duration: "50 min" },
  { id: 3,  filename: "03_Generateurs.ipynb",              title: "Générateurs",               duration: "40 min" },
  { id: 4,  filename: "04_Multithreading.ipynb",           title: "Multithreading",            duration: "45 min" },
  { id: 5,  filename: "05_Multiprocessing.ipynb",          title: "Multiprocessing",           duration: "45 min" },
  { id: 6,  filename: "06_Programmation_asynchrone.ipynb", title: "Programmation asynchrone",  duration: "50 min" },
  { id: 7,  filename: "07_Module functools.ipynb",         title: "Module functools",          duration: "35 min" },
  { id: 8,  filename: "08_Module_sys.ipynb",               title: "Module sys",                duration: "30 min" },
  { id: 9,  filename: "09_Module_GC.ipynb",                title: "Module GC",                 duration: "35 min" },
  { id: 10, filename: "10_Distribuer_son_package.ipynb",   title: "Distribuer son package",    duration: "40 min" },
  { id: 11, filename: "11_Projet_avance.md",               title: "Projet avancé",             duration: "120 min", isMd: true },
];

export const examensCourses = [
  { id: 1, filename: "decorateurs en python.md",     title: "Décorateurs en Python",     duration: "45 min", isMd: true },
  { id: 2, filename: "Decorateurs en python.md",     title: "Décorateurs (variante)",    duration: "45 min", isMd: true },
  { id: 3, filename: "Generateurs en python.md",     title: "Générateurs en Python",     duration: "45 min", isMd: true },
  { id: 4, filename: "Les tris de listes.md",        title: "Les tris de listes",        duration: "45 min", isMd: true },
  { id: 5, filename: "POO avec python.md",           title: "POO avec Python",           duration: "60 min", isMd: true },
  { id: 6, filename: "Recherche Binary Search.md",   title: "Recherche Binary Search",   duration: "45 min", isMd: true },
  { id: 7, filename: "Voyageur de commerce.md",      title: "Voyageur de commerce",      duration: "60 min", isMd: true },
];

export const correctionsData = {
  projets: [
    {
      id: "projet-debutant",
      title: "Projet Débutant",
      folder: "Correction projets/01_Projet_debutant",
      files: [
        { filename: "Projet debutant.ipynb", title: "Correction Projet Débutant" },
      ],
    },
    {
      id: "projets-intermediaires",
      title: "Projets Intermédiaires",
      folder: "Correction projets/02_Projets_intermediaires",
      files: [
        { filename: "Projet Usine de fabrication/Projet_Usine.ipynb", title: "Usine de fabrication" },
      ],
    },
    {
      id: "projet-avance",
      title: "Projet Avancé",
      folder: "Correction projets/03_Projet_Avance",
      files: [],
    },
  ],
  examens: [
    { filename: "CORRECTION decorateurs en python.ipynb",   title: "Correction – Décorateurs" },
    { filename: "CORRECTION generateurs en python.ipynb",   title: "Correction – Générateurs" },
    { filename: "CORRECTION Les tris de listes.ipynb",      title: "Correction – Tris de listes" },
    { filename: "CORRECTION POO avec python.ipynb",         title: "Correction – POO" },
    { filename: "CORRECTION Recherche Binary Search.ipynb", title: "Correction – Binary Search" },
    { filename: "CORRECTION voyageur de commerce.ipynb",    title: "Correction – Voyageur de commerce" },
  ],
};

export function getCoursesByLevel(levelId) {
  switch (levelId) {
    case "debutant":      return debutantCourses;
    case "intermediaire": return intermediaireCourses;
    case "avance":        return avanceCourses;
    case "examens":       return examensCourses;
    default:              return [];
  }
}

export function getLevelFolder(levelId) {
  const level = pythonLevels.find((l) => l.id === levelId);
  return level ? `${BASE}/${level.folder}` : "";
}

export function getCorrectionBasePath() {
  return `${BASE}/corrections`;
}
