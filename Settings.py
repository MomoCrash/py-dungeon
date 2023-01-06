
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
        (4, 6), (5, 6), (4, 7), (5, 7),  # eau
        (10, 6), (11, 6), (10, 7), (11, 7),  # eau
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
DEAFEAT_FIRST_PART = lambda x, y: (x, y, 2, 0, 240, 32, 16, 7)
DEAFEAT_SECOND_PART = lambda x, y: (x, y, 2, 16, 224, 16, 16, 7)

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
    "BabyDragon": lambda x, y: (x, y, 1, 32, 64, 16, 16, 7),
}


# Text

TEXTS = {
    "touches": "[Touches]\n"
               "\t - Z,Q,S,D -> Déplacements\n"
               "\t - A -> Attaquer\n"
               "\t - E -> Interagir/Ramasser\n"
               "\t - Flèches -> Diriger la visée\n"
               "\t - F -> Echanger d'armes\n"
               "\t - W -> Skip la salle de loot\n"
               "\t - TAB -> Ouvrir/Fermer les menus\n"
               "\t - X -> Ouvrir le Bestiaire",
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
            "testtesttesttesttesttesttesttesttesttest\n",
    "Zombie": "Voilà le Zombie, un mort vivant enfin je vous refais pas\n"
              "toute l'histoire quoi vous voyez ...",
    "Squelette": "Le Squelette, En char et en os... Enfin surtout \n"
                 "en os puisque c'est un squelette.",
    "Demon": "je ne sais pas mais voila",
    "Bat": "I'M BATMAN",
    "Ghost": "je ne sais pas mais voila",
    "Golem": "je ne sais pas mais voila",
    "Spider": "CHUIS SPIDERMAN FDP",
    "Diablotin": "je ne sais pas mais voila",
    "Vampire": "je ne sais pas mais voila",
    "BlobFeu": "je ne sais pas mais voila",
    "Necromancien": "je ne sais pas mais voila",
    "Aligator": "je ne sais pas mais voila",
    "Abomination": "je ne sais pas mais voila",
    "Mommies": "je ne sais pas mais voila",
    "Loup": "je ne sais pas mais voila",
    "Fox": "je ne sais pas mais voila",
    "BlobEau": "je ne sais pas mais voila",
    "Witch": "je ne sais pas mais voila",
    "BabyDragon": "je ne sais pas mais voila",
}

song = [
    "end",
    "catacomb theme",
    "damage",
    "desert",
    "item",
    "hell",

]