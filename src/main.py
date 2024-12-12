import pygame
import random

from utilities import *
from world import *
from blueman import *
from ground import * 
from snowman import *
from snowball import *
from collectible import *
from device import *
from apple import *

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

BLACK = (0, 0, 0)
GOBLUE = (0, 100, 200)

GRAVITY = 0.6

A_BUTTON_INDEX = 0
X_BUTTON_INDEX = 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BlueMan")

pygame.joystick.init()

xAxis = None
yAxis = None

joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

clock = pygame.time.Clock()
FPS = 60

# -----------------------------------------------------------------------------------------------------------------

# World
world = World()

# Ground
groundWidth = 300
groundHeight = 151 *  (groundWidth / 1000)
groundLevel = SCREEN_HEIGHT - groundHeight
ground = Ground(0, groundLevel + 1, groundWidth, groundHeight, groundLevel)

groundObjects = []
widthStopper = 0
count = 0

while widthStopper < SCREEN_WIDTH * 2:
    
    groundItem = Ground(count * groundWidth, groundLevel + 1, groundWidth, groundHeight, groundLevel)
    groundObjects.append(groundItem)
    widthStopper += groundWidth

    count += 1

# Blueman
blueman = BlueMan(100, 0, 75, 75)
bluemanBuffer = 10
initVelocity = 7
blueman.y = groundLevel - blueman.h  + (bluemanBuffer)
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

# Apples

apple = Apple(SCREEN_WIDTH * 2, 0, 45, 45)
apple.y = groundLevel - apple.h

for x in range(4):
    snowballImages.append(loadImage("snowball" + str(x + 1) + ".png", snowball.w, snowball.h))

# Collectibles

collectibles = []
collectiblesCollected = []

# -----------------------------------------------------------------------------------------------------------------

