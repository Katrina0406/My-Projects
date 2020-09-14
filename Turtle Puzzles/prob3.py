######### team members ######### 
#    Yinan Wu      id: yinanwu
#    Yuqiao Hu     id: yuqiaohu
#    Xiangyu Wang  id: xw4
################################
###Turtle Puzzle 3


import turtle

def mousePressed(x, y):
  screen = turtle.Screen()
  winTop = screen.window_height()//2
  winWidth = screen.window_width()//2
  # set rgb value
  distanceToCenter = (x**2 + y**2)**0.5
  longestdist = (winTop**2 + winWidth**2)**0.5
  r = 1 - (distanceToCenter / longestdist)/2
  # cutomize turtle shape
  s = turtle.Shape("compound")
  poly1 = ((0,25),(25,0),(0,-25))
  s.addcomponent(poly1, "", (r,r,r))
  screen.register_shape("triangle2", s)
  turtle.shape("triangle2")
  turtle.resizemode("user")
  turtle.shapesize(outline=10)
  # move turtle and leave footprint
  turtle.goto(x, y)
  turtle.stamp()

  
def appStarted():
  screen = turtle.Screen()
  winTop = screen.window_height()//2
  winWidth = screen.window_width()//2
  drawText('Turtle Puzzle 3', 0, winTop - 40)
  drawText('Click the mouse!', 0, winTop - 65, size=20)
  drawText('White triangles near center, darker as you move away',
            0, winTop - 90, size=20)
  #place a dot in center
  turtle.color("blue")
  turtle.dot(20)
  turtle.stamp()
  #we dont need the trace
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