from cmu_112_graphics import *
import random
from PIL import Image

def midpointDisplacement(iters, points, randomRange):
    # base case
    if iters == 0:
        return points
    # recursive case
    else:
        # finding midpoint coordinates
        midX = (points[0][0] + points[len(points) - 1][0])//2
        midY = (points[0][1] + points[len(points) - 1][1])//2

        yDisplacement = random.uniform(-randomRange, randomRange) # random offset

        middle = len(points) // 2
        points.insert(middle, [midX, midY + yDisplacement]) # inserting calculated midpoint

        # left line segment
        points[0: middle + 1] = midpointDisplacement(iters - 1, points[0: middle + 1], randomRange)

        # right line segment
        points[middle: len(points)] = midpointDisplacement(iters - 1, points[middle: len(points)], randomRange)
        
        return points

def appStarted(app):
    app.height = 600
    app.width = 800

    ##### terrain gen #####
    app.iterations = 20
    app.terrainHeight = 400
    app.points = [[0, app.terrainHeight], [app.width, app.terrainHeight]]
    app.randomRange = 40

    ##### sprites #####
    dinoSprite = 'dinosaursprite.png'
    spriteStripDino = app.loadImage(dinoSprite)
    app.dinoSprite = []
    
    for i in range(4):
        # cropping each sprite movement
        sprite = spriteStripDino.crop((i, 20, i+60, 90))
        app.dinoSprite.append(sprite)
    app.spriteCounterDino = 0

    ##### camera movement #####
    app.cameraOffset = 0
    app.scrollMargin = app.width/0.2
    app.dinosaur = app.scrollMargin

    ##### cacti #####
    # cactus images
    app.cactus1 = app.loadImage('cactus1.png')
    app.cactus2 = app.loadImage('cactus2.png')
    app.cactus3 = app.loadImage('cactus3.png')
    app.cacti = [app.cactus1, app.cactus2, app.cactus3]
    
    # list of cactus spawn places
    app.cactusMap = [None] * (len(app.points))
    app.randomIndexCactus = random.randint(0, len(app.points) - 1) # some point on the terrain
    app.randomCactus = random.randint(0, 2) # picks random cactus img
    # picks random coordinates for the cactus to be placed at
    app.cactusCoords = app.points[app.randomIndexCactus] 
    app.placedCactus = app.cacti[app.randomCactus].crop((0, 0, 50, 100))

    ##### bird enemies #####
    birdsSprite = 'birds.png'
    spriteStripBirds = app.loadImage(birdsSprite)
    app.birdsSprite = []

    # list of bird spawn places
    app.birdMap = [None] * (len(app.points))
    app.randomIndexBirds = random.randint(0, len(app.points) - 1) # some point on the terrain

    # picks random coordinates for the bird to be placed at
    app.birdCoords = app.points[app.randomIndexBirds]
    app.birdCoords[1] += 70 # float the bird in the air
    
    # sprite
    for i in range(2):
        sprite = spriteStripBirds.crop((i, 10, i + 100, 100))
        app.birdsSprite.append(sprite)
    app.spriteCounterBirds = 0

def timerFired(app):
    # running movement
    app.spriteCounterDino = (1 + app.spriteCounterDino) % len(app.dinoSprite)

    # bird flying movement
    app.spriteCounterBirds = (1 + app.spriteCounterBirds) % len(app.birdsSprite)
    moveCamera(app, 15)

def placeCactus(app): # check if cactus can be placed
    if (app.cactusMap[app.randomIndexCactus] == None and 
        app.birdMap[app.randomIndexCactus] == None):
        app.cactusMap[app.randomIndexCactus] = app.placedCactus

def placeBirds(app): # check if bird can be placed
    if (app.birdMap[app.randomIndexBirds] == None and 
        app.cactusMap[app.randomIndexBirds] == None):
        app.birdMap[app.randomIndexBirds] = app.birdsSprite

def moveCamera(app, dx): # reminder: needs to be changed 
    # dinosaur is moving right
    # once it reaches the scroll margin -> camera moves left
    if (app.dinosaur > app.width - app.scrollMargin - app.cameraOffset):
        app.cameraOffset -= dx


def midpointDisplacementTerrainGen(app, canvas):
    midpointDisplacement(app.iterations, app.points, app.randomRange)
    canvas.create_line(app.points,
                        fill = "black")
'''
def drawTerrain(app, canvas):
    # drawing individual lines for every point
    canvas.create_line(app.points,
                        fill = "black")
'''
# draws dinosaur
def drawDinoSprite(app, canvas):
    sprite = app.dinoSprite[app.spriteCounterDino]
    canvas.create_image(100, 400, image = ImageTk.PhotoImage(sprite))

# draws bird enemies
def drawBirdsSprite(app, canvas):
    sprite = app.birdsSprite[app.spriteCounterBirds]
    x = app.birdCoords[0]
    y = app.birdCoords[1]

    canvas.create_image(x, y, image = ImageTk.PhotoImage(sprite))

# draws cactus enemies
def drawCactus(app, canvas):
    x = app.cactusCoords[0]
    y = app.cactusCoords[1]

    canvas.create_image(x, y, image = ImageTk.PhotoImage(app.placedCactus))

def redrawAll(app, canvas):
    midpointDisplacementTerrainGen(app, canvas)
    drawDinoSprite(app, canvas)
    drawCactus(app, canvas)
    drawBirdsSprite(app, canvas)

def playDinosaurGame():
    runApp(width = 800, height = 600)

playDinosaurGame()