Background = loadImage("background.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
GroundImg = loadImage("ground.png", ground.w, ground.h)
SnowmanImg = loadImage("snowman.png", snowman.w, snowman.h)
HeartImg = loadImage("heart.png", 20, 20)
AppleImg = loadImage("apple.png", apple.w, apple.h)

# -----------------------------------------------------------------------------------------------------------------

pygame.font.init()
font = pygame.font.Font(None, 24)
text = font.render("DISTANCE: 0", True, BLACK)
text2 = None

# -----------------------------------------------------------------------------------------------------------------

running = True
gameOver = False
runCount = 0
jump = False
retrieveCount = 0
nextCollectible = 50
deletedCollectible = None

#

UfoCount = 0
InvincibilityCount = 0
SuperJumpCount = 0
CannonCount = 0

ufoCollected = False
invincibilityCollected = False
superJumpCollected = False
cannonCollected = False

collidedWith = None
collideSnowball = False

while running:

    # Quitting Process ----------------------------------------------------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not gameOver:
        screen.blit(Background, (0, 0))


        # Collectibles Generation
        if world.distanceRan > nextCollectible:
            nextCollectible = world.distanceRan + random.randint(50, 350)
            randomCollect = random.randint(1, 4) 
            collect = Collectible("", SCREEN_WIDTH * random.randint(2, 5), groundLevel - 60, 50, 50)
            if randomCollect == 1:
                collect.type = "ufo"
                collect.pngName = collect.type + "_collectible.png"
                collectibles.append(collect)
            elif randomCollect == 2:
                collect.type = "invincibility"
                collect.pngName = collect.type + "_collectible.png"
                collectibles.append(collect)
            elif randomCollect == 3:
                collect.type = "superJump"
                collect.pngName = collect.type + "_collectible.png"
                collectibles.append(collect)
            else:
                collect.type = "cannon"
                collect.pngName = collect.type + "_collectible.png"
                collectibles.append(collect)

        # Velocity Up

        if blueman.velocity < initVelocity:
            blueman.velocity += 0.05

        # Joystick Functionality -----------------------------------------------------------------------------

        if joystick:

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == A_BUTTON_INDEX:
    
                    if blueman.velocityY == 0:
                        jump = True
                        blueman.velocityY = -blueman.jumpVelocity 
                
                elif event.button == X_BUTTON_INDEX:
                    pass

                        
        if (blueman.y <= groundLevel - blueman.h + (bluemanBuffer)) and jump:
            blueman.velocityY += GRAVITY

        else:
            jump = False
            blueman.y = groundLevel - blueman.h + (bluemanBuffer)
            blueman.velocityY = 0

        blueInteger = int(world.runCount / 50) % 3
        snowballInteger = int(world.runCount / 100) % 4

        if not jump:
            screen.blit(bluemanImages[blueInteger], (blueman.x, blueman.y))
        else:
            screen.blit(bluemanImages[1], (blueman.x, blueman.y))

        # Snowballs 

        if world.distanceRan > 200:
            screen.blit(snowballImages[snowballInteger], (snowball.x, snowball.y))
            if is_collision(blueman, snowball, (blueman.w + snowball.w) / 2):
                if not collideSnowball:
                    collideSnowball = True
                    jump =  True
                    blueman.velocityY = -1.5 * blueman.jumpVelocity
            else:
                collideSnowball = False
            
            snowball.x -= blueman.velocity * 1.5
            if snowball.x <  -100:
                snowball.x = random.randint(SCREEN_WIDTH * 5, SCREEN_WIDTH * 10)


        for x in snowmanObjects:
            if x.x < SCREEN_WIDTH and x.x > -x.w:
                screen.blit(SnowmanImg, (x.x, x.y))
            
            if x.x < -x.w - 10:
                x.x = random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 600)

        snowClose = None
        minimum = SCREEN_HEIGHT
        for x in snowmanObjects:
            if x.x > blueman.x and x.x < minimum:
                snowClose = x
                minimum = x.x - blueman.x

        
        if snowClose != None:
            if is_collision(blueman, snowClose, 50):

                if blueman.lives > 0 and not(inCollision):
                        blueman.lives -= 1

                elif blueman.lives == 0:
                    gameOver = True

                inCollision = True
                    
            else:
                text2 = None
                inCollision = False


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

        # Collectibles - Collisions and Movement

        for x in range(len(collectibles)):
            item = collectibles[x]
            item.x -= blueman.velocity * 0.65
            screen.blit(loadImage(item.pngName, item.w, item.h), (item.x, item.y))
            if is_collision(blueman, item, (blueman.w + item.w) / 2):
                if collidedWith == None:
                    if item.type == "ufo":
                        UfoCount += 1
                    elif item.type == "invincibility":
                        InvincibilityCount += 1
                    elif item.type == "superJump":
                        SuperJumpCount += 1
                    else:
                        CannonCount += 1

                    collidedWith = item
                    deletedCollectible = x
            else:
                collidedWith = None
                if item.x < -item.w:
                    deletedCollectible = x
                else:
                    deletedCollectible = None
            
        # Process Deletion of Collectible
        if deletedCollectible != None and len(collectibles) > 0:
            
            del collectibles[deletedCollectible]

        for x in range(4):
            if x == 0:
                xVal = (SCREEN_WIDTH  - 60) - (x * 60)
                text = font.render(str(UfoCount), True, BLACK)
                screen.blit(text, (xVal + 15, 10))
                img = loadImage("ufo_collectible.png", 40, 40)
                screen.blit(img, (xVal, 40))
            elif x == 1:
                xVal = (SCREEN_WIDTH  - 60) - (x * 60)
                text = font.render(str(InvincibilityCount), True, BLACK)
                screen.blit(text, (xVal + 15, 10))
                img = loadImage("invincibility_collectible.png", 40, 40)
                screen.blit(img, (xVal, 40))
            elif x == 2:
                xVal = (SCREEN_WIDTH  - 60) - (x * 60)
                text = font.render(str(SuperJumpCount), True, BLACK)
                screen.blit(text, (xVal + 15, 10))
                img = loadImage("superJump_collectible.png", 40, 40)
                screen.blit(img, (xVal, 40))
            else:
                xVal = (SCREEN_WIDTH  - 60) - (x * 60)
                text = font.render(str(CannonCount), True, BLACK)
                screen.blit(text, (xVal + 15, 10))
                img = loadImage("cannon_collectible.png", 40, 40)
                screen.blit(img, (xVal, 40))
            

        # Apple
        apple.x -= blueman.velocity * 0.65
        if apple.x < -apple.w:
            apple.x = SCREEN_WIDTH * random.randint(3, 7)
        
        if is_collision(blueman, apple, (blueman.h + apple.h) / 2):
            blueman.lives += 1
            apple.x = SCREEN_WIDTH * random.randint(3, 7)

        # Distance & Velocity Changes
        world.distanceRan = int(world.runCount / 75)
        blueman.velocity = initVelocity + int(world.distanceRan / 100)

        screen.blit(AppleImg, (apple.x, apple.y))

        # Top Display Items ----------------------------------------------------------------------------------

        # Distance
        text = font.render("DISTANCE: " + str(int(world.distanceRan)) + " : " + str(len(collectiblesCollected)), True, BLACK)
        screen.blit(text, (10, 40))

        # Blueman Lives
        for x in range(blueman.lives):
            screen.blit(HeartImg, (10 + (25 * x), 10))

        world.runCount += blueman.velocity

    else:
        screen.blit(Background, (0, 0))

        for x in groundObjects:
            screen.blit(GroundImg, (x.x, x.y))

        for x in groundObjects:
                x.x -= blueman.velocity

        if groundObjects[0].x < -groundWidth - 50:
            del groundObjects[0]
            endIndex = len(groundObjects) - 1
            item = Ground(groundObjects[endIndex].x + groundWidth, groundLevel + 1, groundWidth, groundHeight, groundLevel)
            groundObjects.append(item)

        if blueman.velocity > 0:
            blueman.velocity -= 0.05

        world.runCount += blueman.velocity

        blueInteger = int(world.runCount / 50) % 3

        screen.blit(bluemanImages[blueInteger], (blueman.x, blueman.y))

        text = font.render("DISTANCE: " + str(int(world.distanceRan)), True, BLACK)
        screen.blit(text, (10, 40))


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()