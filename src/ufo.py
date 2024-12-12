class Ufo:
    def __init__(self, x, y, w, h):
        self.pngName = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.activated = False
        self.pngName = "ufo.png"
        self.velocity = 5
        self.startDistance = None
        self.distanceInterval = 200

    def Operate(self, obj1, dist):

        if self.x > obj1.x - obj1.w and dist < (self.startDistance + self.distanceInterval):
            self.x -= self.velocity
        
        
        



