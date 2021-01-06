# project created by Rika(Ruijia) Xing, Erica Hsu, Eleanor Xiao, Katrina(Yuqiao) Hu

# the following two documents cited from http://www.cs.cmu.edu/~112/index.html
from cmu_112_graphics import *
from basic_graphics import *

import tkinter as tk
from drawBoba import *
from getbobafromtext import *
from PIL import Image, ImageTk

def appStarted(app):
    app.diaryH = 60
    app.diaryW = 120
    app.writeDiary = False
    app.getBoba = False
    app.text = ''

def keyReleased(app, event):
    if app.writeDiary:
        if (len(app.text)*9) % 540 < 8:
            app.text += '\n'
        if event.key == 'Space':
            app.text += ' '
        elif event.key == 'Enter':
            app.text += '\n'
        elif event.key == 'Delete':
            app.text = app.text[:-1]
        else:
            app.text += f'{event.key}'

def mousePressed(app, event):
    # if clicking on new diary button
    if (app.width-event.x <= app.diaryW 
    and abs(app.height/2-10-event.y) <= app.diaryH/2):
        if app.writeDiary:
            app.getBoba = True
            app.writeDiary = False
        else:
            app.writeDiary = True
    if ((app.width/2-100) <= event.x <= (app.width/2+100)
     and (app.height/2-50) <= event.y <= (app.height/2+50)):
        if app.getBoba:
            app.writeDiary = True
            app.getBoba = False
            app.text = ''
            
def writeDiary(app, canvas):
    canvas.create_rectangle(app.width/2-290, app.height/2-200, app.width/2+290, app.height/2+200, outline='black', width=5, fill='#FFCF0B')
    canvas.create_text(app.width/2-270, app.height/2-190, anchor=NW, text=app.text, font='Arial 18')

# Calls on function from drawBoba.py
def returnBoba(app, canvas):
    result = te.get_emotion(app.text)
    average = teaAverage(result)
    flavor, colorForTea = returnFlavor(average)
    topping, colorForTopping = returnToppings(result)
    colorForStraw = "black"
    if "Boba" in topping:
        toppingType = "boba"
    else:
        toppingType = topping
    drawCup(app, canvas, 50, 100, 150, 200, colorForStraw, colorForTea, colorForTopping, toppingType)
    drawCup(app, canvas, 650, 100, 750, 200, colorForStraw, colorForTea, colorForTopping, toppingType)
    canvas.create_text(450, 60, text = f"{flavor} with {topping}", font = "Arial 15 bold")
    canvas.create_rectangle(app.width/2-100, app.height/2-20, app.width/2+100, app.height/2+20, fill=colorForTea, outline = colorForTopping, width=5)
    canvas.create_text(app.width/2, app.height/2, text='Try Again!', font='Arial 23', fill=colorForTopping)

def drawDashboard(app, canvas):
    if app.getBoba:
        img = ImageTk.PhotoImage(Image.open("dashboardV3.png"))
        canvas.create_image(0, 0, anchor = NW, image = img)
        returnBoba(app, canvas)
    elif app.writeDiary:
        img = ImageTk.PhotoImage(Image.open("dashboardV2.png"))
        canvas.create_image(0, 0, anchor = NW, image = img)
        writeDiary(app, canvas)
    else:
        img = ImageTk.PhotoImage(Image.open("dashboardV1.png"))
        canvas.create_image(0, 0, anchor = NW, image = img)

def redrawAll(app, canvas):
	drawDashboard(app, canvas)
	
runApp(width=800, height=600)
