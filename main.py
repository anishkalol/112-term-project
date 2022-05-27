from cmu_112_graphics import *
import random
from PIL import Image

# imported files
from terrain import *
from dinosaurSprite import *
from cacti import *
from birds import *
from coins import *
from ui import *
from clouds import *

##### sources #####
# dinosaur sprite, bird sprite, and cacti images from: https://www.spriters-resource.com/browser_games/googledinosaurrungame/sheet/78171/
# coin sprite: https://in.pinterest.com/pin/723883340082448043/
# clouds: screenshotted from the original game, edited by me 
# sun: https://stock.adobe.com/search?k=pixel+sun&asset_id=358656579, edited by me
# terrain gen: https://www.cs.cmu.edu/~112/notes/student-tp-guides/Terrain.pdf 
# ^ used to figure out which algo is appropriate for 1d hill gen

def almostEqual(x, y):
    return abs(x - y) <= 1

def appStarted(app):
    ##### mode #####
    app.splashScreen = True
    app.playDinosaurGame = False

    ##### start game #####
    pic = 'startGame.png'
    app.startGamePic = app.loadImage(pic)
    app.startGamePic = app.scaleImage(app.startGamePic, 2/5.1)

    ##### terrain gen #####
    app.iterations = 7
    app.numPoints = 2**(app.iterations + 1)
    app.terrainHeight = 400
    app.randomRange = 100
    app.points = midpointDisplacement(app.iterations, [[0, app.terrainHeight], [app.width, app.terrainHeight]], app.randomRange)
    
    ##### side scrolling #####
    app.scrollX = 0
    app.scrollY = 0
    app.timerDelay = 20

    ##### dino sprite #####
    dinoSprite = 'dinosaursprite.png'
    spriteStripDino = app.loadImage(dinoSprite)
    app.dinoSprite = []
    
    for i in range(2):
        # cropping each sprite movement
        sprite = spriteStripDino.crop((i*53, 10, 54 + 45*i, 90))
        app.dinoSprite.append(sprite)
    app.spriteCounterDino = 0

    app.dinosaurX = 100
    app.dinosaurY = app.points[0][1]

    # vars for jump/fall
    app.isJumping = False
    app.jumpCount = 0
    app.timePassed = 0 # for checking if dino stayed in the air long enough before coming down

    ##### cacti #####
    # cactus images
    app.cactus1 = app.loadImage('cactus1.png')
    app.cactus2 = app.loadImage('cactus2.png')
    app.cactus3 = app.loadImage('cactus3.png')
    app.cacti = [app.cactus1, app.cactus2, app.cactus3]
    
    # list of cactus spawn places
    app.cactusMap = [[1,1]]
    app.randomCactus = random.randint(0, 2) # picks random cactus img

    ##### bird enemies #####
    birdsSprite = 'birds.png'
    spriteStripBirds = app.loadImage(birdsSprite)
    app.birdsSprite = []

    # list of bird spawn places
    app.birdMap = [[0,0]]
    app.birdHeight = 0
   
    # sprite
    for i in range(2):
        sprite = spriteStripBirds.crop((55*i, 0, 55*i + 55, 51))
        app.birdsSprite.append(sprite)
    app.spriteCounterBirds = 0

    ##### coins #####
    coinSprite = 'coins.png'
    spriteStripCoins = app.loadImage(coinSprite)
    app.coinSprite = []
    app.coinMap = [[0,0]]
    app.coinPoint = 0
    app.score = 0
    app.leaderboard = []
    
    # sprite
    for i in range(6):
        sprite = spriteStripCoins.crop((64*i, 0, 64*i + 60, 73))
        app.coinSprite.append(sprite)
    app.spriteCounterCoins = 0

    ##### clouds #####
    app.cloud = app.loadImage('cloud.png')
    app.cloud = app.scaleImage(app.cloud, 1/4)

    # list of cloud spawn places
    app.cloudMap = [[1,1]]

    ##### ui #####
    pic = 'downBar.png'
    app.downBar = app.loadImage(pic)
    app.downBar = app.scaleImage(app.downBar, 1/4)

    # sun
    sunPic = 'sun.png'
    app.sun = app.loadImage(sunPic)
    app.sun = app.scaleImage(app.sun, 1/7)

    ##### game over #####
    app.isGameOver = False
    topPic = 'top.png'
    bottomPic = 'bottom.png'
    app.gameOverPicTop = app.loadImage(topPic)
    app.gameOverPicTop = app.scaleImage(app.gameOverPicTop, 2/5.1) 
    app.gameOverPicBottom = app.loadImage(bottomPic)
    app.gameOverPicBottom = app.scaleImage(app.gameOverPicBottom, 1/3)
    scorePic = 'finalscore.png'
    app.finalScore = app.loadImage(scorePic)
    app.finalScore = app.scaleImage(app.finalScore, 1/3)

