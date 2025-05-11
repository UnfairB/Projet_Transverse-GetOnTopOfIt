import pygame

BEIGE = (255,229,204)
RED = (255,0,0)

class Menu:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):

        # Fond blanc (provisoire)
        self.display.fill(BEIGE)

        # Récupère les positions x,y et les cliques de la souris à chaque frame
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Police d'écriture
        font = pygame.font.SysFont(None, 36)

        # Texte inscrit sur le bouton
        button_text = font.render("JOUER", True, 'black')

        # Dimension du bouton
        button_rect = pygame.Rect(450, 360, 200, 60)

        # Changement de couleur du bouton au survol de la souris dessus
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.display, 'green', button_rect)
            if mouse_click[0]:
                self.gameStateManager.set_state('spawn')
        else:
            pygame.draw.rect(self.display, 'blue', button_rect)

        # Centre le texte sur le bouton
        text_rect = button_text.get_rect(center=button_rect.center)
        self.display.blit(button_text, text_rect)

        # Cacher le curseur de la souris
        pygame.mouse.set_visible(False)

        # Remplace la souris par un viseur (un cercle rouge)
        pygame.draw.circle(self.display, RED, (mouse_pos), 10, 2)