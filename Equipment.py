import pyxel as py


class Weapon:
    def __init__(self, owner):
        self.owner = owner
        self.patern = {}
        self.attaque_tile = (0, 32)

    def blit(self):
        for x in range()
        py.blt(self.owner.x, self.owner.y, 0, self.attaque_tile[0], self.attaque_tile[1], 16, 16)


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.patern = { "left": (1, 0),
                        "right": (-1, 0),
                        "top": (-1, 0),
                        "bottom": (1, 0),
        }


class Armor:
    def __init__(self, owner):
        self.owner = owner

