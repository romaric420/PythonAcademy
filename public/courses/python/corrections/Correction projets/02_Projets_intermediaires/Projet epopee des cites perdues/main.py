#!/usr/bin/env python3
"""
Point d'entrée principal du jeu 'L’Épopée des Cités Perdues'.
Gère la boucle principale et les interactions avec le joueur.
"""

import sys
from game_logic import Game
from display_utils import clear_screen, display_title, display_menu, display_message, wait_for_input
from data_manager import load_game_data, load_game_state, save_game_state

def main():
    """Fonction principale pour démarrer et exécuter le jeu."""
    clear_screen()
    display_title("L’Épopée des Cités Perdues")

    # Charger les données du jeu depuis data.json
    game_data = load_game_data("data.json")
    if not game_data:
        display_message("Erreur : Impossible de charger les données du jeu.", error=True)
        sys.exit(1)

    # Charger l'état du jeu depuis game_state.json (ou démarrer une nouvelle partie)
    game_state = load_game_state("game_state.json")
    if not game_state:
        display_message("Aucune sauvegarde trouvée. Démarrage d'une nouvelle partie...")
        game_state = {
            "player": {"health": 100, "strength": 5, "inventory": {}},
            "current_location": None,
            "allies": [],
            "quests": []
        }

    # Initialiser le jeu
    game = Game(game_data, game_state)

    # Boucle principale du jeu
    while True:
        display_menu(game)
        choice = input("Votre choix : ").strip().lower()

        if choice == "1":
            game.explore_location()
            wait_for_input()  # Attendre l'entrée du joueur avant de revenir au menu
        elif choice == "2":
            game.interact_with_character()
            wait_for_input()
        elif choice == "3":
            game.manage_inventory()
            wait_for_input()
        elif choice == "4":
            game.display_quests()
            wait_for_input()
        elif choice == "5":
            game.validate_quest()
            wait_for_input()
        elif choice == "6":
            display_message("Sauvegarde en cours...")
            save_game_state("game_state.json", game.game_state)
            display_message("Jeu sauvegardé !")
            wait_for_input()
        elif choice == "7":
            display_message("Merci d'avoir joué ! À bientôt !")
            save_game_state("game_state.json", game.game_state)
            break
        else:
            display_message("Choix invalide. Veuillez réessayer.", error=True)
            wait_for_input()

if __name__ == "__main__":
    main()
