import pyxel as py
from Entity import *
from Tile import Tile


class Game:
    def __init__(self):
        py.init(256, 256, fps=60)
        py.load("assets.pyxres")
        # map basique de taille : 16 par 16
        self.map_dim = [0, 0, 16, 16]
        self.grille = []
        self.new_map(self.map_dim[0], self.map_dim[1], self.map_dim[2], self.map_dim[3],)
        self.player = Player(self, 1, 0)
        self.ennemi = [TestEn(self, 10, 10)]

    def new_map(self, u, v, w, h):
        self.grille = []
        for i in range(w):
            self.grille.append([])
            for j in range(h):
                self.grille[i].append(Tile(u+i, v+j))
        """for i in grid:
            print([j.tiles for j in i])"""

    def check_full_tile(self, x, y):
        for e in self.ennemi:
            if e.x == x and e.y == y:
                return True
        if self.player.x == x and self.player.y == y:
            return True
        return False

    def update(self):
        if py.btnp(py.KEY_Q, hold=60):
            self.player.left()
            self.ennemi[0].rand_move()
        if py.btnp(py.KEY_D, hold=60):
            self.player.right()
            self.ennemi[0].rand_move()
        if py.btnp(py.KEY_Z, hold=60):
            self.player.top()
            self.ennemi[0].rand_move()
        if py.btnp(py.KEY_S, hold=60):
            self.player.bottom()
            self.ennemi[0].rand_move()

        if py.btnp(py.KEY_LEFT, hold=60):
            self.player.watch_left()
        if py.btnp(py.KEY_RIGHT, hold=60):
            self.player.watch_right()
        if py.btnp(py.KEY_UP, hold=60):
            self.player.watch_top()
        if py.btnp(py.KEY_DOWN, hold=60):
            self.player.watch_bottom()

    def draw(self):
        py.cls(0)
        py.bltm(0, 0, 0, self.map_dim[0]*16, self.map_dim[1]*16, self.map_dim[2]*16, self.map_dim[3]*16, 0)
        for e in self.ennemi:
            py.blt(e.x*16, e.y*16, 0, e.img[0], e.img[1], e.size[0], e.size[1], e.colkey)
        py.blt(self.player.x * 16, self.player.y * 16, 0, self.player.img[0], self.player.img[1], self.player.size[0], self.player.size[1], self.player.colkey)

    def run(self):
        py.run(self.update, self.draw)


g = Game()
g.run()
