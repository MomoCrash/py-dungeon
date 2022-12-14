from Equipment import *
from random import random


class Loot:
    taux_loot = {
        "NakedArmor": 0.1,
        "LeatherArmor": 3,
        "IronArmor": 2,
        "GoldArmor": 1,
        "DiamondArmor": 0.5,
        "MagmaArmor": 0.2,
        "DragonScaleArmor": 0.1,
        "Spear": 1,
        "Hammer": 0.1,
        "Bow": 1.2,
        "Hallebarde": 0.9,
        "Axe": 1.5,
        "Life": 3
    }
    
    def __init__(self, niveau, x, y, forced=(False, )):
        self.forced = forced
        self.x = x
        self.y = y
        if not forced[0]:
            self.niveau = niveau
            r = random()
            somme = 0
            for v in self.taux_loot.values():
                somme += v
            r *= somme
            self.type = ""
            for k, v in self.taux_loot.items():
                r -= v
                if r <= 0:
                    self.type = k
                    break

    def get_loot(self, getter):
        if self.forced[0]:
            if type(self.forced[1]) in Weapon.__subclasses__():
                getter.game.loots.append(Loot(0, getter.x, getter.y, (True, getter.weapon)))
                getter.set_weapon(self.forced[1])
                getter.game.loots.remove(self)
            else:
                getter.game.loots.append(Loot(0, getter.x, getter.y, (True, getter.armor)))
                getter.set_armor(self.forced[1])
                getter.game.loots.remove(self)
        else:
            all_armor_loot = Armor.__subclasses__()
            all_weapon_loot = Weapon.__subclasses__()
            if self.type == "Life":
                getter.hp += self.niveau*10
                if getter.hp > getter.maxhp:
                    getter.hp = getter.maxhp
                getter.game.loots.remove(self)
            else:
                for classe in all_weapon_loot:
                    if self.type == classe.__name__:
                        getter.game.loots.append(Loot(0, getter.x, getter.y, (True, getter.weapon)))
                        getter.set_weapon(classe(getter, self.niveau))
                        getter.game.loots.remove(self)

                for classe in all_armor_loot:
                    if self.type == classe.__name__:
                        getter.game.loots.append(Loot(0, getter.x, getter.y, (True, getter.armor)))
                        getter.set_armor(classe(getter))
                        getter.game.loots.remove(self)

    def blit(self):
        py.blt(self.x*16, self.y*16, IMAGE_EQUIPMENT, 0, 32, 16, 16, 7)

    def blit_inv(self):
        if self.forced[0]:
            self.forced[1].blit(decalY=176 if type(self.forced[1]) in Weapon.__subclasses__() else 208)
        elif self.type == "Life":
            py.blt(256, 208, IMAGE_EQUIPMENT, 0, 48, 16, 32, 7)
        else:
            img = LOOT_IMAGE[self.type]
            py.blt(256, 208, IMAGE_EQUIPMENT, img[0], img[1], 16, 32, 7)
            temp = str(self.niveau)
            chaine = ""
            for i in range(len(temp)):
                if i == 16:
                    chaine += "..."
                    break
                chaine += temp[i]
                if i % 4 == 3:
                    chaine += "\n"
            py.text(272, 208, "lvl: \n"+chaine, 7)


if __name__ == '__main__':
    loot1 = []
    a = Armor.__subclasses__()
    for i in range(100):
        loot1.append(Loot(1, 1, 1))
    nbr = [[t, 0] for t in Loot.taux_loot.keys()]
    print([l.type for l in loot1])
    for l in loot1:
        for i in range(len(nbr)):
            if nbr[i][0] == l.type:
                nbr[i][1] += 1
    print(nbr)



