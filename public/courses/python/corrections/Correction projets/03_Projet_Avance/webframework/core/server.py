"""
Serveur HTTP asynchrone principal
"""
import asyncio
import logging
from typing import Callable, Dict, List, Optional
from .request import Request
from .response import Response
from .router import Router
from ..middleware.base import Middleware
from ..utils.parser import HTTPParser
from ..utils.logger import setup_logger


class App:
    """Application principale du framework web"""
    
    def __init__(self, name: str = "WebApp"):
        self.name = name
        self.router = Router()
        self.middlewares: List[Middleware] = []
        self.error_handlers: Dict[int, Callable] = {}
        self.logger = setup_logger(name)
        
    def route(self, path: str, methods: List[str] = None):
        """Décorateur pour enregistrer une route"""
        if methods is None:
            methods = ["GET"]
        
        def decorator(handler):
            self.router.add_route(path, handler, methods)
            return handler
        return decorator
    
    def use_middleware(self, middleware: Middleware):
        """Enregistrer un middleware"""
        self.middlewares.append(middleware)
        self.logger.info(f"Middleware registered: {middleware.__class__.__name__}")
    
    def error_handler(self, status_code: int):
        """Décorateur pour gérer les erreurs par code"""
        def decorator(handler):
            self.error_handlers[status_code] = handler
            return handler
        return decorator
    
    async def handle_connection(self, reader: asyncio.StreamReader, 
                               writer: asyncio.StreamWriter):
        """Gérer une connexion client"""
        addr = writer.get_extra_info('peername')
        self.logger.info(f"New connection from {addr}")
        
        try:
            # Parser la requête HTTP
            raw_request = await reader.read(8192)
            if not raw_request:
                return
            
            request = HTTPParser.parse_request(raw_request.decode('utf-8', errors='ignore'))
            
            # Traiter la requête
            response = await self.handle_request(request)
            
            # Envoyer la réponse
            writer.write(response.to_bytes())
            await writer.drain()
            
        except Exception as e:
            self.logger.error(f"Error handling connection: {e}", exc_info=True)
            error_response = Response(
                body=f"Internal Server Error: {str(e)}",
                status=500
            )
            writer.write(error_response.to_bytes())
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
    
    async def handle_request(self, request: Request) -> Response:
        """Traiter une requête complète avec middleware"""
        import time
        start_time = time.time()
        
        try:
            # Exécuter les middleware (avant)
            for middleware in self.middlewares:
                result = await middleware.before_request(request)
                if isinstance(result, Response):
                    return result
            
            # Router vers le handler approprié
            handler, path_params = self.router.match(request.path, request.method)
            
            if handler is None:
                # Chercher un error handler pour 404
                if 404 in self.error_handlers:
                    response = await self.error_handlers[404](request, None)
                else:
                    response = Response.json(
                        {"error": "Not Found", "path": request.path},
                        status=404
                    )
            else:
                # Ajouter les paramètres de path à la requête
                request.path_params = path_params
                
                # Exécuter le handler
                response = await handler(request)
                
                # S'assurer que c'est bien une Response
                if not isinstance(response, Response):
                    response = Response(str(response))
            
            # Exécuter les middleware (après)
            for middleware in reversed(self.middlewares):
                response = await middleware.after_request(request, response)
            
            # Logger la requête
            duration = (time.time() - start_time) * 1000
            self.logger.info(
                f"{request.method} {request.path} {response.status} - {duration:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in request handler: {e}", exc_info=True)
            
            # Chercher un error handler pour 500
            if 500 in self.error_handlers:
                response = await self.error_handlers[500](request, e)
            else:
                response = Response.json(
                    {"error": "Internal Server Error", "message": str(e)},
                    status=500
                )
            
            return response
    
    async def _run_server(self, host: str, port: int):
        """Démarrer le serveur asyncio"""
        server = await asyncio.start_server(
            self.handle_connection,
            host,
            port
        )
        
        addr = server.sockets[0].getsockname()
        self.logger.info(f"Server running on http://{addr[0]}:{addr[1]}")
        
        async with server:
            await server.serve_forever()
    
    def run(self, host: str = "127.0.0.1", port: int = 8000):
        """Point d'entrée pour démarrer le serveur"""
        try:
            asyncio.run(self._run_server(host, port))
        except KeyboardInterrupt:
            self.logger.info("Server stopped by user")