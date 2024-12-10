import pygame

from utilities import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

GOBLUE = (0, 100, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlueMan")

pygame.joystick.init()

xAxis = None
yAxis = None

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    xAxis = 0
    yAxis = 0


clock = pygame.time.Clock()
FPS = 60

# -----------------------------------------------------------------------------------------------------------------

Obstacle = loadImage("obstacle.png", 50, 50)
Runner1 = loadImage("runner1.png", 40, 40)
Runner2 = loadImage("runner2.png", 40, 40)
Runner3 = loadImage("runner3.png", 40, 40)

# -----------------------------------------------------------------------------------------------------------------

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, GOBLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    if joystick:
   
        xAxis = joystick.get_axis(0)  
        yAxis = joystick.get_axis(1)

    pygame.display.flip()
     
    clock.tick(FPS)

pygame.quit()