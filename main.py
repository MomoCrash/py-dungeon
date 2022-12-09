import pyxel as py
from Entity import *
from Tile import Tile
from random import randint


class Game:
    def __init__(self):
        py.init(256, 256, fps=60)
        py.load("assets.pyxres")
        # map basique de taille : 16 par 16
        self.map_dim = []
        self.grille = []
        self.new_map(0, 0, 15, 15)
        self.player = Player(self, 1, 0)
        self.ennemi = []
        self.rand_spawns(3, local_section=(8, 8, 6, 6))

    def new_map(self, u, v, w, h):
        self.map_dim = [u, v, w, h]
        self.grille = []
        for i in range(self.map_dim[2]):
            self.grille.append([])
            for j in range(self.map_dim[3]):
                self.grille[i].append(Tile(self.map_dim[0]+i, self.map_dim[1]+j))

    def rand_spawns(self, n, local_section=(0, 0, 14, 14)):
        spawned = 0
        while spawned < n:
            x = randint(local_section[0], local_section[0]+local_section[2])
            y = randint(local_section[1], local_section[1]+local_section[3])
            if "obst" not in self.grille[x][y].types and not self.check_full_tile(x, y):
                self.ennemi.append(Zombie(self, x, y))
                spawned += 1

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
            for e in self.ennemi:
                e.rand_move()
        if py.btnp(py.KEY_D, hold=60):
            self.player.right()
            for e in self.ennemi:
                e.rand_move()
        if py.btnp(py.KEY_Z, hold=60):
            self.player.top()
            for e in self.ennemi:
                e.rand_move()
        if py.btnp(py.KEY_S, hold=60):
            self.player.bottom()
            for e in self.ennemi:
                e.rand_move()

        if py.btnp(py.KEY_LEFT, hold=60):
            self.player.watch_left()
        if py.btnp(py.KEY_RIGHT, hold=60):
            self.player.watch_right()
        if py.btnp(py.KEY_UP, hold=60):
            self.player.watch_top()
        if py.btnp(py.KEY_DOWN, hold=60):
            self.player.watch_bottom()

        if py.btnp(py.KEY_A, hold=60):
            touched = self.player.weapon.get_ennemi_in_range()
            for e in touched:
                e.damage(self.player.weapon.dmg)
            for e in self.ennemi:
                e.rand_move()
        if py.btnp(py.KEY_E, hold=60):
            for e in self.ennemi:
                print(e.get_if_player_touched())
        if py.btnp(py.KEY_R, hold=60):
            self.rand_spawns(3)
        if py.btnp(py.KEY_F, hold=60):
            self.player.damage(10)

    def draw(self):
        py.cls(0)
        py.bltm(0, 0, 0, self.map_dim[0]*16, self.map_dim[1]*16, self.map_dim[2]*16, self.map_dim[3]*16, 0)
        for e in self.ennemi:
            e.blit_entity()
            e.blit_life_bar()
            e.range_blit()
        self.player.blit_entity()
        self.player.weapon.blit_range()
        py.rect(0, 240, 240, 16, 8)
        py.rect(0, 240, (self.player.hp/self.player.maxhp)*240, 16, 11)

    def run(self):
        py.run(self.update, self.draw)


g = Game()
g.run()
