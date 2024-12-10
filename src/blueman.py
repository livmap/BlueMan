class BlueMan:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.velocity = 5
        self.velocityY = 0
        self.jumpVelocity = 15
        self.lives = 5