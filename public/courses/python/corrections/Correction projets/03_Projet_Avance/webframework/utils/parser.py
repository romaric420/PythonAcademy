"""
Parser de requêtes HTTP
"""
from typing import Dict
from ..core.request import Request


class HTTPParser:
    """Parser pour les requêtes HTTP/1.1"""
    
    @staticmethod
    def parse_request(raw_data: str) -> Request:
        """
        Parser une requête HTTP brute
        Format:
        GET /path HTTP/1.1
        Header1: value1
        Header2: value2
        
        body
        """
        if not raw_data:
            raise ValueError("Empty request")
        
        # Séparer headers et body
        parts = raw_data.split('\r\n\r\n', 1)
        if len(parts) == 2:
            header_section, body = parts
        else:
            header_section = parts[0]
            body = ""
        
        # Séparer les lignes du header
        lines = header_section.split('\r\n')
        if not lines:
            raise ValueError("Invalid request format")
        
        # Parser la première ligne (request line)
        request_line = lines[0]
        method, path, version = HTTPParser._parse_request_line(request_line)
        
        # Parser les headers
        headers = HTTPParser._parse_headers(lines[1:])
        
        # Créer l'objet Request
        return Request(
            method=method,
            path=path,
            headers=headers,
            body=body,
            version=version
        )
    
    @staticmethod
    def _parse_request_line(line: str) -> tuple:
        """Parser la ligne de requête: GET /path HTTP/1.1"""
        parts = line.split(' ')
        if len(parts) != 3:
            raise ValueError(f"Invalid request line: {line}")
        
        method, path, version = parts
        return method, path, version
    
    @staticmethod
    def _parse_headers(lines: list) -> Dict[str, str]:
        """Parser les headers HTTP"""
        headers = {}
        
        for line in lines:
            if not line:
                continue
            
            # Format: "Header-Name: value"
            if ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
        
        return headers