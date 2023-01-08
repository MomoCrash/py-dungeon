import pyxel as py
from Settings import BOUTON_ADD, BOUTON_SUB


class Box:
    def __init__(self, xy, *elem, wh=None, bg=None, root=None, exit=None):
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
            func = exit[5]
        except (IndexError, TypeError):
            func = None
        self.exit = Button(self, exit[0], exit[1], exit[2], exit[3], exit[4], func) if exit is not None else None

    def blit(self):
        if self.bgc is not None:
            py.rect(self.x, self.y, self.w, self.h, self.bgc)
        for e in self.element:
            e.blit()
        if self.exit is not None:
            self.exit.update()
            self.exit.blit()

    def close(self):
        if issubclass(type(self.root), Box):
            self.element.clear()
        else:
            self.root.menu = None

    def update(self):
        for e in self.element:
            e.update()


class Bloc:
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
    def __init__(self, root,  *imgs):
        self.root = root
        self.imgs = list(imgs)

    def blit(self):
        for im in self.imgs:
            py.blt(im[0], im[1], im[2], im[3], im[4], im[5], im[6], im[7])

    def update(self):
        pass


class Button(Box):
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
        x_text, y_text = xy[0] +  (wh[0]-size[0])/2, xy[1] + (wh[1]-size[1])/2 -2
        super().__init__(xy, (Text, (x_text, y_text), format_text, col), wh=wh, bg=bcol, root=root)
        self.cmd = cmd
        self.cooldown = 15

    def blit(self):
        super().blit()

    def update(self):
        if self.x <= py.mouse_x <= self.x+self.w and self.y <= py.mouse_y <= self.y + self.h and py.btn(py.MOUSE_BUTTON_LEFT) and self.cooldown <= 0:
            if self.cmd is None:
                self.root.close()
            else:
                self.cmd()
            self.cooldown = 15
        elif self.cooldown > 0:
            self.cooldown -= 1


class Iframe(Box):
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
    def __init__(self, root, xy, txt, col):
        self.root = root
        self.text = txt
        self.x, self.y = xy
        self.col = col

    def set_text(self, txt):
        self.text = str(txt)

    def blit(self):
        py.text(self.x, self.y, self.text, self.col)

    def update(self):
        pass


class ScoreText(Text):
    def __init__(self, root, xy, score, col):
        super().__init__(root, xy, f"Votre score est de : {score}", col)


class StatText(Box):
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

    def actu_points(self):
        self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

    def add_to_sante(self):
        if self.p.stats["points"] > 0:
            self.p.stats["points"] -= 1
            self.p.stats["sante"] += 1
            self.p.maxhp = 100 + self.p.stats["sante"] * 5
            self.element[3].set_text(self.p.stats["sante"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

    def sub_to_sante(self):
        if self.p.stats["sante"] > 0:
            self.p.stats["points"] += 1
            self.p.stats["sante"] -= 1
            self.p.maxhp = 100 + self.p.stats["sante"] * 5
            if self.p.maxhp < self.p.hp:
                self.p.hp = self.p.maxhp
            self.element[3].set_text(self.p.stats["sante"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

    def add_to_attaque(self):
        if self.p.stats["points"] > 0:
            self.p.stats["points"] -= 1
            self.p.stats["attaque"] += 1
            self.element[7].set_text(self.p.stats["attaque"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

    def sub_to_attaque(self):
        if self.p.stats["attaque"] > 0:
            self.p.stats["points"] += 1
            self.p.stats["attaque"] -= 1
            self.element[7].set_text(self.p.stats["attaque"])
            self.element[0].set_text(f"[ STATS ] | POINTS : {self.p.stats['points']}")

