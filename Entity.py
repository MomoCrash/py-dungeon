import pyxel as py
from random import randint
from Equipment import *
from Loot import Loot
from Animate import *
import random


# Variables globals :
IMAGE_ENTITE = 1


class Entity:
    """
    classe générique pour n'importe quel Entité, c'est-a-dire tout ce qui est capable de bouger et interagir avec d'autre Entité
    """
    def __init__(self, game, x: int, y: int, img: tuple, size: tuple, hp: int, colkey: int = 0):
        """
        :param game: Game                   | accès au jeu entier
        :param x: int                       | position x (en tuiles)
        :param y: int                       | position y (en tuiles)
        :param img: tuple(u: int, v: int)   | coordonnés de l'image de l'entité
        :param size: tuple(w: int, h: int)  | taille (toujours 16 par 16 normalement)
        :param hp: int                      | point de vies
        :param colkey: int                  | couleur à retirer dans l'affichage
        :var self.orient: str               | défini l'orientation du personnage
        :var self.imgY: tuple(int, int)     | image a utiliser pour haut, bas
        :var self.imgX: tuple(int, int)     | image a utiliser pour gauche droite
        :var self.debuff: list()            | liste de tout les debuffs actifs
        :var self.buff: list()              | liste de tout les buffs actifs
        """
        self.maxhp = hp
        self.hp = hp
        self.x = x
        self.y = y
        self.reel_x = x*16
        self.reel_y = y*16
        self.imgX = img
        self.imgY = (img[0] + size[0], img[1])
        self.img = self.imgX
        self.size = size
        self.game = game
        self.colkey = colkey
        self.orient = 1
        self.debuff = []
        self.buff = []

    def watch_left(self) -> None:
        """regarder à gauche"""
        self.size = (abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX
        self.orient = 0

    def left(self) -> None:
        """se déplacer si possible vers la case à gauche"""
        if not self.x > 0:
            return
        c1 = "obst" not in self.game.carte.grille[self.x - 1][self.y].types
        c2 = not self.game.check_full_tile(self.x-1, self.y)
        c3 = "ground" not in self.game.carte.grille[self.x - 1][self.y].types
        if c1 and c2 and c3:
            self.x -= 1
            self.game.animation_list.insert(0, Move(self.game, self, 0))

        self.watch_left()

    def watch_right(self) -> None:
        """regarder à droite"""
        self.size = (-abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX
        self.orient = 1

    def right(self) -> None:
        """se déplacer à droite si possible"""
        if not self.x < len(self.game.carte.grille) - 1:
            return
        c1 = "obst" not in self.game.carte.grille[self.x + 1][self.y].types
        c2 = not self.game.check_full_tile(self.x+1, self.y)
        c3 = "ground" not in self.game.carte.grille[self.x + 1][self.y].types
        if c1 and c2 and c3:
            if "end" in self.game.carte.grille[self.x+1][self.y].types:
                if self.game.carte.etage_completed:
                    self.game.carte.new_stage()
            else:
                self.x += 1
                self.game.animation_list.insert(0, Move(self.game, self, 1))
        self.watch_right()

    def watch_top(self) -> None:
        """regarder en haut"""
        self.size = (abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgY
        self.orient = 2

    def top(self) -> None:
        """se déplcaer vers le haut si possible"""
        if not self.y > 0:
            return
        c1 = "obst" not in self.game.carte.grille[self.x][self.y - 1].types
        c2 = not self.game.check_full_tile(self.x, self.y-1)
        c3 = "ground" not in self.game.carte.grille[self.x][self.y - 1].types
        if c1 and c2 and c3:
            self.y -= 1
            self.game.animation_list.insert(0, Move(self.game, self, 2))
        self.watch_top()

    def watch_bottom(self) -> None:
        """regarder vers le bas"""
        self.size = (abs(self.size[0]), -abs(self.size[1]))
        self.img = self.imgY
        self.orient = 3

    def bottom(self) -> None:
        """se déplacer vers le bas si possible"""
        if not self.y < len(self.game.carte.grille[0]) - 1:
            return
        c1 = "obst" not in self.game.carte.grille[self.x][self.y + 1].types
        c2 = not self.game.check_full_tile(self.x, self.y+1)
        c3 = "ground" not in self.game.carte.grille[self.x][self.y + 1].types
        if c1 and c2 and c3:
            if "end" in self.game.carte.grille[self.x][self.y+1].types:
                if self.game.carte.etage_completed:
                    self.game.carte.new_stage()
            else:
                self.y += 1
                self.game.animation_list.insert(0, Move(self.game, self, 3))
        self.watch_bottom()

    def place(self, x, y):
        self.x = x
        self.y = y
        self.reel_x = x*16
        self.reel_y = y*16

    def damage(self, amount, el, source) -> None:
        """
        applique <amount> dégâts à l'entité, le calcul et les conséquence en cas de morts sont fais dans les sous classes indépendement
        :param amount: int | quantité de dégâts
        :param el: int | element des degâts (0 à 3)
        :param source: Player or Ennemies | source des dégâts
        """
        pass

    def attaque(self) -> None:
        """action d'attaquer"""
        pass

    def blit_entity(self) -> None:
        """affiche une entité"""
        py.blt(self.reel_x, self.reel_y, IMAGE_ENTITE, self.img[0], self.img[1], self.size[0], self.size[1], self.colkey)

    def distance(self, other_entity) -> tuple:
        distance_x = self.x - other_entity.x
        distance_y = self.y - other_entity.y
        return distance_x, distance_y

    def low_distance_side(self, other_entity) -> str:
        distances = self.distance(other_entity)
        if abs(distances[0]) > abs(distances[1]):
            if distances[0] > 0:
                return 0
            else:
                return 1
        else:
            if distances[1] > 0:
                return 2
            else:
                return 3


class Player(Entity):
    """
    classe Player hérité de Entité.
    """
    def __init__(self, game, x:int, y:int):
        """
        :param game: accès au jeu
        :param x: position x en tuiles
        :param y: position y en tuiles
        :var self.weapon: Equipment.Weapon...   | arme du joueur
        :var self.armor: Equipment.Armor...     | armure du joueur
        """
        super().__init__(game, x, y, (0, 0), (16, 16), 100)
        self.weapon = RustySword(self)
        self.secondary_weapon = RustySword(self)
        self.armor = NakedArmor(self)

    def blit_life_bar(self) -> None:
        """affiche la bar de vie du joueur en bas de l'écran"""
        py.rect(0, 256, 256, 16, 8)
        py.rect(0, 256, (self.hp/self.maxhp)*256, 16, 11)
        py.text(90, 264, f"{self.hp}/{self.maxhp}", 7)

    def damage(self, amount, el, source) -> None:
        """applique une quantité de dégâts, et défend grâce à l'armure, en cas de mort le Player est reset"""
        total = amount * self.armor.defence() * EFFICACITE[0][el]
        self.hp -= total
        if self.hp <= 0:
            self.game.player = Player(self.game, 0, 0)

    def attaque(self) -> None:
        """attaque avec les stats de l'arme"""
        self.game.animation_list.append(AttaquePlayer(self.game, self.weapon))

    def set_armor(self, armor: Armor) -> None:
        """remplace l'armure"""
        self.armor = armor

    def set_weapon(self, weapon: Weapon) -> None:
        """remplace l'arme"""
        self.weapon = weapon

    def swap_weapon(self) -> None:
        """échange les deux armes"""
        self.weapon, self.secondary_weapon = self.secondary_weapon, self.weapon


class Ennemies(Entity):
    """classe des Ennemies hérité de Entité"""
    def __init__(self, game, x: int, y: int, img: tuple, size: tuple, hp: int, lvl: int, dmg: int,  colkey: int = 0):
        """
                :param game: Game                   | accès au jeu entier
        :param x: int                       | position x (en tuiles)
        :param y: int                       | position y (en tuiles)
        :param img: tuple(u: int, v: int)   | coordonnés de l'image de l'entité
        :param size: tuple(w: int, h: int)  | taille (toujours 16 par 16 normalement)
        :param hp: int                      | point de vies
        :param colkey: int                  | couleur à retirer dans l'affichage
        :param lvl: int                     | niveau de l'ennemi
        :param dmg: int                     | point de dégâts de l'ennemi
        :var self.patern: dict(...)         | représentation de l'attaque case par case
        :var self.maxhp: int                | point de vie maximum
        :var self.speed: int                | nombre d'action par tour
        :var self.attaque_tile: tuple       | coordonné de l'image de la tuile d'attaque ennemi
        """
        super().__init__(game, x, y, img, size, hp, colkey=colkey)
        self.patern = {"left": [[(-1, 0)]],
                       "right": [[(1, 0)]],
                       "top": [[(0, -1)]],
                       "bottom": [[(0, 1)]],
                       }
        self.attaque_tile = (16, 32)
        self.lvl = lvl
        self.speed = 1
        self.dmg = (lvl - 1) * dmg + randint(1, dmg-1)
        self.hp = (lvl - 1) * hp + randint(1, hp-1)
        self.maxhp = self.hp
        self.element = 0

    def action(self, forced=None):
        """effectue une action"""
        left_action = self.speed
        while left_action > 0:
            if forced is not None:
                if forced == "Attaque":
                    self.game.animation_list.append(AttaqueEnnemi(self.game, self))
                    left_action -= 1
                if forced == "Move":
                    distances = self.distance(self.game.player)
                    if abs(distances[0]) + abs(distances[1]) > 10:
                        side = self.low_distance_side(self.game.player)
                        if side == 0:
                            self.top()
                        elif side == 1:
                            self.bottom()
                        elif side == 2:
                            self.left()
                        elif side == 3:
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

            if self.get_if_player_touched():
                self.game.animation_list.append(AttaqueEnnemi(self.game, self))
                left_action -= 1
            if left_action > 0:
                distances = self.distance(self.game.player)
                if abs(distances[0])+abs(distances[1]) > 10:
                    side = self.low_distance_side(self.game.player)
                    if side == 0:
                        self.top()
                    elif side == 1:
                        self.bottom()
                    elif side == 2:
                        self.left()
                    elif side == 3:
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

    def damage(self, amount, el, source):
        """applique les dégâts, en cas de mort, ajoute un loot et détruit sa propre itération"""
        self.hp -= amount * EFFICACITE[self.element][el]
        if self.hp <= 0:
            if bool(randint(0, 1)):
                self.game.loots.append(Loot(self.lvl, self.x, self.y))
            self.game.ennemi.remove(self)

    def range_blit(self):
        """affiche la porté du l'ennemi en fonction de son patern"""
        for line in self.patern[ORIENT_EQ[self.orient]]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.x + pos[0] < len(self.game.carte.grille) and 0 <= self.y + pos[1] < len(self.game.carte.grille[0]) and not "obst" in self.game.carte.grille[self.x + pos[0]][self.y + pos[1]].types:
                    py.blt((self.x + pos[0]) * 16, (self.y + pos[1]) * 16, 0, self.attaque_tile[0],self.attaque_tile[1], 16, 16, 0)
                else:
                    blocked = True

    def get_if_player_touched(self) -> bool:
        """vérifie si joueur est dans les cases où l'ennemi attaque"""
        for line in self.patern[ORIENT_EQ[self.orient]]:
            blocked = False
            for pos in line:
                if not blocked and 0 <= self.x + pos[0] < len(self.game.carte.grille) and 0 <= self.y + pos[1] < len(self.game.carte.grille[0]) and not "obst" in self.game.carte.grille[self.x + pos[0]][self.y + pos[1]].types:
                    if self.game.player.x == self.x + pos[0] and self.game.player.y == self.y + pos[1]:
                        return True
                else:
                    blocked = True
        return False

    def attaque(self):
        """action d'attaque"""
        if self.get_if_player_touched():
            self.game.player.damage(self.dmg, self.element, self)

    def blit_life_bar(self):
        """affichage de la bar de vie au dessus + niveau"""
        py.rect(self.reel_x, self.reel_y-5, 16, 5, 8)
        py.rect(self.reel_x, self.reel_y-5, (self.hp/self.maxhp)*16, 5, 11 if self.game.carte.biome != "Grass" else 3)
        py.text(self.reel_x, self.reel_y-10, "lvl "+str(self.lvl), 7)


# Tout les différents ennemis possibles : ------------------------------------------------------------------------------

class Zombie(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 16), (16, 16), 25, lvl, 11, colkey=7)
        self.speed = 1
        self.element = 0


class Squelette(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 32), (16, 16), 16, lvl, 9, colkey=6)
        self.patern = {"left": [[(-i, 0) for i in range(1, 17)]],
                       "right": [[(i, 0) for i in range(1, 17)]],
                       "top": [[(0, -i) for i in range(1, 17)]],
                       "bottom": [[(0, i) for i in range(1, 17)]],
                       }
        self.speed = 1
        self.element = 0


class Bat(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 64), (16, 16), 12, lvl, 7, colkey=7)
        self.speed = 1
        self.element = 0


