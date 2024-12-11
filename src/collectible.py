class Collectible:
    def __init__(self, t, x, y, w, h):
        self.type = t
        self.pngName = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.retrieved = True

        self.pngName = t + "_collectible.png"

