import pygame

class Tiles:
    def __init__(self):
        self.scene_actu = 1

    def level(self,player_y):
        if player_y >= 720:
            self.scene_actu += 1
        elif player_y <= 0:
            self.scene_actu -= 1