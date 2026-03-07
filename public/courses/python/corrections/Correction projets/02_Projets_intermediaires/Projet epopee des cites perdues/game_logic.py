"""
Contient les mécaniques principales du jeu : exploration, combat, gestion des ressources, etc.
"""

import random
from display_utils import display_message, display_location, display_character, display_combat, display_inventory, display_quests

class Game:
    """Classe principale pour gérer la logique du jeu."""

    def __init__(self, game_data, game_state):
        """
        Initialiser le jeu avec les données et l'état du jeu.

        Args:
            game_data (dict): Données chargées depuis data.json.
            game_state (dict): État du jeu (sauvegarde ou nouvelle partie).
        """
        self.game_data = game_data
        self.game_state = game_state
        self.locations = game_data["lieux"]
        self.characters = game_data["personnages"]
        self.resources = game_data["ressources"]
        self.quests = game_data["quetes"]

    def explore_location(self):
        """Permet au joueur d'explorer un lieu et de gérer les événements associés."""
        display_message("Lieux disponibles :")
        for idx, location in enumerate(self.locations, 1):
            print(f"{idx}. {location['nom']} - {location['description']}")

        try:
            choice = int(input("Choisir un lieu à explorer (numéro) : ")) - 1
            if 0 <= choice < len(self.locations):
                selected_location = self.locations[choice]
                self.game_state["current_location"] = selected_location["nom"]
                display_location(selected_location)

                # Récupérer des ressources
                self.collect_resources(selected_location)

                # Événement aléatoire (par exemple, rencontre avec un ennemi ou une quête)
                if random.random() < 0.5:  # 50% de chance
                    self.handle_event(selected_location)
            else:
                display_message("Choix invalide.", error=True)
        except ValueError:
            display_message("Veuillez entrer un numéro valide.", error=True)

    def handle_event(self, location):
        """Gérer un événement aléatoire dans un lieu (combat, quête, etc.)."""
        event_type = random.choice(["combat", "quest"])
        if event_type == "combat" and "ennemis" in location and location["ennemis"]:
            enemy_name = random.choice(location["ennemis"])
            enemy = next((char for char in self.characters if char["nom"] == enemy_name), None)
            if enemy:
                self.combat(enemy)
        elif event_type == "quest":
            available_quests = [q for q in self.quests if q["lieu"] == location["nom"] and q not in self.game_state["quests"]]
            if available_quests:
                quest = random.choice(available_quests)
                self.start_quest(quest)

    def combat(self, enemy):
        """Gérer un combat entre le joueur et un ennemi."""
        display_combat(self.game_state["player"], enemy)
        player_strength = self.game_state["player"]["strength"]
        enemy_strength = enemy["force"]

        if player_strength > enemy_strength:
            damage = random.randint(5, 15)
            self.game_state["player"]["health"] -= damage
            display_message(f"Vous avez vaincu {enemy['nom']} ! Mais vous perdez {damage} points de vie.")
        else:
            damage = random.randint(10, 20)
            self.game_state["player"]["health"] -= damage
            display_message(f"{enemy['nom']} vous a vaincu ! Vous perdez {damage} points de vie.", error=True)

        if self.game_state["player"]["health"] <= 0:
            display_message("Vous êtes mort... Fin de la partie.", error=True)
            exit()

    def interact_with_character(self):
        """Permet au joueur d'interagir avec un personnage."""
        display_message("Personnages disponibles :")
        for idx, char in enumerate(self.characters, 1):
            print(f"{idx}. {char['nom']} ({char['type']})")

        try:
            choice = int(input("Choisir un personnage à interagir (numéro) : ")) - 1
            if 0 <= choice < len(self.characters):
                selected_char = self.characters[choice]
                display_character(selected_char)
                if selected_char["type"] == "allié":
                    self.handle_ally(selected_char)
                else:
                    self.handle_enemy(selected_char)
            else:
                display_message("Choix invalide.", error=True)
        except ValueError:
            display_message("Veuillez entrer un numéro valide.", error=True)

    def handle_ally(self, ally):
        """Gérer l'interaction avec un allié (par exemple, payer pour de l'aide)."""
        if "cout" in ally:
            resource, cost = ally["cout"]["ressource"], ally["cout"]["quantite"]
            if resource in self.game_state["player"]["inventory"] and self.game_state["player"]["inventory"][resource] >= cost:
                self.game_state["player"]["inventory"][resource] -= cost
                self.game_state["player"]["strength"] += ally["force"]
                self.game_state["allies"].append(ally["nom"])
                display_message(f"{ally['nom']} rejoint votre équipe ! Votre force augmente de {ally['force']}.")
            else:
                display_message(f"Vous n'avez pas assez de {resource} pour engager {ally['nom']}.")
        else:
            display_message(f"{ally['nom']} n'a pas besoin de ressources pour vous aider.")

    def handle_enemy(self, enemy):
        """Gérer l'interaction avec un ennemi (combattre ou fuir)."""
        display_message("1. Combattre\n2. Fuir")
        choice = input("Votre choix : ").strip()
        if choice == "1":
            self.combat(enemy)
        elif choice == "2":
            if random.random() < 0.7:  # 70% de chance de fuir
                display_message(f"Vous avez réussi à fuir {enemy['nom']} !")
            else:
                display_message(f"Échec de la fuite ! {enemy['nom']} vous attaque !", error=True)
                self.combat(enemy)
        else:
            display_message("Choix invalide.", error=True)

    def manage_inventory(self):
        """Afficher et gérer l'inventaire du joueur."""
        display_inventory(self.game_state["player"]["inventory"])
        display_message(f"Points de vie : {self.game_state['player']['health']}\nForce : {self.game_state['player']['strength']}")

    def start_quest(self, quest):
        """Démarrer une quête et gérer ses objectifs."""
        display_message(f"Nouvelle quête : {quest['nom']}")
        display_message(quest["description"])
        self.game_state["quests"].append(quest)

    def collect_resources(self, location):
        """Récupérer des ressources dans un lieu et vérifier la progression des quêtes."""
        if "ressources" in location:
            for resource in location["ressources"]:
                amount = random.randint(1, 5)
                if resource not in self.game_state["player"]["inventory"]:
                    self.game_state["player"]["inventory"][resource] = 0
                self.game_state["player"]["inventory"][resource] += amount
                display_message(f"Vous avez collecté {amount} unités de {resource}.")
                # Vérifier si cela fait progresser une quête
                self.check_quest_progress(resource, amount)

    def check_quest_progress(self, resource, amount):
        """Vérifier si la collecte de ressources fait progresser une quête."""
        for quest in self.game_state["quests"]:
            if "objectif" in quest and quest["objectif"]["type"] == "collecter":
                if quest["objectif"]["ressource"] == resource:
                    # Mettre à jour la progression dans l'état du jeu
                    if "progression" not in quest:
                        quest["progression"] = 0
                    quest["progression"] += amount
                    required = quest["objectif"]["quantite"]
                    current = min(quest["progression"], required)  # Ne pas dépasser la quantité requise
                    display_message(f"Progression de la quête '{quest['nom']}' : {current}/{required}")
                    if current >= required:
                        display_message(f"Objectif de la quête '{quest['nom']}' atteint ! Vous pouvez maintenant valider la quête.")

    def validate_quest(self):
        """Permettre au joueur de valider une quête terminée."""
        display_message("Quêtes actives :")
        completable_quests = []
        for idx, quest in enumerate(self.game_state["quests"], 1):
            if "progression" in quest and quest["progression"] >= quest["objectif"]["quantite"]:
                completable_quests.append((idx, quest))
                print(f"{idx}. {quest['nom']} (Objectif atteint : {quest['progression']}/{quest['objectif']['quantite']})")
            else:
                current = quest.get("progression", 0)
                required = quest["objectif"]["quantite"]
                print(f"{idx}. {quest['nom']} (En cours : {current}/{required})")

        if not completable_quests:
            display_message("Aucune quête n'est prête à être validée.")
            return

        try:
            choice = int(input("Choisir une quête à valider (numéro) ou 0 pour annuler : ")) - 1
            if choice == -1:
                display_message("Validation annulée.")
                return
            if 0 <= choice < len(completable_quests):
                quest_idx, quest = completable_quests[choice]
                self.complete_quest(quest)
                # Retirer la quête des quêtes actives
                self.game_state["quests"].remove(quest)
                display_message(f"Quête '{quest['nom']}' validée et retirée de vos quêtes actives.")
            else:
                display_message("Choix invalide.", error=True)
        except ValueError:
            display_message("Veuillez entrer un numéro valide.", error=True)

    def complete_quest(self, quest):
        """Appliquer la récompense d'une quête terminée."""
        reward_type = quest["recompense"]["type"]
        reward_amount = quest["recompense"]["quantite"]
        if reward_type == "force":
            self.game_state["player"]["strength"] += reward_amount
            display_message(f"Récompense : Votre force augmente de {reward_amount} !")
        elif reward_type in self.game_state["player"]["inventory"]:
            if reward_type not in self.game_state["player"]["inventory"]:
                self.game_state["player"]["inventory"][reward_type] = 0
            self.game_state["player"]["inventory"][reward_type] += reward_amount
            display_message(f"Récompense : Vous gagnez {reward_amount} unités de {reward_type} !")
        else:
            display_message(f"Récompense : {reward_amount} {reward_type} ajoutés (non implémenté comme ressource).")

    def display_quests(self):
        """Afficher les quêtes actives avec leur progression."""
        display_quests(self.game_state["quests"])
        # Proposer de valider une quête si applicable
        if self.game_state["quests"]:
            display_message("Voulez-vous valider une quête terminée ?")
            display_message("1. Oui\n2. Non")
            choice = input("Votre choix : ").strip()
            if choice == "1":
                self.validate_quest()
