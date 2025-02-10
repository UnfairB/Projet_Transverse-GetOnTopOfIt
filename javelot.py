import pygame

class Spear(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('Sprites/lance.png')
        self.rect = self.image.get_rect()
        self.rect.x = x-10
        self.rect.y = y-25
        self.direction = 1
