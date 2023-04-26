"""
Contient Presque toute les varaibles global et les constantes néccéssaire
C'est un stock énorme ou on y retrouve :
- l'image de la sortie des étages ouverte/fermée (sont vecteur)
- la classification des tuiles selon si elle sont des murs, des demis murs etc ...
- les limites des cartes dessinée pour l'instant (à modifier en cas de rajout)
- une fonction qui prends l'entier entre 1 et 4 qui représente la direction et qui renvoie le tuple qui défini le mouvmement de 1 vers cette même direction.
- Image des entite (1)
- Image de l'équipment (2)
- les images dans l'inventaire de tout ce qui est ramassable
- la table des efficacité (efficacite[dest][source])
- equivalence des orientation : int to str
- fonctions de param (x ; y) qui renvoient un gros tuples avec tout ce qu'il faut pour définir une image
- MONSTER_IMG : dictionnaire qui lie le nom d'un monstre à sa fonction de param (x ; y) pour pouvoir le dessiner
- TEXTS : tout les dialogs, les texts à mettre dans les menu etc ...
"""

LARGEUR = 3
WIN_W = LARGEUR*128 + 33 - 1
WIN_H = LARGEUR*128 + 17 - 1


IMAGE_PORTE_FERMEE = (32, 0)
IMAGE_PORTE_OUVERTE = (48, 0)

TAUX_DROP = 50 / 100
TAUX_PV = 30
MAX_LOOT = 2

