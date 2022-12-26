import pyxel as py
from random import randint
from Settings import IMAGE_EQUIPMENT, LOOT_IMAGE, ORIENT_EQ, orient_to_coor


class Weapon:
    """Classe Génériques des armes"""
    def __init__(self, owner, image: tuple, lvl: int, dmg: int, element: int = 0):
        """
        :param owner: Player                | joueur qui à l'arme
        :param image: tuple(u:int, v:int)   | image de l'armes (pour l'inventaire)
        :param lvl: int                     | niveau de l'arme pour gérer les stats
        :param dmg: int                     | dégâts de base de l'arme au niveau 1 max
        :param element: int                 | entier qui représente l'élément
        :var self. patern dict()            | défini les attaques des armes tuile par tuile
        :var self.attaque_tile: tuple       | image de la case de visé de l'attque
        """
        self.element = element
        self.owner = owner
        self.patern = {}
        self.attaque_tile = (0, 32)
        self.image = (image[0]+self.element*16, image[1])
        self.lvl = lvl
        self.dmg = dmg*lvl + randint(0, dmg-1)

    def blit_range(self) -> None:
        """affiche la portée de l'arme"""
        for line in self.patern[ORIENT_EQ[self.owner.orient]]:
            blocked = False
            for pos in line:
                is_in_width = 0 <= self.owner.x + pos[0] < len(self.owner.game.carte.grille)
                is_in_height = 0 <= self.owner.y + pos[1] < len(self.owner.game.carte.grille[0])
                if not blocked and is_in_width and is_in_height and "obst" not in self.owner.game.carte.grille[self.owner.x + pos[0]][self.owner.y + pos[1]].types:
                    py.blt(self.owner.reel_x + pos[0] * 16, self.owner.reel_y + pos[1] * 16, 0, self.attaque_tile[0],
                           self.attaque_tile[1], 16, 16, 0)
                else:
                    blocked = True

    def get_ennemi_in_range(self) -> list:
        """renvoie une liste avec tout les ennemis touchés"""
        ennemi = []
        for line in self.patern[ORIENT_EQ[self.owner.orient]]:
            blocked = False
            for pos in line:
                is_in_width = 0 <= self.owner.x + pos[0] < len(self.owner.game.carte.grille)
                is_in_height = 0 <= self.owner.y + pos[1] < len(self.owner.game.carte.grille[0])
                if not blocked and is_in_width and is_in_height and "obst" not in self.owner.game.carte.grille[self.owner.x + pos[0]][self.owner.y + pos[1]].types:
                    for e in self.owner.game.ennemi:
                        if e.x == self.owner.x + pos[0] and e.y == self.owner.y + pos[1]:
                            ennemi.append(e)
                else:
                    blocked = True
        return ennemi

    def get_coor_in_range(self) -> list:
        """renvoie une liste avec tout les tuiles dans la portée"""
        coors = []
        for line in self.patern[ORIENT_EQ[self.owner.orient]]:
            blocked = False
            for pos in line:
                is_in_width = 0 <= self.owner.x + pos[0] < len(self.owner.game.carte.grille)
                is_in_height = 0 <= self.owner.y + pos[1] < len(self.owner.game.carte.grille[0])
                if not blocked and is_in_width and is_in_height and "obst" not in self.owner.game.carte.grille[self.owner.x + pos[0]][self.owner.y + pos[1]].types:
                    coors.append((self.owner.reel_x + pos[0]*16, self.owner.reel_y + pos[1]*16))
                else:
                    blocked = True
        return coors

    def attaque(self) -> None:
        """attaque avec l'arme"""
        touched = self.get_ennemi_in_range()
        for e in touched:
            e.damage(self.owner.weapon.dmg, self.element, self.owner)

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
        py.blt(256, decalY, IMAGE_EQUIPMENT, self.image[0], self.image[1], 16, 32,
               self.image[3] if len(self.image) == 3 else 0)
        py.text(272, decalY, chaine, 7)


class RustySword(Weapon):
    """
    héritage de Weapon avec des charactéristique défini (Epee rouillé)
    patern : 1 case en avant
    """
    def __init__(self, owner):
        super().__init__(owner, (0, 80), 1, 10, 0)
        self.dmg = 10
        self.patern = {
            "left": [[(-1, 0)]],
            "right": [[(1, 0)]],
            "top": [[(0, -1)]],
            "bottom": [[(0, 1)]],
        }


class Sword(Weapon):
    """
    héritage de Weapon avec des charactéristique défini (Epee)
    patern : 1 case en avant
    """
    def __init__(self, owner, lvl):
        super().__init__(owner, LOOT_IMAGE["Sword"], lvl, 10, randint(0, 3))
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
        self.element = randint(0, 3)
        super().__init__(owner, LOOT_IMAGE["Spear"], lvl, 10, randint(0, 3))
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
        super().__init__(owner, LOOT_IMAGE["Hammer"], lvl, 18, randint(0, 3))
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
        super().__init__(owner, LOOT_IMAGE["Hallebarde"], lvl, 15, randint(0, 3))
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
        super().__init__(owner, LOOT_IMAGE["Axe"], lvl, 12, randint(0, 3))
        self.patern = {
            "left": [[(-1, 0)], [(-1, 1)], [(-1, -1)]],
            "right": [[(1, 0)], [(1, 1)], [(1, -1)]],
            "top": [[(0, -1)], [(-1, -1)], [(1, -1)]],
            "bottom": [[(0, 1)], [(-1, 1)], [(1, 1)]],
        }


class Armor:
    def __init__(self, owner, name, defence_p, image, element):
        """
        :param owner: Joueur qui porte l'armure
        :param name: nom de l'armure
        :param defence_p: valeur de la défense
        :param image: image de l'armure
        """
        self.owner = owner
        self.defence_coef = 1 - defence_p/100
        self.defence_percent = defence_p
        self.name = name
        self.image = image
        self.colkey = 0
        self.element = element

    def defence(self) -> float:
        """renvoie un coeficient de défense"""
        return 1/self.defence_coef

    def blit(self, decalY=0) -> None:
        """
        affiche l'armure dans l'inventaire.
        :param decalY: int | décale verticalement (en pixels)
        """
        temp = str(self.defence_percent) + "%"
        chaine = ""
        for i in range(len(temp)):
            if i == 17:
                chaine += "..."
                break
            chaine += temp[i]
            if i % 4 == 3:

                chaine += "\n"
        py.blt(256, decalY, IMAGE_EQUIPMENT, self.image[0], self.image[1], 16, 32, self.colkey)
        py.text(272, decalY, chaine, 7)


class NakedArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Tout nu", 0, LOOT_IMAGE["NakedArmor"], 0)


class LeatherArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Cuir", 2.5, LOOT_IMAGE["LeatherArmor"], 0)


class IronArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Fer", 5, LOOT_IMAGE["IronArmor"], 0)


class GoldArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Or", 10, LOOT_IMAGE["GoldArmor"], 0)


class DiamondArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Diamants", 15, LOOT_IMAGE["DiamondArmor"], 0)


class MagmaArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Magma", 25, LOOT_IMAGE["MagmaArmor"], 2)
        self.colkey = 7


class DragonScaleArmor(Armor):
    """héritage de Armor avec des charactéristique défini"""
    def __init__(self, owner):
        super().__init__(owner, "Armure en Ecaille", 35, LOOT_IMAGE["DragonScaleArmor"], 2)