import pyxel as py
from Entity import *
from random import randint
from Carte import Carte


class Game:
    def __init__(self):
        py.init(272, 272, fps=60, quit_key=py.KEY_ESCAPE)
        py.load("assets.pyxres")
        self.carte = Carte(1, 1)
        self.player = Player(self, 1, 0)
        self.ennemi = []
        self.rand_spawns(3, local_section=(8, 8, 6, 6))

    def rand_spawns(self, n, local_section=(0, 0, 14, 14)):
        spawned = 0
        while spawned < n:
            x = randint(local_section[0], local_section[0]+local_section[2])
            y = randint(local_section[1], local_section[1]+local_section[3])
            if "obst" not in self.carte.grille[x][y].types and not self.check_full_tile(x, y):
                r = randint(1, 2)
                if r == 1:
                    self.ennemi.append(Zombie(self, x, y, 1))
                else:
                    self.ennemi.append(Squelette(self, x, y, 1))
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
                e.action()
        if py.btnp(py.KEY_D, hold=60):
            self.player.right()
            for e in self.ennemi:
                e.action()
        if py.btnp(py.KEY_Z, hold=60):
            self.player.top()
            for e in self.ennemi:
                e.action()
        if py.btnp(py.KEY_S, hold=60):
            self.player.bottom()
            for e in self.ennemi:
                e.action()

        if py.btnp(py.KEY_LEFT, hold=60):
            self.player.watch_left()
        if py.btnp(py.KEY_RIGHT, hold=60):
            self.player.watch_right()
        if py.btnp(py.KEY_UP, hold=60):
            self.player.watch_top()
        if py.btnp(py.KEY_DOWN, hold=60):
            self.player.watch_bottom()

        if py.btnp(py.KEY_A, hold=60):
            for e in self.ennemi:
                e.action()
            self.player.attaque()
        if py.btnp(py.KEY_E, hold=60):
            for e in self.ennemi:
                print(e.get_if_player_touched())
        if py.btnp(py.KEY_R, hold=60):
            self.rand_spawns(3)
        if py.btnp(py.KEY_F, hold=60):
            self.player.damage(10)

    def draw(self):
        py.cls(0)
        self.carte.blit()
        for e in self.ennemi:
            e.blit_entity()
            e.range_blit()
            e.blit_life_bar()
        self.player.blit_entity()
        self.player.weapon.blit_range()
        py.rect(0, 256, 256, 16, 8)
        py.rect(0, 256, (self.player.hp/self.player.maxhp)*256, 16, 11)

    def run(self):
        py.run(self.update, self.draw)


g = Game()
g.run()
