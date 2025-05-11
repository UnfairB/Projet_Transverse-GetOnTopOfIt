import pygame as pg
from settings import BLACK, WHITE, GREEN # Assuming some colors are defined in settings

class Button:
    """
    Classe simple pour un bouton cliquable.
    """
    def __init__(self, x, y, width, height, text, callback, font, text_color=BLACK, button_color=WHITE, hover_color=GREEN):
        """
        Initialise un bouton.
        :param x, y: Position du coin supérieur gauche du bouton.
        :param width, height: Dimensions du bouton.
        :param text: Texte à afficher sur le bouton.
        :param callback: Fonction à appeler lorsque le bouton est cliqué.
        :param font: Objet pg.font.Font pour rendre le texte.
        :param text_color: Couleur du texte.
        :param button_color: Couleur du bouton.
        :param hover_color: Couleur du bouton lorsque la souris est dessus.
        """
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        """
        Dessine le bouton sur la surface donnée.
        """
        current_color = self.hover_color if self.is_hovered else self.button_color
        pg.draw.rect(surface, current_color, self.rect)
        pg.draw.rect(surface, BLACK, self.rect, 2) # Bordure

        if self.font and self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Gère les événements pour le bouton (survol, clic).
        """
        if event.type == pg.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered: # Clic gauche
                if self.callback:
                    self.callback()
                    return True # Événement géré
        return False # Événement non géré par ce bouton
