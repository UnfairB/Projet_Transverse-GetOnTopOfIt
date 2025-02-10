import pygame
from personnage import Player
from javelot import Spear

#Classe qui va représenter notre jeu
class Game:
    def __init__(self):
        # Initialisation du personnage
        self.perso = Player()
        self.javelot = Spear(self.perso.rect.x,self.perso.rect.y)
        self.pressed = {}