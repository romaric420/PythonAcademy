"""
Fonctions utilitaires pour gérer les affichages dans le jeu.
"""

import os
import time
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans la console
init()

def clear_screen():
    """Effacer l'écran de la console."""
    os.system("cls" if os.name == "nt" else "clear")

def display_title(title):
    """Afficher un titre avec une mise en forme."""
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{title.center(50)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def display_menu(game):
    """Afficher le menu principal du jeu."""
    clear_screen()
    display_title("Menu Principal")
    print(f"{Fore.GREEN}Points de vie : {game.game_state['player']['health']}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Force : {game.game_state['player']['strength']}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Lieu actuel : {game.game_state['current_location'] or 'Aucun'}{Style.RESET_ALL}")
    print("\nOptions :")
    print("1. Explorer un lieu")
    print("2. Interagir avec un personnage")
    print("3. Gérer l'inventaire")
    print("4. Voir les quêtes")
    print("5. Valider une quête")
    print("6. Sauvegarder")
    print("7. Quitter")

def display_message(message, error=False):
    """Afficher un message avec une mise en forme."""
    color = Fore.RED if error else Fore.GREEN
    print(f"{color}{message}{Style.RESET_ALL}")

def display_location(location):
    """Afficher les détails d'un lieu."""
    print(f"{Fore.YELLOW}Lieu : {location['nom']}{Style.RESET_ALL}")
    print(f"Description : {location['description']}")
    if "ressources" in location:
        print(f"Ressources disponibles : {', '.join(location['ressources'])}")
    if "ennemis" in location:
        print(f"Ennemis possibles : {', '.join(location['ennemis'])}")
    print(f"{Fore.YELLOW}{'=' * 50}{Style.RESET_ALL}")

def display_character(character):
    """Afficher les détails d'un personnage."""
    print(f"{Fore.MAGENTA}Personnage : {character['nom']} ({character['type']}){Style.RESET_ALL}")
    print(f"Force : {character['force']}")
    print(f"Dialogue : {character['dialogue']}")
    if "cout" in character:
        print(f"Coût pour engager : {character['cout']['quantite']} {character['cout']['ressource']}")
    print(f"{Fore.MAGENTA}{'=' * 50}{Style.RESET_ALL}")

def display_combat(player, enemy):
    """Afficher les détails d'un combat."""
    print(f"{Fore.RED}=== COMBAT ==={Style.RESET_ALL}")
    print(f"Joueur (Force : {player['strength']}) vs {enemy['nom']} (Force : {enemy['force']})")

def display_inventory(inventory):
    """Afficher l'inventaire du joueur."""
    print(f"{Fore.CYAN}=== INVENTAIRE ==={Style.RESET_ALL}")
    if not inventory:
        print("Votre inventaire est vide.")
    else:
        for resource, amount in inventory.items():
            print(f"{resource.capitalize()} : {amount}")
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def display_quests(quests):
    """Afficher les quêtes actives avec leur progression."""
    print(f"{Fore.CYAN}=== QUÊTES ==={Style.RESET_ALL}")
    if not quests:
        print("Aucune quête active.")
    else:
        for quest in quests:
            print(f"Quête : {quest['nom']}")
            print(f"Description : {quest['description']}")
            print(f"Récompense : {quest['recompense']['quantite']} {quest['recompense']['type']}")
            if "objectif" in quest:
                current = quest.get("progression", 0)
                required = quest["objectif"]["quantite"]
                print(f"Progression : {current}/{required} {quest['objectif']['ressource']}")
            print("-" * 30)
    print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def wait_for_input():
    """Attendre que le joueur appuie sur Entrée pour continuer."""
    input(f"{Fore.YELLOW}Appuyez sur Entrée pour revenir au menu principal...{Style.RESET_ALL}")