# définition des murs et des pièges
EQUIVALANCE = {
    "obst": [  # Tuiles qui bloque le déplacement et les attaques
        (0, 2), (0, 3), (1, 2), (1, 3),  # rondin sur dalle
        (2, 2), (2, 3), (3, 2), (3, 3),  # brick (brown)
        (12, 6), (13, 6), (12, 7), (13, 7),  # rondin sur herbe
        (14, 6), (15, 6), (14, 7), (15, 7),  # buisson
        (2, 10), (3, 10), (2, 11), (3, 11),  # Carcasse
        (4, 10), (5, 10), (4, 11), (5, 11),  # Carcasse
        (6, 10), (7, 10), (6, 11), (7, 11),  # Carcasse
        (6, 12), (7, 12), (6, 13), (7, 13),  # Cactus
        (8, 12), (9, 12), (8, 13), (9, 13),  # feuille
        (10, 12), (11, 12), (10, 13), (11, 13),  # cailloux
        (2, 14), (3, 14), (2, 15), (3, 15),  # grave
        (4, 14), (5, 14), (4, 15), (5, 15),  # grave
        (6, 14), (7, 14), (6, 15), (7, 15),  # brick (blue)
        (0, 16), (1, 16), (0, 17), (1, 17),  # grave
        (2, 16), (3, 16), (2, 17), (3, 17),  # grave
        (20, 16), (21, 16), (20, 17), (21, 17),  # grave
        (4, 16), (5, 16), (4, 17), (5, 17),  # bones
        (6, 16), (7, 16), (6, 17), (7, 17),  # bones
        (8, 16), (9, 16), (8, 17), (9, 17),  # bones
        (14, 16), (15, 16), (14, 17), (15, 17),  # siege
        (20, 2), (21, 2), (20, 3), (21, 3),  # buisson
    ],
    "ground": [  # Tuiles qui bloque le déplacement mais pas les attaques
        (16, 6), (17, 6), (16, 7), (17, 7),  # eau
        (18, 6), (19, 6), (18, 7), (19, 7),  # eau
        (20, 6), (21, 6), (20, 7), (21, 7),  # eau
        (22, 6), (23, 6), (22, 7), (23, 7),  # eau
        (24, 6), (25, 6), (24, 7), (25, 7),  # eau
        (26, 6), (27, 6), (26, 7), (27, 7),  # eau
        (28, 6), (29, 6), (28, 7), (29, 7),  # eau
        (2, 8), (3, 8), (2, 9), (3, 9),  # eau
        (4, 8), (5, 8), (4, 9), (5, 9),  # eau
        (6, 8), (7, 8), (6, 9), (7, 9),  # eau
        (8, 8), (9, 8), (8, 9), (9, 9),  # eau
        (10, 8), (11, 8), (10, 9), (11, 9),  # eau
        (12, 8), (13, 8), (12, 9), (13, 9),  # eau
        (14, 8), (15, 8), (14, 9), (15, 9),  # eau
        (16, 8), (17, 8), (16, 9), (17, 9),  # eau
        (18, 8), (19, 8), (18, 9), (19, 9),  # eau
        (20, 8), (21, 8), (20, 9), (21, 9),  # eau
        (22, 8), (23, 8), (22, 9), (23, 9),  # eau
        (8, 10), (9, 10), (8, 11), (9, 11),  # eau
        (10, 10), (11, 10), (10, 11), (11, 11),  # eau
        (12, 10), (13, 10), (12, 11), (13, 11),  # eau
        (14, 10), (15, 10), (14, 11), (15, 11),  # eau
        (16, 10), (17, 10), (16, 11), (17, 11),  # eau
        (18, 10), (19, 10), (18, 11), (19, 11),  # eau
        (20, 10), (21, 10), (20, 11), (21, 11),  # eau
        (22, 10), (23, 10), (22, 11), (23, 11),  # eau
        (24, 10), (25, 10), (24, 11), (25, 11),  # eau
        (26, 10), (27, 10), (26, 11), (27, 11),  # eau
        (28, 10), (29, 10), (28, 11), (29, 11),  # eau
        (20, 12), (21, 12), (20, 13), (21, 13),  # eau
        (22, 12), (23, 12), (22, 13), (23, 13),  # eau
        (24, 12), (25, 12), (24, 13), (25, 13),  # eau
        (26, 12), (27, 12), (26, 13), (27, 13),  # eau
        (16, 12), (17, 12), (16, 13), (17, 13),  # eau
        (18, 12), (19, 12), (18, 13), (19, 13),  # eau
        (28, 8), (29, 8), (28, 9), (29, 9),  # eau
        (30, 8), (31, 8), (30, 9), (31, 9),  # eau
        (28, 12), (29, 12), (28, 13), (29, 13),  # eau
        (30, 12), (31, 12), (30, 13), (31, 13),  # eau
        (24, 2), (25, 2), (24, 3), (25, 3),  # eau
        (26, 2), (27, 2), (26, 3), (27, 3),  # eau
        (28, 2), (29, 2), (28, 3), (29, 3),  # eau
        (30, 2), (31, 2), (30, 3), (31, 3),  # eau
        (18, 4), (19, 4), (18, 5), (19, 5),  # eau
        (20, 4), (21, 4), (20, 5), (21, 5),  # eau
        (22, 4), (23, 4), (22, 5), (23, 5),  # eau
        (24, 4), (25, 4), (24, 5), (25, 5),  # eau
        (26, 4), (27, 4), (26, 5), (27, 5),  # eau
        (28, 4), (29, 4), (28, 5), (29, 5),  # eau
        (30, 4), (31, 4), (30, 5), (31, 5),  # eau
        (4, 6), (5, 6), (4, 7), (5, 7),  # eau
        (10, 6), (11, 6), (10, 7), (11, 7),  # eau
        (30, 10), (31, 10), (30, 11), (31, 11),  # eau
        (0, 30), (1, 30), (0, 31), (1, 31),  # nuage en rond
        (12, 28), (13, 28), (12, 29), (13, 29),  # nuage plein
        (8, 28), (9, 28), (8, 29), (9, 29),  # nuage haut + buisson
        (8, 26), (9, 26), (8, 27), (9, 27),  # nuage bas + buisson
        (2, 20), (3, 20), (2, 21), (3, 21),  # lave
    ],
    "left-side": [
        (22, 16), (23, 16), (22, 17), (23, 17),  # wall (top left corner)
        (26, 16), (27, 16), (26, 17), (27, 17),  # wall (bottom left corner)
        (30, 16), (31, 16), (30, 17), (31, 17),  # wall (left)
        (14, 14), (15, 14), (14, 15), (15, 15),  # trap wall (left)
        (18, 14), (19, 14), (18, 15), (19, 15),  # laser wall (left)
        (14, 26), (15, 26), (14, 27), (15, 27),  # nuage left 1
        (14, 28), (15, 28), (14, 29), (15, 29),  # nuage left 2
        (6, 30), (7, 30), (6, 31), (7, 31),  # nuage bottom left 1
        (18, 26), (19, 26), (18, 27), (19, 27),  # nuage bottom left 2
        (8, 30), (9, 30), (8, 31), (9, 31),  # nuage top left 1
        (18, 28), (19, 28), (18, 29), (19, 29),  # nuage top left 2
        (22, 30), (23, 30), (22, 31), (23, 31),  # nuage + passerelle bas
        (8, 20), (9, 20), (8, 21), (9, 21),  # lave bas-gauche
        (10, 20), (11, 20), (10, 21), (11, 21),  # lave haut-gauche
        (8, 22), (9, 22), (8, 23), (9, 23),  # lave left 1
        (10, 22), (11, 22), (10, 23), (11, 23),  # lave left 2
        (10, 2), (11, 2), (10, 3), (11, 3),  # lave haut-gauche 2
        (14, 2), (15, 2), (14, 3), (15, 3),  # lave haut-gauche 3
        (12, 2), (13, 2), (12, 3), (13, 3),  # lave bas-gauche 2
    ],
    "right-side": [
        (24, 16), (25, 16), (24, 17), (25, 17),  # wall (bottom right corner)
        (28, 16), (29, 16), (28, 17), (29, 17),  # wall (top right corner)
        (30, 14), (31, 14), (30, 15), (31, 15),  # wall (right)
        (16, 14), (17, 14), (16, 15), (17, 15),  # trap wall (right)
        (20, 14), (21, 14), (20, 15), (21, 15),  # laser wall (right)
        (16, 26), (17, 26), (16, 27), (17, 27),  # nuage right 1
        (16, 28), (17, 28), (16, 29), (17, 29),  # nuage right 2
        (10, 30), (11, 30), (10, 31), (11, 31),  # nuage top right 1
        (20, 26), (21, 26), (20, 27), (21, 27),  # nuage top right 2
        (4, 30), (5, 30), (4, 31), (5, 31),  # nuage bottom right 1
        (20, 28), (21, 28), (20, 29), (21, 29),  # nuage bottom right 2
        (26, 30), (27, 30), (26, 31), (27, 31),  # nuage + passerelle bas
        (0, 22), (1, 22), (0, 23), (1, 23),  # lave bas-droite
        (2, 22), (3, 22), (2, 23), (3, 23),  # lave haut-droite
        (4, 22), (5, 22), (4, 23), (5, 23),  # lave right 1
        (6, 22), (7, 22), (6, 23), (7, 23),  # lave right 2
        (10, 0), (11, 0), (10, 1), (11, 1),  # lave bas-droite 2
        (8, 2), (9, 2), (8, 3), (9, 3),  # lave bas-droite 3
        (14, 0), (15, 0), (14, 1), (15, 1),  # lave haut-droite 2
    ],
    "top-side": [
        (22, 16), (23, 16), (22, 17), (23, 17),  # wall (top left corner)
        (28, 16), (29, 16), (28, 17), (29, 17),  # wall (top right corner)
        (26, 14), (27, 14), (26, 15), (27, 15),  # wall (top)
        (10, 14), (11, 14), (10, 15), (11, 15),  # trap wall (top)
        (24, 14), (25, 14), (24, 15), (25, 15),  # laser wall (top)
        (4, 28), (5, 28), (4, 29), (5, 29),  # nuage haut 1
        (6, 28), (7, 28), (6, 29), (7, 29),  # nuage haut 2
        (8, 30), (9, 30), (8, 31), (9, 31),  # nuage top left 1
        (18, 28), (19, 28), (18, 29), (19, 29),  # nuage top left 2
        (10, 30), (11, 30), (10, 31), (11, 31),  # nuage top right 1
        (20, 26), (21, 26), (20, 27), (21, 27),  # nuage top right 2
        (14, 30), (15, 30), (14, 31), (15, 31),  # nuage + passerelle droite
        (16, 30), (17, 30), (16, 31), (17, 31),  # nuage + passerelle gauche
        (2, 22), (3, 22), (2, 23), (3, 23),  # lave haut-droite
        (6, 20), (7, 20), (6, 21), (7, 21),  # lave haut 1
        (10, 20), (11, 20), (10, 21), (11, 21),  # lave haut-gauche
        (12, 0), (13, 0), (12, 1), (13, 1),  # lave haut 2
        (14, 0), (15, 0), (14, 1), (15, 1),  # lave haut-droite 2
        (10, 2), (11, 2), (10, 3), (11, 3),  # lave haut-gauche 2
        (14, 2), (15, 2), (14, 3), (15, 3),  # lave haut-gauche 3
        (14, 4), (15, 4), (14, 5), (15, 5),  # lave bas

    ],
    "bottom-side": [
        (24, 16), (25, 16), (24, 17), (25, 17),  # wall (bottom right corner)
        (26, 16), (27, 16), (26, 17), (27, 17),  # wall (bottom left corner)
        (28, 14), (29, 14), (28, 15), (29, 15),  # wall (bottom)
        (12, 14), (13, 14), (12, 15), (13, 15),  # trap wall (bottom)
        (22, 14), (23, 14), (22, 15), (23, 15),  # laser wall (bottom)
        (4, 26), (5, 26), (4, 27), (5, 27),  # nuage bas 1
        (6, 26), (7, 26), (6, 27), (7, 27),  # nuage bas 2
        (4, 30), (5, 30), (4, 31), (5, 31),  # nuage bottom right 1
        (20, 28), (21, 28), (20, 29), (21, 29),  # nuage bottom right 2
        (6, 30), (7, 30), (6, 31), (7, 31),  # nuage bottom left 1
        (18, 26), (19, 26), (18, 27), (19, 27),  # nuage bottom left 2
        (0, 22), (1, 22), (0, 23), (1, 23),  # lave bas-droite
        (4, 20), (5, 20), (4, 21), (5, 21),  # lave bas 1
        (8, 20), (9, 20), (8, 21), (9, 21),  # lave bas-gauche
        (10, 0), (11, 0), (10, 1), (11, 1),  # lave bas-droite 2
        (8, 2), (9, 2), (8, 3), (9, 3),  # lave bas-droite 3
        (12, 2), (13, 2), (12, 3), (13, 3),  # lave bas-gauche 2
    ],
    "event": [  # déclancheur d'évênement
        (5, 2), (6, 2), (5, 3), (6, 3),  # piège éclaté
        (8, 14), (9, 14), (8, 15), (9, 15),  # piège sol
    ]
}

