# CONSTANTES SERVANTS DANS LE PROGRAMME


### Constantes pour le jeu en lui-même

## Variables de fonctionnement
MAP_WIDTH, MAP_HEIGHT = 10, 10  # taille du plateau, en case
MAX_APPLE = 3  # nombre de pommes présentes en même temps sur un plateau
TICK_DELAY = 1 / 100  # temps entre chaque déplacement, en secondes

## Pour gérer les déplacements, à ne pas modifier
DIR = [ (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0) ]
DIR_STR = [ "up", "right", "down", "left" ]
STR_TO_DIR = { 
    "up" : 0,
    "right" : 1,
    "down" : 2,
    "left" : 3
 }
DIR8 = [
    (-1, -1), (0, -1),
    (1, -1), (1, 0),
    (1, 1), (0, 1),
    (-1, 1), (-1, 0)
]

## Variables pour l'affichage

# Affichage du jeu
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720  # taille de la fenêtre, en pixel
CELL_SIZE = 67  # taille en pixel d'une case
BACKGROUND_COLOR = (50, 50, 50)  # couleur d'une case vide
SNAKE_CELL_COLOR = (50, 255, 50)  # couleur d'une case contenant une partie du snake
APPLE_CELL_COLOR = (255, 50, 50)  # couleur d'une case contenant une pomme
GAME_OVER_COLOR = (255, 255, 255)  # couleur du texte affiché en cas de mort
GAME_ID_COLOR = (255, 255, 255)  # couleur du texte en bas annonçant l'id de la partie

# Affichages relatifs à l'IA
INPUT_NEURON_SIZE = 15  # taille d'un neurone de la couche d'entrée
HIDDEN_NEURON_SIZE = 15  # taille d'un neurone d'une couche cachée
OUTPUT_NEURON_SIZE = 25  # taille d'un neurone de la couche de sortie
NEGATIVE_SYNAPSE_COLOR = (50, 255, 50)  # couleur d'une synapse transportant une valeur négative
POSITIVE_SYNAPSE_COLOR = (255, 50, 50)  # couleur d'une synapse transportant une valeur positive
SYNAPSE_MIN_OPACITY = 0.05  # opacité minimale d'une synapse, plus le poids est élevé, plus la synapse est opaque
SYNAPSE_THICKNESS = 5  # épaisseur des synapses
NEURON_POSITIVE_ACTIVATION = (50, 50, 50)  # couleur d'un neurone activé positivement
NEURON_NEGATIVE_ACTIVATION = (255, 255, 255)  # couleur d'un neurone activé négativement
NN_HEIGHT = 300  # hauteur accordée à l'affichage d'un réseau de neurone
NN_WIDTH = 300  # largeur accordée à l'affichage d'un réseau de neurone
NN_DISPLAY_RECT = (720, 0, 560, 710)  # zone dédiée à l'affichage du réseau de neurone


## Variables concernant le fonctionnement de l'IA

# fonctionnement général de l'évolution

TICK_WITHOUT_GROWING_LIMIT = 30  # nombre de tick avant que l'IA soit supprimée, si elle ne grandit pas
OTHER_PARENT_WEIGHT_CHANCES = 0.5  # chance qu'un enfant prenne le poids d'une connexion du parent le moins bon
WEIGHT_MUTATION_CHANCES = 0.5  # chances que le poids d'une connexion change pendant une mutation
WEIGHT_MAX_CHANGES = 0.3  # changement maximal de poids pendant la mutation d'une connexion
WEIGHT_RESET_CHANCES = 0.5  # chances que le poids d'une connexion soit réinitialisé pendant une mutation
MUTATION_AMOUNT = 5  # nombres de mutation après la création d'un enfant
MUTATE_WEIGHTS_CHANCE = 0.85  # chances que les poids changent
MUTATE_ADD_CONNECTION_CHANCE = 0.7  # chances qu'une connexion se créée entre deux neurones non connectés
MUTATE_ADD_NEURON_CHANCE = 0.2  # chances qu'un neurone s'ajoute entre deux neurones déjà connectés

# concernant les population d'IA

POPULATION_SIZE = 50  # nombre d'individus présents de base dans une population
ELITE_COUNT = 5  # nombre des meilleurs individus conservés entre chaque génération

