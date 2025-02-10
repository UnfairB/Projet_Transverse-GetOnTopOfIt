import pygame

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

#Classe qui va représenter notre personnage
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.isMoving = False
        self.on_ground = True
        self.speed = 8
        self.jump_max = -12
        self.saut = 0
        self.gravity = 0.5
        self.frame = 0
        self.frame_counter = 0
        self.image = pygame.image.load('Sprites/PersoIdleDroite.png')
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500
        self.direction = 1

    #Déplacement vers la droite du personnage
    def move_right(self):
        self.rect.x += self.speed

    #Déplacement vers la gauche du personnage
    def move_left(self):
        self.rect.x -= self.speed

    def jump(self):
        if self.on_ground:
            self.saut = self.jump_max  # Déclenche le saut
            self.on_ground = False

    def saut_maj(self, platforms):
        # Appliquer la gravité
        self.saut += self.gravity
        self.rect.y += self.saut

        # Vérifier les collisions avec les plateformes
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform) and self.saut > 0:
                self.rect.bottom = platform[1]  # Corrige la position
                self.saut = 0  # Stoppe la chute
                self.on_ground = True


    # Animation du personnage
    def maj(self, keys):
        if keys[pygame.K_LEFT]:
            self.frame_counter += 1
            if self.frame_counter >= 6:
                self.frame_counter = 0
                self.image = pygame.image.load(walking_gauche[self.frame])
                self.frame += 1
                self.direction = -1
                if self.frame >= len(walking_gauche):
                    self.frame = 0
                    self.frame_counter = 0
        elif keys[pygame.K_RIGHT]:
            self.frame_counter += 1
            if self.frame_counter >= 6:
                self.frame_counter = 0
                self.image = pygame.image.load(walking_droite[self.frame])
                self.frame += 1
                self.direction = 1
                if self.frame >= len(walking_droite):
                    self.frame = 0
                    self.frame_counter = 0
        else:
            self.frame = 0
            if self.direction == -1:
                self.image = pygame.image.load(idle[0])
            else:
                self.image = pygame.image.load(idle[1])