import pyxel as py
from random import randint
from Equipment import *


class Entity:
    def __init__(self, game, x: int, y: int, img: tuple, size: tuple, hp: int, colkey: int = 0):
        self.maxhp = hp
        self.hp = hp
        self.x = x
        self.y = y
        self.imgX = img
        self.imgY = (img[0] + size[0], img[1])
        self.img = self.imgX
        self.size = size
        self.game = game
        self.colkey = colkey
        self.orient = "right"

    def watch_left(self):
        self.size = (abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX
        self.orient = "left"

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
        self.orient = "right"

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
        self.orient = "top"

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
        self.orient = "bottom"

    def bottom(self):
        if not self.y < len(self.game.grille[0]) - 1:
            return
        c1 = "obst" not in self.game.grille[self.x][self.y + 1].types
        c2 = not self.game.check_full_tile(self.x, self.y+1)
        if c1 and c2:
            self.y += 1
        self.watch_bottom()

    def damage(self, amount):
        pass

    def blit_entity(self):
        py.blt(self.x * 16, self.y * 16, 0, self.img[0], self.img[1], self.size[0],self.size[1], self.colkey)

    def blit_life_bar(self):
        py.rect(self.x*16, self.y*16-5, 16, 5, 8)
        py.rect(16*self.x, 16*self.y-5, (self.hp/self.maxhp)*16, 5, 11)


class Player(Entity):
    def __init__(self, game, x:int, y:int):
        super().__init__(game, x, y, (32, 0), (16, 16), 100)
        self.weapon = Spear(self)
        self.armor = Armor(self)

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.game.player = Player(self.game, 0, 0)


class Ennemies(Entity):
    def __init__(self, game, x: int, y: int, img: tuple, size: tuple, hp: int, colkey: int = 0):
        super().__init__(game, x, y, img, size, hp, colkey=colkey)
        self.dmg = 10
        self.patern = {"left": [[(-1, 0)]],
                       "right": [[(1, 0)]],
                       "top": [[(0, -1)]],
                       "bottom": [[(0, 1)]],
                       }
        self.attaque_tile = (16, 32)

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

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.game.ennemi.remove(self)

    def range_blit(self):
        for line in self.patern[self.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.x + pos[0] < len(self.game.grille) and 0 <= self.y + pos[1] < len(self.game.grille[0]) and not "obst" in self.game.grille[self.x + pos[0]][self.y + pos[1]].types:
                    py.blt((self.x + pos[0]) * 16, (self.y + pos[1]) * 16, 0, self.attaque_tile[0],self.attaque_tile[1], 16, 16, 0)
                else:
                    blocked = True

    def get_if_player_touched(self):
        for line in self.patern[self.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.x + pos[0] < len(self.game.grille) and 0 <= self.y + pos[1] < len(self.game.grille[0]) and not "obst" in self.game.grille[self.x + pos[0]][self.y + pos[1]].types:
                    if self.game.player.x == self.x + pos[0] and self.game.player.y == self.y + pos[1]:
                        return True
                else:
                    blocked = True
        return False


class TestEn(Ennemies):
    def __init__(self, game, x: int, y: int):
        super().__init__(game, x, y, (32, 16), (16, 16), 20, colkey=7)
