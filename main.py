from Entity import *
from Carte import Carte
from Menu import *
from Settings import (TEXTS, KATANA0, KATANA1, KATANA2, DEAFEAT_FIRST_PART, DEAFEAT_SECOND_PART, MONSTER_IMG)

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
    - Settings
    - Loot
    - Animate
    

Other files :
    - assets.pyxres -> fichier avec tout les graphismes modifié avec la librairie Pyxel
    (Data.txt -> récapitulatif des infos du projects + lien utiles)

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
        self.next_lvl = 2
        self.all_menus = {
            "TAB": Box((0, 0),
                       (Bloc, (0, 0), (288, 25), 1),
                       (Text, (119, 7), "MENU", 7),
                       (Text, (35, 30), TEXTS["touches"], 0),
                       (Bloc, (5, 46), (16, 40), 14),
                       (Bloc, (5, 96), (16, 40), 14),
                       (Bloc, (5, 146), (16, 40), 14),
                       (Bloc, (5, 196), (16, 40), 14),
                       (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                       (Text, (30, 82), TEXTS["test"], 0),
                       (Button, (246, 33), (60, 16), "Menu      >>", 1, 7, self.open_tab),
                       (Button, (230, 50), (60, 16), "Bestiaire >>", 1, 7, self.open_header),
                       (Button, (230, 67), (60, 16), "Niveau    >>", 1, 7, self.open_stats),
                       wh=(288, 272), bg=10, root=self, exit=((0, 252), (288, 20), "QUIT", 15, 8)),
            "START": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 1),
                         (Text, (110, 7), "-| Py-Dungeon |-", 7),
                         (Text, (35, 26), TEXTS["touches"], 0),
                         (Bloc, (5, 46), (16, 40), 14),
                         (Bloc, (5, 96), (16, 40), 14),
                         (Bloc, (5, 146), (16, 40), 14),
                         (Bloc, (5, 196), (16, 40), 14),
                         (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                         (Text, (30, 82), TEXTS["test"], 0),
                         wh=(288, 272), bg=10, root=self, exit=((109, 240), (70, 20), "START !", 1, 6, self.start)),
            "STATS": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 1),
                         (Text, (119, 7), "NIVEAU", 7),
                         (StatText, (35, 30), 5, self.player),
                         (Bloc, (5, 46), (16, 40), 14),
                         (Bloc, (5, 96), (16, 40), 14),
                         (Bloc, (5, 146), (16, 40), 14),
                         (Bloc, (5, 196), (16, 40), 14),
                         (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                         #(Text, (30, 82), TEXTS["test"], 0),
                         (Button, (230, 33), (60, 16), "Menu      >>", 1, 7, self.open_tab),
                         (Button, (230, 50), (60, 16), "Bestiaire >>", 1, 7, self.open_header),
                         (Button, (246, 67), (60, 16), "Niveau    >>", 1, 7, self.open_stats),
                         wh=(288, 272), bg=10, root=self, exit=((0, 252), (288, 20), "QUIT", 15, 8)),
        }

        self.bestiaire = {
            "HEADER": Box((0, 0),
                          (Bloc, (0, 0), (288, 25), 1),
                          (Text, (115, 10), "BESTIAIRE", 7),
                          (Bloc, (5, 46), (16, 40), 14),
                          (Bloc, (5, 96), (16, 40), 14),
                          (Bloc, (5, 146), (16, 40), 14),
                          (Bloc, (5, 196), (16, 40), 14),
                          (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                          (Iframe, MONSTER_IMG["Zombie"](41, 40), 0, self.open_Zombie),
                          (Iframe, MONSTER_IMG["Squelette"](75, 40), 0, self.open_Squelette),
                          (Iframe, MONSTER_IMG["Demon"](109, 40), 1, self.open_Demon),
                          (Iframe, MONSTER_IMG["Bat"](142, 40), 0, self.open_Bat),
                          (Iframe, MONSTER_IMG["Ghost"](176, 40), 1, self.open_Ghost),
                          (Iframe, MONSTER_IMG["Golem"](210, 40), 0, self.open_Golem),
                          (Iframe, MONSTER_IMG["Spider"](41, 74), 7, self.open_Spider),
                          (Iframe, MONSTER_IMG["Diablotin"](75, 74), 1, self.open_Diablotin),
                          (Iframe, MONSTER_IMG["Vampire"](109, 74), 1, self.open_Vampire),
                          (Iframe, MONSTER_IMG["BlobFeu"](142, 74), 0, self.open_BlobFeu),
                          (Iframe, MONSTER_IMG["BlobEau"](176, 74), 0, self.open_BlobEau),
                          (Bloc, (210, 75), (16, 16), 11),
                          (Iframe, MONSTER_IMG["Aligator"](41, 108), 0, self.open_Aligator),
                          (Iframe, MONSTER_IMG["Mommies"](75, 108), 0, self.open_Mommies),
                          (Iframe, MONSTER_IMG["Loup"](109, 108), 0, self.open_Loup),
                          (Iframe, MONSTER_IMG["Fox"](142, 108), 0, self.open_Fox),
                          (Iframe, MONSTER_IMG["Necromancien"](176, 108), 0, self.open_Necromancien),
                          (Iframe, MONSTER_IMG["Witch"](210, 108), 0, self.open_Witch),
                          (Iframe, MONSTER_IMG["BabyDragon"](41, 141), 0, self.open_BabyDragon),
                          (Iframe, MONSTER_IMG["Abomination"](75, 141), 0, self.open_Abomination),
                          (Button, (230, 33), (60, 16), "Menu      >>", 1, 7, self.open_tab),
                          (Button, (246, 50), (60, 16), "Bestiaire >>", 1, 7, self.open_header),
                          (Button, (230, 67), (60, 16), "Niveau    >>", 1, 7, self.open_stats),
                          wh=(288, 272), bg=10, root=self, exit=((0, 252), (288, 20), "QUIT", 15, 8)),
            "Zombie": Box((0, 0),
                          (Bloc, (0, 0), (288, 25), 10),
                          (Text, (115, 10), "ZOMBIE", 1),
                          (Iframe, MONSTER_IMG["Zombie"](41, 40), 0, self.open_header),
                          (Text, (57, 40), TEXTS["Zombie"], 7),
                          wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Squelette": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "SQUELETTE", 1),
                             (Iframe, MONSTER_IMG["Squelette"](75, 40), 0, self.open_header),
                             (Text, (91, 40), TEXTS["Squelette"], 7),
                             wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Demon": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "DEMON", 1),
                         (Iframe, MONSTER_IMG["Demon"](109, 40), 1, self.open_header),
                         (Text, (125, 40), TEXTS["Demon"], 7),
                         wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Bat": Box((0, 0),
                       (Bloc, (0, 0), (288, 25), 10),
                       (Text, (115, 10), "BAT", 1),
                       (Iframe, MONSTER_IMG["Bat"](142, 40), 0, self.open_header),
                       (Text, (158, 40), TEXTS["Bat"], 7),
                       wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Ghost": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "GHOST", 1),
                         (Iframe, MONSTER_IMG["Ghost"](176, 40), 1, self.open_header),
                         (Text, (192, 40), TEXTS["Ghost"], 7),
                         wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Golem": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "GOLEM", 1),
                         (Iframe, MONSTER_IMG["Golem"](210, 40), 0, self.open_header),
                         (Text, (226, 40), TEXTS["Golem"], 7),
                         wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Spider": Box((0, 0),
                          (Bloc, (0, 0), (288, 25), 10),
                          (Text, (115, 10), "SPIDER", 1),
                          (Iframe, MONSTER_IMG["Spider"](41, 74), 7, self.open_header),
                          (Text, (57, 74), TEXTS["Spider"], 7),
                          wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Diablotin": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "DIABLOTIN", 1),
                             (Iframe, MONSTER_IMG["Diablotin"](75, 74), 1, self.open_header),
                             (Text, (91, 74), TEXTS["Diablotin"], 7),
                             wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Vampire": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "VAMPIRE", 1),
                           (Iframe, MONSTER_IMG["Vampire"](109, 74), 1, self.open_header),
                           (Text, (125, 74), TEXTS["Vampire"], 7),
                           wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "BlobFeu": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "BLOB FEU", 1),
                           (Iframe, MONSTER_IMG["BlobFeu"](142, 74), 0, self.open_header),
                           (Text, (158, 74), TEXTS["BlobFeu"], 7),
                           wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "BlobEau": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "BLOB EAU", 1),
                           (Iframe, MONSTER_IMG["BlobEau"](176, 74), 0, self.open_header),
                           (Text, (192, 74), TEXTS["BlobEau"], 7),
                           wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Aligator": Box((0, 0),
                            (Bloc, (0, 0), (288, 25), 10),
                            (Text, (115, 10), "ALIGATOR", 1),
                            (Iframe, MONSTER_IMG["Aligator"](41, 108), 0, self.open_header),
                            (Text, (57, 108), TEXTS["Aligator"], 7),
                            wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Mommies": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "MOMMIES", 1),
                           (Iframe, MONSTER_IMG["Mommies"](75, 108), 0, self.open_header),
                           (Text, (91, 108), TEXTS["Mommies"], 7),
                           wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Loup": Box((0, 0),
                        (Bloc, (0, 0), (288, 25), 10),
                        (Text, (115, 10), "LOUP", 1),
                        (Iframe, MONSTER_IMG["Loup"](109, 108), 0, self.open_header),
                        (Text, (125, 108), TEXTS["Loup"], 7),
                        wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Fox": Box((0, 0),
                       (Bloc, (0, 0), (288, 25), 10),
                       (Text, (115, 10), "FOX", 1),
                       (Iframe, MONSTER_IMG["Fox"](142, 108), 0, self.open_header),
                       (Text, (158, 108), TEXTS["Fox"], 7),
                       wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Necromancien": Box((0, 0),
                                (Bloc, (0, 0), (288, 25), 10),
                                (Text, (115, 10), "NECROMANCIEN", 1),
                                (Iframe, MONSTER_IMG["Necromancien"](176, 108), 0, self.open_header),
                                (Text, (192, 108), TEXTS["Necromancien"], 7),
                                wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Witch": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "WITCH", 1),
                         (Iframe, MONSTER_IMG["Witch"](210, 108), 0, self.open_header),
                         (Text, (226, 108), TEXTS["Witch"], 7),
                         wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "BabyDragon": Box((0, 0),
                              (Bloc, (0, 0), (288, 25), 10),
                              (Text, (115, 10), "BABY DRAGON", 1),
                              (Iframe, MONSTER_IMG["BabyDragon"](41, 141), 0, self.open_header),
                              (Text, (57, 141), TEXTS["BabyDragon"], 7),
                              wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
            "Abomination": Box((0, 0),
                               (Bloc, (0, 0), (288, 25), 10),
                               (Text, (115, 10), "ABOMINATION", 1),
                               (Iframe, MONSTER_IMG["Abomination"](75, 141), 0, self.open_header),
                               (Text, (91, 141), TEXTS["Abomination"], 7),
                               wh=(288, 272), bg=0, root=self, exit=((0, 252), (288, 20), "QUIT", 7, 8)),
        }
        self.menu = None
        self.open_start()

    def start(self):
        """remet à zéro tout le jeu"""
        py.load("assets.pyxres")
        self.carte = Carte(self)
        self.player.reset_stats()
        self.ennemi = []
        self.loots = []
        self.looting = True
        self.carte.new_stage()
        self.animation_list = []
        self.animation_layer = []
        self.menu = None
        self.score = 0
        self.next_lvl = 2

    def loose(self):
        self.menu = Box((0, 0),
                        (Canevas, DEAFEAT_FIRST_PART(110, 50), DEAFEAT_SECOND_PART(142, 50)),
                        (ScoreText, (70, 70), self.score, 0),
                        wh=(288, 272), bg=8, root=self, exit=((0, 250), (288, 22), "RESTART !", 0, 7, self.start))

    def open_start(self):
        self.menu = self.all_menus["START"]

    def open_tab(self):
        self.menu = self.all_menus["TAB"]

    def open_stats(self):
        self.all_menus["STATS"].element[2].actu_points()
        self.menu = self.all_menus["STATS"]

    def open_header(self):
        self.menu = self.bestiaire["HEADER"]

    def open_Zombie(self):
        self.menu = self.bestiaire["Zombie"]

    def open_Squelette(self):
        self.menu = self.bestiaire["Squelette"]

    def open_Demon(self):
        self.menu = self.bestiaire["Demon"]

    def open_Bat(self):
        self.menu = self.bestiaire["Bat"]

    def open_Ghost(self):
        self.menu = self.bestiaire["Ghost"]

    def open_Golem(self):
        self.menu = self.bestiaire["Golem"]

    def open_Spider(self):
        self.menu = self.bestiaire["Spider"]

    def open_Diablotin(self):
        self.menu = self.bestiaire["Diablotin"]

    def open_Vampire(self):
        self.menu = self.bestiaire["Vampire"]

    def open_BlobFeu(self):
        self.menu = self.bestiaire["BlobFeu"]

    def open_Necromancien(self):
        self.menu = self.bestiaire["Necromancien"]

    def open_Aligator(self):
        self.menu = self.bestiaire["Aligator"]

    def open_Abomination(self):
        self.menu = self.bestiaire["Abomination"]

    def open_Mommies(self):
        self.menu = self.bestiaire["Mommies"]

    def open_Loup(self):
        self.menu = self.bestiaire["Loup"]

    def open_Fox(self):
        self.menu = self.bestiaire["Fox"]

    def open_BlobEau(self):
        self.menu = self.bestiaire["BlobEau"]

    def open_Witch(self):
        self.menu = self.bestiaire["Witch"]

    def open_BabyDragon(self):
        self.menu = self.bestiaire["BabyDragon"]

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
            self.menu.update()
            if py.btnp(py.KEY_TAB, hold=60):
                """changer d'arme"""
                self.menu = None

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
            if loot.x == self.player.x and loot.y == self.player.y and (
                    self.looting or (not loot.forced[0] and loot.type == "Life")):
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
        self.menu.blit() if self.menu is not None else None

    def run(self) -> None:
        """lance le jeu et sa fenêtre"""
        py.run(self.update, self.draw)


g = Game()
g.run()
