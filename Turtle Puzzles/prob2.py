######### team members ######### 
#    Yinan Wu      id: yinanwu
#    Yuqiao Hu     id: yuqiaohu
#    Xiangyu Wang  id: xw4
################################
###Turtle Puzzle 2


import turtle


def mousePressed(x, y):
  turtle.pensize(8)
  oldx,oldy = turtle.position()
  newx = (x+oldx)/2
  newy = (y+oldy)/2
  distance = ((oldx-x)**2+(oldy-y)**2)**0.5
  if distance > 20:
    turtle.goto(newx,newy)
    turtle.dot(20)
  else:
    turtle.clear()
    appStarted() ##clear

  
def appStarted():
    screen = turtle.Screen()
    winTop = screen.window_height()//2
    drawText('Turtle Puzzle 2', 0, winTop - 40)
    drawText('Click the mouse!', 0, winTop - 65, size=20)
    drawText('Click on the last-drawn dot to reset!',
             0, winTop - 90, size=20)
    turtle.hideturtle()
    

############################################
# Simple Turtle Framework
# (ignore code below here)
############################################

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