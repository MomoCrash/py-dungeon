import pyxel as py


class Weapon:
    def __init__(self, owner):
        self.owner = owner
        self.patern = {}
        self.attaque_tile = (0, 32)
        self.dmg = 0

    def blit_range(self):
        for line in self.patern[self.owner.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.owner.x + pos[0] < len(self.owner.game.grille) and 0 <= self.owner.y + pos[1] < len(self.owner.game.grille[0]) and not "obst" in self.owner.game.grille[self.owner.x + pos[0]][self.owner.y + pos[1]].types:
                    py.blt((self.owner.x + pos[0]) * 16, (self.owner.y + pos[1]) * 16, 0, self.attaque_tile[0],
                           self.attaque_tile[1], 16, 16, 0)
                else:
                    blocked = True

    def get_ennemi_in_range(self):
        ennemi = []
        for line in self.patern[self.owner.orient]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.owner.x + pos[0] < len(self.owner.game.grille) and 0 <= self.owner.y + pos[1] < len(self.owner.game.grille[0]) and not "obst" in self.owner.game.grille[self.owner.x + pos[0]][self.owner.y + pos[1]].types:
                    for e in self.owner.game.ennemi:
                        if e.x == self.owner.x + pos[0] and e.y == self.owner.y + pos[1]:
                            ennemi.append(e)
                else:
                    blocked = True
        for e in ennemi: print(e.hp)
        return ennemi


class Sword(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.dmg = 10
        self.patern = {"left": [[(-1, 0)]],
                       "right": [[(1, 0)]],
                       "top": [[(0, -1)]],
                       "bottom": [[(0, 1)]],
                       }


class Spear(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.dmg = 10
        self.patern = {"left": [[(-1, 0), (-2, 0), (-3, 0)]],
                       "right": [[(1, 0), (2, 0), (3, 0)]],
                       "top": [[(0, -1), (0, -2), (0, -3)]],
                       "bottom": [[(0, 1), (0, 2), (0, 3)]],
                       }


class Hammer(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.dmg = 18
        self.patern = {"left": [[(-1, 0), (-2, 0)], [(-1, 1), (-2, 1)], [(-1, -1), (-2, -1)]],
                       "right": [[(1, 0), (2, 0)], [(1, 1), (2, 1)], [(1, -1), (2, -1)]],
                       "top": [[(0, -1), (0, -2)], [(-1, -1), (-1, -2)], [(1, -1), (1, -2)]],
                       "bottom": [[(0, 1), (0, 2)], [(-1, 1), (-1, 2)], [(1, 1), (1, 2)]],
                       }


class Armor:
    def __init__(self, owner):
        self.owner = owner