# position des biomes
LIMITE = {
    "Cave": (0, 0, 2, 2),
    "Grass": (0, 3, 8, 2),
    "Grass2": (9, 3, 2, 2),
    'Desert': (0, 6, 3, 2),
    "Catacombes": (0, 9, 3, 2),
    "Enfer": (0, 13, 8, 2),
    "Paradis": (9, 0, 2, 2),

}

# math pour transformer le int de l'orientation en coordonné
f = lambda x: round((2 / 3) * x ** 3 - (7 / 2) * x ** 2 + (29 / 6) * x - 1)
g = lambda x: round((2 / 3) * x ** 3 - (5 / 2) * x ** 2 + (11 / 6) * x)

orient_to_coor = lambda orient: (f(orient), g(orient))

# numméro de l'images du fichier
IMAGE_EQUIPMENT = 2

# toute les images des différents items
LOOT_IMAGE = {
    "NakedArmor": (0, 0),
    "LeatherArmor": (0, 208),
    "IronArmor": (0, 144),
    "GoldArmor": (0, 176),
    "DiamondArmor": (0, 112),
    "MagmaArmor": (64, 224),
    "DragonScaleArmor": (48, 224),
    "Sword": (16, 0),
    "Spear": (16, 32),
    "Hammer": (16, 128),
    "Bow": (16, 152),
    "Hallebarde": (16, 64),
    "Axe": (16, 96),
    "Katana": (16, 184)
}

