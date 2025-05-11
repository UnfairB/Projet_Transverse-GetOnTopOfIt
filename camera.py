import pygame as pg
from settings import WIDTH, HEIGHT

class Camera:
    """
    Classe pour gérer la caméra du jeu. La caméra suit le joueur
    """
    def __init__(self, map_width_pixels, map_height_pixels):
        """
        Initialiser la caméra
        """
        # Le rectangle de la caméra représente la "vue" sur le monde du jeu
        self.camera_rect = pg.Rect(0, 0, map_width_pixels, map_height_pixels)
        self.map_width = map_width_pixels
        self.map_height = map_height_pixels

    def apply(self, entity_rect):
        """
        Appliquer la transformation de la caméra au rectangle d'une entité
        Retourne un nouveau rectangle décalé pour le dessin
        """
        return entity_rect.move(self.camera_rect.topleft)

    def update(self, target_rect):
        """
        Mettre à jour la position de la caméra pour qu'elle soit centrée sur la cible (target_rect) 
        La caméra ne peut pas montrer les zones en dehors des limites de la carte
        """
        # Calculer la position x pour centrer la cible, puis la décale
        # Le décalage est négatif par rapport à la position de la cible
        x = -target_rect.centerx + int(WIDTH / 2)
        y = -target_rect.centery + int(HEIGHT / 2)

        # Empêche la caméra de montrer des zones en dehors de la carte.
        x = min(0, x)
        y = min(0, y)
        
        x = max(-(self.map_width - WIDTH), x)
        y = max(-(self.map_height - HEIGHT), y)
        
        self.camera_rect.topleft = (x, y)

    def screen_to_world(self, screen_pos):
        """
        Convertir les coordonnées de l'écran en coordonnées du monde
        """
        world_x = screen_pos[0] - self.camera_rect.x
        world_y = screen_pos[1] - self.camera_rect.y
        return (world_x, world_y)
