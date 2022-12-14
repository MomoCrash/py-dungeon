import pyxel as py
from Tile import Tile
from random import randint

IMAGE_PORTE_FERMEE = (32, 0)
IMAGE_PORTE_OUVERTE = (48, 0)


class Carte:
    def __init__(self, limiteX: int, limiteY: int, game):
        self.game = game
        self.limite = (limiteX, limiteY)
        # map basique de taille : 16 par 16
        self.map_dim = [()]
        self.grille = []
        self.new_map()
        self.etage_completed = False
        self.stage = 1

    def new_map(self, loot=False):
        if loot:
            self.map_dim = [(3, 0) for _ in range(4)]
        else:
            self.map_dim = [(randint(0, self.limite[0]), randint(0, self.limite[1])) for _ in range(4)]
        self.grille = []
        temp = []
        for i in range(4):
            temp.append([])
            for x in range(8):
                temp[i].append([])
                for y in range(8):
                    temp[i][x].append(Tile(self.map_dim[i][0]*128+x*16, self.map_dim[i][1]*128+y*16))
        for i in range(2):
            for iColumn in range(8):
                self.grille.append(temp[i*2][iColumn]+temp[i*2+1][iColumn])
        self.grille[15][15].types.append("end")

    def new_stage(self):
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
            self.new_map(True)
            self.game.player.x = 0
            self.game.player.y = 0
            for iloot in range(len(self.game.loots)):
                self.game.loots[iloot].x = 1 + iloot % 14
                self.game.loots[iloot].y = 1 + iloot // 14
            self.etage_completed = False
            self.stage += 1
            self.game.looting = not self.game.looting

    def actualisation(self):
        if len(self.game.ennemi) == 0:
            self.etage_completed = True

    def blit(self):
        for y in range(2):
            for x in range(2):
                py.bltm(x*128, y*128, 0, self.map_dim[int(f"{x}{y}", 2)][0]*128, self.map_dim[int(f"{x}{y}", 2)][1]*128, 128, 128, 0)
        if self.etage_completed:
            py.blt(240, 240, 0, IMAGE_PORTE_OUVERTE[0], IMAGE_PORTE_OUVERTE[1], 16, 16, 7)
        else:
            py.blt(240, 240, 0, IMAGE_PORTE_FERMEE[0], IMAGE_PORTE_FERMEE[1], 16, 16, 7)

        py.text(256, 240, f" stage: \n {self.stage if self.stage < 999 else '999+'}", 7)
