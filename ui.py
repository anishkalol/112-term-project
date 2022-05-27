from cmu_112_graphics import *
from PIL import Image

# fonts for splash screen and game over screen --> 'Press Start 2P' by Google Fonts


def drawFinalScore(app, canvas):
    if app.isGameOver:
        canvas.create_image(app.width//2, app.height//2,
                            image = ImageTk.PhotoImage(app.finalScore))
        canvas.create_text(app.width//1.47, app.height//2.01, 
                            text = f'{app.score}',
                            fill = 'black', 
                            font = 'Arial 20 bold')

def drawSplashScreen(app, canvas):
    if app.splashScreen and not app.playDinosaurGame:
        canvas.create_rectangle(0, 0, app.width, app.height,
                                fill = "white")
        canvas.create_image(app.width//2, app.height//2,
                            image = ImageTk.PhotoImage(app.startGamePic))

def drawScore(app, canvas):
    canvas.create_text(2.7 * app.width//3, app.height//12, 
                       text = f'Score: {app.score}',
                       fill = 'black', 
                       font = 'Arial 18 bold')

def drawDownBar(app, canvas):
    canvas.create_image(app.width//2, app.height//1.04,
                        image = ImageTk.PhotoImage(app.downBar))

def drawSun(app, canvas):
    canvas.create_image(20, 15,
                        image = ImageTk.PhotoImage(app.sun))

def drawGameOver(app, canvas):
    if app.isGameOver:
        canvas.create_rectangle(0, 0, app.width, app.height,
                                fill = "white")
        canvas.create_image(app.width//2, app.height//5,
                            image = ImageTk.PhotoImage(app.gameOverPicTop))
        canvas.create_image(app.width//2, app.height//1.4,
                            image = ImageTk.PhotoImage(app.gameOverPicBottom))
