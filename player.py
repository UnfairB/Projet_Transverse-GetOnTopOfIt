# player.py
import pygame as pg
from settings import *
from javelin import Javelin

#Toutes les images du personnage (animation)
idle = ['Sprites/L_Idle_Vagabond1.png',
        'Sprites/R_Idle_Vagabond1.png']

walking_droite = ['Sprites/WR_Vagabond1.png',
           'Sprites/WR_Vagabond2.png',
           'Sprites/WR_Vagabond3.png']

walking_gauche = ['Sprites/WL_Vagabond1.png',
                  'Sprites/WL_Vagabond2.png',
                  'Sprites/WL_Vagabond3.png']

idle_javelin = ['Sprites/L_Idle_Vagabaton1.png',
                'Sprites/R_Idle_Vagabaton1.png']

walking_droite_javelin = ['Sprites/RW_Vagabaton1.png',
                        'Sprites/RW_Vagabaton2.png',
                        'Sprites/RW_Vagabaton3.png']

walking_gauche_javelin = ['Sprites/LW_Vagabaton1.png',
                        'Sprites/LW_Vagabaton2.png',
                        'Sprites/LW_Vagabaton3.png']

jump_gauche = ['Sprites/L_Jump_Vagabond1.png']  
jump_droite = ['Sprites/R_Jump_Vagabond1.png'] 

jump_gauche_javelin = ['Sprites/L_Jump_Vagabaton1.png'] 
jump_droite_javelin = ['Sprites/R_Jump_Vagabaton1.png'] 

death = ['Sprites/L_Dead_Vagabond.png',
        'Sprites/R_Dead_Vagabond.png']

dead_smoke_droite = ['Sprites/R_dead_smoke1.png',
              'Sprites/R_dead_smoke2.png',
              'Sprites/R_dead_smoke3.png',
              'Sprites/R_dead_smoke4.png',]

dead_smoke_gauche = ['Sprites/L_dead_smoke1.png',
              'Sprites/L_dead_smoke2.png',
              'Sprites/L_dead_smoke3.png',
              'Sprites/L_dead_smoke4.png',]