class Ghost(Ennemies):
    """
    héritage de Ennemi avec des valeurs prédéfini
    compétence :
        - résistance extrême aux Arcs
    """
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 80), (16, 16), 20, lvl, 7, colkey=7)
        self.speed = 1

    def damage(self, amount, el, source):
        if type(source.weapon) == Bow:
            amount *= 0.1
        super().damage(amount, el, source)


class BabyDragon(Ennemies):
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (32, 64), (16, 16), 35, lvl, 15, colkey=7)
        self.patern = {"left": [[(-1, 0), (-2, 0), (-3, 0)]],
                       "right": [[(1, 0), (2, 0), (3, 0)]],
                       "top": [[(0, -1), (0, -2), (0, -3)]],
                       "bottom": [[(0, 1), (0, 2), (0, 3)]]
                       }
        self.speed = 1
        self.element = 2


class Golem(Ennemies):
    """
    héritage de Ennemi avec des valeurs prédéfini
    compétence :
        - résistance aux dégats physique mais faiblesse aux dégâts élémentaires.
    """
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 96), (16, 16), 35, lvl, 15, colkey=7)
        if self.game.carte.biome != "Cave":
            self.img = (0, 96)
        else:
            self.img = (0, 112)
        self.imgX = self.img
        self.imgY = (self.img[0] + self.size[0], self.img[1])
        self.patern = {"left": [[(-1, 0), (-2, 0)]],
                       "right": [[(1, 0), (2, 0)]],
                       "top": [[(0, -1), (0, -2)]],
                       "bottom": [[(0, 1), (0, 2)]]
                       }
        self.speed = 1
        self.element = 3

    def damage(self, amount, el, source):
        """application des statistiques du golem aux dégâts"""
        if el != 0:
            amount *= 0.5
        else:
            amount *= 1.2
        super().damage(amount, el, source)


