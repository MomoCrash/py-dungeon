import pyxel as py
from random import randint

# variable globals -----------------------------------------------------------------------------------------------------

# image de la porte de sortie :
IMAGE_PORTE_FERMEE = (32, 0)
IMAGE_PORTE_OUVERTE = (48, 0)

# définition des murs et des pièges
_equivalance = {
    "obst": [
        (0, 2), (0, 3), (1, 2), (1, 3),
        (2, 2), (2, 3), (3, 2), (3, 3),
        (12, 6), (13, 6), (12, 7), (13, 7),
        (14, 6), (15, 6), (14, 7), (15, 7)
    ],
    "trap": [
        (5, 2), (6, 2), (5, 3), (6, 3)
    ]
}

# position des biomes
LIMITE = {
    "Cave": (0, 3, 3),
    "Grass": (1, 2, 1)
}


# Objects --------------------------------------------------------------------------------------------------------------
class Tile:
    """
    classe qui représente une tuile sois 16x16 pixels
    """

    def __init__(self, x, y):
        """
        :param x: int                           | position en x (en pixels)
        :param y: int                           | position en y (en pixels)
        :var x: int                             | position en x en pixels
        :var y: int                             | position en y en pixels
        :var self.tiles: list(tuple(int, int)) | images des 4 petite tuiles dans le carré de 16x16
        :var self.types: list(str)              | pour les 4 petites tuiles, avec la variable _equivalance je peux savoir si c'est un mur, un piège ou autre ou rien

        """
        self.x = x
        self.y = y
        self.tiles = []
        for i in range(2):
            self.tiles.append([])
            for j in range(2):
                self.tiles[i].append(py.tilemap(0).pget((self.x + i * 8) / 8, (self.y + j * 8) / 8))
        self.types = []
        for k in _equivalance.keys():
            for i in self.tiles:
                for j in i:
                    if j in _equivalance[k] and k not in self.types:
                        self.types.append("obst")


class Carte:
    """classe qui représente la carte formé de plein de grandes tuiles composé de tuiles plus petite"""

    def __init__(self, limiteX: int, limiteY: int, game):
        """
        :param game: Game | lien d'accès au jeu entier
        :var self.game: Game | accès au jeu entier
        :var self.limite: /
        :var self.map_dim: list(tuple(x int, y int)) | liste avec les positions des morceaux de map (en map c'est-a-dire, 0 = première, 1 = deuxième)
        :var self.grille: list(list(Tile)) | matrice avec les tuiles dedans (liste de colonne grille[x][y])
        :var self.etage_completed: bool | défini si la porte est ouverte
        :var self.stage: int | niveau actuel
        """
        self.game = game
        self.limite = (limiteX, limiteY)
        # map basique de taille : 16 par 16
        self.map_dim = [()]
        self.grille = []
        self.new_map()
        self.etage_completed = False
        self.stage = 1

    def new_map(self, forced: list = None, loot=False) -> None:
        """
        Créé une nouvelle map, quand elle est aléatoire, on va récupérer 4 morceaux de map prédéfini pour ne pas créé
        de problème de chemin et on les assemble au hasard pour créer une map.

        Aussi, si loot et forced sont renseigné, loot prend l'ascendent

        :param loot: défini si c'est une salle de loot ou non (vide ou non)
        :param forced: si renseigné créé une map en particulier (non random)
        """
        if loot:
            self.map_dim = [(3, 0) for _ in range(4)]
        elif forced is not None:
            self.map_dim = forced
        else:
            self.map_dim = [(randint(0, self.limite[0]), randint(0, self.limite[1])) for _ in range(4)]
        self.grille = []
        temp = []
        for i in range(4):
            temp.append([])
            for x in range(8):
                temp[i].append([])
                for y in range(8):
                    temp[i][x].append(Tile(self.map_dim[i][0] * 128 + x * 16, self.map_dim[i][1] * 128 + y * 16))
        for i in range(2):
            for iColumn in range(8):
                self.grille.append(temp[i * 2][iColumn] + temp[i * 2 + 1][iColumn])
        self.grille[15][15].types.append("end")

    def new_stage(self) -> None:
        """créé un nouveau stage en fonction de la situation du personnage."""
        if self.game.looting:
            self.new_map()
            self.game.player.x = 0
            self.game.player.y = 0
            self.game.loots.clear()
            self.game.rand_spawns(randint(2, 5), local_section=(8, 8, 7, 7))
            self.etage_completed = False
            self.stage += 1
            self.game.looting = not self.game.looting
        else:
            self.new_map(loot=True)
            self.game.player.x = 0
            self.game.player.y = 0
            for iloot in range(len(self.game.loots)):
                self.game.loots[iloot].x = 1 + iloot % 14
                self.game.loots[iloot].y = 1 + iloot // 14
            self.etage_completed = False
            self.stage += 1
            self.game.looting = not self.game.looting

    def actualisation(self) -> None:
        """actualise les évênements sur la map"""
        if len(self.game.ennemi) == 0:
            self.etage_completed = True

    def blit(self) -> None:
        """affichage du layer de la map et du stage où on se trouve."""
        for y in range(2):
            for x in range(2):
                py.bltm(x * 128, y * 128, 0, self.map_dim[int(f"{x}{y}", 2)][0] * 128,
                        self.map_dim[int(f"{x}{y}", 2)][1] * 128, 128, 128, 0)
        if self.etage_completed:
            py.blt(240, 240, 0, IMAGE_PORTE_OUVERTE[0], IMAGE_PORTE_OUVERTE[1], 16, 16, 7)
        else:
            py.blt(240, 240, 0, IMAGE_PORTE_FERMEE[0], IMAGE_PORTE_FERMEE[1], 16, 16, 7)

        py.text(256, 240, f" stage: \n {self.stage if self.stage < 999 else '999+'}", 7)
