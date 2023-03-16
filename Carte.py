from random import choice, random
from Entity import *
from Settings import EQUIVALANCE, IMAGE_PORTE_FERMEE, IMAGE_PORTE_OUVERTE, LIMITE

# variable globals -----------------------------------------------------------------------------------------------------

CARTE_SPAWN = {
    "Cave": [(Zombie, 1), (Squelette, 1), (Diablotin, 1), (Golem, 1), (Ghost, 1), (Bat, 1), (Witch, 1), (DragonFeu, 1), (DragonDark, 1), (BlobDark, 1), (Creeper, 1)],
    "Grass": [(Spider, 1), (Loup, 1), (Fox, 1), (BlobFeu, 1), (BlobEau, 1), (DragonFeu, 1), (BlobPlant, 1), (BlobLight, 1), (BlobDark, 1), (DragonPlant, 1)],
    "Grass2": [(Zombie, 1)],
    "Desert": [(Aligator, 1), (Golem, 1), (Mommies, 1), (Squelette, 1), (Mommies, 1), (Snake, 1), (DragonEau, 1)],
    "Catacombes": [(Zombie, 1), (Squelette, 1), (Vampire, 1), (Necromancien, 1), (Rampant, 1)],
    "Paradis": [(Angel, 1), (Arcangel, 1), (DragonLight, 1), (BlobLight, 1)],
    "Enfer": [(Diablotin, 1)]
}

CARTE_BOSS = {
    "Cave": ({"class": Abomination, "hp": 10, "attack": 2}, {"class": Notch, "hp": 10, "attack": 2}, {"class": Demon, "hp": 10, "attack": 2}),
    "Grass": (),
    "Desert": (),
    "Catacombes": ()
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
        for k in EQUIVALANCE.keys():
            for i in self.tiles:
                for j in i:
                    if j in EQUIVALANCE[k] and k not in self.types:
                        self.types.append(k)


class Carte:
    """classe qui représente la carte formé de plein de grandes tuiles composé de tuiles plus petite"""

    def __init__(self, game):
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
        # map basique de taille : 16 par 16
        self.map_dim = [()]
        self.grille = []
        self.new_map()
        self.etage_completed = False
        self.biome = "Grass"
        self.stage = 0

    def new_map(self, forced: list = None, loot=False) -> None:
        """
        Créé une nouvelle map, quand elle est aléatoire, on va récupérer 4 morceaux de map prédéfini pour ne pas créé
        de problème de chemin et on les assemble au hasard pour créer une map.

        Aussi, si loot et forced sont renseigné, loot prend l'ascendent

        :param loot: défini si c'est une salle de loot ou non (vide ou non)
        :param forced: si renseigné créé une map en particulier (non random)
        """
        if loot:
            self.map_dim = [(LIMITE[self.biome][0], LIMITE[self.biome][1]) for _ in range(4)]
        elif forced is not None:
            self.map_dim = forced
        else:
            self.biome = choice(list(LIMITE.keys()))
            self.map_dim = [(randint(LIMITE[self.biome][0], LIMITE[self.biome][0] + LIMITE[self.biome][2]),  # X
                             randint(LIMITE[self.biome][1], LIMITE[self.biome][3] + LIMITE[self.biome][1]))  # Y
                            for _ in range(4)]
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

    def new_stage(self, forced: list = None) -> None:
        """créé un nouveau stage en fonction de la situation du personnage."""
        if self.game.looting:
            self.new_map(forced=forced)
            self.game.player.place(0, 0)
            self.game.loots.clear()
            self.rand_spawns(randint(2, 5), specifique_biome=CARTE_SPAWN[self.biome], local_section=(8, 8, 7, 7))
            self.etage_completed = False
            self.stage += 1
            self.game.looting = not self.game.looting
        else:
            self.new_map(loot=True)
            self.game.player.place(0, 0)
            for iloot in range(len(self.game.loots)):
                self.game.loots[iloot].x = 1 + iloot % 14
                self.game.loots[iloot].y = 1 + iloot // 14
            self.etage_completed = False
            self.game.looting = not self.game.looting

    def rand_spawns(self, n, loot=True, specifique_biome: list = None, local_section=(0, 0, 15, 15)) -> None:
        """
        Rajoute des ennemies aléatoirement sur la map, où il n'y a pas de mur.
        :param loot: bool                               | défini si les ennemis laisse de l'equipment ou non
        :param specifique_biome: list(type)             | liste de tout les monstres qui peuvent apparaître dans un biome
        :arg n: int                                     | nombre d'ennemis à rajouter.
        :arg local_section: tuple(int, int, int, int)   | représente le rectangle où peut spawn les ennemies par défault toute la map. (x, y, width, height)
        """
        specifique = Zombie
        spawned = 0
        if specifique_biome is None:
            specifique_biome = [(e, 1) for e in Ennemies.__subclasses__()]
        while spawned < n:
            x = randint(local_section[0], local_section[0] + local_section[2])
            y = randint(local_section[1], local_section[1] + local_section[3])
            if "obst" not in self.grille[x][y].types and "ground" not in self.grille[x][y].types and not self.game.check_full_tile(x, y):
                total = 0
                for monster in specifique_biome:
                    total += monster[1]
                val = total * random.random()
                for monster in specifique_biome:
                    val -= monster[1]
                    if val <= 0:
                        specifique = monster[0]
                        break
                type_spawn = specifique
                self.game.ennemi.append(type_spawn(self.game, x, y, self.stage // 4 + 1, loot))
                spawned += 1

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
