from cmu_112_graphics import *
import random
###### sources ######
# info on midpoint displacement algo: https://www.cs.cmu.edu/~112/notes/student-tp-guides/Terrain.pdf

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
        # random.uniform picks a random float b/w the two args, source --> https://www.w3schools.com/python/ref_random_uniform.asp

        middle = len(points) // 2
        points.insert(middle, [midX, midY + yDisplacement]) # inserting calculated midpoint

        # left line segment
        left = midpointDisplacement(iters - 1, points[0: middle + 1], randomRange/2) 
        # adjusting randomRange to get smaller makes more details in terrain 
        # ^ a TA recommended to do this

        # right line segment
        right = midpointDisplacement(iters - 1, points[middle: len(points)], randomRange/2)
        
        return left + right

def midpointDisplacementTerrainGen(app):
    app.points = midpointDisplacement(app.iterations, app.points, app.randomRange)
    

def drawTerrain(app, canvas):
    # drawing individual lines for every point
    for i in range(len(app.points) - 1):
        canvas.create_line(app.points[i][0] - app.scrollX, app.points[i][1], 
                           app.points[i + 1][0] - app.scrollX, app.points[i + 1][1],
                           fill = "black")
