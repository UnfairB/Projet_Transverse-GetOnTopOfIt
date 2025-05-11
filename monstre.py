import pygame as pg

class Monster(pg.sprite.Sprite):
    def __init__(self, x, y, images, platforms, speed=100):
        super().__init__()
        self.images = images  # Liste de surfaces pour l'animation
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.platforms = platforms  # Groupe de sprites plateformes pour collision
        self.speed = speed
        self.direction = 1  # 1 = droite, -1 = gauche
        self.animation_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.15  # Plus petit = plus rapide

    def update(self, dt):
        # Animation
        self.animation_timer += dt
        if self.animation_timer > self.animation_speed:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]
            self.animation_timer = 0

        # Déplacement horizontal
        dx = self.direction * self.speed * dt
        self.rect.x += dx

        # Collision avec plateformes (rebondit)
        collided = pg.sprite.spritecollideany(self, self.platforms)
        if collided:
            # Revenir en arrière et changer de direction
            self.rect.x -= dx
            self.direction *= -1

    def turn(self):
        self.direction *= -1

class Zombie(Monster):
    def __init__(self, x, y, images, platforms, speed=100, walk_distance=200):
        super().__init__(x, y, images, platforms, speed)
        self.walk_distance = walk_distance  # distance à parcourir avant de se retourner (en pixels)
        self.start_x = x  # position de départ pour le calcul de la distance

    def update(self, dt):
        super().update(dt)
        # Calcul de la distance parcourue depuis le dernier retournement
        distance = abs(self.rect.x - self.start_x)
        if distance >= self.walk_distance:
            self.turn()
            self.start_x = self.rect.x  # réinitialise la position de départ

    def turn(self):
        self.direction *= -1
        # Retourner toutes les images horizontalement
        self.images = [pg.transform.flip(img, True, False) for img in self.images]
        self.image = self.images[self.animation_index]
