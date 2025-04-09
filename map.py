import pygame
import pytmx

RED = (255,0,0)

class Map:
    def __init__(self,display,gameStateManager,map_file):
        self.display = display
        self.gameStateManager = gameStateManager
        self.tmx_data = pytmx.load_pygame(map_file, pixelalpha=True)

    def run(self,surface):
        # Fond blanc (provisoire)
        self.display.fill('blue')

        # Récupère les positions x,y et les cliques de la souris à chaque frame
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()


        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight))

        # Cacher le curseur de la souris
        pygame.mouse.set_visible(False)

        # Remplace la souris par un viseur (un cercle rouge)
        pygame.draw.circle(self.display, RED, (mouse_pos), 10, 2)