import pyxel as py
from Settings import BOUTON_ADD, BOUTON_SUB, HEALTH_ICO, DAMAGE_ICO


"""
permet des créer des menus de la menière suivante :
la racine doit être un Box qui contient des sous instance.
ces sous instances peuvent être formé entre eux d'autre sous instances

puis si on veut l'afficher il suffit d'afficher la racine, qui va afficher les 
sous instances, qui vont eux aussi afficher leurs dépendances etc...

De même pour les actualisations.

aussi, il est possible de modifier un menu si on connais l'indice d'une sous instance.
"""


class Box:
    """class principale des menu, capable de contenir d'autres sous classe"""
    def __init__(self, xy, *elem, wh=None, bg=None, root=None, but_exit=None):
        """
        :param xy: tuple(int, int) coordonnée de l'angle haut gauche de manière absolue
        :param elem: instanceof(Box) sous classe de Box qui sont des sous partie du menu
        :param wh: tuple(int, int) taille de l'interface (fond)
        :param bg: couleur du fond
        :param root: Game ou istanceof(Box), incusion dans cette racine
        :param but_exit: ((x, y), (w, h), str, col_fond, col_text, func)) définition d'un bouton pour quitter par défaut mais peut être une autre fonction si func est défini
        """
        self.root = root
        self.x, self.y = xy
        self.w, self.h = wh if wh is not None else (-1, -1)
        self.bgc = bg
        self.element = []
        for e in elem:
            type = e[0]
            args = [e[i] for i in range(1, len(e))]
            args.insert(0, self)
            self.element.append(type(*args))
        try:
            func = but_exit[5]
        except (IndexError, TypeError):
            func = None
        self.exit = Button(self, but_exit[0], but_exit[1], but_exit[2], but_exit[3], but_exit[4], func) if but_exit is not None else None

    def blit(self):
        """affiche lui même (le fond)  et toute les sous instance par récurrence + met a jout le bouton et l'affiche"""
        if self.bgc is not None:
            py.rect(self.x, self.y, self.w, self.h, self.bgc)
        for e in self.element:
            e.blit()
        if self.exit is not None:
            self.exit.update()
            self.exit.blit()

    def close(self):
        """ferme le menu si il est hérité directement de game sinon supprime tout les sous instances"""
        if issubclass(type(self.root), Box):
            self.element.clear()
        else:
            self.root.menu = None

    def update(self):
        """met a jour toute les sous instance (récurrence)"""
        for e in self.element:
            e.update()


class Bloc:
    """juste un rectangle a dessiner"""
    def __init__(self, root, xy, wh, c):
        self.root = root
        self.x, self.y = xy
        self.w, self.h = wh
        self.c = c

    def blit(self):
        py.rect(self.x, self.y, self.w, self.h, self.c)

    def update(self):
        pass


class Canevas:
    """image du jeux"""
    def __init__(self, root,  *imgs):
        """
        :param imgs: tuple(x, y, Tilemap, u, v, w, h, col_key) définissant une image déjà positionnée
        """
        self.root = root
        self.imgs = list(imgs)

    def blit(self):
        for im in self.imgs:
            py.blt(im[0], im[1], im[2], im[3], im[4], im[5], im[6], im[7])

    def update(self):
        pass


class Button(Box):
    """bouton : bloc avec un text qui active une fontion quand il est cliqué (les fonctions doivent impérativement ne pas avoir d'arguments)"""
    def __init__(self, root, xy, wh, text, bcol, col, cmd):
        format_text = ""
        size = [0, 0]
        for char in text:
            size[0] += 1
            format_text += char
            if size[0]*4 >= wh[0]-8:
                size[0] = 0
                size[1] += 1
                format_text += "\n"
        size[0] *= 4
        if size[1] > 1:
            size[0] = wh[0]
        size[1] *= 8
        x_text, y_text = xy[0] + (wh[0]-size[0])/2, xy[1] + (wh[1]-size[1])/2 - 2
        super().__init__(xy, (Text, (x_text, y_text), format_text, col), wh=wh, bg=bcol, root=root)
        self.cmd = cmd
        self.cooldown = 15  # permet de ne pas activer un bouton qui renvoi à ce menu si et qui repart et ainsi de suite a l'infini ce qui peit causer de l'inconfort chez l'utilisateur

    def blit(self):
        super().blit()

    def update(self):
        """actualisation de la fonction si le bouton est cliqué et que le cooldown est écoulé, sinon descendre le cooldown"""
        if self.x <= py.mouse_x <= self.x+self.w and self.y <= py.mouse_y <= self.y + self.h and py.btn(py.MOUSE_BUTTON_LEFT) and self.cooldown <= 0:
            if self.cmd is None:
                self.root.close()
            else:
                self.cmd()
            self.cooldown = 15
        elif self.cooldown > 0:
            self.cooldown -= 1


