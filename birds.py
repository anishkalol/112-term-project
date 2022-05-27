from cmu_112_graphics import *
from PIL import Image

# draws bird enemies
def drawBirdsSprite(app, canvas):
    sprite = app.birdsSprite[app.spriteCounterBirds]
    for i in range(len(app.birdMap)):
        canvas.create_image(app.birdMap[i][0] - app.scrollX,
                            app.birdMap[i][1], 
                            image = ImageTk.PhotoImage(sprite))
