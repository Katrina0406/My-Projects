######### team members #########
#    Yinan Wu      id: yinanwu
#    Yuqiao Hu     id: yuqiaohu
#    Xiangyu Wang  id: xw4
################################
###Customized Turtle


import turtle


def mousePressed(x, y):
    distancetoRed = ((-300 - x) ** 2 + (-100 - y) ** 2) ** 0.5
    if distancetoRed <= 40:
        turtle.penup()
        turtle.goto(0, 0)
        turtle.pendown()
    else:
        oldx, oldy = turtle.position()
        distancetoBlue = ((-300 - oldx) ** 2 + (100 - oldy) ** 2) ** 0.5
        mousetoBlue = ((-300 - x) ** 2 + (100 - y) ** 2) ** 0.5
        if distancetoBlue > 40:
            if mousetoBlue > 40:
                turtle.pendown()
                turtle.goto(x, y)
                turtle.dot(20)
            else:
                turtle.penup()
                turtle.goto(x, y)           

            
def appStarted():
    screen = turtle.Screen()
    winTop = screen.window_height() // 2
    drawText('Creative Turtle', 0, winTop - 40)
    drawText('Blue to freeze, Red to restart from (0,0)!', 0, winTop - 65, size=20)
    drawText('You guys enjoy?', 0, winTop - 90, size=20)
    # drawText('Draw dot near top of window to freeze (until you clear)!.',
    #        0, winTop - 115, size=20)
    # drawText('Click in center to clear!.', 0, winTop - 140, size=20)
    turtle.pensize(8)
    turtle.penup()
    turtle.goto(-300, 100)
    turtle.color("blue")
    turtle.dot(40)
    turtle.goto(-300, -100)
    turtle.color("red")
    turtle.dot(40)
    turtle.goto(0, 0)
    turtle.pendown()
    turtle.color('black')
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