class Iframe(Box):
    """mélange du canevas et du bouton, permet de faire une image qui active une fonction quand il est cliqué"""
    def __init__(self, root, img, bcol, cmd):
        super().__init__((img[0], img[1]), (Canevas, img), wh=(img[5], img[6]), bg=bcol, root=root)
        self.cmd = cmd
        self.cooldown = 15

    def blit(self):
        super().blit()

    def update(self):
        if self.x <= py.mouse_x <= self.x + self.w and self.y <= py.mouse_y <= self.y + self.h and py.btn(
                py.MOUSE_BUTTON_LEFT) and self.cooldown <= 0:
            if self.cmd is None:
                self.root.close()
            else:
                self.cmd()
            self.cooldown = 15
        elif self.cooldown > 0:
            self.cooldown -= 1


class Text:
    """simple affichage de texte"""
    def __init__(self, root, xy, txt, col):
        self.root = root
        self.text = txt
        self.x, self.y = xy
        self.col = col

    def set_text(self, txt):
        """chage le texte pour autre chose"""
        self.text = str(txt)

    def blit(self):
        py.text(self.x, self.y, self.text, self.col)

    def update(self):
        pass


class ScoreText(Text):
    """outils spécifique au menu de Game over"""
    def __init__(self, root, xy, score, col):
        super().__init__(root, xy, f"Votre score est de : {score}", col)


class StatsEnnemi(Box):
    """outil spécifique pour les stats d'un ennemi en particulier"""
    def __init__(self, root, xy, w, max, maxhp, attack, hp=None):
        super().__init__(xy,
                         (Text, xy, f'Point de vie ({maxhp}) : ', 7),
                         (Canevas, HEALTH_ICO(xy[0], xy[1]+10)),
                         (Bloc, (xy[0]+20, xy[1]+10), (w * maxhp/max, 8), 8),
                         (Bloc, (xy[0]+20, xy[1]+10), (w * hp/max, 8), 11) if hp is not None else (Bloc, (0, 0), (0, 0), 0),
                         (Text, (xy[0], xy[1] + 40), f"Attaque ({attack}) :", 7),
                         (Canevas, DAMAGE_ICO(xy[0], xy[1]+50)),
                         (Bloc, (xy[0]+20, xy[1]+50), (w * attack/max, 8), 9),
                         wh=(w, 50), root=root
                         )

    def set_attack(self, attack):
        """redéfini la stats d'attack affichée"""
        self.element[3].set_text(f"Attaque lv1 ({attack}) :")
        self.element[5].w = self.w * attack/120

    def set_hp(self, hp):
        """redéfini la stats de maxhp affichée"""
        self.element[0].set_text(f"Attaque lv1 ({hp}) :")
        self.element[2].w = self.w * hp/120


class StatText(Box):
    """outil spécifique pour l'inglet Niveau des menus"""
    def __init__(self, root, xy, col, player):
        self.p = player
        super().__init__(xy,
                         (Text, xy, f"[ STATS ] | POINTS : {self.p.stats['points']}", col),
                         (Text, (xy[0], xy[1]+13), "Sante : ", col),
                         (Iframe, BOUTON_SUB(xy[0] + 32, xy[1] + 9), None, self.sub_to_sante),
                         (Text, (xy[0] + 50, xy[1]+13), str(self.p.stats["sante"]), col),
                         (Iframe, BOUTON_ADD(xy[0] + 70, xy[1] + 9), None, self.add_to_sante),
                         (Text, (xy[0], xy[1] + 29), "Attaque : ", col),
                         (Iframe, BOUTON_SUB(xy[0] + 32, xy[1] + 26), None, self.sub_to_attaque),
                         (Text, (xy[0] + 50, xy[1] + 30), str(self.p.stats["attaque"]), col),
                         (Iframe, BOUTON_ADD(xy[0] + 70, xy[1] + 26), None, self.add_to_attaque),
                         wh=(0, 0), bg=0, root=root
                         )

    def actu(self):
        """met à jour la fenêtre avec les nouveaux textes"""
        self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")
        self.element[3].set_text(self.p.stats["sante"])
        self.element[7].set_text(self.p.stats["attaque"])

    def add_to_sante(self):
        """
        ajouter des pv max sans toucher aux pv de base et met à jout
        """
        if self.p.stats["points"] > 0:
            self.p.stats["points"] -= 1
            self.p.stats["sante"] += 1
            self.p.maxhp = 100 + self.p.stats["sante"] * 5
            self.element[3].set_text(self.p.stats["sante"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

    def sub_to_sante(self):
        """
        enleve de la sante et modifie toute les implication si les pv sont superieur aux
        pv maximum (mettre les pv à pv max) et met à jout
        """
        if self.p.stats["sante"] > 0:
            self.p.stats["points"] += 1
            self.p.stats["sante"] -= 1
            self.p.maxhp = 100 + self.p.stats["sante"] * 5
            if self.p.maxhp < self.p.hp:
                self.p.hp = self.p.maxhp
            self.element[3].set_text(self.p.stats["sante"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

    def add_to_attaque(self):
        """ajoute 1 point d'attaque et met à jout"""
        if self.p.stats["points"] > 0:
            self.p.stats["points"] -= 1
            self.p.stats["attaque"] += 1
            self.element[7].set_text(self.p.stats["attaque"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

    def sub_to_attaque(self):
        """enlève 1 point d'attaque et met à jout"""
        if self.p.stats["attaque"] > 0:
            self.p.stats["points"] += 1
            self.p.stats["attaque"] -= 1
            self.element[7].set_text(self.p.stats["attaque"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")
