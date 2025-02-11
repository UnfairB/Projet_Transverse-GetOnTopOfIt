import pygame

class Spear(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Sprites/lance.png')
        self.rect = self.image.get_rect()
        self.rect.x = 2000
        self.rect.y = 2000
        self.direction = 1
