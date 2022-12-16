from Equipment import *
from random import random


class Loot:
    """classe qui représente un loot particulier, qui peut être aléatoire ou prédéfini"""

    # définition des taux de drop : (valeur / total des valeurs)
    taux_loot = {
        "NakedArmor": 0.7,
        "LeatherArmor": 0.6,
        "IronArmor": 0.5,
        "GoldArmor": 0.4,
        "DiamondArmor": 0.3,
        "MagmaArmor": 0.2,
        "DragonScaleArmor": 0.1,
        "Spear": 1,
        "Hammer": 0.2,
        "Bow": 1.2,
        "Hallebarde": 0.8,
        "Axe": 1.2,
        "Life": 2
    }
    
    def __init__(self, niveau, x, y, forced=(False, )):
        """
        :param niveau: int                      | niveau de l'arme, l'arme ou la vie généré
        :param x: int                           | position x (en tuiles) ou le loot se trouve
        :param y: int                           | position y (en tuiles) ou le loot se trouve
        :param forced: tuple(bool, Equipment)   | permet de forcer le loot à avoir des attributs prédéfini (dans ce cas seul x et y seront défini en dehors de forced)
        :var self.type: str(Class-name)         | défini le type de l'objet par une chaine de charactère (nom de l'Objet ou 'Life')
        """
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
        """récupère le loot et le donne à getter (Player) en appliquant toute les modifications implicite"""
        if self.forced[0]:
            if type(self.forced[1]) in Weapon.__subclasses__():
                getter.game.loots.insert(0, Loot(0, getter.x, getter.y, (True, getter.weapon)))
                getter.set_weapon(self.forced[1])
                getter.game.loots.remove(self)
            else:
                getter.game.loots.insert(0, Loot(0, getter.x, getter.y, (True, getter.armor)))
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
                        getter.game.loots.insert(0, Loot(0, getter.x, getter.y, (True, getter.weapon)))
                        getter.set_weapon(classe(getter, self.niveau))
                        getter.game.loots.remove(self)

                for classe in all_armor_loot:
                    if self.type == classe.__name__:
                        getter.game.loots.insert(0, Loot(0, getter.x, getter.y, (True, getter.armor)))
                        getter.set_armor(classe(getter))
                        getter.game.loots.remove(self)

    def blit(self):
        """affiche le loot par terre"""
        py.blt(self.x*16, self.y*16, IMAGE_EQUIPMENT, 0, 32, 16, 16, 0)

    def blit_inv(self):
        """affiche l'objet dans l'inventaire à l'emplacement pour voir ce qui est au sol"""
        if self.forced[0]:
            self.forced[1].blit(decalY=176 if type(self.forced[1]) in Weapon.__subclasses__() else 208)
        elif self.type == "Life":
            py.blt(256, 208, IMAGE_EQUIPMENT, 0, 48, 16, 32, 7)
        else:
            img = LOOT_IMAGE[self.type]
            py.blt(256, 208, IMAGE_EQUIPMENT, img[0], img[1], 16, 32, 0)
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





