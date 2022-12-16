import pyxel as py
from random import randint

# Varibales globals ----------------------------------------------------------------------------------------------------

# numméro de l'images du fichier
IMAGE_EQUIPMENT = 2

# toute les images des différents items
LOOT_IMAGE = {
    "NakedArmor": (0, 0),
    "LeatherArmor": (0, 72),
    "IronArmor": (0, 104),
    "GoldArmor": (0, 136),
    "DiamondArmor": (0, 168),
    "MagmaArmor": (0, 200),
    "DragonScaleArmor": (0, 200),
    "Sword": (16, 0),
    "Spear": (16, 32),
    "Hammer": (16, 128),
    "Bow": (16, 152),
    "Hallebarde": (16, 64),
    "Axe": (16, 96),
}

# Objects --------------------------------------------------------------------------------------------------------------


class Weapon:
    """Classe Génériques des armes"""
    def __init__(self, owner, image: tuple, lvl: int, dmg: int):
        """
        :param owner: Player                | joueur qui à l'arme
        :param image: tuple(u:int, v:int)   | image de l'armes (pour l'inventaire)
        :param lvl: int                     | niveau de l'arme pour gérer les stats
        :param dmg: int                     | dégâts de base de l'arme au niveau 1 max
        :var self. patern dict()            | défini les attaques des armes tuile par tuile
        :var self.attaque_tile: tuple       | image de la case de visé de l'attque
        """
        self.owner = owner
        self.patern = {}
        self.attaque_tile = (0, 32)
        self.image = image
        self.lvl = lvl
        self.dmg = dmg*lvl + randint(0, dmg-1)

    def blit_range(self) -> None:
        """affiche la portée de l'arme"""
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

    def get_ennemi_in_range(self) -> list:
        """renvoie une liste avec tout les ennemis touchés"""
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

    def attaque(self) -> None:
        """attaque avec l'arme"""
        touched = self.get_ennemi_in_range()
        for e in touched:
            e.damage(self.owner.weapon.dmg)

    def blit(self, decalY=0) -> None:
        """
        affiche l'arme dans linventaire
        :param decalY: int décalage pour afficher plus bas dans l'inventaire (objet au sol)
        """
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
    """
    héritage de Weapon avec des charactéristique défini (Epee rouillé)
    patern : 1 case en avant
    """
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Sword"], lvl, 10)
        self.patern = {
            "left": [[(-1, 0)]],
            "right": [[(1, 0)]],
            "top": [[(0, -1)]],
            "bottom": [[(0, 1)]],
        }


class Spear(Weapon):
    """
    héritage de Weapon avec des charactéristique défini (Pique/Lance)
    patern: 3 cases en avant
    """
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Spear"], lvl, 10)
        self.patern = {
            "left": [[(-1, 0), (-2, 0), (-3, 0)]],
            "right": [[(1, 0), (2, 0), (3, 0)]],
            "top": [[(0, -1), (0, -2), (0, -3)]],
            "bottom": [[(0, 1), (0, 2), (0, 3)]],
        }


class Hammer(Weapon):
    """
    héritage de Weapon avec des charactéristique défini (Marteau)
    patern: 6 case devant
    """
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Hammer"], lvl, 18)
        self.patern = {
            "left": [[(-1, 0), (-2, 0)], [(-1, 1), (-2, 1)], [(-1, -1), (-2, -1)]],
            "right": [[(1, 0), (2, 0)], [(1, 1), (2, 1)], [(1, -1), (2, -1)]],
            "top": [[(0, -1), (0, -2)], [(-1, -1), (-1, -2)], [(1, -1), (1, -2)]],
            "bottom": [[(0, 1), (0, 2)], [(-1, 1), (-1, 2)], [(1, 1), (1, 2)]],
        }


class Bow(Weapon):
    """
    héritage de Weapon avec des charactéristique défini (arc)
    patern: 16 case vers l'avant (map entière)
    """

    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Bow"], lvl, 5)
        self.patern = {
            "left": [[(-i, 0) for i in range(1, 17)]],
            "right": [[(i, 0) for i in range(1, 17)]],
            "top": [[(0, -i) for i in range(1, 17)]],
            "bottom": [[(0, i) for i in range(1, 17)]]
        }


class Hallebarde(Weapon):
    """
    héritage de Weapon avec des charactéristique défini (Hallebarde)
    patern: deux case en avant sur les deux rangée parallèle a la vision
    """
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Hallebarde"], lvl, 15)
        self.patern = {
            "left": [[(-1, 1), (-2, 1)], [(-1, -1), (-2, -1)]],
            "right": [[(1, 1), (2, 1)], [(1, -1), (2, -1)]],
            "top": [[(-1, -1), (-1, -2)], [(1, -1), (1, -2)]],
            "bottom": [[(-1, 1), (-1, 2)], [(1, 1), (1, 2)]],
        }


class Axe(Weapon):
    """
    héritage de Weapon avec des charactéristique défini (Hache)
    patern : attaque les trois case devant
    """
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
        """
        :param owner: Joueur qui porte l'armure
        :param name: nom de l'armure
        :param defence_p: valeur de la défense
        :param image: image de l'armure
        """
        self.owner = owner
        self.defence_point = defence_p
        self.name = name
        self.image = image

    def defence(self) -> float:
        """renvoie un coeficient de défense"""
        return 1 / self.defence_point

    def blit(self, decalY=0) -> None:
        """
        affiche l'armure dans l'inventaire.
        :param decalY: int | décale verticalement (en pixels)
        """
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
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Tout nu", 1, LOOT_IMAGE["NakedArmor"])


class LeatherArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Cuir", 12, LOOT_IMAGE["LeatherArmor"])


class IronArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Fer", 19, LOOT_IMAGE["IronArmor"])


class GoldArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Or", 26, LOOT_IMAGE["GoldArmor"])


class DiamondArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Diamants", 32, LOOT_IMAGE["DiamondArmor"])


class MagmaArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Magma", 52, LOOT_IMAGE["MagmaArmor"])


class DragonScaleArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Ecaille", 72, LOOT_IMAGE["DragonScaleArmor"])