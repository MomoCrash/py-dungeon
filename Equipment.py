import pyxel as py
from random import randint

IMAGE_EQUIPMENT = 2

LOOT_IMAGE = {
    "NakedArmor": (0, 0),
    "LeatherArmor": (0, 72),
    "IronArmor": (0, 104),
    "GoldArmor": (0, 136),
    "DiamondArmor": (0, 168),
    "MagmaArmor": (0, 0),
    "DragonScaleArmor": (0, 200),
    "Sword": (16, 0),
    "Spear": (16, 32),
    "Hammer": (16, 128),
    "Bow": (16, 152),
    "Hallebarde": (16, 64),
    "Axe": (16, 96),
}


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

    def blit(self, decalY=0):
        temp = str(self.dmg)
        chaine = ""
        for i in range(len(temp)):
            if i == 17:
                chaine += "..."
                break
            chaine += temp[i]
            if i % 4 == 3:
                chaine += "\n"
        py.blt(256, 32+decalY, IMAGE_EQUIPMENT, self.image[0], self.image[1], 16, 32,
               self.image[3] if len(self.image) == 3 else 0)
        py.text(272, 32+decalY, chaine, 7)


class Sword(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Sword"], lvl, 10)
        self.patern = {
            "left": [[(-1, 0)]],
            "right": [[(1, 0)]],
            "top": [[(0, -1)]],
            "bottom": [[(0, 1)]],
        }


class Spear(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Spear"], lvl, 10)
        self.patern = {
            "left": [[(-1, 0), (-2, 0), (-3, 0)]],
            "right": [[(1, 0), (2, 0), (3, 0)]],
            "top": [[(0, -1), (0, -2), (0, -3)]],
            "bottom": [[(0, 1), (0, 2), (0, 3)]],
        }


class Hammer(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Hammer"], lvl, 18)
        self.patern = {
            "left": [[(-1, 0), (-2, 0)], [(-1, 1), (-2, 1)], [(-1, -1), (-2, -1)]],
            "right": [[(1, 0), (2, 0)], [(1, 1), (2, 1)], [(1, -1), (2, -1)]],
            "top": [[(0, -1), (0, -2)], [(-1, -1), (-1, -2)], [(1, -1), (1, -2)]],
            "bottom": [[(0, 1), (0, 2)], [(-1, 1), (-1, 2)], [(1, 1), (1, 2)]],
        }


class Bow(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Bow"], lvl, 5)
        self.patern = {
            "left": [[(-i, 0) for i in range(1, 17)]],
            "right": [[(i, 0) for i in range(1, 17)]],
            "top": [[(0, -i) for i in range(1, 17)]],
            "bottom": [[(0, i) for i in range(1, 17)]]
        }


class Hallebarde(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Hallebarde"], lvl, 15)
        self.patern = {
            "left": [[(-1, 1), (-2, 1)], [(-1, -1), (-2, -1)]],
            "right": [[(1, 1), (2, 1)], [(1, -1), (2, -1)]],
            "top": [[(-1, -1), (-1, -2)], [(1, -1), (1, -2)]],
            "bottom": [[(-1, 1), (-1, 2)], [(1, 1), (1, 2)]],
        }


class Axe(Weapon):
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Axe"], lvl, 12)
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

    def blit(self, decalY=0):
        temp = str(self.defence_point)
        chaine = ""
        for i in range(len(temp)):
            if i == 17:
                chaine += "..."
                break
            chaine += temp[i]
            if i % 4 == 3:
                chaine += "\n"
        py.blt(256, decalY, IMAGE_EQUIPMENT, self.image[0], self.image[1], 16, 32, 0)
        py.text(272, decalY, chaine, 7)


class NakedArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Tout nu", 1, LOOT_IMAGE["NakedArmor"])


class LeatherArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Armure en Cuir", 12, LOOT_IMAGE["LeatherArmor"])


class IronArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Armure en Fer", 19, LOOT_IMAGE["IronArmor"])


class GoldArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Armure en Or", 26, LOOT_IMAGE["GoldArmor"])


class DiamondArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Armure en Diamants", 32, LOOT_IMAGE["DiamondArmor"])


class MagmaArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Armure en Magma", 52, LOOT_IMAGE["MagmaArmor"])


class DragonScaleArmor(Armor):
    def __init__(self, owner):
        super().__init__(owner, "Armure en Ecaille", 72, LOOT_IMAGE["DragonScaleArmor"])