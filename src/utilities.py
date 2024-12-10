import pygame
import math

def loadImage(name, w=None, h=None):
    base_path = "/Users/princemaphupha/Desktop/Games/BlueMan/assets/"
    img = pygame.image.load(base_path + name)

    if w != None and h != None:
        img = pygame.transform.scale(img, (w, h))

    return img

def distance(x1, y1, w1, h1, x2, y2, w2, h2):

    dist = 0

    cx1 = x1 + (w1 / 2)
    cx2 = x2 + (w2 / 2)
    cy1 = y1 + (h1 / 2)
    cy2 = y2 + (h2 / 2)

    dist = math.sqrt(math.pow(cx2 - cx1, 2) + math.pow(cy2 - cy1, 2))

    return dist

def is_collision(obj1, obj2, d):
    dist = distance(obj1.x, obj1.y, obj1.w, obj1.h, obj2.x, obj2.y, obj2.w, obj2.h)

    return dist < d

