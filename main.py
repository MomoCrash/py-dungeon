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
    - Pyxel 1.9.2
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
        self.rand_spawns(3, local_section=(8, 8, 7, 7))
        self.loots = []
        self.looting = False

    def rand_spawns(self, n, local_section=(0, 0, 15, 15)) -> None:
        """
        Rajoute des ennemies aléatoirement sur la map, où il n'y a pas de mur.
        :arg n: int | nombre d'ennemis à rajouter.
        :arg local_section: tuple(int, int, int, int) | représente le rectangle où peut spawn les ennemies
        par défault toute la map. (x, y, width, height)
        """
        spawned = 0
        while spawned < n:
            x = randint(local_section[0], local_section[0]+local_section[2])
            y = randint(local_section[1], local_section[1]+local_section[3])
            if "obst" not in self.carte.grille[x][y].types and not self.check_full_tile(x, y):
                type_spawn = choice(Ennemies.__subclasses__())
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

        if py.btnp(py.KEY_A, hold=60):
            """attaquer"""
            for e in self.ennemi:
                e.action()
            self.player.attaque()
        if py.btnp(py.KEY_E, hold=60):
            """interact"""
            for loot in self.loots:
                if loot.x == self.player.x and loot.y == self.player.y:
                    loot.get_loot(self.player)
        if py.btnp(py.KEY_Q, hold=60):
            """aller à gauche"""
            self.player.left()
            for e in self.ennemi:
                e.action()
        if py.btnp(py.KEY_D, hold=60):
            """aller à droite"""
            self.player.right()
            for e in self.ennemi:
                e.action()
        if py.btnp(py.KEY_Z, hold=60):
            """aller à haut"""
            self.player.top()
            for e in self.ennemi:
                e.action()
        if py.btnp(py.KEY_S, hold=60):
            """aller à bas"""
            self.player.bottom()
            for e in self.ennemi:
                e.action()

        if py.btnp(py.KEY_LEFT, hold=60):
            """regarger gauche"""
            self.player.watch_left()
        if py.btnp(py.KEY_RIGHT, hold=60):
            """regarger droit"""
            self.player.watch_right()
        if py.btnp(py.KEY_UP, hold=60):
            """regarger haut"""
            self.player.watch_top()
        if py.btnp(py.KEY_DOWN, hold=60):
            """regarger bas"""
            self.player.watch_bottom()

        if py.btnp(py.KEY_W, hold=60):
            """skip on looting zone"""
            if self.looting:
                self.carte.new_stage()
        if py.btnp(py.KEY_R, hold=60):
            """spawn"""
            self.rand_spawns(3)
        if py.btnp(py.KEY_F, hold=60):
            """self damage"""
            self.player.damage(10)

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
        self.player.armor.blit()
        self.player.weapon.blit()
        for loot in self.loots:
            if loot.x == self.player.x and loot.y == self.player.y and (self.looting or (not loot.forced[0] and loot.type == "Life")):
                loot.blit_inv()

    def run(self) -> None:
        """lance le jeu et sa fenêtre"""
        py.run(self.update, self.draw)


g = Game()
g.run()
