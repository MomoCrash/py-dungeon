import pyxel as py
from Tile import Tile
from random import randint


class Carte:
    def __init__(self, limiteX: int, limiteY: int):
        self.limite = (limiteX, limiteY)
        # map basique de taille : 16 par 16
        self.map_dim = [()]
        self.grille = []
        self.new_map()

    def new_map(self):
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

    def blit(self):
        for y in range(2):
            for x in range(2):
                py.bltm(x*128, y*128, 0, self.map_dim[int(f"{x}{y}", 2)][0]*128, self.map_dim[int(f"{x}{y}", 2)][1]*128, 128, 128, 0)


if __name__ == '__main__':
    py.init(256, 256)
    py.load("assets.pyxres")
    c = Carte()

    for x in range(16):
        print([c.grille[i][x].types for i in range(16)])

    camPosX = 0
    camPosY = 0

    def update():
        global camPosY, camPosX
        if py.btn(py.KEY_LEFT):
            camPosX -= 1
            py.camera(py.camera(camPosX, camPosY))
        if py.btn(py.KEY_RIGHT):
            camPosX += 1
            py.camera(py.camera(camPosX, camPosY))
        if py.btn(py.KEY_UP):
            camPosY -= 1
            py.camera(py.camera(camPosX, camPosY))
        if py.btn(py.KEY_DOWN):
            camPosX += 1
            py.camera(py.camera(camPosX, camPosY))


    def draw():
        c.blit()


    py.run(update, draw)