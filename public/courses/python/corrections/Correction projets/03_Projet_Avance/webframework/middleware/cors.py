"""
Middleware CORS (Cross-Origin Resource Sharing)
"""
from typing import List, Optional
from .base import Middleware
from ..core.request import Request
from ..core.response import Response


class CORSMiddleware(Middleware):
    """Middleware pour gérer les headers CORS"""
    
    def __init__(self, 
                 allow_origins: List[str] = None,
                 allow_methods: List[str] = None,
                 allow_headers: List[str] = None,
                 max_age: int = 3600):
        """
        Args:
            allow_origins: Liste des origines autorisées, ou ["*"] pour toutes
            allow_methods: Méthodes HTTP autorisées
            allow_headers: Headers autorisés
            max_age: Durée de cache pour les preflight requests
        """
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]
        self.max_age = max_age
    
    async def before_request(self, request: Request) -> Optional[Response]:
        """Gérer les preflight requests (OPTIONS)"""
        if request.method == "OPTIONS":
            # Réponse preflight
            response = Response(status=204)  # No Content
            self._add_cors_headers(response, request)
            return response
        
        return None
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """Ajouter les headers CORS à toutes les réponses"""
        self._add_cors_headers(response, request)
        return response
    
    def _add_cors_headers(self, response: Response, request: Request):
        """Ajouter les headers CORS appropriés"""
        origin = request.get_header("Origin", "*")
        
        # Vérifier si l'origine est autorisée
        if "*" in self.allow_origins or origin in self.allow_origins:
            response.set_header("Access-Control-Allow-Origin", origin)
        
        response.set_header(
            "Access-Control-Allow-Methods",
            ", ".join(self.allow_methods)
        )
        
        if "*" in self.allow_headers:
            # Autoriser tous les headers demandés
            requested_headers = request.get_header("Access-Control-Request-Headers")
            if requested_headers:
                response.set_header("Access-Control-Allow-Headers", requested_headers)
            else:
                response.set_header("Access-Control-Allow-Headers", "*")
        else:
            response.set_header(
                "Access-Control-Allow-Headers",
                ", ".join(self.allow_headers)
            )
        
        response.set_header("Access-Control-Max-Age", str(self.max_age))
        response.set_header("Access-Control-Allow-Credentials", "true")