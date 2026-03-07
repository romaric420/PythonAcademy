"""
Middleware d'authentification basique
"""
import base64
from typing import Dict, Optional, Callable
from .base import Middleware
from ..core.request import Request
from ..core.response import Response


class BasicAuthMiddleware(Middleware):
    """
    Middleware pour l'authentification HTTP Basic
    """
    
    def __init__(self, users: Dict[str, str], realm: str = "Protected Area"):
        """
        Args:
            users: Dictionnaire {username: password}
            realm: Nom du domaine protégé
        """
        self.users = users
        self.realm = realm
    
    async def before_request(self, request: Request) -> Optional[Response]:
        """Vérifier les credentials"""
        auth_header = request.get_header("Authorization")
        
        if not auth_header or not auth_header.startswith("Basic "):
            return self._unauthorized_response()
        
        # Décoder les credentials
        try:
            encoded = auth_header[6:]  # Enlever "Basic "
            decoded = base64.b64decode(encoded).decode('utf-8')
            username, password = decoded.split(':', 1)
        except Exception:
            return self._unauthorized_response()
        
        # Vérifier les credentials
        if username not in self.users or self.users[username] != password:
            return self._unauthorized_response()
        
        # Authentification réussie, ajouter l'utilisateur à la requête
        request.user = username
        return None
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """Rien à faire après la requête"""
        return response
    
    def _unauthorized_response(self) -> Response:
        """Créer une réponse 401 Unauthorized"""
        response = Response.json(
            {"error": "Unauthorized", "message": "Valid credentials required"},
            status=401
        )
        response.set_header("WWW-Authenticate", f'Basic realm="{self.realm}"')
        return response


class TokenAuthMiddleware(Middleware):
    """
    Middleware pour l'authentification par token (Bearer)
    """
    
    def __init__(self, validate_token: Callable[[str], Optional[dict]]):
        """
        Args:
            validate_token: Fonction qui valide un token et retourne les infos user
                           Retourne None si le token est invalide
        """
        self.validate_token = validate_token
    
    async def before_request(self, request: Request) -> Optional[Response]:
        """Vérifier le token"""
        auth_header = request.get_header("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return self._unauthorized_response()
        
        token = auth_header[7:]  # Enlever "Bearer "
        
        # Valider le token
        user_info = self.validate_token(token)
        
        if not user_info:
            return self._unauthorized_response()
        
        # Token valide, ajouter les infos à la requête
        request.user = user_info
        return None
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """Rien à faire après la requête"""
        return response
    
    def _unauthorized_response(self) -> Response:
        """Créer une réponse 401 Unauthorized"""
        return Response.json(
            {"error": "Unauthorized", "message": "Valid token required"},
            status=401
        )


class RateLimitMiddleware(Middleware):
    """
    Middleware simple de rate limiting
    """
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """
        Args:
            max_requests: Nombre maximum de requêtes
            window_seconds: Fenêtre de temps en secondes
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # {ip: [(timestamp, ...), ...]}
    
    async def before_request(self, request: Request) -> Optional[Response]:
        """Vérifier le rate limit"""
        import time
        
        # Utiliser l'IP comme clé (simplifié)
        # Dans une vraie app, on utiliserait request.client_ip
        client_key = "default"  # Simplification
        
        now = time.time()
        
        # Nettoyer les vieilles entrées
        if client_key in self.requests:
            self.requests[client_key] = [
                ts for ts in self.requests[client_key]
                if now - ts < self.window_seconds
            ]
        else:
            self.requests[client_key] = []
        
        # Vérifier le nombre de requêtes
        if len(self.requests[client_key]) >= self.max_requests:
            return Response.json(
                {
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded: {self.max_requests} requests per {self.window_seconds}s"
                },
                status=429
            )
        
        # Ajouter la requête actuelle
        self.requests[client_key].append(now)
        return None
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """Ajouter des headers de rate limit"""
        client_key = "default"
        remaining = max(0, self.max_requests - len(self.requests.get(client_key, [])))
        
        response.set_header("X-RateLimit-Limit", str(self.max_requests))
        response.set_header("X-RateLimit-Remaining", str(remaining))
        response.set_header("X-RateLimit-Reset", str(self.window_seconds))
        
        return response