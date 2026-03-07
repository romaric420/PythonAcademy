"""
Classe Response pour représenter les réponses HTTP
"""
import json
from typing import Dict, Any, AsyncGenerator, Union


class Response:
    """Représente une réponse HTTP"""
    
    STATUS_CODES = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable"
    }
    
    def __init__(self, body: Union[str, bytes] = "", status: int = 200, 
                 headers: Dict[str, str] = None):
        self.body = body
        self.status = status
        self.headers = headers or {}
        self.streaming_generator = None
        
        # Ajouter des headers par défaut
        if "Content-Type" not in self.headers and body:
            self.headers["Content-Type"] = "text/plain; charset=utf-8"
    
    @classmethod
    def json(cls, data: Any, status: int = 200, headers: Dict[str, str] = None):
        """Créer une réponse JSON"""
        headers = headers or {}
        headers["Content-Type"] = "application/json; charset=utf-8"
        
        body = json.dumps(data, ensure_ascii=False, indent=2)
        return cls(body=body, status=status, headers=headers)
    
    @classmethod
    def html(cls, html: str, status: int = 200, headers: Dict[str, str] = None):
        """Créer une réponse HTML"""
        headers = headers or {}
        headers["Content-Type"] = "text/html; charset=utf-8"
        return cls(body=html, status=status, headers=headers)
    
    @classmethod
    def stream(cls, generator: AsyncGenerator, status: int = 200, 
               headers: Dict[str, str] = None):
        """Créer une réponse en streaming"""
        headers = headers or {}
        headers["Transfer-Encoding"] = "chunked"
        headers["Content-Type"] = "text/event-stream"
        
        response = cls(body="", status=status, headers=headers)
        response.streaming_generator = generator
        return response
    
    def to_bytes(self) -> bytes:
        """Convertir la réponse en bytes HTTP"""
        status_text = self.STATUS_CODES.get(self.status, "Unknown")
        
        # Ligne de status
        response_lines = [f"HTTP/1.1 {self.status} {status_text}"]
        
        # Headers
        if not self.streaming_generator:
            # Calculer Content-Length pour les réponses non-streaming
            if isinstance(self.body, str):
                body_bytes = self.body.encode('utf-8')
            else:
                body_bytes = self.body
            
            if "Content-Length" not in self.headers:
                self.headers["Content-Length"] = str(len(body_bytes))
        
        for key, value in self.headers.items():
            response_lines.append(f"{key}: {value}")
        
        # Ligne vide séparant headers et body
        response_lines.append("")
        response_lines.append("")
        
        # Construire la réponse
        header_bytes = "\r\n".join(response_lines).encode('utf-8')
        
        if self.streaming_generator:
            # Pour le streaming, on retourne juste les headers
            # Le body sera envoyé séparément
            return header_bytes
        else:
            # Body
            if isinstance(self.body, str):
                body_bytes = self.body.encode('utf-8')
            else:
                body_bytes = self.body
            
            return header_bytes + body_bytes
    
    def set_header(self, name: str, value: str):
        """Définir un header"""
        self.headers[name] = value
    
    def set_cookie(self, name: str, value: str, max_age: int = None, 
                   path: str = "/", http_only: bool = True):
        """Définir un cookie"""
        cookie = f"{name}={value}; Path={path}"
        if max_age:
            cookie += f"; Max-Age={max_age}"
        if http_only:
            cookie += "; HttpOnly"
        
        if "Set-Cookie" in self.headers:
            # Supporter plusieurs cookies
            self.headers["Set-Cookie"] += f", {cookie}"
        else:
            self.headers["Set-Cookie"] = cookie
    
    def __repr__(self) -> str:
        return f"<Response {self.status}>"