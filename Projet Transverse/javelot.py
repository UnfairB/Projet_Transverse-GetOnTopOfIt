import pygame
import math

class Spear(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.IsReturning = False
        self.IsThrown = False
        self.IsPlatform = False
        self.image = pygame.image.load('Sprites/lance.png')
        self.rect = self.image.get_rect()
        self.rect.x = 2000
        self.rect.y = 2000
        self.throw_speed = 15
        self.velocity_x = 0
        self.velocity_y = 0

    def lancer_javelot(self, player_x, player_y, mouse_x, mouse_y):

        if self.IsPlatform:

            #Si le javelot est déjà lancé, on le renvoie
            self.IsReturning = True
            self.IsPlatform = False

        elif not self.IsThrown and not self.IsReturning:

            #Sinon, on le lance normalement
            self.IsThrown = True
            self.IsReturning = False

        if self.IsThrown and not self.IsReturning:

            #Positionne la javelot juste au dessus du joueur
            self.rect.x = player_x + 10
            self.rect.y = player_y - 10

            # Calculer l'angle de tir
            dx = mouse_x - player_x
            dy = mouse_y - player_y
            angle = math.atan2(dy, dx)

             # Initialiser la vitesse du javelot
            self.velocity_x = self.throw_speed * math.cos(angle)
            self.velocity_y = self.throw_speed * math.sin(angle)

    def javelot_maj(self,player_x,player_y,platforms):
        if self.IsThrown and not self.IsReturning:

            # Déplacement du javelot
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y

            # Détecte la collision avec les plateformes
            for platform in platforms:
                if self.rect.colliderect(platform):
                    self.IsPlatform = True
                    self.IsThrown = False
                    break

        elif self.IsReturning:

            #Retour du javelot au personnage
            dx = player_x - self.rect.x
            dy = player_y - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            #Si le javelot est assez proche du personnage on le vire de l'écran
            if distance < 10:
                self.IsThrown = False
                self.IsReturning = False
                self.IsPlatform = False
                self.rect.x = 2000
                self.rect.y = 2000

            #Sinon on continue de le rapprocher vers le personnage
            else:
                self.rect.x += (dx / distance) * self.throw_speed
                self.rect.y += (dy / distance) * self.throw_speed