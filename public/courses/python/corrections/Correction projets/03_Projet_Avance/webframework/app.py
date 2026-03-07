"""
Application exemple complète utilisant le framework
"""
import asyncio
from core.server import App
from core.response import Response
from middleware.logging import LoggingMiddleware, PerformanceMiddleware
from middleware.cors import CORSMiddleware
from middleware.auth import BasicAuthMiddleware, RateLimitMiddleware


# Créer l'application
app = App("ExampleApp")

# Enregistrer les middleware
app.use_middleware(LoggingMiddleware())
app.use_middleware(PerformanceMiddleware())
app.use_middleware(CORSMiddleware(allow_origins=["*"]))
app.use_middleware(RateLimitMiddleware(max_requests=10, window_seconds=60))

# Base de données simulée
users_db = {
    "1": {"id": "1", "name": "Alice", "email": "alice@example.com"},
    "2": {"id": "2", "name": "Bob", "email": "bob@example.com"},
    "3": {"id": "3", "name": "Charlie", "email": "charlie@example.com"}
}

posts_db = {}
post_counter = 1


# Routes de base
@app.route("/", methods=["GET"])
async def home(request):
    """Page d'accueil"""
    return Response.json({
        "message": "Welcome to the Example API",
        "version": "1.0",
        "endpoints": {
            "GET /": "This page",
            "GET /health": "Health check",
            "GET /users": "List all users",
            "GET /users/{id}": "Get a specific user",
            "POST /users": "Create a new user",
            "GET /stream": "Server-sent events demo",
            "GET /protected": "Protected route (auth required)"
        }
    })


@app.route("/health", methods=["GET"])
async def health(request):
    """Health check endpoint"""
    return Response.json({
        "status": "healthy",
        "uptime": "running"
    })


# Routes CRUD pour users
@app.route("/users", methods=["GET"])
async def list_users(request):
    """Lister tous les utilisateurs"""
    return Response.json({
        "users": list(users_db.values()),
        "count": len(users_db)
    })


@app.route("/users/{id}", methods=["GET"])
async def get_user(request):
    """Récupérer un utilisateur par ID"""
    user_id = request.path_params["id"]
    
    if user_id not in users_db:
        return Response.json(
            {"error": "User not found", "id": user_id},
            status=404
        )
    
    return Response.json(users_db[user_id])


@app.route("/users", methods=["POST"])
async def create_user(request):
    """Créer un nouvel utilisateur"""
    try:
        data = await request.json()
        
        # Validation basique
        if "name" not in data or "email" not in data:
            return Response.json(
                {"error": "Missing required fields: name, email"},
                status=400
            )
        
        # Créer l'utilisateur
        user_id = str(len(users_db) + 1)
        new_user = {
            "id": user_id,
            "name": data["name"],
            "email": data["email"]
        }
        users_db[user_id] = new_user
        
        return Response.json(
            {"created": True, "user": new_user},
            status=201
        )
    
    except ValueError as e:
        return Response.json(
            {"error": "Invalid JSON", "message": str(e)},
            status=400
        )


@app.route("/users/{id}", methods=["PUT"])
async def update_user(request):
    """Mettre à jour un utilisateur"""
    user_id = request.path_params["id"]
    
    if user_id not in users_db:
        return Response.json(
            {"error": "User not found", "id": user_id},
            status=404
        )
    
    try:
        data = await request.json()
        
        # Mettre à jour les champs fournis
        if "name" in data:
            users_db[user_id]["name"] = data["name"]
        if "email" in data:
            users_db[user_id]["email"] = data["email"]
        
        return Response.json({
            "updated": True,
            "user": users_db[user_id]
        })
    
    except ValueError as e:
        return Response.json(
            {"error": "Invalid JSON", "message": str(e)},
            status=400
        )


@app.route("/users/{id}", methods=["DELETE"])
async def delete_user(request):
    """Supprimer un utilisateur"""
    user_id = request.path_params["id"]
    
    if user_id not in users_db:
        return Response.json(
            {"error": "User not found", "id": user_id},
            status=404
        )
    
    deleted_user = users_db.pop(user_id)
    
    return Response.json({
        "deleted": True,
        "user": deleted_user
    })


# Route avec streaming
@app.route("/stream", methods=["GET"])
async def stream_data(request):
    """Démonstration de streaming avec Server-Sent Events"""
    async def generate():
        for i in range(10):
            yield f"data: Event {i} at {asyncio.get_event_loop().time()}\n\n"
            await asyncio.sleep(0.5)
        yield "data: Stream completed\n\n"
    
    return Response.stream(generate())


# Route protégée (nécessite authentification)
@app.route("/protected", methods=["GET"])
async def protected_route(request):
    """Route protégée - nécessite un header X-API-Key"""
    api_key = request.get_header("X-API-Key")
    
    if api_key != "secret123":
        return Response.json(
            {"error": "Unauthorized", "message": "Invalid or missing API key"},
            status=401
        )
    
    return Response.json({
        "message": "Access granted",
        "secret_data": "This is protected information"
    })


# Gestionnaires d'erreurs personnalisés
@app.error_handler(404)
async def not_found(request, error):
    """Handler personnalisé pour 404"""
    return Response.json({
        "error": "Not Found",
        "path": request.path,
        "message": "The requested resource does not exist",
        "suggestion": "Check the API documentation at /"
    }, status=404)


@app.error_handler(500)
async def server_error(request, error):
    """Handler personnalisé pour 500"""
    return Response.json({
        "error": "Internal Server Error",
        "message": "Something went wrong on our end",
        "details": str(error) if error else "Unknown error"
    }, status=500)


# Point d'entrée
if __name__ == "__main__":
    print("=" * 50)
    print("  Example Web Application")
    print("=" * 50)
    print("\nStarting server...")
    print("Try these commands in another terminal:")
    print("\n  curl http://localhost:8000/")
    print("  curl http://localhost:8000/users")
    print("  curl http://localhost:8000/users/1")
    print("  curl -X POST http://localhost:8000/users -H 'Content-Type: application/json' -d '{\"name\":\"Dave\",\"email\":\"dave@example.com\"}'")
    print("  curl http://localhost:8000/stream")
    print("  curl http://localhost:8000/protected -H 'X-API-Key: secret123'")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host="127.0.0.1", port=8000)