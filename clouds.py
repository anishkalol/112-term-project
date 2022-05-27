from cmu_112_graphics import *
from PIL import Image

# draws clouds in the sky
def drawClouds(app, canvas):
    for i in range(len(app.cloudMap)):
            canvas.create_image(app.cloudMap[i][0] - app.scrollX, 
                                app.cloudMap[i][1],
                                image = ImageTk.PhotoImage(app.cloud))
