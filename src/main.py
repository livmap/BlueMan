import pygame

from utilities import *
from blueman import *
from ground import * 

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

groundWidth = 300
groundHeight = 151 *  (groundWidth / 1000)
groundLevel = SCREEN_HEIGHT - groundHeight
ground = Ground(0, groundLevel + 1, groundWidth, groundHeight, groundLevel)

groundObjects = []
widthStopper = 0
count = 0

while widthStopper < SCREEN_WIDTH + (SCREEN_WIDTH  * 0.2):
    
    groundItem = Ground(count * groundWidth, groundLevel + 1, groundWidth, groundHeight, groundLevel)
    groundObjects.append(groundItem)
    widthStopper += groundWidth
    count += 1

blueman = BlueMan(100, 0, 75, 75)

blueman.y = groundLevel - blueman.h  + (10)

# -----------------------------------------------------------------------------------------------------------------

GroundImg = loadImage("ground.png", ground.w, ground.h)
Obstacle = loadImage("obstacle.png", 50, 50)
Runner1 = loadImage("runner1.png", blueman.w, blueman.h)
Runner2 = loadImage("runner2.png", blueman.w, blueman.h)
Runner3 = loadImage("runner3.png", blueman.w, blueman.h)

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

    screen.blit(Runner1, (blueman.x, blueman.y))
    for x in groundObjects:

        screen.blit(GroundImg, (x.x, x.y))

    pygame.display.flip()
     
    clock.tick(FPS)

pygame.quit()