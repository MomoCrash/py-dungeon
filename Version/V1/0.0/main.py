import pyxel as py
from Entity import Entity
from Tile import Tile


class Game:
    def __init__(self):
        py.init(256, 256, fps=60)
        py.load("assets.pyxres")
        # map basique de taille : 16 par 16
        self.map_dim = [0, 0, 16, 16]
        self.grille = self.new_map(self.map_dim[0], self.map_dim[1], self.map_dim[2], self.map_dim[3],)
        self.player = Entity(self, 1, 0, (32, 0), (16, 16), 100, colkey=0)

    def new_map(self, u, v, w, h):
        grid = []
        for i in range(w):
            grid.append([])
            for j in range(h):
                grid[i].append(Tile(u+i, v+j))
        """for i in grid:
            print([j.tiles for j in i])"""
        return grid

    def update(self):
        if py.btnp(py.KEY_Q, hold=60):
            self.player.left()
        if py.btnp(py.KEY_D, hold=60):
            self.player.right()
        if py.btnp(py.KEY_Z, hold=60):
            self.player.top()
        if py.btnp(py.KEY_S, hold=60):
            self.player.bottom()

    def draw(self):
        py.cls(0)
        py.bltm(0, 0, 0, self.map_dim[0]*16, self.map_dim[1]*16, self.map_dim[2]*16, self.map_dim[3]*16, 0)
        py.blt(self.player.x*16, self.player.y*16, 0, self.player.img[0], self.player.img[1], self.player.size[0], self.player.size[1], self.player.colkey)

    def run(self):
        py.run(self.update, self.draw)


g = Game()
g.run()