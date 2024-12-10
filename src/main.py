import pygame
import random

from utilities import *
from blueman import *
from ground import * 
from snowman import *
from snowball import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

BLACK = (0, 0, 0)
GOBLUE = (0, 100, 200)

GRAVITY = 0.6

A_BUTTON_INDEX = 0

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

# Ground
groundWidth = 300
groundHeight = 151 *  (groundWidth / 1000)
groundLevel = SCREEN_HEIGHT - groundHeight
ground = Ground(0, groundLevel + 1, groundWidth, groundHeight, groundLevel)

groundObjects = []
widthStopper = 0
count = 0

while widthStopper < SCREEN_WIDTH + (SCREEN_WIDTH  * 2):
    
    groundItem = Ground(count * groundWidth, groundLevel + 1, groundWidth, groundHeight, groundLevel)
    groundObjects.append(groundItem)
    widthStopper += groundWidth
    count += 1

# Blueman
blueman = BlueMan(100, 0, 75, 75)
bluemanBuffer = 10
initVelocity = 10
blueman.y = groundLevel - blueman.h  + (bluemanBuffer)
blueman.velocity = initVelocity
bluemanImages = []

for x in range(3):
    bluemanImages.append(loadImage("runner" + str(x + 1) + ".png", blueman.w, blueman.h))


# Snowman

snowmanObjects = []
buffer = 15
snowman = Snowman(1200, 0, 100, 100)
snowman.y = groundLevel - snowman.h + (buffer)
snowman2 = Snowman(2000, 0, 100, 100)
snowman2.y = groundLevel - snowman2.h + (buffer)

snowmanObjects.append(snowman)
snowmanObjects.append(snowman2)

# Snowball
snowballImages = []
snowball = SnowBall(2 * SCREEN_WIDTH, 0, 100, 100)
snowballBuffer = 10
snowball.y = groundLevel - snowball.h + (snowballBuffer)

for x in range(4):
    snowballImages.append(loadImage("snowball" + str(x + 1) + ".png", snowball.w, snowball.h))

# -----------------------------------------------------------------------------------------------------------------

GroundImg = loadImage("ground.png", ground.w, ground.h)
SnowmanImg = loadImage("snowman.png", snowman.w, snowman.h)
HeartImg = loadImage("heart.png", 20, 20)


# -----------------------------------------------------------------------------------------------------------------

pygame.font.init()
font = pygame.font.Font(None, 24)
text = font.render("DISTANCE: 0", True, BLACK)
text2 = None

# -----------------------------------------------------------------------------------------------------------------

running = True
runCount = 0
jump = False
distance = 0
collidedWithSnowClose = False
snowCloseCopy = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, GOBLUE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    if joystick:

        if event.type == pygame.JOYBUTTONDOWN and event.button == A_BUTTON_INDEX:
  
            if blueman.velocityY == 0:
                jump = True
                blueman.velocityY = -blueman.jumpVelocity 
                    
    if (blueman.y <= groundLevel - blueman.h + (bluemanBuffer)) and jump:
        blueman.velocityY += GRAVITY

    else:
        jump = False
        blueman.y = groundLevel - blueman.h + (bluemanBuffer)
        blueman.velocityY = 0

    blueInteger = int(runCount / 50) % 3
    snowballInteger = int(runCount / 100) % 4

    if not jump:
        screen.blit(bluemanImages[blueInteger], (blueman.x, blueman.y))
    else:
        screen.blit(bluemanImages[1], (blueman.x, blueman.y))

    if distance > 200:
        screen.blit(snowballImages[snowballInteger], (snowball.x, snowball.y))
        snowball.x -= snowball.velocity
        if snowball.x <  -100:
            snowball.x = random.randint(SCREEN_WIDTH * 1.5, SCREEN_WIDTH * 3)


    for x in snowmanObjects:
        if x.x < SCREEN_WIDTH and x.x > -x.w:
            screen.blit(SnowmanImg, (x.x, x.y))
        
        if x.x < -x.w - 10:
            x.x = random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 600)

    snowClose = None
    minimum = 100000000
    for x in snowmanObjects:
        if x.x > blueman.x and x.x < minimum:
            snowClose = x
            if snowClose != snowCloseCopy:
                collidedWithSnowClose == False
            minimum = x.x - blueman.x

    
    if snowClose != None:
        if is_collision(blueman, snowClose, 50):
            text2 = font.render("COLLIDED", True, BLACK)

            
            if not collidedWithSnowClose:
                collidedWithSnowClose = True
                snowCloseCopy = snowClose
                if blueman.lives > 0:
                    blueman.lives -= 1
        else:
            text2 = None


    for x in groundObjects:
        screen.blit(GroundImg, (x.x, x.y))

    if jump:
        blueman.y += blueman.velocityY

    if blueman.x < 330:
        blueman.x += blueman.velocity
    else:
        for x in groundObjects:
            x.x -= blueman.velocity

        for x in snowmanObjects:
            x.x -= blueman.velocity

    if groundObjects[0].x < -groundWidth - 50:
        del groundObjects[0]
        endIndex = len(groundObjects) - 1
        item = Ground(groundObjects[endIndex].x + groundWidth, groundLevel + 1, groundWidth, groundHeight, groundLevel)
        groundObjects.append(item)

    distance += count / 100
    blueman.velocity = initVelocity + int(distance / 100000)

    text = font.render("DISTANCE: " + str(int(distance)), True, BLACK)
    screen.blit(text, (10, 40))
    
    if text2 != None:
        screen.blit(text2, (10, 25))

    for x in range(blueman.lives):
        screen.blit(HeartImg, (10 + (25 * x), 10))

    pygame.display.flip()
     
    runCount += blueman.velocity
    clock.tick(FPS)

pygame.quit()