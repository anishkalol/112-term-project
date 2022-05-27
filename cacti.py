from cmu_112_graphics import *
from PIL import Image

# draws cactus obstacles
def drawCactus(app, canvas):
    for i in range(len(app.cactusMap)):
            canvas.create_image(app.cactusMap[i][0] - app.scrollX, 
                                app.cactusMap[i][1],
                                image = ImageTk.PhotoImage(app.cacti[app.randomCactus]))
