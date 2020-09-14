######### team members ######### 
#    Yinan Wu      id: yinanwu
#    Yuqiao Hu     id: yuqiaohu
#    Xiangyu Wang  id: xw4
################################
###Turtle Puzzle 1


import turtle

def mousePressed(x, y):
  if x<0 and 0.75*x<y<-0.75*x:
    turtle.color('navy')
  elif x>0 and -0.75*x<y<0.75*x:
    turtle.color('navy')
  else:
    turtle.color('gold')
  turtle.goto(x,y)
  turtle.dot(20)
  
def appStarted():
    screen = turtle.Screen()
    winTop = screen.window_height()//2
    turtle.goto(400,300)
    turtle.goto(-400,-300)
    turtle.goto(0,0)
    turtle.goto(-400,300)
    turtle.goto(400,-300)    
    drawText('Turtle Puzzle 1', 0, winTop - 40)
    drawText('Click the mouse!', 0, winTop - 65, size=20)
    drawText('Gold dots in top and bottom, navy dots on the side''',
             0, winTop - 90, size=20)
    turtle.penup()
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