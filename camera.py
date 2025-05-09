import pygame as pg
from settings import WIDTH, HEIGHT

class Camera:
    """
    Classe pour gérer la caméra du jeu.
    La caméra suit une cible (généralement le joueur) et ajuste les coordonnées de dessin
    pour donner l'illusion que la caméra se déplace sur une grande carte.
    """
    def __init__(self, map_width_pixels, map_height_pixels):
        """
        Initialise la caméra.
        :param map_width_pixels: Largeur totale de la carte en pixels.
        :param map_height_pixels: Hauteur totale de la carte en pixels.
        """
        # Le rectangle de la caméra représente la "vue" sur le monde du jeu.
        # Ses coordonnées (x, y) sont l'offset par lequel le monde doit être décalé.
        # Si camera.rect.x est -10, le monde est dessiné 10 pixels vers la gauche.
        self.camera_rect = pg.Rect(0, 0, map_width_pixels, map_height_pixels)
        self.map_width = map_width_pixels
        self.map_height = map_height_pixels

    def apply(self, entity_rect):
        """
        Applique la transformation de la caméra au rectangle d'une entité.
        Retourne un nouveau rectangle décalé pour le dessin.
        :param entity_rect: Le rectangle de l'entité (ex: sprite.rect) dans les coordonnées du monde.
        :return: Un nouveau pg.Rect avec les coordonnées pour le dessin à l'écran.
        """
        return entity_rect.move(self.camera_rect.topleft)

    def update(self, target_rect):
        """
        Met à jour la position de la caméra pour qu'elle soit centrée sur la cible (target_rect).
        La caméra est contrainte de ne pas montrer de zones en dehors des limites de la carte.
        :param target_rect: Le rectangle de la cible à suivre (ex: player.rect).
        """
        # Calcule la position x pour centrer la cible, puis la décale.
        # Le décalage est négatif par rapport à la position de la cible.
        x = -target_rect.centerx + int(WIDTH / 2)
        y = -target_rect.centery + int(HEIGHT / 2)

        # Contraint le défilement aux limites de la carte.
        # Empêche la caméra de montrer des zones en dehors de la carte.
        x = min(0, x)  # Limite gauche (ne pas aller plus à droite que le bord gauche de la carte)
        y = min(0, y)  # Limite haute (ne pas aller plus bas que le bord haut de la carte)
        
        # Limite droite: ne pas aller plus à gauche que le bord droit de la carte moins la largeur de l'écran.
        x = max(-(self.map_width - WIDTH), x)
        # Limite basse: ne pas aller plus haut que le bord bas de la carte moins la hauteur de l'écran.
        y = max(-(self.map_height - HEIGHT), y)
        
        # Met à jour la position de la caméra (son coin supérieur gauche, qui est l'offset)
        self.camera_rect.topleft = (x, y)

    def screen_to_world(self, screen_pos):
        """
        Convertit les coordonnées de l'écran en coordonnées du monde.
        :param screen_pos: Tuple (x, y) des coordonnées à l'écran.
        :return: Tuple (x, y) des coordonnées dans le monde du jeu.
        """
        world_x = screen_pos[0] - self.camera_rect.x
        world_y = screen_pos[1] - self.camera_rect.y
        return (world_x, world_y)
