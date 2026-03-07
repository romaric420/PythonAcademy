"""
Configuration du système de logging
"""
import logging
import logging.handlers
from pathlib import Path


def setup_logger(name: str, log_dir: str = "logs") -> logging.Logger:
    """
    Configurer un logger avec rotation de fichiers
    """
    # Créer le répertoire de logs s'il n'existe pas
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Créer le logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Éviter les doublons si le logger existe déjà
    if logger.handlers:
        return logger
    
    # Format des logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour la console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler pour les fichiers avec rotation (10MB max, 5 fichiers)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / f"{name}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler séparé pour les erreurs
    error_handler = logging.handlers.RotatingFileHandler(
        log_path / f"{name}_errors.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger