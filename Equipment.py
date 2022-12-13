import pyxel as py
from random import randint

IMAGE_EQUIPMENT = 2


class Weapon:
    def __init__(self, owner, image: tuple, lvl: int, dmg: int):
        self.owner = owner
        self.patern = {}
        self.attaque_tile = (0, 32)
        self.dmg = 0
        self.image = image
        self.lvl = lvl
        self.dmg = dmg*lvl + randint(0, dmg-1)

    def blit_range(self):
        for line in self.patern[self.owner.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.owner.x + pos[0] < len(
                        self.owner.game.carte.grille) and 0 <= self.owner.y + pos[1] < len(
                        self.owner.game.carte.grille[0]) and not "obst" in \
                                                                 self.owner.game.carte.grille[self.owner.x + pos[0]][
                                                                     self.owner.y + pos[1]].types:
                    py.blt((self.owner.x + pos[0]) * 16, (self.owner.y + pos[1]) * 16, 0, self.attaque_tile[0],
                           self.attaque_tile[1], 16, 16, 0)
                else:
                    blocked = True

    def get_ennemi_in_range(self):
        ennemi = []
        for line in self.patern[self.owner.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.owner.x + pos[0] < len(
                        self.owner.game.carte.grille) and 0 <= self.owner.y + pos[1] < len(
                        self.owner.game.carte.grille[0]) and not "obst" in \
                                                                 self.owner.game.carte.grille[self.owner.x + pos[0]][
                                                                     self.owner.y + pos[1]].types:
                    for e in self.owner.game.ennemi:
                        if e.x == self.owner.x + pos[0] and e.y == self.owner.y + pos[1]:
                            ennemi.append(e)
                else:
                    blocked = True
        return ennemi

    def attaque(self):
        touched = self.get_ennemi_in_range()
        for e in touched:
            e.damage(self.owner.weapon.dmg)

    def blit(self):
        temp = str(self.dmg)
        chaine = ""
        for i in range(len(temp)):
            if i == 17:
                chaine += "..."
                break
            chaine += temp[i]
            if i % 4 == 3:
                chaine += "\n"
        py.blt(256, 32, IMAGE_EQUIPMENT, self.image[0], self.image[1], 16, 32,
               self.image[3] if len(self.image) == 3 else 0)
        py.text(272, 32, chaine, 7)


class Sword(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, (16, 0), lvl, 10)
        self.patern = {
            "left": [[(-1, 0)]],
            "right": [[(1, 0)]],
            "top": [[(0, -1)]],
            "bottom": [[(0, 1)]],
        }


class Spear(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, (100, 0), lvl, 10)
        self.patern = {
            "left": [[(-1, 0), (-2, 0), (-3, 0)]],
            "right": [[(1, 0), (2, 0), (3, 0)]],
            "top": [[(0, -1), (0, -2), (0, -3)]],
            "bottom": [[(0, 1), (0, 2), (0, 3)]],
        }


class Hammer(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, (100, 0), lvl, 18)
        self.patern = {
            "left": [[(-1, 0), (-2, 0)], [(-1, 1), (-2, 1)], [(-1, -1), (-2, -1)]],
            "right": [[(1, 0), (2, 0)], [(1, 1), (2, 1)], [(1, -1), (2, -1)]],
            "top": [[(0, -1), (0, -2)], [(-1, -1), (-1, -2)], [(1, -1), (1, -2)]],
            "bottom": [[(0, 1), (0, 2)], [(-1, 1), (-1, 2)], [(1, 1), (1, 2)]],
        }


class Bow(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, (100, 0), lvl, 5)
        self.patern = {
            "left": [[(-i, 0) for i in range(1, 17)]],
            "right": [[(i, 0) for i in range(1, 17)]],
            "top": [[(0, -i) for i in range(1, 17)]],
            "bottom": [[(0, i) for i in range(1, 17)]]
        }


class Hallebarde(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, (100, 0), lvl, 15)
        self.patern = {
            "left": [[(-1, 1), (-2, 1)], [(-1, -1), (-2, -1)]],
            "right": [[(1, 1), (2, 1)], [(1, -1), (2, -1)]],
            "top": [[(-1, -1), (-1, -2)], [(1, -1), (1, -2)]],
            "bottom": [[(-1, 1), (-1, 2)], [(1, 1), (1, 2)]],
        }


class Axe(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, (100, 0), lvl, 12)
        self.patern = {
            "left": [[(-1, 0)], [(-1, 1)], [(-1, -1)]],
            "right": [[(1, 0)], [(1, 1)], [(1, -1)]],
            "top": [[(0, -1)], [(-1, -1)], [(1, -1)]],
            "bottom": [[(0, 1)], [(-1, 1)], [(1, 1)]],
        }


class Armor:
    def __init__(self, owner, name, defence_p, image):
        self.owner = owner
        self.defence_point = defence_p
        self.name = name
        self.image = image

    def defence(self):
        return 1 / self.defence_point

    def blit(self):
        temp = str(self.defence_point)
        chaine = ""
        for i in range(len(temp)):
            if i == 17:
                chaine += "..."
                break
            chaine += temp[i]
            if i % 4 == 3:
                chaine += "\n"
        py.blt(256, 0, IMAGE_EQUIPMENT, self.image[0], self.image[1], 16, 32, 0)
        py.text(272, 0, chaine, 7)


class NakedArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Tout nu", 1, (0, 0))
