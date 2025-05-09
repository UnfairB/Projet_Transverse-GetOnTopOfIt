import pygame as pg
import pytmx
from settings import TILE_SIZE # GREEN is not used here anymore

class Platform(pg.sprite.Sprite):
    """
    Représente une plateforme de collision simple.
    """
    def __init__(self, x, y, width, height):
        """
        Initialise une plateforme.
        :param x, y: Coordonnées du coin supérieur gauche.
        :param width, height: Dimensions de la plateforme.
        """
        super().__init__()
        self.rect = pg.Rect(x, y, width, height)


class Map:
    """
    Classe pour charger et afficher la carte du jeu à partir d'un fichier TMX.
    Génère également les objets de collision à partir des calques de tuiles.
    """
    def __init__(self, game_state, filename):
        """
        Initialise la carte.
        :param game_state: Référence à l'instance GameState.
        :param filename: Chemin vers le fichier .tmx de la carte.
        """
        self.game_state = game_state
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        # Noms des calques de tuiles qui doivent générer des collisions
        self.collidable_layer_names = ["Calque de Tuiles 1"]


    def render(self, surface, camera):
        """
        Dessine toutes les tuiles visibles de la carte sur la surface donnée,
        en tenant compte de la position de la caméra.
        :param surface: Surface Pygame sur laquelle dessiner.
        :param camera: Objet Camera pour appliquer le décalage.
        """
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, item in layer.tiles(): # item can be a GID (int) or an image (Surface)
                    if item: # Check if there's a tile/image
                        if isinstance(item, pg.Surface): # If item is already a Surface (image)
                            tile_image = item
                        else: # Otherwise, item should be a GID (int)
                            tile_image = self.tmx_data.get_tile_image_by_gid(item)
                        
                        if tile_image:
                            # Appliquer le décalage de la caméra à la position de la tuile
                            tile_rect = pg.Rect(x * self.tile_width, 
                                                y * self.tile_height, 
                                                self.tile_width, 
                                                self.tile_height)
                            surface.blit(tile_image, camera.apply(tile_rect))

    def load_map_objects(self):
        """
        Charge les objets de la carte, en particulier les plateformes de collision
        générées à partir des calques de tuiles spécifiés.
        """
        for layer in self.tmx_data.layers: 
            if isinstance(layer, pytmx.TiledTileLayer) and layer.name in self.collidable_layer_names:
                for x, y, gid in layer.tiles(): # x, y are tile coordinates (columns, rows)
                    if gid != 0: # If a tile exists at this position (non-zero GID)
                        # Create a collision platform for this tile
                        platform_x = x * self.tile_width
                        platform_y = y * self.tile_height
                        
                        platform = Platform(platform_x, platform_y, self.tile_width, self.tile_height)
                        
                        self.game_state.platforms.add(platform)

        if not self.game_state.platforms:
            print("Warning: No collision platforms were loaded.")
        else:
            # This print can be useful for final checks, but can be removed if too verbose for prod
            print(f"{len(self.game_state.platforms)} collision platforms loaded.")


    def get_map_dimensions(self):
        """
        Retourne les dimensions de la carte en pixels.
        """
        return self.width, self.height