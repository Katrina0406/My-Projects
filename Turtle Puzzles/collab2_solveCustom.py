#Haipei Bie (hbie)
#Katarina Hansen (kghansen)
#Yuqiao Hu (yuqiaohu)

#
import turtle
import random


def appStarted():
  screen = turtle.Screen()
  winTop = screen.window_height()//2
  winWidth = screen.window_width()//2
  drawText('Custom Turtle Puzzle', 0, winTop - 40)
  drawText("Guess the word!(it's totally not turtle)", 0, winTop - 65, size=20)

  secretWord = "random"
  guess = input("Enter in the secret word:")
  
  turtle.colormode(255)
  
  while True:
    if guess == secretWord:
        drawText("Good Job!",0, winTop - 350, align = 'center', size = 120, color='red')
        break
    x = random.randint(-winWidth+10, winWidth-10)
    y = random.randint(-winTop+10, winTop-65)
    turtle.penup()
    turtle.goto(x, y)
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    drawText("no", x, y, size = 30, color=(r, g, b))
    guess = input("Enter in the secret word:")   


#########################################################
import string

def drawText(label, x, y, font='Arial', size=30, style='bold', align='center', color='black'):
    oldx, oldy = turtle.position()
    turtle.penup()
    turtle.goto(x, y)
    turtle.color(color)
    turtle.write(label, color, font=(font, size, style), align=align)
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