from Entity import *
from Carte import Carte
from Menu import *
from Settings import texts, KATANA0, KATANA1, KATANA2, DEAFEAT_FIRST_PART, DEAFEAT_SECOND_PART

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
        self.score = 0
        self.all_menus = {
            "TAB": Box((0, 0),
                   (Bloc, (0, 0), (288, 25), 1),
                   (Text, (119, 7), "MENU", 7),
                   (Text, (35, 30), texts["touches"], 0),
                   (Bloc, (5, 46), (16, 40), 14),
                   (Bloc, (5, 96), (16, 40), 14),
                   (Bloc, (5, 146), (16, 40), 14),
                   (Bloc, (5, 196), (16, 40), 14),
                   (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                   (Text, (30, 82), texts["test"], 0),
                   wh=(288, 272), bg=10, root=self, f=((109, 240), (70, 20), "EXIT", 1, 6, None)),
            "START": Box((0, 0),
                     (Bloc, (0, 0), (288, 25), 1),
                     (Text, (110, 7), "-| Py-Dungeon |-", 7),
                     (Text, (35, 30), texts["touches"], 0),
                     (Bloc, (5, 46), (16, 40), 14),
                     (Bloc, (5, 96), (16, 40), 14),
                     (Bloc, (5, 146), (16, 40), 14),
                     (Bloc, (5, 196), (16, 40), 14),
                     (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                     (Text, (30, 82), texts["test"], 0),
                     wh=(288, 272), bg=10, root=self, f=((109, 240), (70, 20), "START !", 1, 6, None)),
        }

        self.menu = None
        self.start()

    def start(self):
        """remet à zéro tout le jeu"""
        py.load("assets.pyxres")
        self.carte = Carte(self)
        self.player = Player(self, 0, 0)
        self.ennemi = []
        self.loots = []
        self.looting = True
        self.carte.new_stage()
        self.animation_list = []
        self.animation_layer = []
        self.menu = self.all_menus["START"]
        self.score = 0

    def loose(self):
        self.menu = Box((0, 0),
                    (Canevas, DEAFEAT_FIRST_PART(110, 50), DEAFEAT_SECOND_PART(142, 50)),
                    (ScoreText, (70, 70), self.score, 0),
                    wh=(288, 272), bg=8, root=self, f=((0, 250), (288, 22), "RESTART !", 0, 7, self.start))

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
        elif self.menu is None:
            py.mouse(False)
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
                self.start()
            if py.btnp(py.KEY_F, hold=60):
                """changer d'arme"""
                self.player.swap_weapon()
            if py.btnp(py.KEY_TAB, hold=60):
                """Affiche le Menu"""
                self.menu = self.all_menus["TAB"]
        else:
            py.mouse(True)
            if py.btnp(py.KEY_TAB, hold=60):
                """changer d'arme"""
                self.menu = None

    def draw(self) -> None:
        """methode appelée à chaque actualisation de l'écran : dessine toute les images à l'écran"""
        py.cls(0)
        if self.menu is None:
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
            py.text(257, 0, "Armor :", 7)
            self.player.armor.blit(decalY=8)
            py.rect(256, 40, 32, 2, 7)
            py.text(257, 45, "weapon \nin hand :", 7)
            self.player.weapon.blit(decalY=59)
            py.text(257, 95, "weapon \nin bag :", 7)
            self.player.secondary_weapon.blit(decalY=110)
            py.rect(256, 145, 32, 2, 7)
            py.text(257, 148, "Au sol :", 7)
            for loot in self.loots:
                if loot.x == self.player.x and loot.y == self.player.y and (self.looting or (not loot.forced[0] and loot.type == "Life")):
                    loot.blit_inv()
            py.rect(256, 195, 32, 2, 7)
            temp = f"Score :\n{self.score} pts"
            chaine = ""
            for i in range(len(temp)):
                if i == 37:
                    chaine += "..."
                    break
                chaine += temp[i]
                if i % 8 == 7:
                    chaine += "\n"
            py.text(257, 200, chaine, 7)
            for anime in self.animation_layer:
                py.blt(anime[0], anime[1], anime[2], anime[3], anime[4], anime[5], anime[6], anime[7])
            self.animation_layer.clear()

        else:
            self.menu.blit()

    def run(self) -> None:
        """lance le jeu et sa fenêtre"""
        py.run(self.update, self.draw)


g = Game()
g.run()
