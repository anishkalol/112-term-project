from cmu_112_graphics import *
from PIL import Image

##### sources #####
# sprite from: https://www.spriters-resource.com/browser_games/googledinosaurrungame/sheet/78171/

def drawDinoSprite(app, canvas):
    sprite = app.dinoSprite[app.spriteCounterDino]  
    canvas.create_image(app.dinosaurX, app.dinosaurY - 7, image = ImageTk.PhotoImage(sprite))
