#Haipei Bie (hbie)
#Katarina Hansen (kghansen)
#Yuqiao Hu (yuqiaohu)

#
import turtle
import math


def appStarted():
    screen = turtle.Screen()
    winTop = screen.window_height()//2
    drawText('Turtle Puzzle with Loops', 0, winTop - 40)
    drawText('type an angle and draw this pattern!', 0, winTop - 65, size=20)

    angleIncrement = int(input('Enter an angle:'))
    drawText(angleIncrement, 0, winTop - 350, size=30)
    
    angle = 0
    radius = 200
    initX, initY = (0 , radius)
    turtle.pensize(3)
    turtle.penup()
    turtle.goto(initX, initY)
    turtle.pendown()
    
    while angle <= angleIncrement or angle%360 != angleIncrement :
      x = radius * math.sin(math.radians(angle))
      y = radius * math.cos(math.radians(angle))
      turtle.goto(x, y)
      angle += angleIncrement
  

#########################################################
import string

def drawText(label, x, y, font='Arial', size=30, style='bold', align='center'):
    oldx, oldy = turtle.position()
    turtle.penup()
    turtle.goto(x, y)
    turtle.write(label, font=(font, size, style), align=align)
    turtle.goto(oldx, oldy)
    turtle.pendown()

def main(winWidth, winHeight, bgColor):
    screen = turtle.Screen()
    turtle.speed(0)
    turtle.setup(width=winWidth, height=winHeight)
    screen.bgcolor(bgColor)
    appStarted()
    turtle.speed(10)
    def safeCall(fnName, *args):
        if (fnName in globals()):
            globals()[fnName](*args)
    def keyPressedWrapper(key):
        if (len(key) > 1): key = key.capitalize()
        safeCall('keyPressed', key)
    def bindKey(key):
        if (len(key) > 1) or (ord(key) > 32):
            screen.onkey(lambda: keyPressedWrapper(key), key)
    keys = (['Up', 'Down', 'Left', 'Right', 'space', 'Tab', 'Return'] + 
            list(string.ascii_letters + string.digits))
    for key in keys:
        bindKey(key)
    screen.listen()
    screen.onclick(lambda x, y: safeCall('mousePressed', x, y))
    screen.mainloop()

main(800, 600, 'lightgreen')