class Player(pg.sprite.Sprite):
    """
    Classe pour représenter le joueur.
    Hérite de pygame.sprite.Sprite.
    """
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game

        # Animation
        self.animations_no_javelin = {
            "idle_gauche": [pg.image.load(idle[0]).convert_alpha()],
            "idle_droite": [pg.image.load(idle[1]).convert_alpha()],
            "walk_gauche": [pg.image.load(img).convert_alpha() for img in walking_gauche],
            "walk_droite": [pg.image.load(img).convert_alpha() for img in walking_droite],
            "jump_gauche": [pg.image.load(img).convert_alpha() for img in jump_gauche] if jump_gauche else [pg.image.load(idle[0]).convert_alpha()],
            "jump_droite": [pg.image.load(img).convert_alpha() for img in jump_droite] if jump_droite else [pg.image.load(idle[1]).convert_alpha()],
        }
        self.animations_javelin = {
            "idle_gauche": [pg.image.load(idle_javelin[0]).convert_alpha()],
            "idle_droite": [pg.image.load(idle_javelin[1]).convert_alpha()],
            "walk_gauche": [pg.image.load(img).convert_alpha() for img in walking_gauche_javelin],
            "walk_droite": [pg.image.load(img).convert_alpha() for img in walking_droite_javelin],
            "jump_gauche": [pg.image.load(img).convert_alpha() for img in jump_gauche_javelin] if jump_gauche_javelin else [pg.image.load(idle_javelin[0]).convert_alpha()],
            "jump_droite": [pg.image.load(img).convert_alpha() for img in jump_droite_javelin] if jump_droite_javelin else [pg.image.load(idle_javelin[1]).convert_alpha()],
        }
        self.state = "idle_droite"  # idle_droite, idle_gauche, walk_droite, walk_gauche, jump_droite, jump_gauche
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.08  # secondes entre frames

        self.image = self.animations_javelin["idle_droite"][0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.on_ground = False

        self.has_javelin = True
        self.active_javelin_sprite = None

        self.facing = "droite"  # Pour savoir dans quel sens on regarde

        # Animation de mort
        self.death_images = {
            "gauche": pg.image.load(death[0]).convert_alpha(),
            "droite": pg.image.load(death[1]).convert_alpha()
        }
        self.dead_smoke_images = {
            "gauche": [pg.image.load(img).convert_alpha() for img in dead_smoke_gauche],
            "droite": [pg.image.load(img).convert_alpha() for img in dead_smoke_droite]
        }
        self.is_dead = False
        self.death_anim_phase = None  # None, 'death', 'smoke'
        self.death_timer = 0
        self.smoke_index = 0
        self.smoke_anim_speed = 0.15  # secondes entre frames

    def jump(self):
        if self.on_ground: 
            self.vel.y = PLAYER_JUMP_STRENGTH

    def update(self, dt):
        if self.is_dead:
            self.death_timer += dt
            if self.death_anim_phase == 'death':
                # Affiche sprite mort pendant 0.5s puis passe à la fumée
                if self.death_timer > 0.5:
                    self.death_anim_phase = 'smoke'
                    self.death_timer = 0
                    self.smoke_index = 0
            elif self.death_anim_phase == 'smoke':
                # Animation de la fumée
                if self.death_timer > self.smoke_anim_speed:
                    self.smoke_index += 1
                    self.death_timer = 0
                    if self.smoke_index >= len(self.dead_smoke_images[self.facing]):
                        # Animation terminée, retour menu principal
                        if hasattr(self.game, 'go_to_main_menu'):
                            self.game.go_to_main_menu()
                        return
                if self.smoke_index < len(self.dead_smoke_images[self.facing]):
                    self.image = self.dead_smoke_images[self.facing][self.smoke_index]
            return  # Ne fait rien d'autre si mort

        self.acc = pg.math.Vector2(0, PLAYER_GRAVITY)

        keys = pg.key.get_pressed()
        current_acc_x = 0
        moving = False
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            current_acc_x = -PLAYER_SPEED 
            self.facing = "gauche"
            moving = True
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            current_acc_x = PLAYER_SPEED
            self.facing = "droite"
            moving = True

        self.vel.x = current_acc_x 

        self.rect.x += self.vel.x
        self.check_collision_x()

        self.vel.y += self.acc.y 
        if self.vel.y > 15: 
            self.vel.y = 15

        self.rect.y += self.vel.y
        self.on_ground = False 
        self.check_collision_y()

        # --- Animation ---
        # Détermine l'état d'animation selon le mouvement ET si le joueur saute
        if not self.on_ground:
            if self.facing == "droite":
                self.state = "jump_droite"
            else:
                self.state = "jump_gauche"
        elif moving:
            if self.facing == "droite":
                self.state = "walk_droite"
            else:
                self.state = "walk_gauche"
        else:
            if self.facing == "droite":
                self.state = "idle_droite"
            else:
                self.state = "idle_gauche"

        # Choix du bon set d'animations selon la possession du javelot
        if self.has_javelin:
            animations = self.animations_javelin
        else:
            animations = self.animations_no_javelin

        self.anim_timer += dt
        frames = animations[self.state]
        if self.anim_timer > self.anim_speed:
            self.anim_index = (self.anim_index + 1) % len(frames)
            self.anim_timer = 0
        # Pour idle, il n'y a qu'une frame donc anim_index reste 0
        if len(frames) == 1:
            self.anim_index = 0
        self.image = frames[self.anim_index]
        # --- Fin animation ---

    def throw_javelin(self, target_pos_world):
        if self.has_javelin:
            print("Joueur lance un javelot.")
            new_javelin = Javelin(self.game, self, target_pos_world)
            self.game.all_sprites.add(new_javelin)
            if hasattr(self.game, 'javelins_flying'):
                self.game.javelins_flying.add(new_javelin)
            self.has_javelin = False
            self.active_javelin_sprite = new_javelin
        elif self.active_javelin_sprite and self.active_javelin_sprite.state == 'stuck':
            print("Joueur rappelle le javelot.")
            self.active_javelin_sprite.recall()

    def retrieve_javelin(self):
        print("Joueur a récupéré le javelot.")
        self.has_javelin = True
        self.active_javelin_sprite = None

    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.death_anim_phase = 'death'
            self.death_timer = 0
            # Affiche le sprite de mort selon l'orientation
            self.image = self.death_images[self.facing]
            # Désactive les collisions/mouvements
            self.vel = pg.math.Vector2(0, 0)
            self.acc = pg.math.Vector2(0, 0)

    def check_collision_x(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit_platform in hits:
            if self.vel.x > 0: 
                self.rect.right = hit_platform.rect.left 
            elif self.vel.x < 0: 
                self.rect.left = hit_platform.rect.right 
            self.vel.x = 0 

    def check_collision_y(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit_platform in hits:
            if self.vel.y > 0:  
                self.rect.bottom = hit_platform.rect.top
                self.vel.y = 0
                self.on_ground = True
            elif self.vel.y < 0:  
                self.rect.top = hit_platform.rect.bottom
                self.vel.y = 0
