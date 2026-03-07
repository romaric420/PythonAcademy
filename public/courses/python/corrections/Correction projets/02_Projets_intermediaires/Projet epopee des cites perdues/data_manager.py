"""
Gère le chargement et la sauvegarde des données JSON.
"""

import json
from display_utils import display_message

def load_game_data(filename):
    """
    Charger les données du jeu depuis un fichier JSON.

    Args:
        filename (str): Chemin du fichier JSON.

    Returns:
        dict: Données chargées ou None en cas d'erreur.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        display_message(f"Erreur : Le fichier {filename} n'existe pas.", error=True)
        return None
    except json.JSONDecodeError:
        display_message(f"Erreur : Le fichier {filename} est invalide.", error=True)
        return None

def load_game_state(filename):
    """
    Charger l'état du jeu depuis un fichier JSON.

    Args:
        filename (str): Chemin du fichier JSON.

    Returns:
        dict: État du jeu ou None si le fichier n'existe pas.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        display_message(f"Erreur : Le fichier {filename} est invalide.", error=True)
        return None

def save_game_state(filename, game_state):
    """
    Sauvegarder l'état du jeu dans un fichier JSON.

    Args:
        filename (str): Chemin du fichier JSON.
        game_state (dict): État du jeu à sauvegarder.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(game_state, file, indent=4, ensure_ascii=False)
    except Exception as e:
        display_message(f"Erreur lors de la sauvegarde : {str(e)}", error=True)
