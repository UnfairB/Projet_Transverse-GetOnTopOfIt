import pygame
from personnage import Player

#Classe qui va représenter notre jeu
class Game:
    def __init__(self):
        # Initialisation du personnage
        self.perso = Player()
        self.pressed = {}