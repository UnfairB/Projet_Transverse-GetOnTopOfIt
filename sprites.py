# sprites.py
import pygame as pg
from settings import *

class Platform(pg.sprite.Sprite):
    """
    Classe pour représenter une plateforme dans le jeu.
    Hérite de pygame.sprite.Sprite pour une gestion facile des groupes de sprites.
    Utilisée principalement pour la détection de collision.
    """
    def __init__(self, x, y, width, height, color=GREEN, visible=False):
        """
        Initialise une plateforme.
        :param x: Position x (coin supérieur gauche) de la plateforme.
        :param y: Position y (coin supérieur gauche) de la plateforme.
        :param width: Largeur de la plateforme.
        :param height: Hauteur de la plateforme.
        :param color: Couleur de la plateforme (si visible).
        :param visible: Si la plateforme doit avoir une image visible.
                        Typiquement False si la carte TMX gère le visuel.
        """
        super().__init__() # Appel du constructeur de la classe parente (Sprite)
        if visible:
            self.image = pg.Surface((width, height)) # Crée une surface pour l'image de la plateforme
            self.image.fill(color) # Remplit la surface avec la couleur spécifiée
        else:
            # Si non visible, on peut utiliser une image transparente ou très petite
            # ou simplement s'assurer qu'elle n'est pas ajoutée au groupe de dessin principal.
            # Pour la robustesse de Sprite, elle doit avoir une image et un rect.
            self.image = pg.Surface((width, height), pg.SRCALPHA) # Surface transparente
            self.image.fill((0,0,0,0)) # Entièrement transparent

        self.rect = self.image.get_rect() # Obtient le rectangle délimitant l'image
        self.rect.x = x # Définit la position x du rectangle
        self.rect.y = y # Définit la position y du rectangle