EFFICACITE = ((1, 1, 1, 1, 1, 1), (1, 0.9, 0.5, 2, 0.7, 0.7), (1, 2, 0.9, 0.5, 0.7, 0.7), (1, 0.5, 2, 0.9, 0.7, 0.7),
              (1, 1, 1, 1, 0, 3), (1, 1, 1, 1, 3, 0))

ORIENT_EQ = ["left", "right", "top", "bottom"]

IMAGE_ENTITE = 1

# images :

KATANA0 = lambda x, y: (x, y, 2, 32, 184, 16, 32, 0)
KATANA1 = lambda x, y: (x, y, 2, 32, 184, 16, 32, 0)
KATANA2 = lambda x, y: (x, y, 2, 16, 184, 16, 32, 0)
DRAGON_SCAlE_ARMOR = lambda x, y: (x, y, 2, 48, 224, 16, 32, 0)
DEAFEAT_FIRST_PART = lambda x, y: (x, y, 2, 0, 240, 32, 16, 7)
DEAFEAT_SECOND_PART = lambda x, y: (x, y, 2, 16, 224, 16, 16, 7)
BOUTON_ADD = lambda x, y: (x, y, 1, 240, 240, 16, 16, 0)
BOUTON_SUB = lambda x, y: (x, y, 1, 224, 240, 16, 16, 0)
CROIX = lambda x, y: (x, y, 2, 208, 192, 32, 32, 0)
VALID = lambda x, y: (x, y, 2, 208, 224, 32, 32, 0)
HEALTH_ICO = lambda x, y: (x, y, 2, 176, 208, 16, 16, 0)
DAMAGE_ICO = lambda x, y: (x, y, 2, 192, 208, 16, 16, 0)

