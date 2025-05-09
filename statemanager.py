import pygame as pg
from states import MenuState, GameState, PauseState # Importer les classes d'état

class StateManager:
    """
    Gère la pile d'états du jeu et les transitions.
    """
    def __init__(self, game_instance):
        self.game = game_instance # Référence à l'instance principale du jeu
        self.states_map = { # Dictionnaire pour stocker les instances des états
            "menu": MenuState(self, self.game),
            "game": GameState(self, self.game),
            "pause": PauseState(self, self.game)
        }
        self.state_stack = [] # Pile pour gérer les états (ex: pause par-dessus jeu)
        
        # Démarrer avec l'état du menu
        self.push_state("menu") 

    def get_active_state(self):
        """ Retourne l'état actif (au sommet de la pile). """
        return self.state_stack[-1] if self.state_stack else None

    def push_state(self, state_key):
        """ Ajoute un état au sommet de la pile et l'active. """
        if self.state_stack:
            self.state_stack[-1].exit_state() # Notifie l'ancien état actif (s'il y en a un)
        
        state = self.states_map.get(state_key)
        if state:
            self.state_stack.append(state)
            state.enter_state() # Notifie le nouvel état actif
        else:
            print(f"Erreur: Clé d'état inconnue '{state_key}'")

    def pop_state(self):
        """ Retire l'état au sommet de la pile. """
        if self.state_stack:
            exiting_state = self.state_stack.pop()
            exiting_state.exit_state()
            if self.state_stack: # Si la pile n'est pas vide après le pop
                self.state_stack[-1].enter_state() # Notifie le nouvel état actif (celui en dessous)
            else: # Si la pile est vide, cela pourrait signifier quitter le jeu ou une erreur
                print("Avertissement: Pile d'états vide après pop_state.")
                self.game.running = False # Comportement par défaut: quitter si plus d'états
        else:
            print("Avertissement: Tentative de pop_state sur une pile vide.")


    def set_state(self, state_key):
        """ Change l'état actif (efface la pile et met le nouvel état). """
        while self.state_stack: # Vide la pile
            exiting_state = self.state_stack.pop()
            exiting_state.exit_state()
        
        self.push_state(state_key) # Ajoute le nouvel état

    def handle_events(self, events):
        active_state = self.get_active_state()
        if active_state:
            active_state.handle_events(events)

    def update(self, dt):
        active_state = self.get_active_state()
        if active_state:
            active_state.update(dt)

    def draw(self, surface):
        # Dessine tous les états dans la pile, du bas vers le haut,
        # pour que les états superposés (comme la pause) se dessinent correctement.
        for state in self.state_stack:
            state.draw(surface)
        # Si vous voulez que seul l'état actif dessine, commentez la boucle ci-dessus et décommentez ci-dessous:
        # active_state = self.get_active_state()
        # if active_state:
        #     active_state.draw(surface)
