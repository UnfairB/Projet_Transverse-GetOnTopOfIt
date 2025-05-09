# GetOnTopOfIt

## Présentation du jeu

**GetOnTopOfIt** est un jeu de plateforme inspiré de *Jump King* et *Celeste*, où la progression se fait à travers différents tableaux divisant l'espace de jeu en plusieurs séquences avec une progression principalement verticale.


### Fonctionnalités principales
- Système de scènes dynamiques
- Mécanique de lancer et rappel du bâton/javelot
- Système de collision précis avec l'environnement
- Progression verticale à travers différents niveaux de difficulté

## Guide d'installation (pour débutants)

### Installation

1. **Récupérer le jeu** (2 options)
   - Option 1: Télécharger le ZIP depuis GitHub et l'extraire
   - Option 2: Cloner le dépôt avec Git:
     ```
     git clone https://github.com/UnfairB/Projet_Transverse-GetOnTopOfIt.git
     cd Projet_Transverse-GetOnTopOfIt
     ```

2. **Installer les dépendances**
   - Ouvrez un terminal/invite de commandes
   - Naviguez vers le dossier du jeu
   - Exécutez la commande:
     ```
     pip install -r requirements.txt
     ```

3. **Lancer le jeu**
   - Exécutez le fichier principal:
     ```
     python main.py
     ```

## Comment jouer

### Contrôles
- **Déplacement**: Flèches gauche/droite ou Q/D
- **Saut**: Barre d'espace, flèche du haut ou Z
- **Lancer javelot**: Clique gauche souris
- **Faire revenir javelot**: Touche maj
- **Quitter**: Échap

## Architecture du projet

Le projet est structuré autour d'une approche orientée objet avec plusieurs fichiers Python:

### Fichiers principaux
- `main.py` - Point d'entrée du jeu, contient la classe `Game` qui gère la boucle principale
- `settings.py` - Toutes les constantes et configurations du jeu (dimensions, couleurs, propriétés physiques)
- `player.py` - La classe `Player` qui gère les mouvements, sauts et collisions du personnage
- `statemanager.py` - Gestionnaire d'états du jeu (menu, jeu, pause)
- `sprites.py` - Classes pour les différents objets du jeu
- `map.py` - Gestion de la carte de jeu et des niveaux

### Dossier TileMap
Ce dossier contient les ressources liées aux cartes et niveaux:
- `game_map.tmx` - Carte principale du jeu au format Tiled
- Fichiers de tileset et assets graphiques

## Fonctionnement technique

Le jeu fonctionne selon un modèle classique de boucle de jeu:
1. Initialisation des composants
2. Boucle principale qui:
   - Gère les événements utilisateur
   - Met à jour l'état du jeu et la physique
   - Dessine les éléments à l'écran
   - Maintient la cadence d'images par seconde

La détection de collisions utilise le système de rectangles de Pygame pour gérer les interactions entre le joueur et l'environnement.

## Contributeurs

- Clément DRIESCH
- Tom GARRIDO
- Faustin MOUROT
- Maxime LAURENT
- Denyce NEGAI

---

*Projet développé dans le cadre d'un projet transverse à EFREI Paris*