MONSTER_IMG = {
    "Zombie": lambda x, y: (x, y, 1, 0, 16, 16, 16, 7),
    "Squelette": lambda x, y: (x, y, 1, 0, 32, 16, 16, 6),
    "Demon": lambda x, y: (x, y, 1, 0, 48, 16, 16, 7),
    "Bat": lambda x, y: (x, y, 1, 0, 64, 16, 16, 7),
    "Ghost": lambda x, y: (x, y, 1, 0, 80, 16, 16, 7),
    "Golem": lambda x, y: (x, y, 1, 0, 112, 16, 16, 7),
    "Spider": lambda x, y: (x, y, 1, 0, 128, 16, 16, 7),
    "Diablotin": lambda x, y: (x, y, 1, 0, 144, 16, 16, 7),
    "Vampire": lambda x, y: (x, y, 1, 0, 160, 16, 16, 6),
    "BlobFeu": lambda x, y: (x, y, 1, 0, 176, 16, 16, 7),
    "Necromancien": lambda x, y: (x, y, 1, 0, 192, 16, 16, 6),
    "Aligator": lambda x, y: (x, y, 1, 0, 208, 16, 16, 7),
    "Abomination": lambda x, y: (x, y, 1, 0, 224, 16, 16, 7),
    "Mommies": lambda x, y: (x, y, 1, 0, 240, 16, 16, 7),
    "Loup": lambda x, y: (x, y, 1, 32, 0, 16, 16, 7),
    "Fox": lambda x, y: (x, y, 1, 32, 16, 16, 16, 7),
    "BlobEau": lambda x, y: (x, y, 1, 32, 32, 16, 16, 7),
    "Witch": lambda x, y: (x, y, 1, 32, 48, 16, 16, 7),
    "DragonFeu": lambda x, y: (x, y, 1, 32, 64, 16, 16, 7),
    "Snake": lambda x, y: (x, y, 1, 32, 80, 16, 16, 7),
    "Creeper": lambda x, y: (x, y, 1, 32, 96, 16, 16, 7),
    "Rampant": lambda x, y: (x, y, 1, 32, 112, 16, 16, 7),
    "Notch": lambda x, y: (x, y, 1, 32, 128, 16, 16, 7),
    "Angel": lambda x, y: (x, y, 1, 32, 144, 16, 16, 6),
    "Arcangel": lambda x, y: (x, y, 1, 32, 160, 16, 16, 6),
    "DragonLight": lambda x, y: (x, y, 1, 32, 176, 16, 16, 6),
    "BlobPlant": lambda x, y: (x, y, 1, 32, 192, 16, 16, 6),
    "DragonDark": lambda x, y: (x, y, 1, 32, 208, 16, 16, 6),
    "DragonEau": lambda x, y: (x, y, 1, 32, 224, 16, 16, 7),
    "DragonPlant": lambda x, y: (x, y, 1, 32, 240, 16, 16, 7),
    "BlobLight": lambda x, y: (x, y, 1, 64, 0, 16, 16, 6),
    "BlobDark": lambda x, y: (x, y, 1, 64, 16, 16, 16, 6),
}

