"""
Système de routing avec support des paramètres dynamiques
"""
import re
from typing import Callable, Dict, List, Optional, Tuple


class Route:
    """Représente une route avec son pattern et handler"""
    
    def __init__(self, path: str, handler: Callable, methods: List[str]):
        self.path = path
        self.handler = handler
        self.methods = [m.upper() for m in methods]
        
        # Compiler le pattern pour les paramètres dynamiques
        self.pattern, self.param_names = self._compile_pattern(path)
    
    def _compile_pattern(self, path: str) -> Tuple[re.Pattern, List[str]]:
        """
        Convertir un path comme /user/{id}/post/{post_id} 
        en regex et extraire les noms des paramètres
        """
        param_names = []
        
        # Trouver tous les {param}
        pattern = path
        for match in re.finditer(r'\{([^}]+)\}', path):
            param_name = match.group(1)
            param_names.append(param_name)
            # Remplacer {param} par un groupe de capture nommé
            pattern = pattern.replace(
                f'{{{param_name}}}',
                f'(?P<{param_name}>[^/]+)'
            )
        
        # Ajouter ^ et $ pour match exact
        pattern = f'^{pattern}$'
        
        return re.compile(pattern), param_names
    
    def match(self, path: str) -> Optional[Dict[str, str]]:
        """Vérifier si le path correspond à cette route"""
        match = self.pattern.match(path)
        if match:
            return match.groupdict()
        return None


class Router:
    """Gestionnaire de routes"""
    
    def __init__(self):
        self.routes: List[Route] = []
    
    def add_route(self, path: str, handler: Callable, methods: List[str]):
        """Ajouter une route"""
        route = Route(path, handler, methods)
        self.routes.append(route)
    
    def match(self, path: str, method: str) -> Tuple[Optional[Callable], Dict[str, str]]:
        """
        Trouver le handler correspondant au path et à la méthode
        Retourne (handler, path_params) ou (None, {})
        """
        method = method.upper()
        
        for route in self.routes:
            # Vérifier si le path correspond
            params = route.match(path)
            
            if params is not None:
                # Vérifier si la méthode est autorisée
                if method in route.methods:
                    return route.handler, params
                # Path match mais méthode incorrecte
                # On pourrait retourner 405 Method Not Allowed
                # Pour l'instant, on continue de chercher
        
        # Aucune route trouvée
        return None, {}
    
    def get_all_routes(self) -> List[Dict]:
        """Retourner toutes les routes (utile pour le debugging)"""
        return [
            {
                "path": route.path,
                "methods": route.methods,
                "handler": route.handler.__name__
            }
            for route in self.routes
        ]