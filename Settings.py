from Menu import *

IMAGE_PORTE_FERMEE = (32, 0)
IMAGE_PORTE_OUVERTE = (48, 0)

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
    ],
    "left-side": [
        (22, 16), (23, 16), (22, 17), (23, 17),  # wall (top left corner)
        (26, 16), (27, 16), (26, 17), (27, 17),  # wall (bottom left corner)
        (30, 16), (31, 16), (30, 17), (31, 17),  # wall (left)
        (14, 14), (15, 14), (14, 15), (15, 15),  # trap wall (left)
        (18, 14), (19, 14), (18, 15), (19, 15),  # laser wall (left)
    ],
    "right-side": [
        (24, 16), (25, 16), (24, 17), (25, 17),  # wall (bottom right corner)
        (28, 16), (29, 16), (28, 17), (29, 17),  # wall (top right corner)
        (30, 14), (31, 14), (30, 15), (31, 15),  # wall (right)
        (16, 14), (17, 14), (16, 15), (17, 15),  # trap wall (right)
        (20, 14), (21, 14), (20, 15), (21, 15),  # laser wall (right)
    ],
    "top-side": [
        (22, 16), (23, 16), (22, 17), (23, 17),  # wall (top left corner)
        (28, 16), (29, 16), (28, 17), (29, 17),  # wall (top right corner)
        (26, 14), (27, 14), (26, 15), (27, 15),  # wall (top)
        (10, 14), (11, 14), (10, 15), (11, 15),  # trap wall (top)
        (24, 14), (25, 14), (24, 15), (25, 15),  # laser wall (top)
    ],
    "bottom-side": [
        (24, 16), (25, 16), (24, 17), (25, 17),  # wall (bottom right corner)
        (26, 16), (27, 16), (26, 17), (27, 17),  # wall (bottom left corner)
        (28, 14), (29, 14), (28, 15), (29, 15),  # wall (bottom)
        (12, 14), (13, 14), (12, 15), (13, 15),  # trap wall (bottom)
        (22, 14), (23, 14), (22, 15), (23, 15),  # laser wall (bottom)
    ],
    "event": [  # déclancheur d'évênement
        (5, 2), (6, 2), (5, 3), (6, 3),  # piège éclaté
        (8, 14), (9, 14), (8, 15), (9, 15),  # piège sol
    ]
}

# position des biomes
LIMITE = {
    "Cave": (0, 3, 2),
    "Grass": (1, 3, 2),
    'Desert': (2, 3, 2),
    "Catacombes": (3, 3, 2),
}

# math pour transformer le int de l'orientation en coordonné
f = lambda x: round((2/3)*x**3 - (7/2)*x**2 + (29/6)*x - 1)
g = lambda x: round((2/3)*x**3 - (5/2)*x**2 + (11/6)*x)

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
}

EFFICACITE = ((1, 1, 1, 1, 1, 1), (1, 0.9, 0.5, 2, 0.7, 0.7), (1, 2, 0.9, 0.5, 0.7, 0.7), (1, 0.5, 2, 0.9, 0.7, 0.7), (1, 1, 1, 1, 0, 3), (1, 1, 1, 1, 3, 0))

ORIENT_EQ = ["left", "right", "top", "bottom"]

IMAGE_ENTITE = 1

# images :

KATANA0 = lambda x, y: (x, y, 2, 16, 184, 16, 32, 0)
KATANA1 = lambda x, y: (x, y, 2, 32, 184, 16, 32, 0)
KATANA2 = lambda x, y: (x, y, 2, 48, 184, 16, 32, 0)
DRAGON_SCAlE_ARMOR = lambda x, y: (x, y, 2, 48, 224, 16, 32, 0)
BABY_DRAGON = lambda x, y: (x, y, 1, 32, 64, 16, 16, 7)

# Text

texts = {
    "touches": "[Touches]\n"
               "\t - Z,Q,S,D -> Déplacements\n"
               "\t - A -> Attaquer\n"
               "\t - E -> Interagir/Ramasser\n"
               "\t - Flèches -> Diriger la visée\n"
               "\t - F -> Echanger d'armes\n"
               "\t - W -> Skip la salle de loot\n"
               "\t - TAB -> Ouvrir/Fermer les menus",
    "test": "[HISTOIRE]\n"
            "   testtesttesttesttesttesttesttesttestt\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
            "testtesttesttesttesttesttesttesttesttest\n"
}