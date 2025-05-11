import pygame as pg
import pygame.mixer
import math
from settings import JAVELIN_SPEED, JAVELIN_GRAVITY, JAVELIN_RECALL_SPEED, TILE_SIZE

class Javelin(pg.sprite.Sprite):
    """
    Classe pour représenter un javelot lancé par le joueur.
    """
    def __init__(self, game_state, player, target_pos_world):
        """
        Initialise le javelot.
        :param game_state: Référence à l'état de jeu actuel (GameState).
        :param player: Référence au joueur qui a lancé le javelot.
        :param target_pos_world: Tuple (x, y) des coordonnées mondiales visées par la souris.
        """
        super().__init__()
        self.game_state = game_state
        self.player = player  # Le propriétaire du javelot

        # Chargement de l'image du javelot
        try:
            self.original_image = pg.image.load("Sprites/javelot.png").convert_alpha()
        except pg.error as e:
            print(f"Erreur: Impossible de charger 'Sprites/javelot.png': {e}")
            self.original_image = pg.Surface((TILE_SIZE, TILE_SIZE // 4))  # Fallback
            self.original_image.fill((100, 100, 100))  # Gris foncé

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        # Calcul de la direction initiale
        direction_vector = pg.math.Vector2(target_pos_world) - pg.math.Vector2(player.rect.center)
        if direction_vector.length() == 0:  # Évite la division par zéro si la souris est sur le joueur
            direction_vector = pg.math.Vector2(1, 0)  # Par défaut, tire vers la droite

        # Position initiale du javelot (juste à l'extérieur du joueur)
        spawn_offset = direction_vector.normalize() * (player.rect.width // 2 + self.rect.width // 2)
        self.pos = pg.math.Vector2(player.rect.center) + spawn_offset
        self.rect.center = self.pos

        # Calcul de la vélocité initiale
        self.vel = direction_vector.normalize() * JAVELIN_SPEED

        # État du javelot: 'flying', 'stuck', 'returning'
        self.state = 'flying'
        self.stuck_angle = 0  # Angle auquel le javelot est planté

        self.rotate()  # Oriente le javelot initialement

    def rotate(self):
        """
        Oriente l'image du javelot en fonction de sa vélocité (s'il vole)
        ou de son angle lorsqu'il est planté.
        """
        if self.state == 'flying':
            # Calcule l'angle basé sur la vélocité. atan2 prend (y, x).
            # Négatif sur Y car les coordonnées Pygame Y augmentent vers le bas.
            angle_rad = math.atan2(-self.vel.y, self.vel.x)
            self.stuck_angle = math.degrees(angle_rad) # Met à jour l'angle pour le cas où il se plante
        
        # La rotation se fait depuis le centre, donc on sauvegarde et restaure le centre.
        center_before_rotation = self.rect.center
        self.image = pg.transform.rotate(self.original_image, self.stuck_angle)
        self.rect = self.image.get_rect(center=center_before_rotation)

    def update(self, dt): # dt (delta time) n'est pas utilisé ici pour rester simple, mais serait utile pour des FPS variables
        """ Met à jour la position et l'état du javelot. """
        if self.state == 'flying':
            # Équation de trajectoire (Mouvement d'un projectile)
            # 1. Appliquer la gravité à la vélocité verticale
            self.vel.y += JAVELIN_GRAVITY
            
            # 2. Mettre à jour la position basée sur la vélocité
            self.pos += self.vel # pos.x += vel.x; pos.y += vel.y
            self.rect.center = self.pos
            
            self.rotate() # Réorienter le javelot en vol

            # --- Détection collision avec zombies ---
            if hasattr(self.game_state, "monsters"):
                for monster in self.game_state.monsters:
                    if not getattr(monster, "is_dead", False) and self.rect.colliderect(monster.rect):
                        # Animation de mort du zombie
                        # Charge les sprites de mort (à adapter selon vos assets)
                        try:
                            death_imgs = [
                                pg.image.load("Sprites/Zombie_dead1.png").convert_alpha(),
                                pg.image.load("Sprites/Zombie_dead2.png").convert_alpha(),
                                pg.image.load("Sprites/Zombie_dead3.png").convert_alpha(),
                            ]
                        except Exception:
                            death_imgs = [monster.image]
                        monster.die(death_imgs)
                        # Empêche la collision avec le joueur (optionnel: retire du groupe monsters)
                        self.game_state.monsters.remove(monster)
                        break

            self.check_collision_walls()

        elif self.state == 'stuck':
            # Le javelot ne bouge plus et ne tourne plus une fois planté.
            # Sa position et son angle sont figés.
            pass

        elif self.state == 'returning':
            direction_to_player = pg.math.Vector2(self.player.rect.center) - self.pos
            if direction_to_player.length_squared() < (JAVELIN_RECALL_SPEED * JAVELIN_RECALL_SPEED /4) : # Proche du joueur
                self.player.retrieve_javelin() # Notifie le joueur
                self.kill() # Se supprime de tous les groupes
                return

            self.vel = direction_to_player.normalize() * JAVELIN_RECALL_SPEED
            self.pos += self.vel
            self.rect.center = self.pos
            self.rotate() # S'oriente vers le joueur pendant le retour

    def check_collision_walls(self):
        """ Vérifie la collision avec les plateformes (murs). """
        collided_platforms = pg.sprite.spritecollide(self, self.game_state.platforms, False)
        if collided_platforms:
            # Le javelot a touché un mur/plateforme
            self.state = 'stuck'

            # Jouer le son Lance.wav
            try:
                lance_sound = pg.mixer.Sound("Sound/Lance.wav")
                lance_sound.play()
            except pg.error as e:
                print(f"Erreur: Impossible de jouer le son 'Sound/Lance.wav': {e}")

            # Ajoute ce javelot au groupe des plateformes
            self.game_state.platforms.add(self)

            # Vérifie si le joueur chevauche le javelot et ajuste sa position
            while self.player.rect.colliderect(self.rect):
                if self.player.vel.y > 0:  # Descending
                    self.player.rect.bottom = self.rect.top
                    self.player.vel.y = 0
                    self.player.on_ground = True
                elif self.player.vel.y < 0:  # Ascending
                    self.player.rect.top = self.rect.bottom
                    self.player.vel.y = 0
                else:
                    # If the player is stationary, nudge them out of the collision
                    self.player.rect.y += 1  # Push the player downward slightly

    def recall(self):
        """ Commence le processus de rappel du javelot. """
        if self.state == 'stuck':
            # S'il était planté, il n'est plus une plateforme solide.
            self.game_state.platforms.remove(self)
            if hasattr(self.game_state, 'javelins_flying') and self not in self.game_state.javelins_flying:
                # S'il n'est pas déjà dans javelins_flying, on l'y ajoute pour qu'il soit mis à jour
                self.game_state.javelins_flying.add(self)


        self.state = 'returning'
        print("Javelot rappelé.")
