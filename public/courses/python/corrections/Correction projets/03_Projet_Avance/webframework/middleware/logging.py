"""
Middleware de logging des requêtes
"""
import logging
import time
from typing import Optional
from .base import Middleware
from ..core.request import Request
from ..core.response import Response


class LoggingMiddleware(Middleware):
    """Middleware pour logger toutes les requêtes/réponses"""
    
    def __init__(self):
        self.logger = logging.getLogger("RequestLogger")
        self.logger.setLevel(logging.INFO)
        
        # Stocker le timestamp de début pour chaque requête
        self._start_times = {}
    
    async def before_request(self, request: Request) -> Optional[Response]:
        """Logger la requête entrante"""
        request_id = id(request)
        self._start_times[request_id] = time.time()
        
        self.logger.info(
            f"→ {request.method} {request.path} | "
            f"Headers: {len(request.headers)} | "
            f"Body: {len(request.body)} bytes"
        )
        
        return None  # Continuer le traitement
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """Logger la réponse"""
        request_id = id(request)
        start_time = self._start_times.pop(request_id, None)
        
        if start_time:
            duration = (time.time() - start_time) * 1000  # en ms
            
            # Niveau de log selon le status code
            if response.status >= 500:
                log_level = logging.ERROR
            elif response.status >= 400:
                log_level = logging.WARNING
            else:
                log_level = logging.INFO
            
            self.logger.log(
                log_level,
                f"← {request.method} {request.path} | "
                f"Status: {response.status} | "
                f"Duration: {duration:.2f}ms"
            )
        
        return response


class PerformanceMiddleware(Middleware):
    """Middleware pour ajouter des headers de performance"""
    
    def __init__(self):
        self._start_times = {}
    
    async def before_request(self, request: Request) -> Optional[Response]:
        """Démarrer le chronomètre"""
        self._start_times[id(request)] = time.time()
        return None
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """Ajouter le header X-Response-Time"""
        request_id = id(request)
        start_time = self._start_times.pop(request_id, None)
        
        if start_time:
            duration = (time.time() - start_time) * 1000
            response.set_header("X-Response-Time", f"{duration:.2f}ms")
        
        return response