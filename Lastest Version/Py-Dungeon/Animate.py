import pyxel as py


class Animation:
    def __init__(self, game, type, origine):
        """
        :param game: accès à la classe de jeu
        :param type: quel type d'animation ? (attaque, déplacement, ...)
        :param origine: acteur de l'animation (si il y en a un)
        """
        self.game = game
        self.type = type
        self.origine = origine

    def animate(self):
        """une occurence de l'animation"""
        pass

    def delete(self) -> None:
        """fini sa propre animation"""
        self.game.animation_list.remove(self)


class Move(Animation):
    def __init__(self, game, origine, sens: int, distance: int = 16, frame: int = 5):
        super().__init__(game, "Move", origine)
        self.baseXY = origine.reel_x, origine.reel_y
        self.sens = sens
        self.frame = frame
        self.distance = distance / self.frame

    def animate(self):
        self.frame -= 1
        if self.sens == 0:
            self.origine.reel_x -= self.distance
        if self.sens == 1:
            self.origine.reel_x += self.distance
        if self.sens == 2:
            self.origine.reel_y -= self.distance
        if self.sens == 3:
            self.origine.reel_y += self.distance
        if self.frame <= 0:
            self.delete()


class AttaquePlayer(Animation):
    def __init__(self, game, origine):
        super().__init__(game, "Attaque", origine)
        self.frame = 4
        self.tiles_coors = origine.get_coor_in_range()

    def animate(self):
        self.frame -= 1
        for coor in self.tiles_coors:
            self.game.animation_layer.append((coor[0], coor[1], 0, 32+(4-self.frame)*16, 32, 16, 16, 0))
        if self.frame <= 0:
            self.origine.attaque()
            self.delete()


class AttaqueEnnemi(Animation):
    def __init__(self, game, origine):
        super().__init__(game, "Attaque", origine)
        self.frame = 4
        self.tiles_coors = origine.get_coor_in_range()

    def animate(self):
        self.frame -= 1
        for coor in self.tiles_coors:
            self.game.animation_layer.append((coor[0], coor[1], 0, 32 + (4 - self.frame) * 16, 32, 16, 16, 0))
        if self.frame <= 0:
            self.origine.attaque()
            self.delete()
