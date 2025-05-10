# settings.py

# Dimensions de la fenêtre de jeu
WIDTH = 800  # Largeur de la fenêtre
HEIGHT = 600 # Hauteur de la fenêtre
FPS = 60     # Images par seconde

# Titre du jeu
TITLE = "GetOnTopOfIt"

# Couleurs (format RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (173, 216, 230) # Couleur de fond
BEIGE = (255, 229, 204)

# Propriétés du joueur
PLAYER_ACC = 0.5  # Accélération du joueur (non utilisé dans ce modèle simple)
PLAYER_FRICTION = -0.12 # Friction (non utilisé dans ce modèle simple)
PLAYER_GRAVITY = 0.8 # Gravité appliquée au joueur
PLAYER_JUMP_STRENGTH = -14 # Force du saut du joueur (valeur négative pour monter)
PLAYER_SPEED = 5 # Vitesse de déplacement horizontal du joueur

# Propriétés de la carte
TILE_SIZE = 40 # Taille d'une tuile (carrée) en pixels

# Propriétés du Javelot
JAVELIN_SPEED = 15       # Vitesse initiale du javelot
JAVELIN_GRAVITY = 0.5    # Gravité affectant le javelot
JAVELIN_RECALL_SPEED = 25 # Vitesse à laquelle le javelot retourne au joueur
JAVELIN_LIFESPAN_STUCK = 10000 # Temps en ms avant qu'un javelot planté disparaisse (optionnel, non implémenté ici)

# Global volume for the game
GAME_VOLUME = 1.0  # Default volume (100%)
