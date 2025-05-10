import pygame as pg
from settings import *
from player import Player
from map import Map
from camera import Camera
from ui_elements import Button
from javelin import Javelin
import os
from settings import GAME_VOLUME  # Import the global volume variable

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
        start_y = HEIGHT // 2 - button_height - spacing

        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y,
            button_width, button_height,
            "Jouer", self.start_game, self.game.font
        ))
        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y + button_height + spacing,
            button_width, button_height,
            "Options", self.open_settings, self.game.font  # Renamed to "Option"
        ))
        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + spacing),
            button_width, button_height,
            "Quitter", self.quit_game, self.game.font
        ))

    def start_game(self):
        self.manager.set_state("game")

    def open_settings(self):
        self.manager.set_state("settings")

    def quit_game(self):
        self.game.running = False

    def enter_state(self):
        super().enter_state()
        # Ensure no music is played in the menu
        pg.mixer.music.stop()

    def exit_state(self):
        super().exit_state()
        # No need to handle music here

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
        self.music_playing = False

    def enter_state(self):
        super().enter_state()
        # Start playing the music when entering the game state
        if not self.music_playing:
            try:
                pg.mixer.music.load("Music/Benz.wav")  # Load the music file
                pg.mixer.music.set_volume(GAME_VOLUME)  # Set the volume based on the global variable
                pg.mixer.music.play(-1)  # Play in a loop
                self.music_playing = True
            except pg.error as e:
                print(f"Erreur: Impossible de charger ou jouer la musique 'Music/Benz.wav': {e}")

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.javelins_flying = pg.sprite.Group()

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

        map_width_pixels, map_height_pixels = self.map.get_map_dimensions()
        self.camera = Camera(map_width_pixels, map_height_pixels)

        spawn_point = self.find_spawn_point()
        player_start_x, player_start_y = TILE_SIZE * 2, self.map.height - TILE_SIZE * 5
        if spawn_point:
            player_start_x, player_start_y = spawn_point.x, spawn_point.y
        else:
            print("Avertissement (GameState): Aucun objet 'SpawnPoint' trouvé. Position par défaut.")

        self.player = Player(self, player_start_x, player_start_y)
        self.all_sprites.add(self.player)

    def exit_state(self):
        super().exit_state()
        # Stop the music when exiting the game state
        if self.music_playing:
            pg.mixer.music.stop()
            self.music_playing = False

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
        super().update(dt)
        # Dynamically update the volume of the music
        if self.music_playing:
            pg.mixer.music.set_volume(GAME_VOLUME)

        if not self.player or not self.camera or not self.all_sprites:
            return

        self.all_sprites.update(dt)
        self.camera.update(self.player.rect)

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


class SettingsState(State):
    """
    État du menu des paramètres.
    """
    def __init__(self, manager, game_instance):
        super().__init__(manager, game_instance)
        self.overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))
        self.title_font = pg.font.Font(None, 74)
        self.slider_rect = pg.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 10)  # Slider bar
        self.knob_rect = pg.Rect(self.slider_rect.x + self.slider_rect.width - 10, self.slider_rect.y - 5, 20, 20)  # Slider knob
        self.dragging = False
        self.volume = 1.0  # Default volume (100%)
        self.setup_buttons()

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        start_y = HEIGHT // 2 + 100

        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y,
            button_width, button_height,
            "Menu", self.return_to_menu, self.game.font
        ))

    def return_to_menu(self):
        self.manager.set_state("menu")

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.knob_rect.collidepoint(event.pos):
                    self.dragging = True
            elif event.type == pg.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pg.MOUSEMOTION and self.dragging:
                # Drag the knob within the slider bar
                self.knob_rect.x = max(self.slider_rect.x, min(event.pos[0] - self.knob_rect.width // 2, self.slider_rect.x + self.slider_rect.width - self.knob_rect.width))
                
                # Update the volume based on the knob's position
                # Ensure the volume is mapped correctly to the range [0.0, 1.0]
                self.volume = (self.knob_rect.x - self.slider_rect.x) / (self.slider_rect.width - self.knob_rect.width)
                self.volume = max(0.0, min(self.volume, 1.0))  # Clamp the volume to [0.0, 1.0]

                global GAME_VOLUME
                GAME_VOLUME = self.volume  # Update the global volume
                pg.mixer.music.set_volume(GAME_VOLUME)  # Adjust the music volume in real-time

    def draw(self, surface):
        # Fill the background with the same color as the main menu
        surface.fill(BEIGE)

        # Draw the title
        title_surf = self.title_font.render("Settings", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(title_surf, title_rect)

        # Draw the slider bar
        pg.draw.rect(surface, BLACK, self.slider_rect)
        # Draw the slider knob
        pg.draw.ellipse(surface, RED, self.knob_rect)

        # Draw the volume percentage
        if self.game.font:
            volume_text = f"Volume: {int(self.volume * 100)}%"
            volume_surf = self.game.font.render(volume_text, True, BLACK)
            volume_rect = volume_surf.get_rect(center=(WIDTH // 2, self.slider_rect.y - 30))
            surface.blit(volume_surf, volume_rect)

        # Draw the buttons
        for button in self.buttons:
            button.draw(surface)
