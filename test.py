# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 21:58:26 2024

@author: tomyj
"""
import pygame
import sys
from menu import Menu
from map import Map

FPS = 60

LARGEUR = 736
LONGUEUR = 1088

class Maitresse:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LONGUEUR, LARGEUR))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager('accueil')
        self.spawn = Map(self.screen,self.gameStateManager,'TileMap/zone0.tmx')
        self.accueil = Menu(self.screen,self.gameStateManager)

        self.states = {'accueil':self.accueil,'spawn':self.spawn}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #self.states[self.gameStateManager.get_state()].run()
            current_state = self.states[self.gameStateManager.get_state()]
            if isinstance(current_state, Map):
                current_state.run(self.screen)
            else:
                current_state.run()

            pygame.display.update()
            self.clock.tick(FPS)

class GameStateManager:
    def __init__(self,currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self,state):
        self.currentState = state

if __name__ == "__main__":
    current = Maitresse()
    current.run()