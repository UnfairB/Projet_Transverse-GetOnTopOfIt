import pygame
import sys
from jeu import Game

#Couleur
BLANC = (255,255,255)
NOIR = (0,0,0)
BLEU = (0,0,255)
VERT = (0,255,0)
ROUGE = (255,0,0)
MARRON = (165,42,42)

#Dimension de l'écran
LARGEUR = 720
LONGUEUR = 1280

#Initialisation de la fenêtre
pygame.init()
pygame.display.set_caption('Projet Transverse')

screen = pygame.display.set_mode((LONGUEUR, LARGEUR))
clock = pygame.time.Clock()

# Charger notre jeu
jeu = Game()

# Cacher le curseur de la souris
pygame.mouse.set_visible(False)

#Boucle du jeu
running = True

while running:

    # Détection des touches pressées
    keys = pygame.key.get_pressed()

    # Image de fond (provisoire)
    screen.fill(BLANC)

    # Plateformes
    platforms = [
                 pygame.draw.rect(screen, VERT,(0, 550, 1280, 20)),
                 pygame.draw.rect(screen, MARRON, (0, 570, 1280, 200)),
                 pygame.draw.rect(screen, VERT,(1080,400,200,150)),
                 pygame.draw.rect(screen, VERT,(650,350,200,50)),
                 pygame.draw.rect(screen, VERT,(250,300,200,50)),
                 pygame.draw.rect(screen, NOIR, (1260, 0, 20, 720)),
                 pygame.draw.rect(screen, NOIR, (0, 0, 20, 720)),
    ]

    # Afficher le personnage
    screen.blit(jeu.javelot.image,jeu.javelot.rect)
    screen.blit(jeu.perso.image, jeu.perso.rect)

    #Déplace le joueur à gauche ou à droite en fonction de la touche pressé
    if jeu.pressed.get(pygame.K_d):
        jeu.perso.move_right(platforms)

    if jeu.pressed.get(pygame.K_q):
        jeu.perso.move_left(platforms)

    if jeu.pressed.get(pygame.K_SPACE) and jeu.perso.on_ground:
        jeu.perso.jump()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Déplacement du personnage
        if event.type == pygame.KEYDOWN:
            jeu.pressed[event.key] = True
        if event.type == pygame.KEYUP:
            jeu.pressed[event.key] = False

    jeu.perso.maj(keys)
    jeu.perso.saut_maj(platforms)
    #Met à jour l'affichage (60 frames par secondes)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

