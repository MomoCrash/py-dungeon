import pyxel as py
from Loot import Loot
from Entity import *
from random import randint, choice
from Carte import Carte

"""
file edit with Python 3.10:

version du jeu : 2.0

librairy :
public :
    - Pyxel 1.9.6
    - random
private :
    - Entity
    - Carte
    - Loot
    - Equipment

Other files :
    - assets.pyxres -> fichier avec tout les graphismes modifié avec la librairie Pyxel

Content :
contient la classe principal du jeu, qui est relié à n'importe quel élément et chaque élément est relié à elle.
Ainsi, depuis n'importe où on peut accéder à n'importe quoi.
"""


class Game:
    """
    Class Principal du jeu :
    """
    def __init__(self):
        """
        Initialise la librarie Pyxel et créé des conteneur pour chaque élément du jeu.
        conteneurs :
            - carte Carte -> carte sur laquel le personnage évolue
            - player Player -> le joueur contrôlé
            - ennemi list(Ennemies) -> tout les ennemis dans une salle
            - loots list(Loot) -> tout les loots actifs
        """
        py.init(288, 272, fps=60, quit_key=py.KEY_ESCAPE)
        py.load("assets.pyxres")
        self.carte = Carte(self)
        self.player = Player(self, 0, 0)
        self.ennemi = []
        self.loots = []
        self.looting = True
        self.carte.new_stage()
        self.animation_list = []
        self.animation_layer = []

    def rand_spawns(self, n, specifique = None, local_section=(0, 0, 15, 15)) -> None:
        """
        Rajoute des ennemies aléatoirement sur la map, où il n'y a pas de mur.
        :arg n: int | nombre d'ennemis à rajouter.
        :arg local_section: tuple(int, int, int, int) | représente le rectangle où peut spawn les ennemies
        :arg specifique: list(type) | liste de tout les monstres qui peuvent apparaître dans un biome
        par défault toute la map. (x, y, width, height)
        """
        spawned = 0
        if specifique is None:
            specifique = Ennemies.__subclasses__()
        while spawned < n:
            x = randint(local_section[0], local_section[0]+local_section[2])
            y = randint(local_section[1], local_section[1]+local_section[3])
            if "obst" not in self.carte.grille[x][y].types and not self.check_full_tile(x, y):
                type_spawn = choice(specifique)
                self.ennemi.append(type_spawn(self, x, y, self.carte.stage//4+1))
                spawned += 1

    def check_full_tile(self, x: int, y: int) -> bool:
        """
        vérifie si la case est remplie par une entité
        :arg x: position x de la case
        :arg y: position y de la case
        """
        for e in self.ennemi:
            if e.x == x and e.y == y:
                return True
        if self.player.x == x and self.player.y == y:
            return True
        return False

    def update(self) -> None:
        """methode appelée à chaque actualisation de l'écran : fait toute les opérations et gère les inputs"""
        self.carte.actualisation()

        if len(self.animation_list) != 0:
            if self.animation_list[0].origine in self.ennemi:
                for anime in self.animation_list:
                    if anime.origine in self.ennemi:
                        anime.animate()
            else:
                self.animation_list[0].animate()
        else:
            if py.btn(py.KEY_A):
                """attaquer"""
                for e in self.ennemi:
                    e.action()
                self.player.attaque()
            if py.btnp(py.KEY_E, hold=60):
                """interact"""
                for loot in self.loots:
                    if loot.x == self.player.x and loot.y == self.player.y:
                        loot.get_loot(self.player)
            if py.btnp(py.KEY_Q, hold=20):
                """aller à gauche"""
                for e in self.ennemi:
                    e.action()
                self.player.left()
            if py.btnp(py.KEY_D, hold=20):
                """aller à droite"""
                for e in self.ennemi:
                    e.action()
                self.player.right()
            if py.btnp(py.KEY_Z, hold=20):
                """aller à haut"""
                for e in self.ennemi:
                    e.action()
                self.player.top()
            if py.btnp(py.KEY_S, hold=20):
                """aller à bas"""
                for e in self.ennemi:
                    e.action()
                self.player.bottom()

            if py.btn(py.KEY_LEFT):
                """regarger gauche"""
                self.player.watch_left()
            if py.btn(py.KEY_RIGHT):
                """regarger droit"""
                self.player.watch_right()
            if py.btn(py.KEY_UP):
                """regarger haut"""
                self.player.watch_top()
            if py.btn(py.KEY_DOWN):
                """regarger bas"""
                self.player.watch_bottom()

            if py.btn(py.KEY_W):
                """skip on looting zone"""
                if self.looting:
                    self.carte.new_stage()
            if py.btn(py.KEY_R):
                """spawn"""
                self.rand_spawns(3)
            if py.btnp(py.KEY_F, hold=60):
                """changer d'arme"""
                self.player.swap_weapon()

    def draw(self) -> None:
        """methode appelée à chaque actualisation de l'écran : dessine toute les images à l'écran"""
        py.cls(0)
        self.carte.blit()
        for loot in self.loots:
            if self.looting or (not loot.forced[0] and loot.type == "Life"):
                loot.blit()
        for e in self.ennemi:
            e.blit_entity()
            e.range_blit()
            e.blit_life_bar()
        self.player.blit_entity()
        self.player.weapon.blit_range()
        self.player.blit_life_bar()
        py.text(256, 0, "Armor :", 7)
        self.player.armor.blit(decalY=8)
        py.rect(256, 40, 32, 2, 7)
        py.text(256, 50, "weapon \nin hand :", 7)
        self.player.weapon.blit(decalY=64)
        py.text(256, 95, "weapon \nin bag :", 7)
        self.player.secondary_weapon.blit(decalY=110)
        for loot in self.loots:
            if loot.x == self.player.x and loot.y == self.player.y and (self.looting or (not loot.forced[0] and loot.type == "Life")):
                loot.blit_inv()
        for anime in self.animation_layer:
            py.blt(anime[0], anime[1], anime[2], anime[3], anime[4], anime[5], anime[6], anime[7])
        self.animation_layer.clear()

    def run(self) -> None:
        """lance le jeu et sa fenêtre"""
        py.run(self.update, self.draw)


g = Game()
g.run()
