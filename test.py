# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 21:58:26 2024

@author: tomyj
"""
import pygame
import sys
from menu import Menu

FPS = 60

LARGEUR = 720
LONGUEUR = 1080

class Maitresse:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LONGUEUR, LARGEUR))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager('accueil')
        self.start = Start(self.screen,self.gameStateManager)
        self.level = Level(self.screen,self.gameStateManager)
        self.accueil = Menu(self.screen,self.gameStateManager)

        self.states = {'start':self.start,'level':self.level,'accueil':self.accueil}
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)

#########################################################
class Level:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('blue')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('start')
#########################################################
#########################################################
class Start:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill('red')
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gameStateManager.set_state('level')
#########################################################

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