import pygame

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (100, 100, 100)
LARGEUR = 800
HAUTEUR = 600


"""
Afficher un texte centré avec une limite sur les côtés pour passer à la ligne
"""
def dessiner_texte(ecran, texte, font, color, x, y):
    largeur_max = LARGEUR - 2 * x
    mots = texte.split(' ')
    lignes = []
    ligne_actuelle = ""

    for mot in mots:
        test_ligne = f"{ligne_actuelle} {mot}".strip()
        if font.size(test_ligne)[0] <= largeur_max:
            ligne_actuelle = test_ligne
        else:
            lignes.append(ligne_actuelle)
            ligne_actuelle = mot
    if ligne_actuelle:
        lignes.append(ligne_actuelle)

    for ligne in lignes:
        texte_surface = font.render(ligne, True, color)
        texte_rect = texte_surface.get_rect(center=(LARGEUR // 2, y))
        ecran.blit(texte_surface, texte_rect)
        y += font.get_linesize()




"""
Dessiner un bouton avec du texte
"""
def draw_button(screen, text, font, color, rect, bg_color):
    pygame.draw.rect(screen, bg_color, rect)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(rect[0] + rect[2] // 2, rect[1] + rect[3] // 2))
    screen.blit(text_surface, text_rect)



"""
Gérer l'affichage de l'intro avec des paragraphes et un bouton "Skip Intro"
"""
def lancer_intro(ecran):
    pygame.font.init()
    font = pygame.font.Font(None, 36)  # Police taille 36

    paragraphes = [
        "La fête faisait rage sur le mont Olympe, un banquet où les dieux se lâchaient complètement, oubliant toute retenue.",
        " Dionysos, le dieu du vin et de la fête, était au centre de l’attention, riant et plaisantant, tandis que les dieux se livraient à des excès de tous genres. Le vin coulait à flots, les mets se succédaient sans fin, et les danses étaient de plus en plus folles.",
        " Mais pour Zeus, le roi des dieux, c’était trop. Il voyait ses pairs sombrer dans la démesure, et l’harmonie de l’Olympe s’effondrer sous le poids des excès. Son regard, habituellement sage, se faisait de plus en plus sombre. Une colère sourde montait en lui, alors que la fête de Dionysos devenait un chaos qu’il ne pouvait plus supporter."
    ]

    clock = pygame.time.Clock()
    button_rect = pygame.Rect(300, 500, 200, 50)  # Bouton "Skip Intro"

    running = True
    displayed_texte = ""  # Conserver tout le texte affiché
    for paragraphe in paragraphes:
        texte_index = 0

        while running and texte_index < len(paragraphe):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):  # Vérifier si le bouton est cliqué
                        return  # Quitter l'intro

            if texte_index < len(paragraphe):
                displayed_texte += paragraphe[texte_index]
                texte_index += 1

            ecran.fill(NOIR)
            dessiner_texte(ecran, displayed_texte, font, BLANC, 100, 60)
            draw_button(ecran, "Skip Intro", font, BLANC, button_rect, GRIS)
            pygame.display.flip()
            clock.tick(50)

        if running:
            pygame.time.wait(2000)

    # Attendre 5 secondes après la fin de l'intro
    if running:
        pygame.time.wait(5000)

    # Retourner à main.py pour continuer
    return
