import pyxel as py
from random import randint

class Entity:
    def __init__(self, game, x: int, y: int, img: tuple, size: tuple, hp: int, colkey: int = 0):
        self.hp = hp
        self.x = x
        self.y = y
        self.imgX = img
        self.imgY = (img[0] + size[0], img[1])
        self.img = self.imgX
        self.size = size
        self.game = game
        self.colkey = colkey

    def watch_left(self):
        self.size = (abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX

    def left(self):
        if not self.x > 0:
            return
        c1 = "obst" not in self.game.grille[self.x - 1][self.y].types
        c2 = not self.game.check_full_tile(self.x-1, self.y)
        if c1 and c2:
            self.x -= 1
        self.watch_left()

    def watch_right(self):
        self.size = (-abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX

    def right(self):
        if not self.x < len(self.game.grille) - 1:
            return
        c1 = "obst" not in self.game.grille[self.x + 1][self.y].types
        c2 = not self.game.check_full_tile(self.x+1, self.y)
        if c1 and c2:
            self.x += 1
        self.watch_right()

    def watch_top(self):
        self.size = (abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgY

    def top(self):
        if not self.y > 0:
            return
        c1 = "obst" not in self.game.grille[self.x][self.y - 1].types
        c2 = not self.game.check_full_tile(self.x, self.y-1)
        if c1 and c2:
            self.y -= 1
        self.watch_top()

    def watch_bottom(self):
        self.size = (abs(self.size[0]), -abs(self.size[1]))
        self.img = self.imgY

    def bottom(self):
        if not self.y < len(self.game.grille[0]) - 1:
            return
        c1 = "obst" not in self.game.grille[self.x][self.y + 1].types
        c2 = not self.game.check_full_tile(self.x, self.y+1)
        if c1 and c2:
            self.y += 1
        self.watch_bottom()


class Player(Entity):
    def __init__(self, game, x:int, y:int):
        super().__init__(game, x, y, (32, 0), (16, 16), 100)


class Ennemies(Entity):
    def __init__(self, game, x: int, y: int, img: tuple, size: tuple, hp: int, colkey: int = 0):
        super().__init__(game, x, y, img, size, hp, colkey=colkey)

    def rand_move(self):
        a = randint(1, 4)
        if a == 1:
            self.left()
        if a == 2:
            self.right()
        if a == 3:
            self.top()
        if a == 4:
            self.bottom()


class TestEn(Ennemies):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, (32, 16), (16, 16), 20, colkey=7)
