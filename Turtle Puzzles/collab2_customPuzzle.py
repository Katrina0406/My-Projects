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

    turtle.pensize(3)
    turtle.penup()
    goFurther = input("Would you like to move your turtle? (yes/no)")

    while(goFurther == "yes"):
      direction = input("Enter top, down, left, or right:")
      distance = int(input("Enter distance from 1-10"))
      (x, y) = turtle.position()
      if direction == 'top':
        turtle.goto(x, y + distance*50)
        turtle.dot(20)
      elif direction == "right":
        turtle.goto(x + distance*50, y)
        turtle.dot(20)
      elif direction == 'down':
        turtle.goto(x, y - distance*50)
        turtle.dot(20)
      elif direction == "left":
        turtle.goto(x-distance*10, y)
        turtle.dot(20)
      else:
        print("Invalid direction or distance.")
      goFurther = input("Would you like to move your turtle again? (yes/no)")

    print('Thank you for playing!')
    


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