# Text

TEXTS = {
    "touches": "[Touches]\n"
               " - Z,Q,S,D -> Deplacements\n"
               " - A -> Attaquer\n"
               " - E -> Interagir/Ramasser\n"
               " - Fleches -> Diriger la visée\n"
               " - F -> Echanger d'armes\n"
               " - W -> Skip la salle de loot\n"
               " - TAB -> Ouvrir/Fermer les menus\n"
               " - F1 -> Fullscreen le jeu\n",
    "resumé": "[RESUME]\n"
              "Vous controlez un jeune aventurier qui, en quete \n"
              "de puissance, alla dans la grotte dimensionnelle \n"
              "afin augmenter sa puissance sans savoir qu'il \n"
              "allait y rester. Et tant que la guerre entre Le \n"
              "Paradis et Les Enfers ne sera pas terminee et que \n"
              "le sorcier qui la controle ne sera pas mort. Vous \n"
              "allez devoir gravir les etages un a un, et, trouver \n"
              "des equipement pour vaincre le magicien tout en \n"
              "evitant la mort.",
    "histoire": "[HISTOIRE]\n"
                "Un jeune chevalier trouva une admiration pour la \n"
                "magie et la sorcellerie. Mais malheureusement, \n"
                "malgre beaucoup d'efforts et de tentatives, \n"
                "il n'arriva pas à manier la magie et se \n"
                "faisait harceler par les autres aventuriers, \n"
                "tous types de sorciers et meme par certains \n"
                "villageois. Un jour, il entendit parler d'une \n"
                "grotte avec un demon pouvant realiser un voeu \n"
                "en echange d'une contrepartie. Un jour, il alla \n"
                "dans cette fameuse grotte pour augmenter sa \n"
                "puissance et pouvoir enfin manier la magie. Une \n"
                "fois au bout du tunnel, le sorcier entra dans \n"
                "une piece sombre avec un feu de bois au milieu \n"
                "et un demon assis a cote de celui-ci. Une fois \n"
                "devant le demon, il lui demanda de faire un pacte \n"
                "avec celui-ci et le demon accepta ! En echange \n"
                "de sa force physique, le demon lui passa un \n"
                "pouvoir magique egal à celui du sorcier suprême \n"
                "et lui offrit aussi un livre de sorcellerie pour\n"
                "preparer diverses concoctions. Le sorcier, \n"
                "tellement puissant, fit de la simple grotte du \n"
                "demon une grotte dimensionnelle pour y accueillir \n"
                "une faune riche et variée pour être maître de \n"
                "son propre monde et, crea également, les enfers \n"
                "à l'interieur comme present au demon. Mais quand \n"
                "le Paradis appris que les Enfers ne n'etait plus \n"
                "a leur endroit habituelle, ils déciderent \n"
                "d'enqueter. Il finirent par trouver la fameuse grotte \n"
                "du demon. Ils entrerent à l'interieur et trouverent \n"
                "un passage dimensionnel. Ils decouvrirent alors un monde \n"
                "entier dans cette grotte. Le Paradis installa \n"
                "leur base principale dans cette grotte pour y \n"
                "combattre leurs ennemies de toujours Les Enfers.",
    "Explications": "QUE FAIRE ? VOICI UN GUIDE : -----\n\n"
                    "1) Tout d'abord le principe, vous etes sur un \n"
                    "grande map avec pleins de tuiles, pleines, creuse\n"
                    ", partiellement creuse ainsi vous devinez qu'il va \n"
                    "falloir se deplacer sur celle ci afin d'atteindre \n"
                    "les monstres et pouvoir les battres.\n\n"
                    "2) Le combat : si vous bougez ou attaquer, cela \n"
                    "compte comme 1 action quand vous effectuez une \n"
                    "action (ce qui n'inclue pas bouger la vision) \n"
                    "tout les ennemis dans la salle effectuerons aussi\n"
                    "une action. Dans l'ordre : \n"
                    " > Deplacement Joueur\n > Deplacement Monstre\n > attaque Monstre\n > attaque Joueur. \n"
                    "Vous pouvez ainsi toucher un ennemi sur la case ou \n"
                    "il va arriver ! c'est une infoa ne surtout pas negliger.\n\n"
                    "3) Le loot : quand vous vainquez un ennemi, \n"
                    "celui ci a 1 chance sur 2 de donner 1 objet \n"
                    "2 fois. (1 chance sur 2 > rien , \n"
                    "1 chance sur 2 > 1 objet , 1 chance sur 4 > 2 objets)\n\n"
                    "4) Les stats : vaincre des ennemis pour la gloire \n"
                    "c'est bien mais pour les points, c'est mieux. Tuer \n"
                    "un ennemi vous donne des points ET de << l'xp >> que vous pouvez\n"
                    " depenser en niveau. Attention ajouter des points \n"
                    "de vie augmente les points de vie MAX, mais pas les pv \n"
                    "et au contraire si vous enlever des stats de pv pour les \n"
                    "mettres en attaque et que les pv MAX < pv alors les pv \n"
                    "seront reduit aux pv MAX.",
    "Zombie": "Voila le Zombie, un mort vivant enfin je vous refais pas\n"
              "toute l'histoire quoi, vous voyez...",
    "Squelette": "Le Squelette, en chaire et en os... Enfin surtout \n"
                 "en os, puisque c'est un squelette du coup.",
    "Demon": "Je suis mechant, tres mechant, vraiment pas gentil du tout.",
    "Bat": "I'M BATMAN !!",
    "Ghost": "GHOST... BUSTER !!! Alors t as peur ?",
    "Golem": "Un tas de pierre mechant !!",
    "Spider": "Spider-cochon",
    "Diablotin": "je suis un mechant (sans sucre, sans aditif et \n"
                 "sans charisme)",
    "Vampire": "Suceur de sang de pere en fils S/o dracula",
    "BlobFeu": "Une boule de slime en feu. ",
    "Necromancien": "Invocateur (fou), attention aux zombies",
    "Aligator": "Il porte pas des TN mais il mord",
    "Abomination": "Un mob moche, tres moche, tu veux pas le voir je pense",
    "Mommies": "Une momie reanime pour te tuer",
    "Loup": "Le Village se reveille ...",
    "Fox": "Goupil, rien de plus.",
    "BlobEau": "Une boule... d'eau en eau'",
    "Witch": "Cette personne est extremement enquiquinante sur le \n"
             "jeu nommee Minecraft.",
    "DragonFeu": "Un dragon qui vole et crache du feu de loin",
    "Snake": "SSSSSSSSSSSsssssssssssssssssssssssSSSSSSSSSSSSS",
    "Creeper": "tsssssssssss... BOOOOOOOOOM (tah la ref)",
    "Rampant": "Discret tel la musaraigne, mord les pieds et les mollets",
    "Notch": "Vous connaissez son jeu ? Moi je l aime bien il est style \n"
             " et peu connu genre 238 millions de telechargement",
    "Angel": "Vous savez se qu on dis, il ne faut pas tuer l habit du moine\n"
             "avant d avoir chasser la pierre qui roule et voir la goutte d'eau\n"
             "sonner a sa porte.",
    "Arcangel": "Wsh Tyrael depuis qu on a battue Diablo, ca se passe bien ?",
    "DragonLight": "Un dragon qui vole et crache de la LUMIERE de loin wow",
    "BlobPlant": "Une boule de plante qui bouge, lourd hein ?",
    "DragonDark": "LE TEMOIN VOUS OBSERVE .. sa forme final approche, mais n ayez crainte\n"
                  "les gardiens sont la.",
    "DragonEau": "Un dragon qui vole et crache de l'EAU... de loin... attention aux eclaboussures",
    "DragonPlant": "Le papier ca coupe.",
    "BlobLight": "Une boule de lumiere... aveuglante et dangereuse",
    "BlobDark": "Une boule de noirceur, toute noire et noire",
}

