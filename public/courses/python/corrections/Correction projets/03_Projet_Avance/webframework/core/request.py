"""
Classe Request pour représenter les requêtes HTTP
"""
import json
from typing import Dict, Any, Optional
from urllib.parse import parse_qs, urlparse


class Request:
    """Représente une requête HTTP"""
    
    def __init__(self, method: str, path: str, headers: Dict[str, str], 
                 body: str = "", version: str = "HTTP/1.1"):
        self.method = method.upper()
        self.path = path
        self.headers = headers
        self.body = body
        self.version = version
        
        # Parser l'URL pour extraire query params
        parsed = urlparse(path)
        self.path_without_query = parsed.path
        self.query_params = self._parse_query_string(parsed.query)
        
        # Sera rempli par le router
        self.path_params: Dict[str, str] = {}
        
        # Cache pour le JSON
        self._json_cache: Optional[Dict] = None
    
    def _parse_query_string(self, query: str) -> Dict[str, str]:
        """Parser les query parameters"""
        if not query:
            return {}
        
        parsed = parse_qs(query, keep_blank_values=True)
        # Convertir les listes en valeurs simples (prendre le premier)
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
    
    async def json(self) -> Dict[str, Any]:
        """Parser le body comme JSON (async pour cohérence)"""
        if self._json_cache is not None:
            return self._json_cache
        
        try:
            self._json_cache = json.loads(self.body) if self.body else {}
            return self._json_cache
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in request body: {e}")
    
    def get_header(self, name: str, default: str = None) -> Optional[str]:
        """Récupérer un header (case-insensitive)"""
        name_lower = name.lower()
        for key, value in self.headers.items():
            if key.lower() == name_lower:
                return value
        return default
    
    @property
    def content_type(self) -> Optional[str]:
        """Récupérer le Content-Type"""
        return self.get_header("Content-Type")
    
    @property
    def content_length(self) -> int:
        """Récupérer le Content-Length"""
        length = self.get_header("Content-Length", "0")
        try:
            return int(length)
        except ValueError:
            return 0
    
    def __repr__(self) -> str:
        return f"<Request {self.method} {self.path}>"