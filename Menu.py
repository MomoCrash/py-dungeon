import pyxel as py


class Box:
    def __init__(self, xy, *elem, wh=None, bg=None, root=None, f=None):
        self.root = root
        self.x, self.y = xy
        self.w, self.h = wh if wh is not None else (-1, -1)
        self.bgc = bg
        self.element = []
        for e in elem:
            if issubclass(e[0], Text):
                self.element.append(e[0](self, e[1], e[2], e[3]))
            if e[0] == Button:
                self.element.append(Button(self, e[1], e[2], e[3], e[4], e[5], e[6]))
            if e[0] == Bloc:
                self.element.append(Bloc(e[1], e[2], e[3]))
            if e[0] == Canevas:
                self.element.append(Canevas(*[e[i] for i in range(1, len(e))]))
        self.f = Button(self, f[0], f[1], f[2], f[3], f[4], f[5]) if f is not None else None

    def blit(self):
        if self.bgc is not None:
            py.rect(self.x, self.y, self.w, self.h, self.bgc)
        for e in self.element:
            e.blit()
        if self.f is not None:
            self.f.update()
            self.f.blit()

    def close(self):
        if issubclass(type(self.root), Box):
            self.element.clear()
        else:
            self.root.menu = None


class Bloc:
    def __init__(self, xy, wh, c):
        self.x, self.y = xy
        self.w, self.h = wh
        self.c = c

    def blit(self):
        py.rect(self.x, self.y, self.w, self.h, self.c)


class Canevas:
    def __init__(self, *imgs):
        self.imgs = list(imgs)

    def blit(self):
        for im in self.imgs:
            py.blt(im[0], im[1], im[2], im[3], im[4], im[5], im[6], im[7])


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

    def blit(self):
        super().blit()

    def update(self):
        if self.x <= py.mouse_x <= self.x+self.w and self.y <= py.mouse_y <= self.y + self.h and py.btn(py.MOUSE_BUTTON_LEFT):
            if self.cmd is None:
                self.root.close()
            else:
                self.cmd()


class Text:
    def __init__(self, root, xy, txt, col):
        self.root = root
        self.text = txt
        self.x, self.y = xy
        self.col = col

    def set_text(self, txt):
        self.text = txt

    def blit(self):
        py.text(self.x, self.y, self.text, self.col)


class ScoreText(Text):
    def __init__(self, root, xy, score, col):
        super().__init__(root, xy, f"Votre score est de : {score}", col)



