import pygame as pg
from settings import *
from player import Player
from map import Map
from camera import Camera
from ui_elements import Button
from javelin import Javelin
from monstre import Zombie
import os

class State:
    """
    Classe de base pour tous les états du jeu.
    """
    def __init__(self, manager, game_instance):
        self.manager = manager
        self.game = game_instance
        self.buttons = []

    def handle_events(self, events):
        """ Gère les événements pour cet état. """
        for event in events:
            if event.type == pg.QUIT:
                self.game.running = False
            for button in self.buttons:
                if button.handle_event(event):
                    break

    def update(self, dt):
        """ Met à jour la logique de cet état. """
        pass

    def draw(self, surface):
        """ Dessine cet état sur la surface donnée. """
        surface.fill(LIGHTBLUE)
        for button in self.buttons:
            button.draw(surface)

    def enter_state(self):
        """ Appelé lorsque l'état devient actif. """
        pass

    def exit_state(self):
        """ Appelé lorsque l'état est quitté. """
        pass


class MenuState(State):
    """
    État du menu principal.
    """
    def __init__(self, manager, game_instance):
        super().__init__(manager, game_instance)
        self.title_font = pg.font.Font(None, 74)
        self.setup_buttons()

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        spacing = 20
        start_y = HEIGHT // 2 - button_height - spacing // 2

        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y,
            button_width, button_height,
            "Jouer", self.start_game, self.game.font
        ))
        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y + button_height + spacing,
            button_width, button_height,
            "Quitter", self.quit_game, self.game.font
        ))

    def start_game(self):
        self.manager.set_state("game")

    def quit_game(self):
        self.game.running = False

    def draw(self, surface):
        super().draw(surface)
        title_surf = self.title_font.render(TITLE, True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(title_surf, title_rect)


class GameState(State):
    """
    État principal du jeu où se déroule la partie.
    """
    def __init__(self, manager, game_instance):
        super().__init__(manager, game_instance)
        self.all_sprites = None
        self.platforms = None
        self.player = None
        self.map = None
        self.camera = None
        self.javelins_flying = None
        self.monsters = None
        self.spikes = None  # Ajout pour les pics

    def enter_state(self):
        super().enter_state()
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.javelins_flying = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.spikes = pg.sprite.Group()  # Initialisation du groupe de pics

        map_file_path = ""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            map_file_path = os.path.join(base_dir, "TileMap", "game_map.tmx")
            
            self.map = Map(self, map_file_path)
        except FileNotFoundError:
            print(f"Erreur critique: Fichier TMX introuvable ({map_file_path}).")
            print("Vérifications suggérées:")
            print(f"1. Le fichier TMX existe-t-il à '{map_file_path}'?")
            print(f"2. Les images des tilesets sont-elles présentes dans '{os.path.dirname(map_file_path)}'?")
            self.manager.set_state("menu")
            return
        except Exception as e:
            print(f"Erreur lors du chargement de la carte TMX ({map_file_path}): {e}.")
            self.manager.set_state("menu")
            return

        self.map.load_map_objects()

        # --- Ajout : Charger les pics depuis la map avec une image ---
        if hasattr(self.map, "tmx_data"):
            try:
                spike_img = pg.image.load("TileMap/picpic.png").convert_alpha()
            except Exception as e:
                print(f"Erreur chargement image pic: {e}")
                spike_img = None
            for layer in self.map.tmx_data.objectgroups:
                for obj in layer:
                    if obj.name == "picpic":
                        spike_sprite = pg.sprite.Sprite()
                        if spike_img:
                            spike_sprite.image = pg.transform.scale(spike_img, (int(obj.width), int(obj.height)))
                        else:
                            spike_sprite.image = pg.Surface((obj.width, obj.height), pg.SRCALPHA)
                        spike_sprite.rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.spikes.add(spike_sprite)

        map_width_pixels, map_height_pixels = self.map.get_map_dimensions()
        self.camera = Camera(map_width_pixels, map_height_pixels)

        spawn_point = self.find_spawn_point()
        player_start_x, player_start_y = 810, 6200 #Coordonnées de départ du personnage
        if spawn_point:
            player_start_x, player_start_y = spawn_point.x, spawn_point.y
        else:
            print("Avertissement (GameState): Aucun objet 'SpawnPoint' trouvé. Position par défaut.")

        self.player = Player(self, player_start_x, player_start_y)
        self.all_sprites.add(self.player)

        # Différents sprites de marche du zombie
        zombie_images = [
            pg.image.load("Sprites/Zombie1.png").convert_alpha(),
            pg.image.load("Sprites/Zombie2.png").convert_alpha(),
            pg.image.load("Sprites/Zombie3.png").convert_alpha(),
            pg.image.load("Sprites/Zombie4.png").convert_alpha(),
            pg.image.load("Sprites/Zombie5.png").convert_alpha(),
            pg.image.load("Sprites/Zombie6.png").convert_alpha(),
            pg.image.load("Sprites/Zombie7.png").convert_alpha(),
            pg.image.load("Sprites/Zombie8.png").convert_alpha(),
        ]
        #différent positionnement de départ des zombies avec toutes leurs caractéristiques
        zombie1 = Zombie(235, 4570, zombie_images, self.platforms, speed=80, walk_distance=110)
        zombie2 = Zombie(385, 1210, zombie_images, self.platforms, speed=80, walk_distance=225)
        # Ajout des zombies au groupe de sprites
        self.all_sprites.add(zombie1)
        self.all_sprites.add(zombie2) 
        self.monsters.add(zombie1)
        self.monsters.add(zombie2) 

    def find_spawn_point(self):
        if not hasattr(self, 'map') or not self.map.tmx_data:
            return None
        for layer in self.map.tmx_data.objectgroups:
            for obj in layer:
                if obj.name == "PlayerSpawn":
                    return obj
        return None

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_z:
                    if self.player:
                        self.player.jump()
                if event.key == pg.K_ESCAPE:
                    self.manager.push_state("pause")
                if event.key == pg.K_LSHIFT or event.key == pg.K_RSHIFT:
                    if self.player and self.player.active_javelin_sprite:
                        self.player.active_javelin_sprite.recall()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.player and self.camera:
                        mouse_screen_pos = event.pos
                        mouse_world_pos = self.camera.screen_to_world(mouse_screen_pos)
                        self.player.throw_javelin(mouse_world_pos)

    def update(self, dt):
        if not self.player or not self.camera or not self.all_sprites:
            return

        self.all_sprites.update(dt)
        self.camera.update(self.player.rect)

        # --- Collision joueur-monstre : recommencer la partie ---
        if self.monsters and pg.sprite.spritecollideany(self.player, self.monsters):
            self.manager.set_state("game")
        # --- Collision joueur-pics : recommencer la partie ---
        if self.spikes and pg.sprite.spritecollideany(self.player, self.spikes):
            self.manager.set_state("game")

    def draw(self, surface):
        if not self.map or not self.camera or not self.all_sprites or not self.player:
            surface.fill(BLACK)
            if self.game.font:
                err_surf = self.game.font.render("Erreur de chargement du jeu", True, RED)
                err_rect = err_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                surface.blit(err_surf, err_rect)
            return

        surface.fill(LIGHTBLUE)
        self.map.render(surface, self.camera)

        for sprite in self.all_sprites:
            if hasattr(sprite, 'image') and hasattr(sprite, 'rect'):
                surface.blit(sprite.image, self.camera.apply(sprite.rect))

        # --- Dessiner les pics ---
        if self.spikes:
            for spike in self.spikes:
                surface.blit(spike.image, self.camera.apply(spike.rect))

        if self.game.font:
            player_world_x = self.player.rect.x
            player_world_y = self.player.rect.y
            coord_text = f"Player X: {int(player_world_x)}, Y: {int(player_world_y)}"
            text_surface = self.game.font.render(coord_text, True, BLACK)
            surface.blit(text_surface, (10, 10))


class PauseState(State):
    """
    État du menu de pause.
    """
    def __init__(self, manager, game_instance):
        super().__init__(manager, game_instance)
        self.overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        self.title_font = pg.font.Font(None, 74)
        self.setup_buttons()

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        spacing = 20
        start_y = HEIGHT // 2 - button_height - spacing // 2

        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y,
            button_width, button_height,
            "Nouvelle partie", self.resume_game, self.game.font
        ))
        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y + button_height + spacing,
            button_width, button_height,
            "Retour Menu", self.quit_to_menu, self.game.font
        ))

    def resume_game(self):
        self.manager.pop_state()

    def quit_to_menu(self):
        self.manager.pop_state()
        self.manager.set_state("menu")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.resume_game()

    def draw(self, surface):
        surface.blit(self.overlay, (0, 0))

        title_surf = self.title_font.render("Pause", True, WHITE)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(title_surf, title_rect)

        for button in self.buttons:
            button.draw(surface)
