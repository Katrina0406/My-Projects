# boba drink graphics

def drawCup(app, canvas, x0, y0, x1, y1, straw, tea, toppingColor, toppingType):
    width = x1-x0
    height = y1-y0
    strawX = width/7
    strawY = height/2.5
    bodyY = height*0.8
    clear = 'pink'
    thick = 1.5

    y2 = (y1+strawY-5)-width/2
    y3 = ((y0+strawY-10)+(y1+strawY))/2
    y4 =  y2+12

    x00 = x0+5
    x01 = x0+15
    x10 = x1-5
    x11 = x1-15
    changeX = 1
    changeY = changeX/(x01-x00)*(bodyY)

    ############
    # Cup body #
    ############
    drawCupBody(app, canvas, x0, x1, y2, y4, bodyY, thick, clear)
    
    #########
    # Drink #
    #########
    drawDrink(app, canvas, x0, x1, bodyY, tea, y4, thick)

    #########
    # Straw #
    #########
    ## base
    canvas.create_line(x0+width//2+strawX/3, y0, 
                    x0+width//2-strawX, y4+bodyY,
                    width = strawX+2)
    canvas.create_line(x0+width//2+strawX/3, y0, 
                    x0+width//2-strawX, y4+bodyY,
                    fill = straw,
                    width = strawX)

    #########
    # Drink #
    #########    
    ## top oval's bottom arc
    canvas.create_arc((x00+changeX)+5, y4+changeY-10, (x10-changeX)-5, y4+changeY+10,
                start = 180, extent = 180,
                fill = tea, width = thick)
    canvas.create_line((x00+changeX)+5+thick, y4+changeY, (x10-changeX)-5-thick, y4+changeY,
                fill = tea, width = thick)

    #######
    # Cap #
    #######
    drawCap(app, canvas, x0, x1, y0, y1, y2, y3, strawX, strawY, width, thick, clear)
    
    #########
    # Straw #
    #########
    diffX = (x0+width//2+strawX/3) - (x0+width//2-strawX)
    diffY = (y4+bodyY) - y0
    strawX0 = x0+width//2+strawX/3
    strawX1 = strawX0 - (diffX/diffY) * strawY
    strawY2 = y0 + strawY*1.5
    strawX2 = strawX1 - (diffX/diffY) * (strawY2 - (y0+strawY))
    strawY3 = strawY2 + strawY - 5
    strawX3 = strawX2 - (diffX/diffY) * (strawY3-strawY2)

    ## above opening
    canvas.create_line(x0+width//2+strawX/3, y0, 
                    strawX1, y0+strawY,
                    fill = straw,
                    width = strawX) 
    ## on cap
    canvas.create_line(strawX2, strawY2, 
                    strawX3, strawY3,
                    fill = straw,
                    width = strawX)
    ## top oval
    starwOpenX = x0+width//2+strawX/3+(strawX)/2
    canvas.create_oval(starwOpenX, y0-3, 
                    starwOpenX - strawX, y0+3,
                    width = thick,
                    fill = straw)


    ############
    # Toppings #
    ############
    r = 8
    cx = (x01+x11)//2 + r
    cy = y4+(bodyY+changeY)//2 + r*0.5
    if 'boba' in toppingType:
        drawBoba(app, canvas, cx, cy, r, toppingColor)
    else:
        drawCube(app, canvas, cx, cy, r, toppingColor)

def drawCupBody(app, canvas, x0, x1, y2, y4, bodyY, thick, clear):
    ############
    # Cup body #
    ############
    y4 =  y2+12
    ## left
    canvas.create_line(x0+5, y4, 
                x0+15, y4+bodyY,
                width = thick)
    ## right
    canvas.create_line(x1-5, y4, 
                x1-15, y4+bodyY,
                width = thick)

    ## bottom
    canvas.create_arc(x0+15, y4+bodyY-15, x1-15, y4+bodyY+15,
                start = 180, extent = 180,
                width = thick)

    canvas.create_line(x0+15, y4+bodyY, x1-15, y4+bodyY,
                fill = clear, width =  thick)

def drawDrink(app, canvas, x0, x1, bodyY, tea, y4, thick):
    #########
    # Drink #
    #########
    x00 = x0+5
    x01 = x0+15
    x10 = x1-5
    x11 = x1-15
    changeX = 1
    changeY = changeX/(x01-x00)*(bodyY)
    points = [\
            (x00+changeX)+5, y4+changeY, 
            (x10-changeX)-5, y4+changeY, 
            x11-5, y4+bodyY,
            x01+5, y4+bodyY
            ]

    ## center
    canvas.create_polygon(points, fill= tea)

    ## left border
    canvas.create_line((x00+changeX)+5, y4+changeY,
                x01+5, y4+bodyY,
                width = thick)
    ## right border
    canvas.create_line((x10-changeX)-5, y4+changeY,
                x11-5, y4+bodyY,
                width = thick)

    ## top oval
    canvas.create_oval((x00+changeX)+5, y4+changeY-10, (x10-changeX)-5, y4+changeY+10,
                fill = tea, width = thick)
    ## bottom arc
    canvas.create_arc(x01+5, y4+bodyY-10, x11-5, y4+bodyY+10,
                start = 180, extent = 180,
                fill = tea, width = thick)
    canvas.create_line(x01+5, y4+bodyY, x11-5, y4+bodyY,
                fill = tea, width = thick)

def drawCap(app, canvas, x0, x1, y0, y1, y2, y3, strawX, strawY, width, thick, clear):
    #######
    # Cap #
    #######
    # (bottom -> top)
    ## bottom 2nd arc
    y2 = (y1+strawY-5)-width/2
    canvas.create_arc(x0-5, y2-10, x1+5, y2+20, 
                start=150, extent=240, 
                width = thick)
    canvas.create_line(x0+10, y2+2, x1-10, y2+2, 
                fill = clear, width = thick*5)

    ## bottom 1st arc
    y3 = ((y0+strawY-10)+(y1+strawY))/2
    canvas.create_arc(x0, y2-15, x1, y2+15, 
                start=180, extent=180, 
                width = thick)
    canvas.create_line(x0, y3, x1, y3, fill = clear)


    ## top arc
    canvas.create_arc(x0, y0+strawY-10, x1, y1+strawY, 
                start=0, extent=180, 
                width = thick)


    canvas.create_line(x0+thick, (y1+strawY-5)-width/2, x1-thick, (y1+strawY-5)-width/2, 
                fill = clear, width = thick)
                
    ## top opening
    canvas.create_oval((x0+width//2)-strawX, y0+strawY-10,
                        (x0+width//2)+strawX, y0+strawY-10+20,
                         width = thick)

# Honey boba & popping boba
def drawBoba(app, canvas, cx, cy, r, color):
    L = [ [cx, cy-3,                1],
          [cx-r-4, cy+r+3,          2],
          [cx+r*2-2, cy+r*3+2,      3],
          [cx+r+4, cy+r*2,          4],
          [cx-r*3+2, cy+r*3+4,      5],
          [cx-1, cy+r*3,            6],
          [cx-r*4+2, cy+r*2,        7],
          [cx-r*3, cy-r*1,          8],
          [cx+r*2, cy,              9],
        ]
    for [cx, cy, num] in L:
        canvas.create_oval(cx-r, cy-r,
                        cx+r, cy+r,
                        fill = color) 

# Lychee Jelly & Aloe
def drawCube(app, canvas, cx, cy, r, color):
    L = [ [cx, cy+r,            1],
          [cx-r-4, cy+r+3,      2],
          [cx+r+2, cy+r*2-2,    3],
          [cx-r-1, cy+r*3,      4],
          [cx-r*4+2, cy+r*2-4,  5],
          [cx-r*3, cy+r*2+4,    6],
          [cx+r, cy+r*2,        7],
          [cx+r*2-2, cy+r*2+4,  8],
          [cx-r*2, cy+r*4,      9],
          [cx, cy+r*4,          10],
          [cx-r*4+2, cy+r*4-4,  11],
          [cx+r+5, cy+r*4-4,    12],
          ]
    for [cx, cy, num] in L:
        drawSphere(app, canvas, cx, cy, r, color)

def drawSphere(app, canvas, cx, cy, r, color):
    canvas.create_rectangle(cx-r/2, cy-r/2,
                cx+r/2, cy+r/2,
                fill = color) 

    top = [\
            cx-r/2, cy-r/2,
            cx+r/2, cy-r/2,
            cx+r/2+r/3, cy-r/2-r/3,
            cx-r/2+r/3, cy-r/2-r/3,
        ]
    canvas.create_polygon(top, fill = color)

    side = [\
            cx+r/2, cy-r/2,
            cx+r/2, cy+r/2,
            cx+r/2+r/3, cy+r/2-r/3,
            cx+r/2+r/3, cy-r/2-r/3,
        ]
    canvas.create_polygon(side, fill = color) 

    for i in range (0, len(top)-3, 2):
        canvas.create_line(top[i], top[i+1], top[i+2], top[i+3])
    canvas.create_line(top[0], top[1], top[6], top[7])

    for i in range (0, len(side)-3, 2):
        canvas.create_line(side[i], side[i+1], side[i+2], side[i+3])
    canvas.create_line(side[0], side[1], side[6], side[7])