def timerFired(app):
    if app.isGameOver:
        return
    elif app.playDinosaurGame:
        # dino running movement
        if app.isJumping == False:
            app.spriteCounterDino = (1 + app.spriteCounterDino) % len(app.dinoSprite)

        # bird flying movement
        app.spriteCounterBirds = (1 + app.spriteCounterBirds) % len(app.birdsSprite)

        # coin movement
        app.spriteCounterCoins = (1 + app.spriteCounterCoins) % len(app.coinSprite)
        
        app.scrollX += 5
        app.scrollY += 5

        # generating infinite terrain
        if app.scrollX % app.width == app.width // 8:
            x0 = app.points[-1][0] + 1
            x1 = app.points[-1][0] + app.width + 1
            app.points += midpointDisplacement(app.iterations, [[x0, app.terrainHeight], [x1, app.terrainHeight]], app.randomRange)
            # making holes
            randomHolePoint = random.randint(app.width//2, len(app.points) - 20)
            for i in range(randomHolePoint, randomHolePoint + 20):
                app.points[i][1] = app.height//0.2

            # placing cacti
            cactusPoint = random.randint(app.width//3, len(app.points) - 1)
            if app.points[cactusPoint][1] != app.height//0.2 and abs(cactusPoint - randomHolePoint) - 40: # so no cacti are placed in holes
                    app.points[cactusPoint][1] = app.points[cactusPoint][1] - 5
                    app.cactusMap.append([app.points[cactusPoint][0], app.points[cactusPoint][1]])

            # placing birds
            birdPoint = random.randint(app.width//3, len(app.points) - 1)
            if abs(birdPoint - cactusPoint) > 30: # spacing the birds and cacti out
                birdHeight = app.points[birdPoint][1] - 150 # finding height of where birds should spawn
                app.birdMap.append([app.points[birdPoint][0], birdHeight])

            # placing coins
            coinPoint = random.randint(app.width//3, len(app.points) - 1)
            if abs(coinPoint - cactusPoint) > 20: # checking for overlap b/w coins and cacti
                app.points[coinPoint][1] = app.points[coinPoint][1] - 5
                app.coinMap.append([app.points[coinPoint][0], app.points[coinPoint][1]])

            # placing clouds
            cloudPoint = random.randint(app.width//3, len(app.points) - 1)
            randomHeightOffset = random.randint(200, 300)
            cloudHeight = app.points[cloudPoint][1] - randomHeightOffset # finding height of where clouds should spawn
            app.cloudMap.append([app.points[cloudPoint][0], cloudHeight])

        # slicing off points that are already drawn
        # and have moved off the canvas
        if app.scrollX % app.width == 0:
            for i in range(app.numPoints):
                app.points.pop(0)

        # walking on terrain
        if app.isJumping == False:
            for i in range(len(app.points)):
                if almostEqual(app.dinosaurX, app.points[i][0] - app.scrollX):              
                        app.dinosaurY = app.points[i][1]

        # checking for cacti collision
        if 0 < len(app.cactusMap):
            if len(app.cactusMap) > 1 and app.cactusMap[0] == [1,1]:
                app.cactusMap.pop(0)
            if abs(app.dinosaurX + app.scrollX - app.cactusMap[0][0]) < 10:
                if abs(app.dinosaurY - app.cactusMap[0][1]) < 10:
                    app.leaderboard.append(app.score)
                    app.isGameOver = True
            if len(app.cactusMap) != 0: # removing cacti positions from list once they moved off the canvas
                if app.cactusMap[0][0] - app.scrollX <= 0:
                    app.cactusMap.pop(0)

        # collecting coins
        if 0 < len(app.coinMap):
            if len(app.coinMap) > 1 and app.coinMap[0] == [0,0]:
                app.coinMap.pop(0)
            if abs(app.dinosaurX + app.scrollX - app.coinMap[0][0]) < 30: # if dino hits coins
                if abs(app.dinosaurY - app.coinMap[0][1]) < 20:
                    app.coinMap.pop(0)
                    app.score += 1
            if len(app.coinMap) != 0: # removing coin positions from list once they moved off the canvas
                if app.coinMap[0][0] - app.scrollX <= 0:
                    app.coinMap.pop(0)
    
        # divebombs
        if 0 < len(app.birdMap):
            if len(app.birdMap) > 1 and app.birdMap[0] == [-25,75]:
                app.birdMap.pop(0)
            if abs(app.dinosaurX + app.scrollX - app.birdMap[0][0]) < 180: # if in close proximity
                app.birdMap[0][0] -= 5 # bird dives down
                app.birdMap[0][1] += 15
                for i in range(len(app.points) - 1):
                    if abs(app.birdMap[0][1] - app.points[i][1]) < 10: # if close to the terrain
                        app.birdMap[0][0] -= 0 # stops dive and flies forwards
                        app.birdMap[0][1] -= 3 
                if (abs(app.dinosaurX + app.scrollX - app.birdMap[0][0]) < 20 and # if hit
                    abs((app.dinosaurY - 40) - (app.birdMap[0][1] - 10)) < 20):
                    app.leaderboard.append(app.score)
                    app.isGameOver = True
            if len(app.birdMap) != 0: # removing bird positions from list once they moved off the canvas
                if app.birdMap[0][0] - app.scrollX <= 0:
                    app.birdMap.pop(0)
        
        # falling in hole
        if app.dinosaurY > 2000:
            app.leaderboard.append(app.score)
            app.isGameOver = True

        # jump/fall movement, source: https://www.youtube.com/watch?v=c4b9lCfSDQM&t=339s
        if app.isJumping:
            if app.jumpCount < 15:
                app.dinosaurY -= 5
                app.jumpCount += 1
            elif app.jumpCount >= 15:
                app.dinosaurY += 5
                app.jumpCount += 1
            app.timePassed += app.timerDelay
            for i in range(len(app.points)):
                if app.timePassed > 500:
                    if almostEqual(app.dinosaurY, app.points[i][1]):
                        app.dinosaurY = app.points[i][1]
                        app.isJumping = False
                        app.jumpCount = 0
                        app.timePassed = 0
            
def keyPressed(app, event):
    if app.splashScreen:
        if event.key == "s": # start game
            app.playDinosaurGame = True
            app.splashScreen = False
    elif app.playDinosaurGame:
        if app.isGameOver == False:
            if event.key == "Space" or event.key == "Up": # jumping
                if app.isJumping == False:
                    app.isJumping = True
        elif event.key == "r": # restarting game
            appStarted(app) 


def redrawAll(app, canvas):
    drawTerrain(app, canvas)
    drawClouds(app, canvas)
    drawSun(app, canvas)
    drawCactus(app, canvas)
    drawBirdsSprite(app, canvas)
    drawCoins(app, canvas)
    drawDinoSprite(app, canvas)
    drawScore(app, canvas)
    drawDownBar(app, canvas)
    drawGameOver(app, canvas)
    drawSplashScreen(app, canvas)
    drawFinalScore(app, canvas)


def playDinosaurGame():
    runApp(width = 800, height = 600)
    
playDinosaurGame()