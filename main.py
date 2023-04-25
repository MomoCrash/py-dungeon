from Settings import *
from Carte import *
from Menu import *

"""
file edit with Python 3.10:

version du jeu : 2.0

librairy :
public :d
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
Ainsi, depuis n'importe où on peut accéder à n'importe quoi. (instance du projet)
"""


class Game:
    """
    Class Principal du jeu :
    """
    def __init__(self):
        """
        Initialise la librarie Pyxel et créé des conteneurs pour chaque élément du jeu.
        conteneurs :
            - carte Carte -> carte sur laquel le personnage évolue
            - player Player -> le joueur contrôlé
            - ennemi list(Ennemies) -> tous les ennemis dans une salle
            - loots list(Loot) -> tout les loots actifs
        """
        py.init(WIN_W, WIN_H, fps=60, quit_key=py.KEY_ESCAPE)
        py.load("assets.pyxres")
        py.fullscreen(False)
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
        self.is_loose = False
        # Create list of menu instance for -> TAB menu (e.g bestiare, start, niveau)
        self.all_menus = {
            "TAB": Box((0, 0),
                       (Bloc, (0, 0), (WIN_W, 25), 1),
                       (Text, ((WIN_W - MILIEUMOT(4)) // 2, 7), "MENU", 7),
                       (Text, (35, 30), TEXTS["touches"], 0),
                       (Bloc, (5, 46), (16, 40), 14),
                       (Bloc, (5, 96), (16, 40), 14),
                       (Bloc, (5, 146), (16, 40), 14),
                       (Bloc, (5, 196), (16, 40), 14),
                       (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                       (Text, (30, 92), TEXTS["resumé"], 0),
                       (Button, (WIN_W - 42, 33), (60, 16), "Menu      >>", 1, 7, self.open_tab),
                       (Button, (WIN_W - 58, 50), (60, 16), "Bestiaire >>", 1, 7, self.open_header),
                       (Button, (WIN_W - 58, 67), (60, 16), "Niveau    >>", 1, 7, self.open_stats),
                       (Button, (WIN_W - 58, 84), (60, 16), "Histoire  >>", 1, 7, self.open_histoire),
                       wh=(WIN_W, WIN_H), bg=10, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 15, 8)),
            "START": Box((0, 0),
                         (Bloc, (0, 0), (WIN_W, 25), 1),
                         (Text, ((WIN_W - MILIEUMOT(16)) // 2, 7), "-| Py-Dungeon |-", 7),
                         (Text, (35, 26), TEXTS["touches"], 0),
                         (Bloc, (5, 46), (16, 40), 14),
                         (Bloc, (5, 96), (16, 40), 14),
                         (Bloc, (5, 146), (16, 40), 14),
                         (Bloc, (5, 196), (16, 40), 14),
                         (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                         (Text, (30, 92), TEXTS["resumé"], 0),
                         wh=(WIN_W, WIN_H), bg=10, root=self, but_exit=(
                ((WIN_W - MILIEUMOT(7) - 40) // 2, WIN_H - 46), (70, 20), "START !", 1, 6, self.start)),
            "STORY": Box((0, 0),
                         (Bloc, (0, 0), (WIN_W, 25), 1),
                         (Text, ((WIN_W - MILIEUMOT(5)) // 2, 7), "STORY", 7),
                         (Bloc, (5, 46), (16, 40), 14),
                         (Bloc, (5, 96), (16, 40), 14),
                         (Bloc, (5, 146), (16, 40), 14),
                         (Bloc, (5, 196), (16, 40), 14),
                         (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                         (Text, (30, 30), TEXTS["histoire"], 0),
                         (Button, (WIN_W - 58, 33), (60, 16), "Menu      >>", 1, 7, self.open_tab),
                         (Button, (WIN_W - 58, 50), (60, 16), "Bestiaire >>", 1, 7, self.open_header),
                         (Button, (WIN_W - 58, 67), (60, 16), "Niveau    >>", 1, 7, self.open_stats),
                         (Button, (WIN_W - 42, 84), (60, 16), "Histoire  >>", 1, 7, self.open_histoire),
                         wh=(WIN_W, WIN_H), bg=10, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 15, 8)),
            "STATS": Box((0, 0),
                         (Bloc, (0, 0), (WIN_W, 25), 1),
                         (Text, ((WIN_W - MILIEUMOT(6)) // 2, 7), "NIVEAU", 7),
                         (StatText, (35, 30), 5, self.player),
                         (Bloc, (5, 46), (16, 40), 14),
                         (Bloc, (5, 96), (16, 40), 14),
                         (Bloc, (5, 146), (16, 40), 14),
                         (Bloc, (5, 196), (16, 40), 14),
                         (Canevas, KATANA0(5, 50), KATANA2(5, 100), KATANA1(5, 150), KATANA2(5, 200)),
                         (Button, (WIN_W - 58, 33), (60, 16), "Menu      >>", 1, 7, self.open_tab),
                         (Button, (WIN_W - 58, 50), (60, 16), "Bestiaire >>", 1, 7, self.open_header),
                         (Button, (WIN_W - 42, 67), (60, 16), "Niveau    >>", 1, 7, self.open_stats),
                         (Button, (WIN_W - 58, 84), (60, 16), "Histoire  >>", 1, 7, self.open_histoire),
                         wh=(WIN_W, WIN_H), bg=10, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 15, 8))
        }

        self.bestiaire = {
            "HEADER": Box((0, 0),
                          (Bloc, (0, 0), (WIN_W, 25), 1),
                          (Text, ((WIN_W - MILIEUMOT(9)) // 2, 10), "BESTIAIRE", 7),
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
                          (Iframe, MONSTER_IMG["BlobPlant"](210, 74), 0, self.open_BlobPlant),
                          (Iframe, MONSTER_IMG["Aligator"](41, 108), 0, self.open_Aligator),
                          (Iframe, MONSTER_IMG["Mommies"](75, 108), 0, self.open_Mommies),
                          (Iframe, MONSTER_IMG["Loup"](109, 108), 0, self.open_Loup),
                          (Iframe, MONSTER_IMG["Fox"](142, 108), 0, self.open_Fox),
                          (Iframe, MONSTER_IMG["Necromancien"](176, 108), 0, self.open_Necromancien),
                          (Iframe, MONSTER_IMG["Witch"](210, 108), 0, self.open_Witch),
                          (Iframe, MONSTER_IMG["DragonFeu"](41, 141), 0, self.open_BabyDragon),
                          (Iframe, MONSTER_IMG["Abomination"](75, 141), 0, self.open_Abomination),
                          (Iframe, MONSTER_IMG["Snake"](109, 141), 0, self.open_Snake),
                          (Iframe, MONSTER_IMG["Creeper"](142, 141), 1, self.open_Creeper),
                          (Iframe, MONSTER_IMG["Rampant"](176, 141), 7, self.open_Rampant),
                          (Iframe, MONSTER_IMG["Notch"](210, 141), 1, self.open_Notch),
                          (Iframe, MONSTER_IMG["Angel"](41, 175), 0, self.open_Angel),
                          (Iframe, MONSTER_IMG["Arcangel"](75, 175), 0, self.open_Arcangel),
                          (Iframe, MONSTER_IMG["DragonLight"](109, 175), 1, self.open_DragonLight),
                          (Iframe, MONSTER_IMG["DragonDark"](142, 175), 1, self.open_DragonDark),
                          (Iframe, MONSTER_IMG["DragonEau"](176, 175), 0, self.open_DragonEau),
                          (Iframe, MONSTER_IMG["DragonPlant"](210, 175), 0, self.open_DragonPlant),
                          (Iframe, MONSTER_IMG["BlobLight"](41, 209), 0, self.open_BlobLight),
                          (Iframe, MONSTER_IMG["BlobDark"](75, 209), 7, self.open_BlobDark),

                          (Button, (WIN_W - 58, 33), (60, 16), "Menu      >>", 1, 7, self.open_tab),
                          (Button, (WIN_W - 42, 50), (60, 16), "Bestiaire >>", 1, 7, self.open_header),
                          (Button, (WIN_W - 58, 67), (60, 16), "Niveau    >>", 1, 7, self.open_stats),
                          (Button, (WIN_W - 58, 84), (60, 16), "Histoire  >>", 1, 7, self.open_histoire),
                          wh=(WIN_W, WIN_H), bg=10, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 15, 8)),
            "Zombie": Box((0, 0),
                          (Bloc, (0, 0), (288, 25), 10),
                          (Text, (115, 10), "ZOMBIE", 1),
                          (Text, (57, 40), "ZOMBIE", 7),
                          (Iframe, MONSTER_IMG["Zombie"](30, 40), 0, self.open_header),
                          (Text, (20, 67), TEXTS["Zombie"], 7),
                          wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Squelette": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "SQUELETTE", 1),
                             (Text, (57, 40), "SQUELETTE", 7),
                             (Iframe, MONSTER_IMG["Squelette"](30, 40), 0, self.open_header),
                             (Text, (20, 67), TEXTS["Squelette"], 7),
                             wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Demon": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "DEMON", 1),
                         (Text, (57, 40), "DEMON", 7),
                         (Iframe, MONSTER_IMG["Demon"](30, 40), 1, self.open_header),
                         (Text, (20, 67), TEXTS["Demon"], 7),
                         wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Bat": Box((0, 0),
                       (Bloc, (0, 0), (288, 25), 10),
                       (Text, (115, 10), "BAT", 1),
                       (Text, (57, 40), "BAT", 7),
                       (Iframe, MONSTER_IMG["Bat"](30, 40), 0, self.open_header),
                       (Text, (20, 67), TEXTS["Bat"], 7),
                       wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Ghost": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "GHOST", 1),
                         (Text, (57, 40), "GHOST", 7),
                         (Iframe, MONSTER_IMG["Ghost"](30, 40), 1, self.open_header),
                         (Text, (20, 67), TEXTS["Ghost"], 7),
                         wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Golem": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "GOLEM", 1),
                         (Text, (57, 40), "GOLEM", 7),
                         (Iframe, MONSTER_IMG["Golem"](30, 40), 1, self.open_header),
                         (Text, (20, 67), TEXTS["Golem"], 7),
                         wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Spider": Box((0, 0),
                          (Bloc, (0, 0), (288, 25), 10),
                          (Text, (115, 10), "SPIDER", 1),
                          (Text, (57, 40), "SPIDER", 7),
                          (Iframe, MONSTER_IMG["Spider"](30, 40), 1, self.open_header),
                          (Text, (20, 67), TEXTS["Spider"], 7),
                          wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Diablotin": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "DIABLOTIN", 1),
                             (Text, (57, 40), "DIABLOTIN", 7),
                             (Iframe, MONSTER_IMG["Diablotin"](30, 40), 1, self.open_header),
                             (Text, (20, 67), TEXTS["Diablotin"], 7),
                             wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Vampire": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "VAMPIRE", 1),
                           (Text, (57, 40), "VAMPIRE", 7),
                           (Iframe, MONSTER_IMG["Vampire"](30, 40), 1, self.open_header),
                           (Text, (20, 67), TEXTS["Vampire"], 7),
                           wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "BlobFeu": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "BLOB FEU", 1),
                           (Text, (57, 40), "BLOB FEU", 7),
                           (Iframe, MONSTER_IMG["BlobFeu"](30, 40), 1, self.open_header),
                           (Text, (20, 67), TEXTS["BlobFeu"], 7),
                           wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "BlobEau": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "BLOB EAU", 1),
                           (Text, (57, 40), "BLOB EAU", 7),
                           (Iframe, MONSTER_IMG["BlobEau"](30, 40), 1, self.open_header),
                           (Text, (20, 67), TEXTS["BlobEau"], 7),
                           wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Aligator": Box((0, 0),
                            (Bloc, (0, 0), (288, 25), 10),
                            (Text, (115, 10), "ALIGATOR", 1),
                            (Text, (57, 40), "ALIGATOR", 7),
                            (Iframe, MONSTER_IMG["Aligator"](30, 40), 1, self.open_header),
                            (Text, (20, 67), TEXTS["Aligator"], 7),
                            wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Mommies": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "MOMMIES", 1),
                           (Text, (57, 40), "MOMMIES", 7),
                           (Iframe, MONSTER_IMG["Mommies"](30, 40), 1, self.open_header),
                           (Text, (20, 67), TEXTS["Mommies"], 7),
                           wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Loup": Box((0, 0),
                        (Bloc, (0, 0), (288, 25), 10),
                        (Text, (115, 10), "LOUP", 1),
                        (Text, (57, 40), "LOUP", 7),
                        (Iframe, MONSTER_IMG["Loup"](30, 40), 1, self.open_header),
                        (Text, (20, 67), TEXTS["Ghost"], 7),
                        wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Fox": Box((0, 0),
                       (Bloc, (0, 0), (288, 25), 10),
                       (Text, (115, 10), "RENARD", 1),
                       (Text, (57, 40), "RENARD", 7),
                       (Iframe, MONSTER_IMG["Fox"](30, 40), 1, self.open_header),
                       (Text, (20, 67), TEXTS["Fox"], 7),
                       wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Necromancien": Box((0, 0),
                                (Bloc, (0, 0), (288, 25), 10),
                                (Text, (115, 10), "NECROMANCIEN", 1),
                                (Text, (57, 40), "NECROMANCIEN", 7),
                                (Iframe, MONSTER_IMG["Necromancien"](30, 40), 1, self.open_header),
                                (Text, (20, 67), TEXTS["Necromancien"], 7),
                                wh=(WIN_W, WIN_H), bg=0, root=self,
                                but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Witch": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "WITCH", 1),
                         (Text, (57, 40), "WITCH", 7),
                         (Iframe, MONSTER_IMG["Witch"](30, 40), 1, self.open_header),
                         (Text, (20, 67), TEXTS["Witch"], 7),
                         wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "DragonFeu": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "DRAGON FEU", 1),
                             (Text, (57, 40), "DRAGON FEU", 7),
                             (Iframe, MONSTER_IMG["DragonFeu"](30, 40), 1, self.open_header),
                             (Text, (20, 67), TEXTS["DragonFeu"], 7),
                             wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Abomination": Box((0, 0),
                               (Bloc, (0, 0), (288, 25), 10),
                               (Text, (115, 10), "ABOMINATION", 1),
                               (Text, (57, 40), "ABOMINATION", 7),
                               (Iframe, MONSTER_IMG["Abomination"](30, 40), 1, self.open_header),
                               (Text, (20, 67), TEXTS["Abomination"], 7),
                               wh=(WIN_W, WIN_H), bg=0, root=self,
                               but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Snake": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "SNAKE", 1),
                         (Text, (57, 40), "SNAKE", 7),
                         (Iframe, MONSTER_IMG["Snake"](30, 40), 1, self.open_header),
                         (Text, (20, 67), TEXTS["Snake"], 7),
                         wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Creeper": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "CREEPER", 1),
                           (Text, (57, 40), "CREEPER", 7),
                           (Iframe, MONSTER_IMG["Creeper"](30, 40), 1, self.open_header),
                           (Text, (20, 67), TEXTS["Creeper"], 7),
                           wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Rampant": Box((0, 0),
                           (Bloc, (0, 0), (288, 25), 10),
                           (Text, (115, 10), "RAMPANT", 1),
                           (Text, (57, 40), "RAMPANT", 7),
                           (Iframe, MONSTER_IMG["Rampant"](30, 40), 1, self.open_header),
                           (Text, (20, 67), TEXTS["Rampant"], 7),
                           wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Notch": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "NOTCH", 1),
                         (Text, (57, 40), "NOTCH", 7),
                         (Iframe, MONSTER_IMG["Notch"](30, 40), 1, self.open_header),
                         (Text, (20, 67), TEXTS["Notch"], 7),
                         wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Angel": Box((0, 0),
                         (Bloc, (0, 0), (288, 25), 10),
                         (Text, (115, 10), "ANGEL", 1),
                         (Text, (57, 40), "ANGEL", 7),
                         (Iframe, MONSTER_IMG["Angel"](30, 40), 1, self.open_header),
                         (Text, (20, 67), TEXTS["Angel"], 7),
                         wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "Arcangel": Box((0, 0),
                            (Bloc, (0, 0), (288, 25), 10),
                            (Text, (115, 10), "ARCANGEL", 1),
                            (Text, (57, 40), "ARCANGEL", 7),
                            (Iframe, MONSTER_IMG["Arcangel"](30, 40), 1, self.open_header),
                            (Text, (20, 67), TEXTS["Arcangel"], 7),
                            wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "DragonLight": Box((0, 0),
                               (Bloc, (0, 0), (288, 25), 10),
                               (Text, (115, 10), "DRAGON LUMIERE", 1),
                               (Text, (57, 40), "DRAGON LUMIERE", 7),
                               (Iframe, MONSTER_IMG["DragonLight"](30, 40), 1, self.open_header),
                               (Text, (20, 67), TEXTS["DragonLight"], 7),
                               wh=(WIN_W, WIN_H), bg=0, root=self,
                               but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "BlobPlant": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "BLOB PLANTE", 1),
                             (Text, (57, 40), "BLOB PLANTE", 7),
                             (Iframe, MONSTER_IMG["BlobPlant"](30, 40), 1, self.open_header),
                             (Text, (20, 67), TEXTS["BlobPlant"], 7),
                             wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "DragonDark": Box((0, 0),
                              (Bloc, (0, 0), (288, 25), 10),
                              (Text, (115, 10), "DRAGON TENEBRE", 1),
                              (Text, (57, 40), "DRAGON TENEBRE", 7),
                              (Iframe, MONSTER_IMG["DragonDark"](30, 40), 1, self.open_header),
                              (Text, (20, 67), TEXTS["DragonDark"], 7),
                              wh=(WIN_W, WIN_H), bg=0, root=self,
                              but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "DragonEau": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "DRAGON EAU", 1),
                             (Text, (57, 40), "DRAGON EAU", 7),
                             (Iframe, MONSTER_IMG["DragonEau"](30, 40), 1, self.open_header),
                             (Text, (20, 67), TEXTS["DragonEau"], 7),
                             wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "DragonPlant": Box((0, 0),
                               (Bloc, (0, 0), (288, 25), 10),
                               (Text, (115, 10), "DRAGON PLANTE", 1),
                               (Text, (57, 40), "DRAGON PLANTE", 7),
                               (Iframe, MONSTER_IMG["DragonPlant"](30, 40), 1, self.open_header),
                               (Text, (20, 67), TEXTS["DragonPlant"], 7),
                               wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "BlobLight": Box((0, 0),
                             (Bloc, (0, 0), (288, 25), 10),
                             (Text, (115, 10), "BLOB LUMIERE", 1),
                             (Text, (57, 40), "BLOB LUMIERE", 7),
                             (Iframe, MONSTER_IMG["BlobLight"](30, 40), 1, self.open_header),
                             (Text, (20, 67), TEXTS["BlobLight"], 7),
                             wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
            "BlobDark": Box((0, 0),
                            (Bloc, (0, 0), (288, 25), 10),
                            (Text, (115, 10), "BLOB TENEBRE", 1),
                            (Text, (57, 40), "BLOB TENEBRE", 7),
                            (Iframe, MONSTER_IMG["BlobDark"](30, 40), 1, self.open_header),
                            (Text, (20, 67), TEXTS["BlobDark"], 7),
                            wh=(WIN_W, WIN_H), bg=0, root=self, but_exit=((0, WIN_H - 20), (WIN_W, 20), "QUIT", 7, 8)),
        }
        self.menu = None
        self.open_start()

    def restart(self):
        """Reset le jeu"""
        self.menu = self.all_menus["START"]

    def start(self):
        """Relance/Lance le jeu"""
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
        self.is_loose = False

    def loose(self):
        """ Lose menu """
        self.menu = Box((0, 0),
                        (Canevas, DEAFEAT_FIRST_PART(WIN_W//2-32, WIN_H//2), DEAFEAT_SECOND_PART(WIN_W//2, WIN_H//2)),
                        (ScoreText, (WIN_W//2-32, WIN_H//2+25), self.score, 0),
                        wh=(WIN_W, WIN_H), bg=8, root=self, but_exit=((0, WIN_H-22), (WIN_W, 22), "RESTART !", 0, 7, self.restart))
        self.is_loose = True

    # LES FONCTIONS SUIVANTES SONT REDONDANTES CAR UTILISEES DANS LES MENUS (DONC SANS ARGUMENT)
    def open_start(self):
        self.menu = self.all_menus["START"]

    def open_tab(self):
        self.menu = self.all_menus["TAB"]

    def open_stats(self):
        self.all_menus["STATS"].element[2].actu()
        self.menu = self.all_menus["STATS"]

    def open_header(self):
        self.menu = self.bestiaire["HEADER"]

    def open_histoire(self):
        self.menu = self.all_menus["STORY"]

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
        self.menu = self.bestiaire["DragonFeu"]

    def open_DragonLight(self):
        self.menu = self.bestiaire["DragonLight"]

    def open_DragonDark(self):
        self.menu = self.bestiaire["DragonDark"]

    def open_DragonEau(self):
        self.menu = self.bestiaire["DragonEau"]

    def open_DragonPlant(self):
        self.menu = self.bestiaire["DragonPlant"]

    def open_BlobPlant(self):
        self.menu = self.bestiaire["BlobPlant"]

    def open_BlobLight(self):
        self.menu = self.bestiaire["BlobLight"]

    def open_BlobDark(self):
        self.menu = self.bestiaire["BlobDark"]

    def open_Snake(self):
        self.menu = self.bestiaire["Snake"]

    def open_Creeper(self):
        self.menu = self.bestiaire["Creeper"]

    def open_Rampant(self):
        self.menu = self.bestiaire["Rampant"]

    def open_Notch(self):
        self.menu = self.bestiaire["Notch"]

    def open_Angel(self):
        self.menu = self.bestiaire["Angel"]

    def open_Arcangel(self):
        self.menu = self.bestiaire["Arcangel"]

    def check_full_tile(self, x: int, y: int) -> bool:
        """
        Vérifie si la case est remplie par une entité
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
        """
        Methode appelée à chaque actualisation de l'écran : fait toutes les opérations et gère les inputs
        """
        self.carte.actualisation()

        if py.btnp(py.KEY_F1):
            """full screen the game"""
            if py.is_fullscreen:
                py.fullscreen(False)
            else:
                py.fullscreen(True)

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
                    if loot.x == self.player.x and loot.y == self.player.y and (self.looting or (not loot.forced[0] and loot.type == "Life") or loot.forced[0] and loot.type == "Life"):
                        loot.get_loot(self.player)
            if py.btnp(py.KEY_Q, hold=20):
                """aller à gauche"""
                for e in self.ennemi:
                    e.action()
                self.player.left()
                self.player.weapon.update()
            if py.btnp(py.KEY_D, hold=20):
                """aller à droite"""
                for e in self.ennemi:
                    e.action()
                self.player.right()
                self.player.weapon.update()
            if py.btnp(py.KEY_Z, hold=20):
                """aller à haut"""
                for e in self.ennemi:
                    e.action()
                self.player.top()
                self.player.weapon.update()
            if py.btnp(py.KEY_S, hold=20):
                """aller à bas"""
                for e in self.ennemi:
                    e.action()
                self.player.bottom()
                self.player.weapon.update()

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

            if py.btnp(py.KEY_W, hold=1):
                """skip on looting zone"""
                if self.carte.etage_completed:
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
            if py.btnp(py.KEY_TAB, hold=60) and not self.is_loose:
                """changer d'arme"""
                self.menu = None
                self.is_loose = False

    def draw(self) -> None:
        """
        Méthode appelée à chaque actualisation de l'écran : dessine toutes les images à l'écran
        """
        py.cls(0)
        self.carte.blit()
        for loot in self.loots:
            if self.looting or (not loot.forced[0] and loot.type == "Sante"):
                loot.blit()
        for e in self.ennemi:
            e.blit_entity()
            e.range_blit()
            e.blit_life_bar()
        self.player.blit_entity()
        self.player.weapon.blit_range()
        self.player.blit_life_bar()
        py.text(WIN_W-30, 0, "Armure :", 7)
        self.player.armor.blit(decalY=8)
        py.rect(WIN_W-32, 60, 32, 2, 7)
        py.text(WIN_W-30, 65, "Arme 1 \n(en main) :", 7)
        self.player.weapon.blit(decalY=79)
        py.text(WIN_W-30, 115, "Arme 2 \n(sac) :", 7)
        self.player.secondary_weapon.blit(decalY=130)
        py.rect(WIN_W-32, 165, 32, 2, 7)
        py.text(WIN_W-32, 168, "Au sol :", 7)
        for loot in self.loots:
            if loot.x == self.player.x and loot.y == self.player.y \
                    and (self.looting or (not loot.forced[0] and loot.type == "Sante")):
                loot.blit_inv()
        py.rect(WIN_W-32, 215, 32, 2, 7)
        temp = f"Score :\n{self.score} pts"
        chaine = ""
        for i in range(len(temp)):
            if i == 37:
                chaine += "..."
                break
            chaine += temp[i]
            if i % 8 == 7:
                chaine += "\n"
        py.text(WIN_W-31, 220, chaine, 7)
        for anime in self.animation_layer:
            py.blt(anime[0], anime[1], anime[2], anime[3], anime[4], anime[5], anime[6], anime[7])
        self.animation_layer.clear()
        self.menu.blit() if self.menu is not None else None

    def run(self) -> None:
        """
        Lance le jeu et ouvre la fenêtre de jeux
        """
        py.run(self.update, self.draw)


g = Game()
g.run()
