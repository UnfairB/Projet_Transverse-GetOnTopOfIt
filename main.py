import pygame
import sys
from jeu import Game

#Couleur
BLANC = (255,255,255)
NOIR = (0,0,0)
BLEU = (0,0,255)
VERT = (0,255,0)
ROUGE = (255,0,0)

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

#Boucle du jeu
running = True

while running:

    # Détection des touches pressées
    keys = pygame.key.get_pressed()

    # Image de fond (provisoire)
    screen.fill(BLANC)

    # Plateformes
    platforms = [(0, 550, 1280, 20),
                 (800,500,200,20),
                 (400,400,200,20),
                 (50,300,200,20)]
    for plateforme in platforms:
        pygame.draw.rect(screen, VERT, plateforme)

    # Afficher le personnage
    screen.blit(jeu.perso.image, jeu.perso.rect)

    #Déplace le joueur à gauche ou à droite en fonction de la touche pressé
    if jeu.pressed.get(pygame.K_RIGHT):
        jeu.perso.move_right()

    if jeu.pressed.get(pygame.K_LEFT):
        jeu.perso.move_left()

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

