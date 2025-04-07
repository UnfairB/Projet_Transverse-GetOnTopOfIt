import pygame

BEIGE = (255,229,204)

class Menu:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        # Récupère les positions x,y et les cliques de la souris à chaque frame
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Fond blanc (provisoire)
        self.display.fill(BEIGE)

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
                self.gameStateManager.set_state('level')
        else:
            pygame.draw.rect(self.display, 'blue', button_rect)

        # Centre le texte sur le bouton
        text_rect = button_text.get_rect(center=button_rect.center)
        self.display.blit(button_text, text_rect)