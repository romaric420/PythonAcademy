"""
Interface de base pour les middleware
"""
from abc import ABC, abstractmethod
from typing import Optional
from ..core.request import Request
from ..core.response import Response


class Middleware(ABC):
    """
    Classe abstraite pour les middleware
    
    Un middleware peut:
    - Intercepter une requête avant qu'elle arrive au handler (before_request)
    - Modifier la réponse après le handler (after_request)
    - Court-circuiter le traitement en retournant une Response dans before_request
    """
    
    @abstractmethod
    async def before_request(self, request: Request) -> Optional[Response]:
        """
        Exécuté avant le handler
        
        Args:
            request: La requête HTTP
            
        Returns:
            None pour continuer le traitement
            Response pour court-circuiter et renvoyer immédiatement
        """
        pass
    
    @abstractmethod
    async def after_request(self, request: Request, response: Response) -> Response:
        """
        Exécuté après le handler
        
        Args:
            request: La requête HTTP
            response: La réponse du handler
            
        Returns:
            Response (modifiée ou non)
        """
        pass