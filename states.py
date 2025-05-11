import pygame as pg
from settings import *
from player import Player
from map import Map
from camera import Camera
from ui_elements import Button
from javelin import Javelin
from monstre import Zombie
import os
from settings import GAME_VOLUME

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


class IntroState(State):
    """
    État d'introduction avec texte défilant et bouton "passer l'intro".
    """
    def __init__(self, manager, game_instance):
        super().__init__(manager, game_instance)
        self.font = pg.font.Font(None, 36)
        self.paragraphes = [
            "La fête faisait rage sur le mont Olympe, un banquet où les dieux se lâchaient complètement, oubliant toute retenue.",
            " Dionysos, le dieu du vin et de la fête, était au centre de l’attention, riant et plaisantant, tandis que les dieux se livraient à des excès de tous genres. Le vin coulait à flots, les mets se succédaient sans fin, et les danses étaient de plus en plus folles.",
            " Mais pour Zeus, le roi des dieux, c’était trop. Il voyait ses pairs sombrer dans la démesure, et l’harmonie de l’Olympe s’effondrer sous le poids des excès. Son regard, habituellement sage, se faisait de plus en plus sombre. Une colère sourde montait en lui, alors que la fête de Dionysos devenait un chaos qu’il ne pouvait plus supporter."
        ]
        self.current_paragraph = 0
        self.current_letter = 0
        self.displayed_text = ""
        self.last_update = pg.time.get_ticks()
        self.letter_delay = 40  # ms
        self.pause_time = 2000  # ms
        self.paused = False
        self.pause_start = 0
        self.finished = False
        self.skip_rect = pg.Rect(300, 500, 200, 50)
        self.skip_hover = False

    def enter_state(self):
        self.current_paragraph = 0
        self.current_letter = 0
        self.displayed_text = ""
        self.last_update = pg.time.get_ticks()
        self.paused = False
        self.pause_start = 0
        self.finished = False

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.game.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.skip_rect.collidepoint(event.pos):
                    self.finished = True

    def update(self, dt):
        if self.finished:
            self.manager.set_state("spawn")
            return

        now = pg.time.get_ticks()
        if self.paused:
            if now - self.pause_start >= self.pause_time:
                self.paused = False
                self.current_paragraph += 1
                self.current_letter = 0
                self.displayed_text = ""
                self.last_update = now
        elif self.current_paragraph < len(self.paragraphes):
            paragraphe = self.paragraphes[self.current_paragraph]
            if self.current_letter < len(paragraphe):
                if now - self.last_update > self.letter_delay:
                    self.displayed_text += paragraphe[self.current_letter]
                    self.current_letter += 1
                    self.last_update = now
            else:
                self.paused = True
                self.pause_start = now
        else:
            # Fin de l'intro, bascule immédiatement sur "spawn"
            self.finished = True

    def draw(self, surface):
        surface.fill((0, 0, 0))
        # Affiche le texte centré, multi-lignes
        self._draw_text(surface, self.displayed_text, self.font, (255,255,255), 100, 60)
        # Bouton "passer l'intro"
        mouse_pos = pg.mouse.get_pos()
        self.skip_hover = self.skip_rect.collidepoint(mouse_pos)
        color = (150,150,150) if self.skip_hover else (100,100,100)
        pg.draw.rect(surface, color, self.skip_rect)
        txt = self.font.render("Passer l'intro", True, (255,255,255))
        txt_rect = txt.get_rect(center=self.skip_rect.center)
        surface.blit(txt, txt_rect)

    def _draw_text(self, ecran, texte, font, color, x, y):
        largeur_max = WIDTH - 2 * x
        mots = texte.split(' ')
        lignes = []
        ligne_actuelle = ""
        for mot in mots:
            test_ligne = f"{ligne_actuelle} {mot}".strip()
            if font.size(test_ligne)[0] <= largeur_max:
                ligne_actuelle = test_ligne
            else:
                lignes.append(ligne_actuelle)
                ligne_actuelle = mot
        if ligne_actuelle:
            lignes.append(ligne_actuelle)
        for ligne in lignes:
            texte_surface = font.render(ligne, True, color)
            texte_rect = texte_surface.get_rect(center=(WIDTH // 2, y))
            ecran.blit(texte_surface, texte_rect)
            y += font.get_linesize()


class OutroState(State):
    """
    État de fin avec texte défilant et retour au menu.
    """
    def __init__(self, manager, game_instance):
        super().__init__(manager, game_instance)
        self.font = pg.font.Font(None, 36)
        self.texte = (
            "Après un long exil loin du Mont Olympe, Dionysos fit enfin son retour.\n"
            "Le silence planait sur les cieux tandis qu’il s’avançait, le pas plus calme,\n"
            "le regard moins enflammé qu’autrefois. Les dieux, d’abord figés, observaient,\n"
            "partagés entre méfiance et nostalgie. Zeus, assis sur son trône, le fixa un instant\n"
            "sans dire un mot. Puis, dans un souffle à peine audible, il hocha la tête.\n"
            "L’Olympe pouvait de nouveau vibrer — non pas dans l’excès, mais dans l’équilibre retrouvé."
        )
        self.displayed_text = ""
        self.current_letter = 0
        self.last_update = pg.time.get_ticks()
        self.letter_delay = 40  # ms
        self.finished = False
        self.pause_time = 2000  # ms
        self.paused = False
        self.pause_start = 0

    def enter_state(self):
        self.displayed_text = ""
        self.current_letter = 0
        self.last_update = pg.time.get_ticks()
        self.finished = False
        self.paused = False
        self.pause_start = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pg.QUIT:
                self.game.running = False

    def update(self, dt):
        if self.finished:
            self.manager.set_state("menu")
            return

        now = pg.time.get_ticks()
        if self.paused:
            if now - self.pause_start >= self.pause_time:
                self.finished = True
        elif self.current_letter < len(self.texte):
            if now - self.last_update > self.letter_delay:
                self.displayed_text += self.texte[self.current_letter]
                self.current_letter += 1
                self.last_update = now
        else:
            # Fin du texte, pause avant retour menu
            self.paused = True
            self.pause_start = now

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self._draw_text(surface, self.displayed_text, self.font, (255,255,255), 100, 60)

    def _draw_text(self, ecran, texte, font, color, x, y):
        largeur_max = WIDTH - 2 * x
        lignes = []
        for ligne in texte.split('\n'):
            mots = ligne.split(' ')
            ligne_actuelle = ""
            for mot in mots:
                test_ligne = f"{ligne_actuelle} {mot}".strip()
                if font.size(test_ligne)[0] <= largeur_max:
                    ligne_actuelle = test_ligne
                else:
                    lignes.append(ligne_actuelle)
                    ligne_actuelle = mot
            if ligne_actuelle:
                lignes.append(ligne_actuelle)
        for ligne in lignes:
            texte_surface = font.render(ligne, True, color)
            texte_rect = texte_surface.get_rect(center=(WIDTH // 2, y))
            ecran.blit(texte_surface, texte_rect)
            y += font.get_linesize()


class MenuState(State):
    """
    État du menu principal.
    """
    def __init__(self, manager, game_instance):
        super().__init__(manager, game_instance)
        self.title_font = pg.font.Font(None, 74)
        self.setup_buttons()

        # Charger l'image de fond
        try:
            self.background_image = pg.image.load("Fond/menu_background.png").convert()
            self.background_image = pg.transform.scale(self.background_image, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Erreur: Impossible de charger l'image de fond du menu: {e}")
            self.background_image = None

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        spacing = 20
        start_y = HEIGHT // 2 - button_height - spacing

        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y,
            button_width, button_height,
            "Jouer", self.start_intro, self.game.font
        ))
        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y + button_height + spacing,
            button_width, button_height,
            "Options", self.open_settings, self.game.font
        ))
        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + spacing),
            button_width, button_height,
            "Quitter", self.quit_game, self.game.font
        ))

    def start_intro(self):
        self.manager.set_state("intro")

    def open_settings(self):
        self.manager.set_state("option")

    def quit_game(self):
        self.game.running = False

    def enter_state(self):
        super().enter_state()
        # Est-ce que la musique est déjà jouée ?
        pg.mixer.music.stop()

    def exit_state(self):
        super().exit_state()
        # Pas besoin de gérer la musique ici, elle est arrêtée dans enter_state

    def draw(self, surface):
        # Dessiner l'image de fond
        if self.background_image:
            surface.blit(self.background_image, (0, 0))
        else:
            surface.fill(LIGHTBLUE)  # Retourne à la couleur de fond par défaut si l'image échoue à charger

        # Dessiner le titre
        title_surf = self.title_font.render(TITLE, True, WHITE)  # Change color to WHITE
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(title_surf, title_rect)

        # Dessiner les boutons
        for button in self.buttons:
            button.draw(surface)


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
        self.portals = None  # Ajout pour les portails
        self.portal_img = None
        self.music_playing = False

        # Charger l'image de fond
        try:
            self.background_image = pg.image.load("Fond/dark_forest.png").convert()
            self.background_image = pg.transform.scale(self.background_image, (WIDTH, HEIGHT))
        except Exception as e:
            print(f"Erreur: Impossible de charger l'image de fond 'fond/dark_forest.png': {e}")
            self.background_image = None

        self.gauge_rect = pg.Rect(WIDTH - 20, HEIGHT // 2 - 150, 20, 300)  # création du rectangle de la jauge
        self.gauge_color = (0, 255, 0)  # Couleur de la jauge (vert)
        self.start_y = 6229  # Coordonée Y de départ
        self.end_y = 341  # Fin de la jauge (coordonnée Y de la carte)

    def draw_altitude_gauge(self, surface):
        """
        Draws the altitude gauge on the screen.
        """
        # calculer la hauteur de la jauge en fonction de la position du joueur
        if self.player:
            player_y = self.player.rect.y
            fill_percentage = max(0, min(1, (self.start_y - player_y) / (self.start_y - self.end_y)))

            # Calculer la hauteur remplie de la jauge
            filled_height = int(self.gauge_rect.height * fill_percentage)

            # dessiner le contour de la jauge
            pg.draw.rect(surface, (0, 0, 0), self.gauge_rect, 2)  # bordure noire

            # Dessiner la jauge remplie
            filled_rect = pg.Rect(
                self.gauge_rect.x,
                self.gauge_rect.y + self.gauge_rect.height - filled_height,
                self.gauge_rect.width,
                filled_height
            )
            pg.draw.rect(surface, self.gauge_color, filled_rect)

    def enter_state(self):
        super().enter_state()
        # commenté la musique si elle est déjà jouée
        if not self.music_playing:
            try:
                pg.mixer.music.load("Music/Benz.wav")  # charger le fichier Benz.wav
                pg.mixer.music.set_volume(GAME_VOLUME)  # mettre le volume (0.0 à 1.0)
                pg.mixer.music.play(-1)  # jouer en boucle (-1 pour une boucle infinie)
                self.music_playing = True
            except pg.error as e:
                print(f"Erreur: Impossible de charger ou jouer la musique 'Music/Benz.wav': {e}")

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.javelins_flying = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.spikes = pg.sprite.Group()  # Initialisation du groupe de pics
        self.portals = pg.sprite.Group()  # Initialisation du groupe de portails

        # Charger l'image du portail
        try:
            self.portal_img = pg.image.load("Sprites/portail.png").convert_alpha()
        except Exception as e:
            print(f"Erreur chargement image portail: {e}")
            self.portal_img = None

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

        # Charger les objets portail_de_l'end
        if hasattr(self.map, "tmx_data"):
            for layer in self.map.tmx_data.objectgroups:
                for obj in layer:
                    if obj.name == "Portail_de_l'end":
                        portal_sprite = pg.sprite.Sprite()
                        if self.portal_img:
                            portal_sprite.image = pg.transform.scale(self.portal_img, (int(obj.width), int(obj.height)))
                        else:
                            portal_sprite.image = pg.Surface((obj.width, obj.height), pg.SRCALPHA)
                        portal_sprite.rect = pg.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.portals.add(portal_sprite)

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

        self._player_dead = False  # Flag pour bloquer le jeu pendant la mort

    def exit_state(self):
        super().exit_state()
        # arrete la musique si elle est en cours
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
        # Bloque toutes les entrées si le joueur est en train de mourir
        if self.player and getattr(self.player, "is_dead", False):
            return
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE or event.key == pg.K_UP or event.key == pg.K_z:
                    if self.player:
                        self.player.jump()
                if event.key == pg.K_ESCAPE:
                    self.manager.push_state("pause")

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.player and self.camera:
                        mouse_screen_pos = event.pos
                        mouse_world_pos = self.camera.screen_to_world(mouse_screen_pos)
                        self.player.throw_javelin(mouse_world_pos)

    def update(self, dt):
        super().update(dt)
        # Augmente dynamique le volume de la musique
        if self.music_playing:
            pg.mixer.music.set_volume(GAME_VOLUME)

        if not self.player or not self.camera or not self.all_sprites:
            return

        # Si le joueur est en train de mourir, ne rien mettre à jour d'autre que lui
        if getattr(self.player, "is_dead", False):
            self.player.update(dt)
            self.camera.update(self.player.rect)
            return

        self.all_sprites.update(dt)
        self.camera.update(self.player.rect)

        # --- Collision joueur-monstre : lancer animation de mort ---
        if self.monsters:
            for monster in list(self.monsters):
                if getattr(monster, "is_dead", False):
                    continue
                if pg.sprite.collide_rect(self.player, monster):
                    if not getattr(self.player, "is_dead", False):
                        self.player.die()
                    break
        # --- Collision joueur-pics : lancer animation de mort ---
        if self.spikes and pg.sprite.spritecollideany(self.player, self.spikes):
            if not getattr(self.player, "is_dead", False):
                self.player.die()

        # Collision joueur-portail_de_l'end
        if hasattr(self, "portals") and self.portals and pg.sprite.spritecollideany(self.player, self.portals):
            self.manager.set_state("outro")
            return

    def draw(self, surface):
        if not self.map or not self.camera or not self.all_sprites or not self.player:
            surface.fill(BLACK)
            if self.game.font:
                err_surf = self.game.font.render("Erreur de chargement du jeu", True, RED)
                err_rect = err_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                surface.blit(err_surf, err_rect)
            return

        # Dessiner l'image de fond
        if self.background_image:
            scaled_height = HEIGHT * 2  # Make the background image twice the screen height
            scaled_width = int(self.background_image.get_width() * (scaled_height / self.background_image.get_height()))
            scaled_background = pg.transform.scale(self.background_image, (scaled_width, scaled_height))

            # calculer le décalage en fonction de la position du joueur
            player_y = self.player.rect.y
            max_offset = scaled_height - HEIGHT  # Maximum scrollable height

            # rendre le décalage proportionnel à la position du joueur
            offset_y = max(0, min(max_offset, (player_y - self.end_y) / (self.start_y - self.end_y) * max_offset))

            # Dessiner l'image de fond avec le décalage
            surface.blit(scaled_background, (0, -offset_y))
        else:
            surface.fill(LIGHTBLUE)

        # dessiner la carte
        self.map.render(surface, self.camera)

        for sprite in self.all_sprites:
            if hasattr(sprite, 'image') and hasattr(sprite, 'rect'):
                surface.blit(sprite.image, self.camera.apply(sprite.rect))

        # --- Dessine les pics ---
        if self.spikes:
            for spike in self.spikes:
                surface.blit(spike.image, self.camera.apply(spike.rect))

        # Dessiner le portail avec une image si disponible
        if hasattr(self, "portals"):
            for portal in self.portals:
                if hasattr(portal, "TileMap/portail1.png"):
                    surface.blit(portal.image, self.camera.apply(portal.rect))

        if self.game.font:
            player_world_x = self.player.rect.x
            player_world_y = self.player.rect.y
            coord_text = f"Player X: {int(player_world_x)}, Y: {int(player_world_y)}"
            text_surface = self.game.font.render(coord_text, True, BLACK)
            surface.blit(text_surface, (10, 10))

        # Dessiner les javelots
        self.draw_altitude_gauge(surface)

    # Méthode appelée par Player à la fin de l'animation de mort
    def go_to_main_menu(self):
        self.manager.set_state("menu")

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
        self.slider_rect = pg.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 10)  # Slider
        self.knob_rect = pg.Rect(self.slider_rect.x + self.slider_rect.width - 10, self.slider_rect.y - 5, 20, 20)  # Slider knob
        self.dragging = False
        self.volume = 1.0  #  volume (100%)
        self.setup_buttons()

    def setup_buttons(self):
        button_width = 200
        button_height = 50
        start_y = HEIGHT // 2 + 100

        self.buttons.append(Button(
            WIDTH // 2 - button_width // 2, start_y,
            button_width, button_height,
            "Retour", self.return_to_menu, self.game.font
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
                # Déplacer le bouton du curseur
                self.knob_rect.x = max(self.slider_rect.x, min(event.pos[0] - self.knob_rect.width // 2, self.slider_rect.x + self.slider_rect.width - self.knob_rect.width))
                
                # mettre à jour le volume
                # volume = (position du curseur - position de départ) / (largeur totale - largeur du curseur)
                self.volume = (self.knob_rect.x - self.slider_rect.x) / (self.slider_rect.width - self.knob_rect.width)
                self.volume = max(0.0, min(self.volume, 1.0))  # Clamp the volume to [0.0, 1.0]

                global GAME_VOLUME
                GAME_VOLUME = self.volume  # mettre à jour le volume global
                pg.mixer.music.set_volume(GAME_VOLUME)  # ajuster le volume de la musique

    def draw(self, surface):
        # remplir l'écran avec une couleur
        surface.fill(BEIGE)

        # dessiner l'overlay
        title_surf = self.title_font.render("Options", True, BLACK)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        surface.blit(title_surf, title_rect)

        # Dessiner le slider
        pg.draw.rect(surface, BLACK, self.slider_rect)
        # Dessiner le curseur
        pg.draw.ellipse(surface, RED, self.knob_rect)

        # dessiner le texte du volume
        if self.game.font:
            volume_text = f"Volume: {int(self.volume * 100)}%"
            volume_surf = self.game.font.render(volume_text, True, BLACK)
            volume_rect = volume_surf.get_rect(center=(WIDTH // 2, self.slider_rect.y - 30))
            surface.blit(volume_surf, volume_rect)

        # Dessiner les boutons
        for button in self.buttons:
            button.draw(surface)

