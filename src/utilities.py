import pygame

def loadImage(name, w=None, h=None):
    base_path = "/Users/princemaphupha/Desktop/Games/BlueMan/assets/"
    img = pygame.image.load(base_path + name)

    if w != None and h != None:
        img = pygame.transform.scale(img, (w, h))