# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 21:58:26 2024

@author: tomyj
"""
import pygame as pg
import sys
from settings import *
from statemanager import StateManager # Importer le StateManager

class Game:
    """
    Classe principale du jeu.
    Gère l'initialisation, la boucle de jeu, et délègue aux états via le StateManager.
    """
    def __init__(self):
        """
        Initialise Pygame, la fenêtre de jeu et les variables de base du jeu.
        """
        pg.init() 
        pg.mixer.init() 
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) 
        pg.display.set_caption(TITLE) 
        self.clock = pg.time.Clock() 
        self.running = True # Variable pour contrôler la boucle principale du jeu
        
        try:
            self.font = pg.font.Font(None, 30) 
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la police: {e}")
            self.font = None 

        # Initialisation du StateManager
        self.state_manager = StateManager(self) # Passe l'instance de Game au StateManager

    def run(self):
        """
        Boucle de jeu principale.
        S'exécute tant que self.running est True.
        Délègue la logique aux états via le StateManager.
        """
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 # Delta-temps

            # Gestion des événements via le StateManager
            events = pg.event.get() # Récupère tous les événements une fois par frame
            self.state_manager.handle_events(events)

            # Mise à jour de la logique via le StateManager
            self.state_manager.update(dt)

            # Dessin via le StateManager
            self.state_manager.draw(self.screen)
            
            pg.display.flip() # Met à jour l'écran

if __name__ == '__main__':
    g = Game() 
    g.run() # Lance la boucle principale du jeu
    
    pg.quit() 
    sys.exit()