ATTRIBUT = {
    "Zombie": "Aucune capacite",
    "Squelette": " - Longue portee",
    "Demon": " - MINI BOSS (peu de chance de spawn) \n - degats tres elevees",
    "Bat": "Aucune capacite",
    "Ghost": " - extremement resistant aux arcs",
    "Golem": " - resistant aux degats elementaires (-50 pourcents) \n - faibles aux degats physisques (+20 pourcents)",
    "Spider": "Aucune capacite",
    "Diablotin": "Aucune capacite",
    "Vampire": " - recupere 50 pourcent de sa vie a chaque coup infligee",
    "BlobFeu": " - insensible a l'element plante",
    "Necromancien": " - fait apparaître 1 ou 2 ennemis a certains tours",
    "Aligator": "Aucune capacite",
    "Abomination": " - MINI BOSS (peu de chance de spawn) \n - gros paterne d'attaque",
    "Mommies": "Aucune capacite",
    "Loup": "Aucune capacite",
    "Fox": " - possede 2 tours pour chaque actions",
    "BlobEau": " - insensible a l'element feu",
    "Witch": "Aucune capacite",
    "DragonFeu": "Aucune capacite",
    "Snake": "Aucune capacite",
    "Creeper": " - inflige de gros degats mais meurt au meme tour",
    "Rampant": "Aucune capacite",
    "Notch": " - MINI BOSS (peu de chance de spawn)\n - points de vie tres elevees",
    "Angel": "Aucune capacite",
    "Arcangel": "Aucune capacite",
    "DragonLight": "Aucune capacite",
    "BlobPlant": " - insensible a l'element eau",
    "DragonDark": "Aucune capacite",
    "DragonEau": "Aucune capacite",
    "DragonPlant": "Aucune capacite",
    "BlobLight": " - insensible a l'element tenebre",
    "BlobDark": " - insensible a l'element lumiere",
}


song = [
    "end",
    "catacomb theme",
    "damage",
    "desert",
    "item",
    "hell",
]

# milieu d'un mot en pixels :
MILIEUMOT = lambda n_lettre: (n_lettre*4-1)/2 - 1
