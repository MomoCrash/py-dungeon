import pyxel as py
from random import randint
from Equipment import *
import random


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
        c1 = "obst" not in self.game.carte.grille[self.x - 1][self.y].types
        c2 = not self.game.check_full_tile(self.x-1, self.y)
        if c1 and c2:
            self.x -= 1
        self.watch_left()

    def watch_right(self):
        self.size = (-abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX
        self.orient = "right"

    def right(self):
        if not self.x < len(self.game.carte.grille) - 1:
            return
        c1 = "obst" not in self.game.carte.grille[self.x + 1][self.y].types
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
        c1 = "obst" not in self.game.carte.grille[self.x][self.y - 1].types
        c2 = not self.game.check_full_tile(self.x, self.y-1)
        if c1 and c2:
            self.y -= 1
        self.watch_top()

    def watch_bottom(self):
        self.size = (abs(self.size[0]), -abs(self.size[1]))
        self.img = self.imgY
        self.orient = "bottom"

    def bottom(self):
        if not self.y < len(self.game.carte.grille[0]) - 1:
            return
        c1 = "obst" not in self.game.carte.grille[self.x][self.y + 1].types
        c2 = not self.game.check_full_tile(self.x, self.y+1)
        if c1 and c2:
            self.y += 1
        self.watch_bottom()

    def damage(self, amount):
        pass

    def attaque(self):
        pass

    def blit_entity(self):
        py.blt(self.x * 16, self.y * 16, 0, self.img[0], self.img[1], self.size[0],self.size[1], self.colkey)

    def distance(self, other_entity):
        distance_x = self.x - other_entity.x
        distance_y = self.y - other_entity.y
        return distance_x, distance_y

    def low_distance_side(self, other_entity):
        distances = self.distance(other_entity)
        if abs(distances[0]) > abs(distances[1]):
            if distances[0] > 0:
                return "left"
            else:
                return "right"
        else:
            if distances[1] > 0:
                return "top"
            else:
                return "bottom"


class Player(Entity):
    def __init__(self, game, x:int, y:int):
        super().__init__(game, x, y, (32, 0), (16, 16), 100)
        self.weapon = Axe(self)
        self.armor = NakedArmor(self)

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.game.player = Player(self.game, 0, 0)

    def attaque(self):
        self.weapon.attaque()


class Ennemies(Entity):
    def __init__(self, game, x: int, y: int, img: tuple, size: tuple, hp: int, lvl: int,  colkey: int = 0):
        super().__init__(game, x, y, img, size, hp, colkey=colkey)
        self.dmg = 10
        self.patern = {"left": [[(-1, 0)]],
                       "right": [[(1, 0)]],
                       "top": [[(0, -1)]],
                       "bottom": [[(0, 1)]],
                       }
        self.attaque_tile = (16, 32)
        self.lvl = lvl
        self.speed = 1

    def action(self):
        left_action = self.speed
        while left_action > 0:
            if self.get_if_player_touched():
                self.attaque()
                left_action -= 1
            if left_action > 0:
                distances = self.distance(self.game.player)
                if abs(distances[0])+abs(distances[1]) > 10:
                    side = self.low_distance_side(self.game.player)
                    if side == "top":
                        self.top()
                    elif side == "bottom":
                        self.bottom()
                    elif side == "left":
                        self.left()
                    elif side == "right":
                        self.right()
                    left_action -= 1
                else:
                    rand = random.randint(0, 3)
                    if rand == 0:
                        self.top()
                    elif rand == 1:
                        self.bottom()
                    elif rand == 2:
                        self.left()
                    elif rand == 3:
                        self.right()
                    left_action -= 1

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.game.ennemi.remove(self)

    def range_blit(self):
        for line in self.patern[self.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.x + pos[0] < len(self.game.carte.grille) and 0 <= self.y + pos[1] < len(self.game.carte.grille[0]) and not "obst" in self.game.carte.grille[self.x + pos[0]][self.y + pos[1]].types:
                    py.blt((self.x + pos[0]) * 16, (self.y + pos[1]) * 16, 0, self.attaque_tile[0],self.attaque_tile[1], 16, 16, 0)
                else:
                    blocked = True

    def get_if_player_touched(self):
        for line in self.patern[self.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.x + pos[0] < len(self.game.carte.grille) and 0 <= self.y + pos[1] < len(self.game.carte.grille[0]) and not "obst" in self.game.carte.grille[self.x + pos[0]][self.y + pos[1]].types:
                    if self.game.player.x == self.x + pos[0] and self.game.player.y == self.y + pos[1]:
                        return True
                else:
                    blocked = True
        return False

    def attaque(self):
        if self.get_if_player_touched():
            self.game.player.damage(self.dmg)

    def blit_life_bar(self):
        py.rect(self.x*16, self.y*16-5, 16, 5, 8)
        py.rect(16*self.x, 16*self.y-5, (self.hp/self.maxhp)*16, 5, 11)
        py.text(16*self.x, 16*self.y-10, "lvl "+str(self.lvl), 7)


class Zombie(Ennemies):
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (32, 16), (16, 16), 20, lvl, colkey=7)
        self.dmg = (self.lvl-1)*10 + randint(1, 9)
        self.hp = (self.lvl-1)*self.hp + randint(1, 19)
        self.maxhp = self.hp


class Squelette(Ennemies):
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (32, 32), (16, 16), 20, lvl, colkey=6)
        self.dmg = (self.lvl - 1) * 10 + randint(1, 9)
        self.hp = (self.lvl - 1) * 20 + randint(1, 19)
        self.maxhp = self.hp
        self.patern = {"left": [[(-i, 0) for i in range(1, 17)]],
                       "right": [[(i, 0) for i in range(1, 17)]],
                       "top": [[(0, -i) for i in range(1, 17)]],
                       "bottom": [[(0, i) for i in range(1, 17)]],
                       }