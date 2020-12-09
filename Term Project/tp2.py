# cited from http://www.cs.cmu.edu/~112/index.html
from cmu_112_graphics import *
import numpy as np
import math

# the three functions below are cited from http://www.cs.cmu.edu/~112/index.html
def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

class MyApp(App):

	def appStarted(self):
		self.width = 1300
		self.height = 800
		self.cameraOn = False
		self.splash = True
		self.help = False
		self.text = None

		MyApp.drawParas(self)
		MyApp.buttonParas(self)
		MyApp.colorParas(self)
		MyApp.cameraParas(self)

		#cited from https://www.google.com/search?source=univ&tbm=isch&q=blue+background&sa=X&ved=2ahUKEwiQ3aWbk7ftAhXWbCsKHdBJBN0QjJkEegQIAhAB
		self.img1 = self.loadImage('dash.jpeg')
		self.img1 = self.scaleImage(self.img1, 2.2)

		try:
			self.text = readFile('draw.txt')
		except:
			return
		# try:
		# 	MyApp.getSaveInfo(self)
		# except:
		# 	return
		MyApp.getSaveInfo(self)

	def getSaveInfo(self):
		# basically extract info from the saved file
		if self.text != None:
			info = self.text.split("+")
			if len(info[0]) > 5:
				self.pensizes = info[0][1:-1]
				self.pensizes = list(self.pensizes.split(", "))
				for i in range(len(self.pensizes)):
					self.pensizes[i] = float(self.pensizes[i])
			if len(info[1]) > 2:
				self.pencolors = info[1][1:-1]
				self.pencolors = list(self.pencolors.split(", "))
				for i in range(len(self.pencolors)):
					self.pencolors[i] = self.pencolors[i][1:-1]

			drawLine = info[2][1:-1]
			i = 0
			while i < len(drawLine):
				if drawLine[i] == ']':
					#(x1, y1), (x2, y2)..
					tempList = drawLine[1:i]
					j = 0
					tempCor = []
					while j < len(tempList):
						if tempList[j] == ')':
							tempT = list(tempList[1:j].split(", "))
							tempCor.append((float(tempT[0]), float(tempT[1])))
							if j != len(tempList)-1:
								tempList = tempList[j+3:]
								j = 0
							else:
								break
						else:
							j += 1
					self.drawLine.append(tempCor)
					if i != len(drawLine)-1:
						drawLine = drawLine[i+3:]
						i = 0
					else:
						break
				else:
					i += 1

			self.trackLine = int(info[3])
			self.bgColor = info[4]
			self.disMoveX = float(info[5])
			self.disMoveY = float(info[6])
			self.probX = float(info[7])
			self.probY = float(info[8])

			contours = info[9][8:-15]
			contours = list(contours.split(", dtype=int32), array("))
			n = 0
			while n < len(contours):
				cont = contours[0][1:-1].strip(" ")
				k = 0
				while k < len(cont)-1:
					if cont[k:k+2] == ']]':
						# [[x1, y1]], [[x2, y2]]...
						tempList = cont[1:k+1]
						m = 0
						tempCor = []
						while m < len(tempList):
							if tempList[m] == ']':
								tempT = list(tempList[1:m].split(", "))
								x = float(tempT[0])
								y = float(tempT[1])
								tempCor.append([(x, y)])
								if m != len(tempList)-1:
									tempList = tempList[m+3:]
									m = 0
								else:
									break
							else:
								m += 1
						self.contours.append(tempCor)
						if k != len(contours)-2:
							contours = contours[k+3:]
							k = 0
						else:
							break
					else:
						k += 1

	def saveDrawing(self):
		if self.saveDraw:
			content = f'{self.pensizes}+{self.pencolors}+{self.drawLine}+{self.trackLine}+{self.bgColor}+{self.disMoveX}+{self.disMoveY}+{self.probX}+{self.probY}+{self.contours}'
			writeFile('draw.txt', content)

	def cameraParas(self):
		self.marginH, self.marginW = 100, 80
		self.snap = None
		self.contours = None
		self.camRangeX, self.camRangeY = 100, 80
		self.camFixed = False

	def drawParas(self):
		self.drx1, self.dry1, self.drx2, self.dry2 = 35, 100, 850, 650
		self.drSize = 4
		self.pensizes = []
		self.drColor = 'black'
		self.pencolors = []
		self.draw = False
		self.drawLine = []
		self.trackLine = -1
		self.saveDraw = False
		self.scrollX = (595+685)/2
		self.scrollY = self.height-43
		self.bgColor = 'lavender'
		self.eraseR = 5
		self.retrieve = False
		# buttons
		self.moveMode = False
		self.xL, self.yL, self.xR, self.yR = -1, -1, -1, -1
		self.disMoveX, self.disMoveY = 0, 0
		self.resizeMode = False
		self.probX, self.probY = 1, 1
		self.resizeX = self.resizeY = 0
		self.rotateMode = False
		self.angle = 0
		self.flipH = False
		self.flipV = False
		self.bgMode = False
		self.contourMode = False
		self.contourColor = 'black'
		self.outputMode = False

		# draw modes
		self.drawMove = False
		self.drawMoveX, self.drawMoveY = 0, 0
		self.moveLine = False
		self.drawResize = False
		self.drawprobX, self.drawprobY = 1, 1
		self.resizeLine = False
		self.drawRotate = False
		self.roAngle = 0
		self.rotateLine = False
		self.drawFlipH = False
		self.flipHLine = False
		self.drawFlipV = False
		self.flipVLine = False
		MyApp.changeTempParas(self)

	def buttonParas(self):
		# splash button parameters
		self.bx1, self.by1, self.bx2, self.by2 = self.width/2-475, self.height/2+50, self.width/2-275, self.height/2+150
		self.bx3, self.by3, self.bx4, self.by4 = self.width/2-225, self.height/2+50, self.width/2-25, self.height/2+150
		self.bx5, self.by5, self.bx6, self.by6 = self.width/2+25, self.height/2+50, self.width/2+225, self.height/2+150
		self.bx7, self.by7, self.bx8, self.by8 = self.width/2+275, self.height/2+50, self.width/2+475, self.height/2+150

		# bottom-left button
		self.lx1, self.ly1, self.lx2, self.ly2 = 30, self.height-90, 150, self.height-30
		# bottom-right button
		self.rx3, self.ry3, self.rx4, self.ry4 = self.width-150, self.height-90, self.width-30, self.height-30
		# bottom-middle button
		self.mx1, self.my1, self.mx2, self.my2 = self.width/2-60, self.height-90, self.width/2+60, self.height-30

		# draw page buttons
		self.dpx1, self.dpy1, self.dpx2, self.dpy2 = self.width-150, 120, self.width-30, 180
		self.dpx3, self.dpy3, self.dpx4, self.dpy4 = self.width-150, 200, self.width-30, 260
		self.dpx5, self.dpy5, self.dpx6, self.dpy6 = self.width-150, 280, self.width-30, 340
		self.dpx7, self.dpy7, self.dpx8, self.dpy8 = self.width-150, 360, self.width-30, 420
		self.dpx9, self.dpy9, self.dpx10, self.dpy10 = self.width-150, 440, self.width-30, 500
		self.dpx11, self.dpy11, self.dpx12, self.dpy12 = self.width-150, 520, self.width-30, 580
		self.dpx13, self.dpy13, self.dpx14, self.dpy14 = self.width-150, 600, self.width-30, 660

		# clear button
		self.clearx1, self.cleary1, self.clearx2, self.cleary2 = self.drx2+20, self.dry2-40, self.drx2+60, self.dry2

	def colorParas(self):
		# firebrick1, IndianRed1, salmon1, chocolate1, gold, yellow2, khaki1, antique white,  green2, spring green, pale green, snow
		self.cxF, self.cxI, self.cxS, self.cxC, self.cxOr, self.cxGo, self.cxY, self.cxK, self.cxA,  self.cxG, self.cxSg, self.cxPg, self.cxSn = 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540
		# aquamarine2, turquoise, dark turquoise, DeepSkyBlue2, DodgerBlue2, SlateBlue1, MediumPurple1, medium orchid, HotPink1, PaleVioletRed1, orchid2, RosyBrown1, black
		self.cxAq, self.cxT, self.cxDt, self.cxDs, self.cxDo, self.cxSb, self.cxMp, self.cxMo, self.cxHp, self.cxPv, self.cxOc, self.cxRb, self.cxB = 180, 210, 240, 270, 300, 330, 360, 390, 420, 450, 480, 510, 540
		# first-line & second-line
		self.cfl, self.csl= self.height-90, self.height-60

	def drawColors(self, canvas):
		# first line
		canvas.create_rectangle(self.cxF, self.cfl, self.cxF+30, self.cfl+30, fill='firebrick1', width=0)
		canvas.create_rectangle(self.cxI, self.cfl, self.cxI+30, self.cfl+30, fill='IndianRed1', width=0)
		canvas.create_rectangle(self.cxS, self.cfl, self.cxS+30, self.cfl+30, fill='salmon1', width=0)
		canvas.create_rectangle(self.cxC, self.cfl, self.cxC+30, self.cfl+30, fill='chocolate1', width=0)
		canvas.create_rectangle(self.cxOr, self.cfl, self.cxOr+30, self.cfl+30, fill='orange', width=0)
		canvas.create_rectangle(self.cxGo, self.cfl, self.cxGo+30, self.cfl+30, fill='gold', width=0)
		canvas.create_rectangle(self.cxY, self.cfl, self.cxY+30, self.cfl+30, fill='yellow2', width=0)
		canvas.create_rectangle(self.cxK, self.cfl, self.cxK+30, self.cfl+30, fill='khaki1', width=0)
		canvas.create_rectangle(self.cxA, self.cfl, self.cxA+30, self.cfl+30, fill='antique white', width=0)
		canvas.create_rectangle(self.cxG, self.cfl, self.cxG+30, self.cfl+30, fill='green2', width=0)
		canvas.create_rectangle(self.cxSg, self.cfl, self.cxSg+30, self.cfl+30, fill='spring green', width=0)
		canvas.create_rectangle(self.cxPg, self.cfl, self.cxPg+30, self.cfl+30, fill='pale green', width=0)
		canvas.create_rectangle(self.cxSn, self.cfl, self.cxSn+30, self.cfl+30, fill='snow', width=0)
		# second line
		canvas.create_rectangle(self.cxAq, self.csl, self.cxAq+30, self.csl+30, fill='aquamarine2', width=0)
		canvas.create_rectangle(self.cxT, self.csl, self.cxT+30, self.csl+30, fill='turquoise', width=0)
		canvas.create_rectangle(self.cxDt, self.csl, self.cxDt+30, self.csl+30, fill='dark turquoise', width=0)
		canvas.create_rectangle(self.cxDs, self.csl, self.cxDs+30, self.csl+30, fill='DeepSkyBlue2', width=0)
		canvas.create_rectangle(self.cxDo, self.csl, self.cxDo+30, self.csl+30, fill='DodgerBlue2', width=0)
		canvas.create_rectangle(self.cxSb, self.csl, self.cxSb+30, self.csl+30, fill='SlateBlue1', width=0)
		canvas.create_rectangle(self.cxMp, self.csl, self.cxMp+30, self.csl+30, fill='MediumPurple1', width=0)
		canvas.create_rectangle(self.cxMo, self.csl, self.cxMo+30, self.csl+30, fill='medium orchid', width=0)
		canvas.create_rectangle(self.cxHp, self.csl, self.cxHp+30, self.csl+30, fill='HotPink1', width=0)
		canvas.create_rectangle(self.cxPv, self.csl, self.cxPv+30, self.csl+30, fill='PaleVioletRed1', width=0)
		canvas.create_rectangle(self.cxOc, self.csl, self.cxOc+30, self.csl+30, fill='orchid2', width=0)
		canvas.create_rectangle(self.cxRb, self.csl, self.cxRb+30, self.csl+30, fill='RosyBrown1', width=0)
		canvas.create_rectangle(self.cxB, self.csl, self.cxB+30, self.csl+30, fill='black', width=0)

	def findTempFrame(self, x, y):
		if self.drawMove and self.moveLine: return
		if self.drawResize and self.resizeLine: return
		if self.drawRotate and self.rotateLine: return
		if self.drawFlipH and self.flipHLine: return
		if self.drawFlipV and self.flipVLine: return
		if ((not self.drawMove) and (not self.drawResize) and (not self.drawRotate)
			and (not self.drawFlipH) and (not self.drawFlipV)):
			return
		if not (self.drx1+8) <= x <= (self.drx2-8): return
		if not (self.dry1+8) <= y <= (self.dry2-8): return
		self.tempF.append((x, y))
		dis = 0
		x0, y0 = self.tempx0, self.tempy0
		x1, y1 = -1, -1
		for tx, ty in self.tempF:
			if tx > x0 and ty > y0:
				tempDis = ((tx-x0)**2 + (ty-y0)**2)**0.5
				if tempDis > dis:
					dis = tempDis
					x1, y1 = tx, ty
		self.tempx1, self.tempy1 = x1, y1

	def rotateDrawLines(self):
		if self.drawLine == []: return
		if not self.rotateLine: return
		cx, cy = MyApp.findGraphRange(self)
		# xnew = (x1 - cx)*cos(θ) - (y1 - cy)*sin(θ) + cx
		# ynew = (x1 - cx)*sin(θ) + (y1 - cy)*cos(θ) + cy
		angle = (self.roAngle/180)*math.pi
		if self.drawLine != []:
			for i in range(0, len(self.drawLine)):
				line = self.drawLine[i]
				for j in range(0, len(line)):
					x1, y1 = line[j]
					if ((self.tempx0+5) <= x1 <= (self.tempx1-5)
							and (self.tempy0+5) <= y1 <= (self.tempy1-5)):
						x = (x1-cx)*math.cos(angle) - (y1-cy)*math.sin(angle) + cx
						y = (x1-cx)*math.sin(angle) + (y1-cy)*math.cos(angle) + cy
						self.drawLine[i][j] = (x, y)

	def findGraphRange(self):
		minLeft, maxRight, minTop, maxBottom = self.tempx1, self.tempx0, self.tempy1, self.tempy0
		for i in range(0, len(self.drawLine)):
			line = self.drawLine[i]
			for j in range(0, len(line)):
				x1, y1 = line[j]
				if ((self.tempx0+5) <= x1 <= (self.tempx1-5)
						and (self.tempy0+5) <= y1 <= (self.tempy1-5)):
					# find the four bounds of the chosen graph
					if x1 < minLeft:
						minLeft = x1
					if x1 > maxRight:
						maxRight = x1
					if y1 < minTop:
						minTop = y1
					if y1 > maxBottom:
						maxBottom = y1
		cx, cy = (minLeft+maxRight)/2, (minTop+maxBottom)/2
		return cx, cy

	def flipDrawLines(self):
		if self.drawLine == []: return
		if (not self.flipHLine) and (not self.flipVLine): return
		cx, cy = MyApp.findGraphRange(self)
		# flip the graph
		for i in range(0, len(self.drawLine)):
			line = self.drawLine[i]
			for j in range(0, len(line)):
				x1, y1 = line[j]
				if ((self.tempx0+5) <= x1 <= (self.tempx1-5)
						and (self.tempy0+5) <= y1 <= (self.tempy1-5)):
					if self.flipHLine:
						if x1 > cx:
							x1 = x1-(x1-cx)*2
						elif x1 < cx:
							x1 = x1+(cx-x1)*2
					elif self.flipVLine:
						if y1 > cy:
							y1 = y1-(y1-cy)*2
						elif y1 < cy:
							y1 = y1+(cy-y1)*2
					self.drawLine[i][j] = (x1, y1)
		
	def moveDrawLines(self, x, y):
		if not self.moveLine: return
		if not (self.tempx0+5) <= x <= (self.tempx1-5): return
		if not (self.tempy0+5) <= y <= (self.tempy1-5): return
		cx, cy = (self.tempx0+self.tempx1)/2, (self.tempy0+self.tempy1)/2
		leftside = self.tempx0+5+(x-cx)
		rightside = self.tempx1-5+(x-cx)
		if leftside >= self.drx1 and rightside <= self.drx2:
			self.drawMoveX = x-cx
		topside = self.tempy0+5+(y-cy)
		bottomside = self.tempy1-5+(y-cy)
		if topside >= self.dry1 and bottomside <= self.dry2:
			self.drawMoveY = y-cy
		changed = False
		if self.drawLine != []:
			for i in range(0, len(self.drawLine)):
				line = self.drawLine[i]
				for j in range(0, len(line)):
					x1, y1 = line[j]
					if ((self.tempx0+5) <= x1 <= (self.tempx1-5)
							and (self.tempy0+5) <= y1 <= (self.tempy1-5)):
						self.drawLine[i][j] = (x1+self.drawMoveX, y1+self.drawMoveY)
						changed = True
		if changed:
			self.tempx0, self.tempy0 = self.tempx0+self.drawMoveX, self.tempy0+self.drawMoveY
			self.tempx1, self.tempy1 = self.tempx1+self.drawMoveX, self.tempy1+self.drawMoveY

	def resizeDrawLines(self, x, y):
		if not self.resizeLine: return
		cx, cy = (self.tempx0+self.tempx1)/2, (self.tempy0+self.tempy1)/2
		disX, disY = (self.tempx1-self.tempx0)/2, (self.tempy1-self.tempy0)/2
		# four corners
		if (self.tempx0-5) <= x <= (self.tempx0+10) and (self.tempy0-5) <= y <= (self.tempy0+10):
			moveX = (self.tempx0 - x)
			moveY = (self.tempy0 - y)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.drawprobX = self.drawprobY = prob
		elif (self.tempx0-5) <= x <= (self.tempx0+10) and (self.tempy1-10) <= y <= (self.tempy1+5):
			moveX = (self.tempx0 - x)
			moveY = (y - self.tempy1)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.drawprobX = self.drawprobY = prob
		elif (self.tempx1-10) <= x <= (self.tempx1+5) and (self.tempy0-5) <= y <= (self.tempy0+10):
			moveX = (x - self.tempx1)
			moveY = (self.tempy0 - y)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.drawprobX = self.drawprobY = prob
		elif (self.tempx1-10) <= x <= (self.tempx1+5) and (self.tempy1-10) <= y <= (self.tempy1+5):
			moveX = (x - self.tempx1)
			moveY = (y - self.tempy1)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.drawprobX = self.drawprobY = prob
		# leftside x
		elif (self.tempx0-10) <= x < self.tempx0:
			moveX = (self.tempx0 - x)
			self.drawprobX = (moveX+disX) / disX
		elif (self.tempx0+5) < x <= (self.tempx0+10):
			moveX = (self.tempx0+5 - x)
			self.drawprobX = (moveX+disX) / disX
		# rightside x
		elif (self.tempx1-5-10) <= x < (self.tempx1-5) :
			moveX = (x - (self.tempx1-5))
			self.drawprobX = (moveX+disX) / disX
		elif self.tempx1 < x <= (self.tempx1+10) :
			moveX = (x - self.tempx1)
			self.drawprobX = (moveX+disX) / disX
		# upside y
		elif (self.tempy0-10) <= y < self.tempy0:
			moveY = (self.tempy0 - y)
			self.drawprobY = (moveY+disY) / disY
		elif (self.tempy0+5) < y <= (self.tempy0+10):
			moveY = (self.tempy0+5 - y)
			self.drawprobY = (moveY+disY) / disY
		# downside y
		elif (self.tempy1-5-10) <= y < (self.tempy1-5):
			moveY = (y - (self.tempy1-5))
			self.drawprobY = (moveY+disY) / disY
		elif self.tempy1 < y <= (self.tempy1+10):
			moveY = (y - self.tempy1)
			self.probY = (moveY+disY) / disY

		changed = False
		if self.drawLine != []:
			for i in range(0, len(self.drawLine)):
				line = self.drawLine[i]
				for j in range(0, len(line)):
					x1, y1 = line[j]
					if ((self.tempx0-15) <= x1 <= (self.tempx1+10)
							and (self.tempy0-15) <= y1 <= (self.tempy1+10)):
						self.drawLine[i][j] = ((x1-cx)*self.drawprobX+cx, (y1-cy)*self.drawprobY+cy)
						changed = True
		if changed:
			self.tempx0, self.tempy0 = (self.tempx0-cx)*self.drawprobX+cx, (self.tempy0-cy)*self.drawprobY+cy
			self.tempx1, self.tempy1 = (self.tempx1-cx)*self.drawprobX+cx, (self.tempy1-cy)*self.drawprobY+cy

	def drawTempFrame(self, canvas):
		if ((not self.drawMove) and (not self.drawResize) and (not self.drawRotate)
			and (not self.drawFlipH) and (not self.drawFlipV)):
			return
		if self.tempx0 == -1 or self.tempx1 == -1: return
		canvas.create_rectangle(self.tempx0, self.tempy0, self.tempx1, self.tempy1, width=5, outline='lightGreen')

	def keyPressed(self, event):
		if event.key == 'q':
			self.quit()
		elif self.bgMode:
			if event.key == 'r':
				self.bgColor = 'lavender'
		elif self.moveMode or self.resizeMode or self.rotateMode:
			cx, cy = (self.xL+self.xR)/2+self.disMoveX, (self.yT+self.yB)/2+self.disMoveY
			x3, y3, x4, y4 = (self.xL-cx)*self.probX+cx+self.disMoveX, (self.yT-cy)*self.probY+cy+self.disMoveY, (self.xR-cx)*self.probX+cx+self.disMoveX, (self.yB-cy)*self.probY+cy+self.disMoveY
			disX, disY = (x3+x4)/2, (y3+y4)/2
			if self.moveMode:
				if event.key == 'Up':
					if y3 >= self.dry1:
						self.disMoveY -= 10
				elif event.key == 'Down':
					if y4 <= self.dry2:
						self.disMoveY += 10
				elif event.key == 'Left':
					if x3 >= self.drx1:
						self.disMoveX -= 10
				elif event.key == 'Right':
					if x4 <= self.drx2:
						self.disMoveX += 10
			elif self.resizeMode:
				if event.key == '=':
					self.resizeX += 10
					self.probX = self.probY = (self.resizeX+disX) / disX
				elif event.key == '-':
					self.resizeX -= 10
					self.probX = self.probY = (self.resizeX+disX) / disX
				elif event.key == 'Up':
					self.resizeY += 10
					self.probY = (self.resizeY+disY) / disY
				elif event.key == 'Down':
					self.resizeY -= 10
					self.probY = (self.resizeY+disY) / disY
				elif event.key == 'Left':
					self.resizeX -= 10
					self.probX = (self.resizeX+disX) / disX
				elif event.key == 'Right':
					self.resizeX += 10
					self.probX = (self.resizeX+disX) / disX
			else:
				if event.key == 'Left':
					self.angle = -10
					MyApp.rotateSnap(self)
				elif event.key == 'Right':
					self.angle = 10
					MyApp.rotateSnap(self)
		elif self.retrieve:
			if event.key == 'Up' and self.eraseR <= 20:
				self.eraseR += 3
			elif event.key == 'Down' and self.eraseR >=4 :
				self.eraseR -= 3
		elif self.rotateLine:
			if event.key == 'Left':
				self.roAngle = -10
				MyApp.rotateDrawLines(self)
			elif event.key == 'Right':
				self.roAngle = 10
				MyApp.rotateDrawLines(self)

	def mouseDragged(self, event):
		if self.draw:
			try:
				MyApp.drawPen(self, event.x, event.y)
				MyApp.penSize(self, event.x, event.y)
				MyApp.moveSnap(self, event.x, event.y)
				MyApp.resizeSnap(self, event.x, event.y)
				MyApp.findTempFrame(self, event.x, event.y)
				MyApp.moveDrawLines(self, event.x, event.y)
				MyApp.resizeDrawLines(self, event.x, event.y)
			except:
				return
		elif self.cameraOn:
			MyApp.adjustSnap(self, event.x, event.y)

	def adjustSnap(self, x, y):
		if (self.camRangeX-90) <= x <= (self.camRangeX+90):
			if self.marginW+5 <= x <= (self.width/2-100):
				self.camRangeX = x
		elif ((self.width-self.camRangeX-90) <= x <= (self.width-self.camRangeX+90)):
			if (self.width/2+100) <= x <= (self.width-self.marginW-5):
				self.camRangeX = self.width-x
		elif (self.camRangeY-90) <= y <= (self.camRangeY+90):
			if self.marginH-15 <= y <= (self.height/2-80):
				self.camRangeY = y
		elif ((self.height-self.camRangeY-90) <= y <= (self.height-self.camRangeY+90)):
			if (self.height/2+80) <= y <= (self.height-self.marginH+15):
				self.camRangeY = self.height-y

	# learned from https://docs.opencv.org/master/d9/df8/tutorial_root.html
	def dealSnap(self):
		gray = cv2.cvtColor(np.float32(self.snap), cv2.COLOR_BGR2GRAY)
		# ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
		thresh = cv2.adaptiveThreshold(np.uint8(gray), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 145, 15)
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
		# make the contour more clear
		erode = cv2.erode(thresh, kernel)
		dilate = cv2.dilate(erode, kernel, iterations=1)

		contours, hierarchy = cv2.findContours(np.uint8(dilate), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
		self.contours = contours

	def penSize(self, x, y):
		if not (self.scrollY-20) <= y <= (self.scrollY+20): return
		if (x-10) < 590 or (x+10) > 690: return
		midX, dis = (595+685)/2, 685-595
		self.drSize = ((x-midX)/dis) * 6 + 4
		self.scrollX = x

	def drawPen(self, x, y):
		if not (self.drx1+8) <= x <= (self.drx2-8): return
		if not (self.dry1+8) <= y <= (self.dry2-8): return
		if (self.moveMode or self.resizeMode or self.rotateMode or self.drawMove or self.drawResize or self.drawRotate or self.drawFlipH or self.drawFlipV or self.outputMode):
			return
		# fill up all the gaps between the last dot and the current dot
		if self.drawLine[self.trackLine] != []:
			x0, y0 = self.drawLine[self.trackLine][-1]
			xr = (x - x0)/45
			yr = (y - y0)/45
			xi, yi = x0+xr, y0+yr
			while not almostEqual(xi, x):
				self.drawLine[self.trackLine].append((xi, yi))
				xi, yi = xi+xr, yi+yr
				if self.retrieve:
					self.pencolors.append(self.bgColor)
					self.pensizes.append(self.eraseR)
				else:
					self.pencolors.append(self.drColor)
					self.pensizes.append(self.drSize)
		else:
			self.drawLine[self.trackLine].append((x, y))

	def timerFired(self):
		if self.cameraOn:
			self.cameraFired()

	# modified from http://www.cs.cmu.edu/~112/index.html
	def getSnapshot2(self):
		if self.camFixed:
			rW, rH = self.marginW*2+20, self.marginH*2.1
		else:
			rW, rH = self.camRangeX*2-10, self.camRangeY*2.1+42
		self._showRootWindow()
		x0 = self._root.winfo_rootx() + self._canvas.winfo_x()
		y0 = self._root.winfo_rooty() + self._canvas.winfo_y()
		result = ImageGrabber.grab((x0+rW,y0+40+rH,self.width*2-rW, self.height*2.1+20-rH))
		return result

	def rotateSnap(self):
		if not self.rotateMode: return
		if self.contours == None: return
		cx, cy = (self.xL+self.xR)/2, (self.yT+self.yB)/2
		# xnew = (x1 - cx)*cos(θ) - (y1 - cy)*sin(θ) + cx
		# ynew = (x1 - cx)*sin(θ) + (y1 - cy)*cos(θ) + cy
		angle = (self.angle/180)*math.pi
		for i in range(1, len(self.contours)):
			cont = self.contours[i]
			for j in range(0, len(cont)):
				cordi = cont[j]
				x, y = cordi[0][0], cordi[0][1]
				x1 = (x-cx)*math.cos(angle) - (y-cy)*math.sin(angle) + cx 
				y1 = (x-cx)*math.sin(angle) + (y-cy)*math.cos(angle) + cy
				self.contours[i][j][0] = (x1, y1)

	def resizeSnap(self, x, y):
		if not self.resizeMode: return
		if self.contours == None: return
		if not self.drx1 <= x <= self.drx2: return
		if not self.dry1 <= y <= self.dry2: return
		cx, cy = (self.xL+self.xR)/2+self.disMoveX, (self.yT+self.yB)/2+self.disMoveY
		x3, y3, x4, y4 = (self.xL-cx)*self.probX+cx+self.disMoveX, (self.yT-cy)*self.probY+cy+self.disMoveY, (self.xR-cx)*self.probX+cx+self.disMoveX, (self.yB-cy)*self.probY+cy+self.disMoveY
		disX, disY = (x4-x3)/2, (y4-y3)/2
		# four corners
		if (x3-50) <= x <= (x3+50) and (y3-50) <= y <= (y3+50):
			moveX = (x3 - x)
			moveY = (y3 - y)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.probX = self.probY = prob
		elif (x3-50) <= x <= (x3+50) and (y4-50) <= y <= (y4+50):
			moveX = (x3 - x)
			moveY = (y - y4)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.probX = self.probY = prob
		elif (x4-50) <= x <= (x4+50) and (y3-50) <= y <= (y3+50):
			moveX = (x - x4)
			moveY = (y3 - y)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.probX = self.probY = prob
		elif (x4-50) <= x <= (x4+50) and (y4-50) <= y <= (y4+50):
			moveX = (x - x4)
			moveY = (y - y4)
			probX, probY = (moveX+disX) / disX, (moveY+disY) / disY
			prob = max(probX, probY)
			self.probX = self.probY = prob
		# leftside x
		elif (x3-80) <= x < x3:
			moveX = (x3 - x)
			self.probX = (moveX+disX) / disX
		elif (x3+5) < x <= (x3+80):
			moveX = (x3+5 - x)
			self.probX = (moveX+disX) / disX
		# rightside x
		elif (x4-80) <= x < (x4-5) :
			moveX = (x - (x4-5))
			self.probX = (moveX+disX) / disX
		elif x4 < x <= (x4+80) :
			moveX = (x - x4)
			self.probX = (moveX+disX) / disX
		# upside y
		elif (y3-80) <= y < y3:
			moveY = (y3 - y)
			self.probY = (moveY+disY) / disY
		elif (y3+5) < y <= (y3+80):
			moveY = (y3+5 - y)
			self.probY = (moveY+disY) / disY
		# downside y
		elif (y4-5-40) <= y < (y4-5):
			moveY = (y - (y4-5))
			self.probY = (moveY+disY) / disY
		elif y4 < y <= (y4+80):
			moveY = (y - y4)
			self.probY = (moveY+disY) / disY

	def drawSnap(self, canvas):
		if self.contours == None:  return
		cx, cy = (self.xL+self.xR)/2+self.disMoveX, (self.yT+self.yB)/2+self.disMoveY
		disR = ((self.xR-self.xL)**2 + (self.yB-self.yT)**2)**0.5
		for i in range(1, len(self.contours)):
			cont = self.contours[i]
			for cordi in cont:
				x, y = cordi[0][0]+(self.drx1+self.drx2)*0.24/2, cordi[0][1]+(self.dry1+self.dry2)*0.5/2
				x = (x-cx)*self.probX+cx+self.disMoveX
				y = (y-cy)*self.probY+cy+self.disMoveY
				if self.flipH:
					if x > cx:
						x = x - (x-cx)*2
					elif x < cx:
						x = x + (cx-x)*2
				elif self.flipV:
					if y > cy:
						y = y - (y-cy)*2
					elif y < cy:
						y = y + (cy-y)*2
				x1, x2 = x-2*self.probX, x+2*self.probX
				y1, y2 = y-2*self.probY, y+2*self.probY
				canvas.create_oval(x1, y1, x2, y2, fill=self.contourColor, width=0)
		
		x3, y3, x4, y4 = (self.xL-cx)*self.probX+cx+self.disMoveX, (self.yT-cy)*self.probY+cy+self.disMoveY, (self.xR-cx)*self.probX+cx+self.disMoveX, (self.yB-cy)*self.probY+cy+self.disMoveY
		if self.moveMode:
			canvas.create_rectangle(x3, y3, x4, y4, outline='lightGreen', width=5)
		elif self.resizeMode:
			canvas.create_rectangle(x3, y3, x4, y4, outline='yellow2', width=5)
			rx1, ry1, rx2, ry2 = x3, y3, x4, y3
			rx3, ry3, rx4, ry4 = x3, y4, x4, y4
			canvas.create_oval(rx1-10, ry1-10, rx1+10, ry1+10, fill='lightGreen', width=0)
			canvas.create_oval(rx2-10, ry2-10, rx2+10, ry2+10, fill='lightGreen', width=0)
			canvas.create_oval(rx3-10, ry3-10, rx3+10, ry3+10, fill='lightGreen', width=0)
			canvas.create_oval(rx4-10, ry4-10, rx4+10, ry4+10, fill='lightGreen', width=0)

	# modified from http://www.cs.cmu.edu/~112/index.html
	def getSnapshot(self):
		self._showRootWindow()
		x0 = self._root.winfo_rootx() + self._canvas.winfo_x()
		y0 = self._root.winfo_rooty() + self._canvas.winfo_y()
		x1, y1 = x0+self.drx1+45, y0+self.dry1+155
		x2, y2 = x0+self.drx2*2-10, y0+self.dry2*2+40
		result = ImageGrabber.grab((x1, y1, x2, y2))
		return result

	def findSnapRange(self):
		if self.contours == None: return
		xL, xR, yT, yB = self.drx2, self.drx1, self.dry2, self.dry1
		for i in range(1, len(self.contours)):
			cont = self.contours[i]
			for cordi in cont:
				x, y = cordi[0][0]+(self.drx1+self.drx2)*0.24/2, cordi[0][1]+(self.dry1+self.dry2)*0.5/2
				if x < xL: xL = x
				if x > xR: xR = x
				if y < yT: yT = y
				if y > yB: yB = y
		self.xL, self.yT, self.xR, self.yB = xL-10, yT-10, xR+10, yB+10

	def mousePressed(self, event):
		if self.splash:
			# camera page
			if self.bx1 <= event.x <= self.bx2 and self.by1 <= event.y <= self.by2:
				self.splash = False
				self.cameraOn = True
			# upload
			elif self.bx3 <= event.x <= self.bx4 and self.by3 <= event.y <= self.by4:
				self.load = str(self.getUserInput('Input your image address:'))
				if self.load != None:
					self.dash = True
			# edit page
			elif self.bx5 <= event.x <= self.bx6 and self.by5 <= event.y <= self.by6:
				self.splash = False
				self.draw = True
			# draw page
			elif self.bx7 <= event.x <= self.bx8 and self.by7 <= event.y <= self.by8:
				self.help = True
				self.splash = False
		elif self.cameraOn:
			# camera back
			if self.lx1 <= event.x <= self.lx2 and self.ly1 <= event.y <= self.ly2:
				self.cameraOn = False
				self.splash = True
				MyApp.cameraParas(self)
			# fix scan pic
			elif self.mx1 <= event.x <= self.mx2 and self.my1 <= event.y <= self.my2:
				self.camFixed = True
				self.snap = self.getSnapshot2()
				self.snap = self.scaleImage(self.snap, 0.5)
			# snapshot convert
			elif self.rx3 <= event.x <= self.rx4 and self.ry3 <= event.y <= self.ry4:
				self.camFixed = False
				self.snap = self.getSnapshot2()
				self.snap = self.scaleImage(self.snap, 0.5)
				MyApp.dealSnap(self)
				self.cameraOn = False
				self.draw = True
				MyApp.findSnapRange(self)
		elif self.help:
			if self.lx1 <= event.x <= self.lx2 and self.ly1 <= event.y <= self.ly2:
				self.help = False
				self.splash = True
		elif self.draw:
			# create a new line list
			if ((self.drx1+8) <= event.x <= (self.drx2-8) and (self.dry1+8) <= event.y <= (self.dry2-8)):
				# move
				if self.drawMove and self.findTemp:
					self.tempx0, self.tempy0 = event.x, event.y
					self.findTemp = False
				elif self.drawMove and (not self.findTemp):
					self.moveLine = True
				# resize
				elif self.drawResize and self.findTemp:
					self.tempx0, self.tempy0 = event.x, event.y
					self.findTemp = False
				elif self.drawResize and (not self.findTemp):
					self.resizeLine = True
				# rotate
				elif self.drawRotate and self.findTemp:
					self.tempx0, self.tempy0 = event.x, event.y
					self.findTemp = False
				elif self.drawRotate and (not self.findTemp):
					self.rotateLine = True
				# flipH
				elif self.drawFlipH and self.findTemp:
					self.tempx0, self.tempy0 = event.x, event.y
					self.findTemp = False
				elif self.drawFlipH and (not self.findTemp):
					self.flipHLine = True
					MyApp.flipDrawLines(self)
				# flipV
				elif self.drawFlipV and self.findTemp:
					self.tempx0, self.tempy0 = event.x, event.y
					self.findTemp = False
				elif self.drawFlipV and (not self.findTemp):
					self.flipVLine = True
					MyApp.flipDrawLines(self)
				else:
					self.drawLine.append([])
					self.trackLine += 1
					self.pencolors.append(self.drColor)
					self.pensizes.append(self.drSize)
			# draw back
			elif self.lx1 <= event.x <= self.lx2 and self.ly1 <= event.y <= self.ly2:
				self.draw = False
				self.splash = True
				if not self.saveDraw:
					MyApp.drawParas(self)
					MyApp.cameraParas(self)
			# draw save
			elif self.rx3 <= event.x <= self.rx4 and self.ry3 <= event.y <= self.ry4:
				self.saveDraw = True
				MyApp.saveDrawing(self)
			# draw clear
			elif (((event.x-(self.clearx1+self.clearx2)/2)**2 + (event.y-(self.cleary1+self.cleary2)/2)**2)**0.5 <= 40):
				MyApp.drawParas(self)
				MyApp.cameraParas(self)
				self.draw = True
			elif (720 <= event.x <= 760 and self.height-60 <= event.y <= self.height-40): 
				self.retrieve = not self.retrieve
			elif (self.dpx1 <= event.x <= self.dpx2 and self.dpy1 <= event.y <= self.dpy2):
				self.moveMode = not self.moveMode
			elif (self.dpx3 <= event.x <= self.dpx4 and self.dpy3 <= event.y <= self.dpy4):
				self.resizeMode = not self.resizeMode
			elif (self.dpx5 <= event.x <= self.dpx6 and self.dpy5 <= event.y <= self.dpy6):
				self.rotateMode = not self.rotateMode
				self.angle = 0
			elif (self.dpx7 <= event.x <= self.dpx8 and self.dpy7 <= event.y <= self.dpy8):
				self.flipH = not self.flipH
			elif (self.dpx9 <= event.x <= self.dpx10 and self.dpy9 <= event.y <= self.dpy10):
				self.flipV = not self.flipV
			elif (self.dpx11 <= event.x <= self.dpx12 and self.dpy11 <= event.y <= self.dpy12):
				self.bgMode = not self.bgMode
				MyApp.drawColorCheck(self, event.x, event.y)
			elif (self.dpx13 <= event.x <= self.dpx14 and self.dpy13 <= event.y <= self.dpy14):
				if self.outputMode:
					self.saveSnapshot()
			# change drawing lines
			elif (((event.x-(self.dpx1-80+self.dpx2-160)/2)**2 + (event.y-(self.dpy1+10+self.dpy2-10)/2)**2)**0.5 <= 40):
				self.drawMove = not self.drawMove
				if not self.findTemp:
					MyApp.changeTempParas(self)
					self.drawMoveX, self.drawMoveY = 0, 0
					self.moveLine = False
			elif (((event.x-(self.dpx3-80+self.dpx4-160)/2)**2 + (event.y-(self.dpy3+10+self.dpy4-10)/2)**2)**0.5 <= 40):
				self.drawResize = not self.drawResize
				if not self.findTemp:
					MyApp.changeTempParas(self)
					self.drawprobX, self.drawprobY = 1, 1
					self.resizeLine = False
			elif (((event.x-(self.dpx5-80+self.dpx6-160)/2)**2 + (event.y-(self.dpy5+10+self.dpy6-10)/2)**2)**0.5 <= 40):
				self.drawRotate = not self.drawRotate
				if not self.findTemp:
					MyApp.changeTempParas(self)
					self.rotateLine = False
					self.roAngle = 0
			elif (((event.x-(self.dpx7-80+self.dpx8-160)/2)**2 + (event.y-(self.dpy7+10+self.dpy8-10)/2)**2)**0.5 <= 40):
				self.drawFlipH = not self.drawFlipH
				if not self.findTemp:
					MyApp.changeTempParas(self)
					self.flipHLine = False
			elif (((event.x-(self.dpx9-80+self.dpx10-160)/2)**2 + (event.y-(self.dpy9+10+self.dpy10-10)/2)**2)**0.5 <= 40):
				self.drawFlipV = not self.drawFlipV
				if not self.findTemp:
					MyApp.changeTempParas(self)
					self.flipVLine = False
			elif (((event.x-(self.dpx11-80+self.dpx12-160)/2)**2 + (event.y-(self.dpy11+10+self.dpy12-10)/2)**2)**0.5 <= 40):
				self.contourMode = not self.contourMode
				MyApp.drawColorCheck(self, event.x, event.y)
			elif (((event.x-(self.dpx13-80+self.dpx14-160)/2)**2 + (event.y-(self.dpy13+10+self.dpy14-10)/2)**2)**0.5 <= 40):
				self.outputMode = not self.outputMode
			else:
				MyApp.drawColorCheck(self, event.x, event.y)
				MyApp.resizeSnap(self, event.x, event.y)

	def changeTempParas(self):
		self.tempx0 = self.tempy0 = -1
		self.tempx1 = self.tempy1 = -1
		self.tempF = []
		self.findTemp = True

	def moveSnap(self, x, y):
		if not self.moveMode: return
		if self.contours ==  None: return
		cx, cy = (self.xL+self.xR)/2, (self.yT+self.yB)/2
		if (self.xL-20) <= x <= (self.xR+20):
			leftside = self.xL+10+(x-cx)
			rightside = self.xR-10+(x-cx)
			if leftside >= self.drx1 and rightside <= self.drx2:
				self.disMoveX = x-cx
		if (self.yT-20) <= y <= (self.yB+20):
			topside = self.yT+10+(y-cy)
			bottomside = self.yB-10+(y-cy)
			if topside >= self.dry1 and bottomside <= self.dry2:
				self.disMoveY = y-cy

	def drawColorCheck(self, x, y):
		if self.cxF <= x <= self.cxF+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'firebrick1'
			elif self.contourMode: self.contourColor = 'firebrick1'
			else: self.drColor = 'firebrick1'
		elif self.cxI <= x <= self.cxI+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'IndianRed1'
			elif self.contourMode: self.contourColor = 'IndianRed1'
			else: self.drColor = 'IndianRed1'
		elif self.cxS <= x <= self.cxS+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'salmon1'
			elif self.contourMode: self.contourColor = 'salmon1'
			else: self.drColor = 'salmon1'
		elif self.cxC <= x <= self.cxC+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'chocolate1'
			elif self.contourMode: self.contourColor = 'chocolate1'
			else: self.drColor = 'chocolate1'
		elif self.cxOr <= x <= self.cxOr+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'orange'
			elif self.contourMode: self.contourColor = 'orange'
			else: self.drColor = 'orange'
		elif self.cxGo <= x <= self.cxGo+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'gold'
			elif self.contourMode: self.contourColor = 'gold'
			else: self.drColor = 'gold'
		elif self.cxY <= x <= self.cxY+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'yellow2'
			elif self.contourMode: self.contourColor = 'yellow2'
			else: self.drColor = 'yellow2'
		elif self.cxK <= x <= self.cxK+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'khaki1'
			elif self.contourMode: self.contourColor = 'khaki1'
			else: self.drColor = 'khaki1'
		elif self.cxA <= x <= self.cxA+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'antique white'
			elif self.contourMode: self.contourColor = 'antique white'
			else: self.drColor = 'antique white'
		elif self.cxG <= x <= self.cxG+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'green2'
			elif self.contourMode: self.contourColor = 'green2'
			else: self.drColor = 'green2'
		elif self.cxSg <= x <= self.cxSg+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'spring green'
			elif self.contourMode: self.contourColor = 'spring green'
			else: self.drColor = 'spring green'
		elif self.cxPg <= x <= self.cxPg+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'pale green'
			elif self.contourMode: self.contourColor = 'pale green'
			else: self.drColor = 'pale green'
		elif self.cxSn <= x <= self.cxSn+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'snow'
			elif self.contourMode: self.contourColor = 'snow'
			else: self.drColor = 'snow'
		elif self.cxS <= x <= self.cxS+30 and self.cfl <= y <= self.cfl+30:
			if self.bgMode: self.bgColor = 'salmon1'
			elif self.contourMode: self.contourColor = 'salmon1'
			else: self.drColor = 'salmon1'
		elif self.cxAq <= x <= self.cxAq+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'aquamarine2'
			elif self.contourMode: self.contourColor = 'aquamarine2'
			else: self.drColor = 'aquamarine2'
		elif self.cxT <= x <= self.cxT+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'turquoise'
			elif self.contourMode: self.contourColor = 'turquoise'
			else: self.drColor = 'turquoise'
		elif self.cxDt <= x <= self.cxDt+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'dark turquoise'
			elif self.contourMode: self.contourColor = 'dark turquoise'
			else: self.drColor = 'dark turquoise'
		elif self.cxDs <= x <= self.cxDs+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'DeepSkyBlue2'
			elif self.contourMode: self.contourColor = 'DeepSkyBlue2'
			else: self.drColor = 'DeepSkyBlue2'
		elif self.cxDo <= x <= self.cxDo+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'DodgerBlue2'
			elif self.contourMode: self.contourColor = 'DodgerBlue2'
			else: self.drColor = 'DodgerBlue2'
		elif self.cxSb <= x <= self.cxSb+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'SlateBlue1'
			elif self.contourMode: self.contourColor = 'SlateBlue1'
			else: self.drColor = 'SlateBlue1'
		elif self.cxMp <= x <= self.cxMp+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'MediumPurple1'
			elif self.contourMode: self.contourColor = 'MediumPurple1'
			else: self.drColor = 'MediumPurple1'
		elif self.cxMo <= x <= self.cxMo+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'medium orchid'
			elif self.contourMode: self.contourColor = 'medium orchid'
			else: self.drColor = 'medium orchid'
		elif self.cxHp <= x <= self.cxHp+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'HotPink1'
			elif self.contourMode: self.contourColor = 'HotPink1'
			else: self.drColor = 'HotPink1'
		elif self.cxPv <= x <= self.cxPv+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'PaleVioletRed1'
			elif self.contourMode: self.contourColor = 'PaleVioletRed1'
			else: self.drColor = 'PaleVioletRed1'
		elif self.cxOc <= x <= self.cxOc+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'orchid2'
			elif self.contourMode: self.contourColor = 'orchid2'
			else: self.drColor = 'orchid2'
		elif self.cxRb <= x <= self.cxRb+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'RosyBrown1'
			elif self.contourMode: self.contourColor = 'RosyBrown1'
			else: self.drColor = 'RosyBrown1'
		elif self.cxB <= x <= self.cxB+30 and self.csl <= y <= self.csl+30:
			if self.bgMode: self.bgColor = 'black'
			elif self.contourMode: self.contourColor = 'black'
			else: self.drColor = 'black'

	def drawSplashPage(self, canvas):
		canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.img1))
		canvas.create_text(self.width/2, self.height/2-100, text='Drawing Black Box', font='Baloo 98', fill='steel blue')
		canvas.create_rectangle(self.bx1, self.by1, self.bx2, self.by2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx1+self.bx2)/2, (self.by1+self.by2)/2, text='Scan', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx3, self.by3, self.bx4, self.by4, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx3+self.bx4)/2, (self.by4+self.by3)/2, text='Upload', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx5, self.by5, self.bx6, self.by6, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx5+self.bx6)/2, (self.by5+self.by6)/2, text='Draw', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx7, self.by7, self.bx8, self.by8, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx7+self.bx8)/2, (self.by7+self.by8)/2, text='Help', font='Baloo 38', fill='steel blue')

	def drawCameraPage(self, canvas):
		canvas.create_rectangle(0, 0, self.width, self.marginH, fill='SkyBlue1', width=0)
		canvas.create_rectangle(0, self.height, self.width, self.height-self.marginH, fill='SkyBlue1', width=0)
		canvas.create_rectangle(0, 0, self.marginW, self.height, fill='SkyBlue1', width=0)
		canvas.create_rectangle(self.width-self.marginW, 0, self.width, self.height, fill='SkyBlue1', width=0)
		# draw snapshot
		if self.camFixed:
			canvas.create_rectangle(0, 0, self.width, self.height-self.marginH, fill='SkyBlue1', width=0)
			canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.snap))
		# snapshot range
		canvas.create_rectangle(self.camRangeX-15, self.camRangeY+15, self.width-self.camRangeX+15, self.height-self.camRangeY-15, outline='lightGreen', width=10)
		canvas.create_rectangle(self.lx1, self.ly1, self.lx2, self.ly2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.lx1+self.lx2)/2, (self.ly1+self.ly2)/2, text='Back', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.rx3, self.ry3, self.rx4, self.ry4, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.rx3+self.rx4)/2, (self.ry3+self.ry4)/2, text='Convert', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.mx1, self.my1, self.mx2, self.my2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.mx1+self.mx2)/2, (self.ry3+self.ry4)/2, text='OK', font='Baloo 28', fill='steel blue')

	def drawHelpboard(self, canvas):
		# canvas.create_image(0, 0, anchor = NW, image = img)
		canvas.create_rectangle(0, 0, self.width, self.height, fill='SkyBlue1')
		canvas.create_text(self.width/2, 52, text='Help Instruction', font='Baloo 48', fill='steel blue')
		canvas.create_text(80, 90, text='* Scan:', font='Baloo 30', fill='MediumPurple1', anchor='nw')
		canvas.create_text(220, 90, text='click "Scan" button,  then click "OK" button to catch a moment', font='Baloo 27', fill='lavender', anchor='nw')
		canvas.create_text(220, 120, text='use the green frame to select the range,  then click "Convert" to extract contours', font='Baloo 27', fill='lavender', anchor='nw')
		canvas.create_text(80, 150, text='* Upload:', font='Baloo 30', fill='MediumPurple1', anchor='nw')
		# "* Draw: "
		# "See the yellow message on the top for each button's function."
		# "You have to click the circle on the left of 'Output'button to open the output mode"
		# "Then click 'Output' button to save your drawing on your computer"
		# canvas.create_text(220, 150, text='click "Scan" button,  then click "OK" button to catch a moment', font='Baloo 27', fill='lavender', anchor='nw')
		# canvas.create_text(80, 150, text='* Upload:', font='Baloo 30', fill='MediumPurple1', anchor='nw')
		# canvas.create_text(80, 150, text='* Upload:', font='Baloo 30', fill='MediumPurple1', anchor='nw')
		# back button
		canvas.create_rectangle(self.lx1, self.ly1, self.lx2, self.ly2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.lx1+self.lx2)/2, (self.ly1+self.ly2)/2, text='Back', font='Baloo 28', fill='steel blue')

	def drawDrawPage(self, canvas):
		canvas.create_rectangle(0, 0, self.width, self.height, fill='SkyBlue1')
		canvas.create_rectangle(self.drx1, self.dry1, self.drx2, self.dry2, fill=self.bgColor, width=8, outline='steel blue')
		# back button
		canvas.create_rectangle(self.lx1, self.ly1, self.lx2, self.ly2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.lx1+self.lx2)/2, (self.ly1+self.ly2)/2, text='Back', font='Baloo 28', fill='steel blue')
		canvas.create_text(self.width-230, 50, text='Drawing Board', font='Baloo 55', fill='steel blue')
		canvas.create_rectangle(self.rx3, self.ry3, self.rx4, self.ry4, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.rx3+self.rx4)/2, (self.ry3+self.ry4)/2, text='Save', font='Baloo 28', fill='steel blue')
		# adjust pensize line
		canvas.create_rectangle(590, self.height-45, 690, self.height-40, fill='steel blue', width=0)
		canvas.create_rectangle(590, self.height-53, 595, self.height-32, fill='steel blue', width=0)
		canvas.create_rectangle(685, self.height-53, 690, self.height-32,  fill='steel blue', width=0)
		pcx, pcy = (595+685)/2, self.height-75
		canvas.create_oval(pcx-self.drSize, pcy-self.drSize, pcx+self.drSize, pcy+self.drSize, fill=self.drColor, width=0)
		canvas.create_rectangle(self.scrollX-7, self.scrollY-7, self.scrollX+7, self.scrollY+7, fill='steel blue', width=3, outline='lavender')
		color1, color2 = 'white', 'yellow2'
		# buttons on the right side
		canvas.create_rectangle(self.dpx1-100, self.dpy1-25, self.dpx14+5, self.dpy1-20, fill='lavender', width=0)
		canvas.create_rectangle(self.dpx1, self.dpy1, self.dpx2, self.dpy2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.dpx1+self.dpx2)/2, (self.dpy1+self.dpy2)/2, text='Move', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.dpx3, self.dpy3, self.dpx4, self.dpy4, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.dpx3+self.dpx4)/2, (self.dpy3+self.dpy4)/2, text='Resize', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.dpx5, self.dpy5, self.dpx6, self.dpy6, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.dpx5+self.dpx6)/2, (self.dpy5+self.dpy6)/2, text='Rotate', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.dpx7, self.dpy7, self.dpx8, self.dpy8, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.dpx7+self.dpx8)/2, (self.dpy7+self.dpy8)/2, text='FlipH', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.dpx9, self.dpy9, self.dpx10, self.dpy10, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.dpx9+self.dpx10)/2, (self.dpy9+self.dpy10)/2, text='FlipV', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.dpx11, self.dpy11, self.dpx12, self.dpy12, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.dpx11+self.dpx12)/2, (self.dpy11+self.dpy12)/2, text='BGColor', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.dpx13, self.dpy13, self.dpx14, self.dpy14, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.dpx13+self.dpx14)/2, (self.dpy13+self.dpy14)/2, text='Output', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.dpx13-100, self.dpy14+20, self.dpx14+5, self.dpy14+25, fill='lavender', width=0)
		canvas.create_oval(self.clearx1, self.cleary1, self.clearx2, self.cleary2, fill='red', width=0)

		# for adjusting drawing lines
		if not self.drawMove:
			canvas.create_oval(self.dpx1-80, self.dpy1+10, self.dpx2-160, self.dpy2-10, fill='steel blue', width=0)
		if self.drawMove:
			canvas.create_oval(self.dpx1-85, self.dpy1+5, self.dpx2-155, self.dpy2-5, fill='steel blue', width=5, outline='yellow2')
		if not self.drawResize:
			canvas.create_oval(self.dpx3-80, self.dpy3+10, self.dpx4-160, self.dpy4-10, fill='lavender', width=0)
		if self.drawResize:
			canvas.create_oval(self.dpx3-85, self.dpy3+5, self.dpx4-155, self.dpy4-5, fill='lavender', width=5, outline='yellow2')
		if not self.drawRotate:
			canvas.create_oval(self.dpx5-80, self.dpy5+10, self.dpx6-160, self.dpy6-10, fill='steel blue', width=0)
		if self.drawRotate:
			canvas.create_oval(self.dpx5-85, self.dpy5+5, self.dpx6-155, self.dpy6-5, fill='steel blue', width=5, outline='yellow2')
		if not self.drawFlipH:
			canvas.create_oval(self.dpx7-80, self.dpy7+10, self.dpx8-160, self.dpy8-10, fill='lavender', width=0)
		if self.drawFlipH:
			canvas.create_oval(self.dpx7-85, self.dpy7+5, self.dpx8-155, self.dpy8-5, fill='lavender', width=5, outline='yellow2')
		if not self.drawFlipV:
			canvas.create_oval(self.dpx9-80, self.dpy9+10, self.dpx10-160, self.dpy10-10, fill='steel blue', width=0)
		if self.drawFlipV:
			canvas.create_oval(self.dpx9-85, self.dpy9+5, self.dpx10-155, self.dpy10-5, fill='steel blue', width=5, outline='yellow2')
		if not self.contourMode:
			canvas.create_oval(self.dpx11-80, self.dpy11+10, self.dpx12-160, self.dpy12-10, fill='lavender', width=0)
		if self.contourMode:
			canvas.create_oval(self.dpx11-85, self.dpy11+5, self.dpx12-155, self.dpy12-5, fill='lavender', width=5, outline='yellow2')
		if not self.outputMode:
			canvas.create_oval(self.dpx13-80, self.dpy13+10, self.dpx14-160, self.dpy14-10, fill='steel blue', width=0)
		if self.outputMode:
			canvas.create_oval(self.dpx13-85, self.dpy13+5, self.dpx14-155, self.dpy14-5, fill='steel blue', width=5, outline='yellow2')

		if self.retrieve:
			canvas.create_rectangle(720, self.height-60, 760, self.height-40, fill=color2, width=2, outline='gray3')
		if not self.retrieve:
			canvas.create_rectangle(720, self.height-60, 760, self.height-40, fill=color1, width=2, outline='gray3')

		# draw top instructions
		if self.moveMode:
			canvas.create_text(50, 32, text='Drag or press direction keys to move your contour.', font='Baloo 32', fill='yellow2', anchor='nw')
		elif self.resizeMode:
			canvas.create_text(50, 22, text='Drag or press direction keys to resize your contour.', font='Baloo 28', fill='yellow2', anchor='nw')
			canvas.create_text(50, 52, text='Press "+" to scale up and "=" to scale down:)', font='Baloo 28', fill='yellow2', anchor='nw')
		elif self.rotateMode:
			canvas.create_text(50, 32, text='Press direction keys:', font='Baloo 32', fill='yellow2', anchor='nw')
			canvas.create_text(400, 22, text='"<–-":  counterclockwise', font='Baloo 28', fill='yellow2', anchor='nw')
			canvas.create_text(400, 52, text='"–->":  clockwise', font='Baloo 28', fill='yellow2', anchor='nw')
		elif self.flipH:
			canvas.create_text(50, 32, text='Click "FlipH" to flip your contour horizontally.', font='Baloo 32', fill='yellow2', anchor='nw')
		elif self.flipV:
			canvas.create_text(50, 32, text='Click "FlipV" to flip your contour vertically.', font='Baloo 32', fill='yellow2', anchor='nw')
		elif self.bgMode:
			canvas.create_text(50, 32, text='Click color blocks to change your background color', font='Baloo 32', fill='yellow2', anchor='nw')
		# circles
		elif self.drawMove:
			canvas.create_text(50, 22, text='Select the part of drawing you want to move.', font='Baloo 28', fill='yellow2', anchor='nw')
			canvas.create_text(50, 52, text='Drag within the green frame to move your drawing.', font='Baloo 28', fill='yellow2', anchor='nw')
		elif self.drawResize:
			canvas.create_text(50, 22, text='Select the part of drawing you want to resize.', font='Baloo 28', fill='yellow2', anchor='nw')
			canvas.create_text(50, 52, text='Drag the green frame to resize your drawing.', font='Baloo 28', fill='yellow2', anchor='nw')
		elif self.drawRotate:
			canvas.create_text(50, 22, text='Select the part of drawing you want to rotate.', font='Baloo 28', fill='yellow2', anchor='nw')
			canvas.create_text(50, 52, text='Press "-->" :  clockwise;    "<--":  counterclockwise.', font='Baloo 28', fill='yellow2', anchor='nw')
		elif self.drawFlipH:
			canvas.create_text(50, 22, text='Select the part of drawing you want to flip.', font='Baloo 28', fill='yellow2', anchor='nw')
			canvas.create_text(50, 52, text='Click on the board to flip horizontally.', font='Baloo 28', fill='yellow2', anchor='nw')
		elif self.drawFlipV:
			canvas.create_text(50, 22, text='Select the part of drawing you want to flip.', font='Baloo 28', fill='yellow2', anchor='nw')
			canvas.create_text(50, 52, text='Click on the board to flip vertically.', font='Baloo 28', fill='yellow2', anchor='nw')
		elif self.contourMode:
			canvas.create_text(50, 32, text="Click color blocks to change your contour's color", font='Baloo 32', fill='yellow2', anchor='nw')
		elif self.outputMode:
			canvas.create_text(50, 32, text='Click "Output" to save your drawing on your computer.', font='Baloo 32', fill='yellow2', anchor='nw')
		elif self.retrieve:
			canvas.create_text(40, 32, text='Press "Up" to increase eraser size or "Down" to decrease.', font='Baloo 32', fill='yellow2', anchor='nw')

	def drawAllLines(self, canvas):
		i = 0
		if self.drawLine != []:
			for line in self.drawLine:
				for x, y in line:
					size = self.pensizes[i]
					canvas.create_oval(x-size, y-size, x+size, y+size, fill=self.pencolors[i], width=0)
					i += 1
		
	def redrawAll(self, canvas):
		if self.splash:
			MyApp.drawSplashPage(self, canvas)
		elif self.cameraOn:
			MyApp.drawCameraPage(self, canvas)
		elif self.help:
			MyApp.drawHelpboard(self, canvas)
		elif self.draw:
			MyApp.drawDrawPage(self, canvas)
			MyApp.drawSnap(self, canvas)
			MyApp.drawAllLines(self, canvas)
			MyApp.drawColors(self, canvas)
			MyApp.drawTempFrame(self, canvas)

if __name__ == "__main__":
	MyApp(width=1300, height=800)
	os._exit(0)