class Demon(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 48), (16, 16), 10, lvl, 30, colkey=7)
        self.speed = 1
        self.element = 2
        self.patern = {"left": [[(-1, 0), (-2, 0)]],
                       "right": [[(1, 0), (2, 0)]],
                       "top": [[(0, -1), (0, -2)]],
                       "bottom": [[(0, 1), (0, 2)]],
                       }


class Spider(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 128), (16, 16), 20, lvl, 12, colkey=7)
        self.speed = 1
        self.element = 3


class Vampire(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 160), (16, 16), 20, lvl, 10, colkey=6)
        self.speed = 1
        self.element = 0

    def damage(self, amount, el, source):
        super().damage(amount, el, source)
        self.hp += self.maxhp/2
        if self.hp > self.maxhp:
            self.hp = self.maxhp


class Diablotin(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 144), (16, 16), 10, lvl, 20, colkey=7)
        self.speed = 1
        self.element = 2


class BlobFeu(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 176), (16, 16), 15, lvl, 15, colkey=7)
        self.speed = 1
        self.element = 2


class BlobEau(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (32, 32), (16, 16), 15, lvl, 15, colkey=7)
        self.speed = 1
        self.element = 1


class Necromancien(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 192), (16, 16), 10, lvl, 2, colkey=6)
        self.speed = 1
        self.element = 0


class Aligator(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 208), (16, 16), 20, lvl, 20, colkey=7)
        self.speed = 1
        self.element = 0


class Abomination(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 224), (16, 16), 75, lvl, 50, colkey=7)
        self.speed = 1
        self.element = 0


class Mommies(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (0, 240), (16, 16), 10, lvl, 10, colkey=7)
        self.speed = 1
        self.element = 0


class Loup(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (32, 0), (16, 16), 8, lvl, 8, colkey=7)
        self.speed = 2
        self.element = 0


class Fox(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (32, 16), (16, 16), 8, lvl, 8, colkey=7)
        self.speed = 2
        self.element = 0


class Witch(Ennemies):
    """héritage de Ennemi avec des valeurs prédéfini"""
    def __init__(self, game, x: int, y: int, lvl: int):
        super().__init__(game, x, y, (32, 48), (16, 16), 10, lvl, 10, colkey=7)
        self.speed = 1
        self.element = 0
