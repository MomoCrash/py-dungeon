import pyxel as py

_equivalance = {
    "obst": [
        (0, 2), (0, 3), (1, 2), (1, 3),
        (2, 2), (2, 3), (3, 2), (3, 3)
    ],
}


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tiles = []
        for i in range(2):
            self.tiles.append([])
            for j in range(2):
                self.tiles[i].append(py.tilemap(0).pget((self.x+i*8)/8, (self.y+j*8)/8))
        self.types = []
        for k in _equivalance.keys():
            for i in self.tiles:
                for j in i:
                    if j in _equivalance[k] and k not in self.types:
                        self.types.append("obst")
