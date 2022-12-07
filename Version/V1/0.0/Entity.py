import pyxel as py


class Entity:
    def __init__(self, game, x, y, img, size, hp, colkey=0):
        self.hp = hp
        self.x = x
        self.y = y
        self.imgX = img
        self.imgY = (img[0]+16, img[1])
        self.img = self.imgX
        self.size = size
        self.game = game
        self.colkey = colkey

    def watch_left(self):
        self.size = (abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX

    def left(self):
        if self.x > 0 and "obst" not in self.game.grille[self.x-1][self.y].types:
            self.x -= 1
        self.watch_left()

    def watch_right(self):
        self.size = (-abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgX

    def right(self):
        if self.x < len(self.game.grille)-1 and "obst" not in self.game.grille[self.x+1][self.y].types:
            self.x += 1
        self.watch_right()

    def watch_top(self):
        self.size = (abs(self.size[0]), abs(self.size[1]))
        self.img = self.imgY

    def top(self):
        if self.y > 0 and "obst" not in self.game.grille[self.x][self.y-1].types:
            self.y -= 1
        self.watch_top()

    def watch_bottom(self):
        self.size = (abs(self.size[0]), -abs(self.size[1]))
        self.img = self.imgY

    def bottom(self):
        if self.y < len(self.game.grille[0])-1 and "obst" not in self.game.grille[self.x][self.y+1].types:
            self.y += 1
        self.watch_bottom()