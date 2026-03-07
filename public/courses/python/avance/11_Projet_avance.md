# Projet Python Avancé : Mini-Framework Web Asynchrone

## 📋 Objectif du Projet

Créer un framework web asynchrone complet (style Flask/FastAPI) en utilisant uniquement les bibliothèques standard Python. Le framework doit permettre de créer des applications web avec routing, middleware, gestion des requêtes/réponses, et système de logging avancé.

**Durée estimée :** 8 heures

---

## 🎯 Fonctionnalités Requises

### 1. Serveur HTTP Asynchrone (2h)
- Créer un serveur TCP asynchrone avec `asyncio`
- Parser les requêtes HTTP/1.1 (méthode, chemin, headers, body)
- Gérer plusieurs connexions simultanées
- Implémenter les méthodes : GET, POST, PUT, DELETE
- Support des query parameters et du body JSON

### 2. Système de Routing (1h30)
- Décorateur `@route(path, methods=[])` pour enregistrer des handlers
- Support des paramètres dynamiques dans les URLs : `/user/{id}/post/{post_id}`
- Gestion des routes avec expressions régulières
- Retour d'erreur 404 pour routes inexistantes

### 3. Objets Request et Response (1h30)
- **Classe Request** :
  - Propriétés : `method`, `path`, `headers`, `query_params`, `path_params`, `body`, `json()`
  - Méthode asynchrone pour lire le body
- **Classe Response** :
  - Constructor : `Response(body, status=200, headers={})`
  - Support des réponses JSON avec `Response.json(data)`
  - Support du streaming avec générateurs asynchrones

### 4. Système de Middleware (1h30)
- Interface pour créer des middleware (avant/après requête)
- Décorateur `@middleware` pour enregistrer des middleware
- Ordre d'exécution : middleware → handler → middleware (reverse)
- Exemples à implémenter :
  - Logging des requêtes/réponses
  - Mesure du temps de traitement
  - Gestion CORS
  - Authentification basique

### 5. Logging Avancé (45min)
- Logger configuré avec rotation de fichiers
- Différents niveaux : INFO (requêtes), WARNING (erreurs 4xx), ERROR (erreurs 5xx)
- Format : timestamp, méthode, path, status, durée
- Logger séparé pour les erreurs applicatives

### 6. Gestion des Erreurs (30min)
- Context manager pour gérer les connexions automatiquement
- Try/except pour capturer les erreurs dans les handlers
- Réponses d'erreur JSON standardisées
- Décorateur `@error_handler(404)` pour personnaliser les erreurs

### 7. Tests Unitaires (45min)
- Tester le parsing de requêtes HTTP
- Tester le routing (routes simples et avec paramètres)
- Tester les middleware (ordre d'exécution)
- Tester les réponses JSON et streaming
- Mock des connexions réseau

---

## Architecture Attendue

```
webframework/
│
├── core/
│   ├── __init__.py
│   ├── server.py          # Serveur asyncio
│   ├── request.py         # Classe Request
│   ├── response.py        # Classe Response
│   └── router.py          # Système de routing
│
├── middleware/
│   ├── __init__.py
│   ├── base.py            # Interface Middleware
│   ├── logging.py         # Middleware de logging
│   ├── cors.py            # Middleware CORS
│   └── auth.py            # Middleware d'authentification
│
├── utils/
│   ├── __init__.py
│   ├── parser.py          # Parser HTTP
│   └── logger.py          # Configuration logging
│
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_router.py
│   ├── test_middleware.py
│   └── test_request_response.py
│
├── app.py                 # Application exemple
└── main.py               # Point d'entrée
```

---

## Exemple d'Utilisation Attendu

```python
from webframework import App, Response
from webframework.middleware import LoggingMiddleware, CORSMiddleware

app = App()

# Enregistrer des middleware
app.use_middleware(LoggingMiddleware())
app.use_middleware(CORSMiddleware(allow_origins=["*"]))

# Route simple
@app.route("/", methods=["GET"])
async def home(request):
    return Response.json({"message": "Hello World"})

# Route avec paramètres
@app.route("/user/{id}", methods=["GET"])
async def get_user(request):
    user_id = request.path_params["id"]
    return Response.json({"user_id": user_id, "name": "John Doe"})

# Route POST avec body JSON
@app.route("/user", methods=["POST"])
async def create_user(request):
    data = await request.json()
    # Traiter data...
    return Response.json({"created": True, "user": data}, status=201)

# Streaming de données
@app.route("/stream", methods=["GET"])
async def stream_data(request):
    async def generate():
        for i in range(10):
            yield f"data: {i}\n\n"
            await asyncio.sleep(0.1)
    
    return Response.stream(generate())

# Gestionnaire d'erreur personnalisé
@app.error_handler(404)
async def not_found(request, error):
    return Response.json({"error": "Route not found"}, status=404)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
```

## Défis Bonus (Optionnels)

1. **Support WebSocket** : Gérer les connexions WebSocket pour la communication bidirectionnelle
2. **Templates HTML** : Mini moteur de templates (sans Jinja2)
3. **Sessions** : Gestion de sessions avec cookies
4. **Rate Limiting** : Middleware pour limiter le nombre de requêtes
5. **Static Files** : Servir des fichiers statiques (CSS, JS, images)

---

## Ressources Autorisées

- Documentation Python officielle
- Modules standard uniquement : `asyncio`, `socket`, `json`, `urllib.parse`, `re`, `logging`, `unittest`
- Aucune bibliothèque tierce (pas de `pip install`)

---

## Conseils

1. **Commencez par le serveur TCP** : Assurez-vous qu'il accepte des connexions avant de parser HTTP
2. **Parser HTTP ligne par ligne** : Méthode/path/version, puis headers, puis body
3. **Testez au fur et à mesure** : Ne passez pas à la fonctionnalité suivante sans tests
4. **Utilisez `asyncio.start_server()`** : Plus simple que de gérer les sockets manuellement
5. **Logging dès le début** : Facilite le débogage

Bon courage !