# player.py
import pygame as pg
from settings import *
from javelin import Javelin


#Toutes les images du personnage (animation)
idle = ['Sprites/PersoIdleGauche.png',
        'Sprites/PersoIdleDroite.png']

walking_droite = ['Sprites/PersoWalking11.png',
           'Sprites/PersoWalking22.png',
           'Sprites/PersoWalking33.png',
           'Sprites/PersoWalking44.png',
           'Sprites/PersoWalking55.png',
           'Sprites/PersoWalking66.png']

walking_gauche = ['Sprites/PersoWalking1.png',
                  'Sprites/PersoWalking2.png',
                  'Sprites/PersoWalking3.png',
                  'Sprites/PersoWalking4.png',
                  'Sprites/PersoWalking5.png',
                  'Sprites/PersoWalking6.png']

class Player(pg.sprite.Sprite):
    """
    Classe pour représenter le joueur.
    Hérite de pygame.sprite.Sprite.
    """
    def __init__(self, game, x, y):
        """
        Initialise le joueur.
        :param game: Référence à l'objet principal du jeu.
        :param x: Position x initiale du joueur.
        :param y: Position y initiale du joueur.
        """
        super().__init__()
        self.game = game

        # Apparence du joueur - un simple rectangle bleu
        player_sprite_width = TILE_SIZE // 2 
        player_sprite_height = TILE_SIZE
        self.image = pg.Surface((player_sprite_width, player_sprite_height))
        self.image.fill(BLUE) # Utilise la couleur BLEU définie dans settings.py

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.vel = pg.math.Vector2(0, 0)
        self.acc = pg.math.Vector2(0, 0)
        self.on_ground = False
        
        self.has_javelin = True # Le joueur commence avec un javelot
        self.active_javelin_sprite = None # Référence au sprite du javelot lancé

    def jump(self):
        """
        Fait sauter le joueur s'il est sur le sol.
        """
        if self.on_ground: 
            self.vel.y = PLAYER_JUMP_STRENGTH

    def update(self, dt):
        """
        Met à jour l'état du joueur à chaque frame (logique de mouvement, gravité, collisions).
        :param dt: Delta-temps, temps écoulé depuis la dernière frame (non utilisé actuellement mais requis par la signature).
        """
        self.acc = pg.math.Vector2(0, PLAYER_GRAVITY)

        keys = pg.key.get_pressed()
        current_acc_x = 0
        if keys[pg.K_LEFT] or keys[pg.K_q]:
            current_acc_x = -PLAYER_SPEED 
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            current_acc_x = PLAYER_SPEED
        
        self.vel.x = current_acc_x 

        self.rect.x += self.vel.x
        self.check_collision_x()

        self.vel.y += self.acc.y 
        if self.vel.y > 15: 
            self.vel.y = 15
        
        self.rect.y += self.vel.y
        
        self.on_ground = False 
        self.check_collision_y()

    def throw_javelin(self, target_pos_world):
        """
        Logique pour que le joueur lance un javelot.
        Appelé depuis GameState en réponse à un clic de souris.
        :param target_pos_world: Coordonnées mondiales où le joueur vise.
        """
        if self.has_javelin:
            print("Joueur lance un javelot.")
            # game_state est accessible via self.game (qui est une instance de GameState)
            new_javelin = Javelin(self.game, self, target_pos_world)
            self.game.all_sprites.add(new_javelin) # Pour le dessin et l'update général
            if hasattr(self.game, 'javelins_flying'): # Assure que le groupe existe dans GameState
                self.game.javelins_flying.add(new_javelin) # Pour une gestion spécifique des javelots en vol
            
            self.has_javelin = False
            self.active_javelin_sprite = new_javelin
        else:
            print("Joueur essaie de lancer, mais n'a pas de javelot.")

    def retrieve_javelin(self):
        """
        Appelé par le javelot lui-même lorsqu'il atteint le joueur pendant un rappel.
        """
        print("Joueur a récupéré le javelot.")
        self.has_javelin = True
        self.active_javelin_sprite = None
        # Le javelot se .kill() lui-même.

    def check_collision_x(self):
        """
        Vérifie et gère les collisions horizontales avec les plateformes.
        """
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit_platform in hits:
            if self.vel.x > 0: 
                self.rect.right = hit_platform.rect.left 
            elif self.vel.x < 0: 
                self.rect.left = hit_platform.rect.right 
            self.vel.x = 0 

    def check_collision_y(self):
        """
        Vérifie et gère les collisions verticales avec les plateformes.
        """
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        for hit_platform in hits:
            if self.vel.y > 0: 
                if self.rect.bottom > hit_platform.rect.top: 
                    self.rect.bottom = hit_platform.rect.top 
                    self.vel.y = 0 
                    self.on_ground = True 
            elif self.vel.y < 0: 
                if self.rect.top < hit_platform.rect.bottom: 
                    self.rect.top = hit_platform.rect.bottom 
                    self.vel.y = 0
