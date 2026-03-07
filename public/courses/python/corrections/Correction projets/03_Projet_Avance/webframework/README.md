# Mini-Framework Web Asynchrone - Solution Complète

## Structure du Projet

```
webframework/
│
├── core/
│   ├── __init__.py           # Exports du module core
│   ├── server.py             # Classe App et serveur asyncio
│   ├── request.py            # Classe Request
│   ├── response.py           # Classe Response
│   └── router.py             # Système de routing avec regex
│
├── middleware/
│   ├── __init__.py           # Exports des middleware
│   ├── base.py               # Interface Middleware abstraite
│   ├── logging.py            # LoggingMiddleware, PerformanceMiddleware
│   ├── cors.py               # CORSMiddleware
│   └── auth.py               # BasicAuth, TokenAuth, RateLimit
│
├── utils/
│   ├── __init__.py           # Exports des utilitaires
│   ├── parser.py             # Parser HTTP
│   └── logger.py             # Configuration logging avec rotation
│
├── tests/
│   ├── __init__.py
│   └── test_all.py           # Tests unitaires complets
│
├── logs/                     # Créé automatiquement
│   ├── ExampleApp.log
│   └── ExampleApp_errors.log
│
├── app.py                    # Application exemple complète
└── README.md                 # Ce fichier
```

---

## Installation et Exécution

### Prérequis
- Python 3.7+ (pour asyncio et annotations)
- Aucune dépendance tierce

### Lancer l'application exemple

```bash
# Lancer l'application
python app.py
```

Le serveur démarre sur `http://127.0.0.1:8000`

### Tester avec curl

```bash
# Page d'accueil
curl http://localhost:8000/

# Lister les utilisateurs
curl http://localhost:8000/users

# Créer un utilisateur
curl -X POST http://localhost:8000/users \
  -H 'Content-Type: application/json' \
  -d '{"name":"Dave","email":"dave@example.com"}'

# Route protégée
curl http://localhost:8000/protected \
  -H 'X-API-Key: secret123'

# Streaming
curl http://localhost:8000/stream
```

---

## 🧪 Exécuter les Tests

```bash
python -m tests.test_all
```

Tous les tests doivent passer avec succès.

---

## Concepts Couverts

### 1. Asyncio
- **`asyncio.start_server()`** : Serveur TCP asynchrone
- **`StreamReader` / `StreamWriter`** : Gestion des connexions
- **`async def` / `await`** : Toutes les fonctions de traitement sont asynchrones
- **Gestion concurrente** : Plusieurs connexions simultanées

### 2. POO Avancée
- **Classes** : `App`, `Request`, `Response`, `Router`, `Route`, `Middleware`
- **Héritage** : `Middleware` est une classe abstraite (ABC)
- **Composition** : `App` contient un `Router` et des `Middleware`
- **Properties** : `@property` pour `content_type`, `content_length`
- **Class methods** : `Response.json()`, `Response.html()`

### 3. Décorateurs
- **`@app.route()`** : Enregistrement de routes
- **`@app.error_handler()`** : Gestion d'erreurs personnalisée
- **`@abstractmethod`** : Méthodes abstraites dans Middleware

### 4. Context Managers
- **Connexions** : `async with server:` dans le serveur
- **Fermeture automatique** : `writer.close()` dans finally

### 5. Générateurs
- **Async generators** : `async def generate(): yield ...`
- **Streaming** : `Response.stream()` pour Server-Sent Events

### 6. Modules Standard
- **`asyncio`** : Programmation asynchrone
- **`socket`** : Implicite via asyncio.start_server
- **`json`** : Parsing et génération JSON
- **`urllib.parse`** : Parser les query parameters
- **`re`** : Regex pour le routing dynamique
- **`logging`** : System de logs complet
- **`unittest`** : Tests unitaires
- **`base64`** : Authentication Basic
- **`pathlib`** : Manipulation de chemins

### 7. Tests Unitaires
- **`unittest.TestCase`** : Tests synchrones
- **`unittest.IsolatedAsyncioTestCase`** : Tests asynchrones
- **Assertions** : `assertEqual`, `assertIn`, `assertIsNone`
- **Test suite** : Organisation des tests en suites

### 8. Logging
- **`logging.Logger`** : Logger configuré
- **`RotatingFileHandler`** : Rotation automatique (10MB)
- **Niveaux** : INFO, WARNING, ERROR
- **Fichiers séparés** : logs normaux + logs d'erreurs

---

## Points Clés de la Solution

### Architecture du Serveur

Le serveur utilise `asyncio.start_server()` qui :
1. Écoute sur un port
2. Accepte les connexions
3. Passe chaque connexion à `handle_connection()`
4. Gère plusieurs clients en parallèle

### Pipeline de Traitement

```
Connexion TCP
    ↓
Parser HTTP (utils/parser.py)
    ↓
Création Request (core/request.py)
    ↓
Middleware.before_request() ← ordre normal
    ↓
Router.match() → Handler
    ↓
Middleware.after_request() ← ordre inverse
    ↓
Conversion Response.to_bytes()
    ↓
Envoi au client
```

### Routing Dynamique

Le router compile les paths avec paramètres en regex :
- `/user/{id}` → `^/user/(?P<id>[^/]+)$`
- Match avec `re.Pattern.match()`
- Extraction des paramètres via `match.groupdict()`

### Système de Middleware

Les middleware forment une chaîne :
1. **Avant** : M1 → M2 → M3 → Handler
2. **Après** : Handler → M3 → M2 → M1

Chaque middleware peut :
- Inspecter/modifier la requête
- Court-circuiter (retourner une Response)
- Modifier la réponse

---

## Fonctionnalités Bonus Implémentées

### 1. Middleware d'Authentification
- **BasicAuth** : HTTP Basic Authentication
- **TokenAuth** : Bearer Token (extensible)
- **RateLimit** : Limitation de requêtes par fenêtre de temps

### 2. Gestion Avancée des Erreurs
- Error handlers personnalisés par code (404, 500)
- Format JSON standardisé pour les erreurs
- Logging automatique selon la gravité

### 3. Performance Monitoring
- Header `X-Response-Time` sur chaque réponse
- Logs avec durée de traitement
- Métriques par requête

### 4. CORS Complet
- Support preflight (OPTIONS)
- Headers configurables
- Wildcard ou liste d'origines

---

## Extensions Possibles

Pour aller plus loin, les élèves peuvent ajouter :

1. **WebSocket** : Support des connexions WebSocket
2. **Templates** : Mini moteur de templates (Jinja-like)
3. **Sessions** : Gestion de sessions avec cookies signés
4. **File Upload** : Parser multipart/form-data
5. **Static Files** : Serveur de fichiers statiques
6. **Database** : Intégration SQLite avec context manager
7. **Validation** : Décorateur `@validate_json(schema)`
8. **Compression** : Middleware de compression gzip
9. **Cache** : Middleware de cache en mémoire
10. **Admin Panel** : Interface web pour voir les routes/logs

---

## Notes Pédagogiques

### Difficultés Courantes

1. **Parser HTTP** : Attention aux `\r\n`, pas juste `\n`
2. **Asyncio** : Ne pas oublier `await` partout
3. **Routing regex** : Bien échapper les caractères spéciaux
4. **Middleware order** : Inverse pour `after_request`
5. **Tests async** : Utiliser `IsolatedAsyncioTestCase`

### Points d'Évaluation

- **Code quality** : PEP8, docstrings, naming
- **Error handling** : Try/except appropriés
- **Tests** : Coverage des cas limites
- **Logging** : Niveaux appropriés
- **Architecture** : Séparation des responsabilités

---