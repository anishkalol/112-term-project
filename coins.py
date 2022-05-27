from cmu_112_graphics import *
from PIL import Image

# coin sprite from: https://in.pinterest.com/pin/723883340082448043/
def drawCoins(app, canvas):
    sprite = app.coinSprite[app.spriteCounterCoins]  
    for i in range(len(app.coinMap)):
            canvas.create_image(app.coinMap[i][0] - app.scrollX,
                                app.coinMap[i][1], 
                                image = ImageTk.PhotoImage(sprite))
