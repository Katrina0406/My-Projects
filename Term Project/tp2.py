# cited from http://www.cs.cmu.edu/~112/index.html
from cmu_112_graphics import *
import numpy as np
import math

# cited from http://www.cs.cmu.edu/~112/index.html
def almostEqual(d1, d2, epsilon=10**-7):
    return (abs(d2 - d1) < epsilon)

class MyApp(App):
	def appStarted(self):
		self.width = 1300
		self.height = 800
		self.cameraOn = False
		self.splash = True
		self.dash = False

		MyApp.drawParas(self)
		MyApp.buttonParas(self)
		MyApp.colorParas(self)
		MyApp.cameraParas(self)

		self.img1 = self.loadImage('dash.jpeg')
		self.img1 = self.scaleImage(self.img1, 2.2)

		# textbox parameters
		self.tx1, self.ty1, self.tx2, self.ty2 = self.width/2-100, self.height/2-330, self.width/2+600, self.height/2+270

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
		self.bgcolor = 'lavender'
		self.erase = False
		self.erases = set()
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
		self.dpx1, self.dpy1, self.dpx2, self.dpy2 = self.width-150, 100, self.width-30, 160
		self.dpx3, self.dpy3, self.dpx4, self.dpy4 = self.width-150, 190, self.width-30, 250
		self.dpx5, self.dpy5, self.dpx6, self.dpy6 = self.width-150, 280, self.width-30, 340
		self.dpx7, self.dpy7, self.dpx8, self.dpy8 = self.width-150, 370, self.width-30, 430
		self.dpx9, self.dpy9, self.dpx10, self.dpy10 = self.width-150, 460, self.width-30, 520

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

	def keyPressed(self, event):
		if event.key == 'q':
			self.quit()
		elif event.key == 'a':
			self.getSnapshot()
		elif event.key == 's':
			self.saveSnapshot()
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
					self.angle -= 10
				elif event.key == 'Right':
					self.angle += 10
		elif self.retrieve:
			if event.key == 'Up' and self.eraseR <= 20:
				self.eraseR += 3
			elif event.key == 'Down' and self.eraseR >=4 :
				self.eraseR -= 3

	def mouseDragged(self, event):
		if self.draw:
			MyApp.drawPen(self, event.x, event.y)
			MyApp.penSize(self, event.x, event.y)
			MyApp.eraseSnap(self, event.x, event.y)
			MyApp.moveSnap(self, event.x, event.y)
			MyApp.resizeSnap(self, event.x, event.y)
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
		if (self.moveMode or self.resizeMode or self.erase or self.rotateMode): 	return
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
					self.pencolors.append(self.bgcolor)
					self.pensizes.append(self.eraseR)
				else:
					self.pencolors.append(self.drColor)
					self.pensizes.append(self.drSize)
		else:
			self.drawLine[self.trackLine].append((x, y))

	def timerFired(self):
		if self.cameraOn:
			self.cameraFired()

	# cited from http://www.cs.cmu.edu/~112/index.html
	def getSnapshot(self):
		if self.camFixed:
			rW, rH = self.marginW*2+20, self.marginH*2.1
		else:
			rW, rH = self.camRangeX*2-10, self.camRangeY*2.1+42
		self._showRootWindow()
		x0 = self._root.winfo_rootx() + self._canvas.winfo_x()
		y0 = self._root.winfo_rooty() + self._canvas.winfo_y()
		result = ImageGrabber.grab((x0+rW,y0+40+rH,self.width*2-rW, self.height*2.1+20-rH))
		return result

	def eraseSnap(self, x, y):
		if not self.erase: return
		self.erases.add((x, y))
		for i in range(1, len(self.contours)):
			for cordi in self.contours[i]:
				if (cordi == [[x, y]]).all():
					self.contours[i] = np.delete(self.contours[i], [[x, y]])

	def resizeSnap(self, x, y):
		if not self.resizeMode: return
		if not self.drx1 <= x <= self.drx2: return
		if not self.dry1 <= y <= self.dry2: return
		cx, cy = (self.xL+self.xR)/2+self.disMoveX, (self.yT+self.yB)/2+self.disMoveY
		x3, y3, x4, y4 = (self.xL-cx)*self.probX+cx+self.disMoveX, (self.yT-cy)*self.probY+cy+self.disMoveY, (self.xR-cx)*self.probX+cx+self.disMoveX, (self.yB-cy)*self.probY+cy+self.disMoveY
		disR = ((self.xR-self.xL)**2 + (self.yB-self.yT)**2)**0.5
		theta3 = math.acos((x3-cx)/disR)
		x3 = cx + disR * math.cos(theta3+self.angle*math.pi/180)
		theta4 = math.acos((x4-cx)/disR)
		x4 = cx + disR * math.cos(theta4+self.angle*math.pi/180)
		theta5 = math.asin((y3-cy)/disR)
		y3 = cy + disR * math.sin(theta5+self.angle*math.pi/180)
		theta6 = math.asin((y4-cy)/disR)
		y4 = cy + disR * math.sin(theta6+self.angle*math.pi/180)
		disX, disY = (x3+x4)/2, (y3+y4)/2
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
		elif y4 < y <= (y4+40):
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
				theta = math.acos((x-cx)/disR)
				x = cx + disR * math.cos(theta+self.angle*math.pi/180)
				y = (y-cy)*self.probY+cy+self.disMoveY
				theta2 = math.asin((y-cy)/disR)
				y = cy + disR * math.sin(theta2+self.angle*math.pi/180)
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
				if (x, y) not in self.erases:
					canvas.create_oval(x1, y1, x2, y2, fill='black', width=0)
		
		x3, y3, x4, y4 = (self.xL-cx)*self.probX+cx+self.disMoveX, (self.yT-cy)*self.probY+cy+self.disMoveY, (self.xR-cx)*self.probX+cx+self.disMoveX, (self.yB-cy)*self.probY+cy+self.disMoveY
		theta3 = math.acos((x3-cx)/disR)
		x3 = cx + disR * math.cos(theta3+self.angle*math.pi/180)
		theta4 = math.acos((x4-cx)/disR)
		x4 = cx + disR * math.cos(theta4+self.angle*math.pi/180)
		theta5 = math.asin((y3-cy)/disR)
		y3 = cy + disR * math.sin(theta5+self.angle*math.pi/180)
		theta6 = math.asin((y4-cy)/disR)
		y4 = cy + disR * math.sin(theta6+self.angle*math.pi/180)
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
		elif self.rotateMode:
			canvas.create_rectangle(x3, y3, x4, y4, outline='MediumPurple2', width=5)
			rx1, ry1, rx2, ry2 = x3, y3, x4, y3
			rx3, ry3, rx4, ry4 = x3, y4, x4, y4
			canvas.create_oval(rx1-10, ry1-10, rx1+10, ry1+10, fill='HotPink1', width=0)
			canvas.create_oval(rx2-10, ry2-10, rx2+10, ry2+10, fill='HotPink1', width=0)
			canvas.create_oval(rx3-10, ry3-10, rx3+10, ry3+10, fill='HotPink1', width=0)
			canvas.create_oval(rx4-10, ry4-10, rx4+10, ry4+10, fill='HotPink1', width=0)


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
				self.dash = True
				self.splash = False
			# draw page
			elif self.bx7 <= event.x <= self.bx8 and self.by7 <= event.y <= self.by8:
				self.splash = False
				self.draw = True
		elif self.cameraOn:
			# camera back
			if self.lx1 <= event.x <= self.lx2 and self.ly1 <= event.y <= self.ly2:
				self.cameraOn = False
				self.splash = True
				MyApp.cameraParas(self)
			# fix scan pic
			elif self.mx1 <= event.x <= self.mx2 and self.my1 <= event.y <= self.my2:
				self.camFixed = True
				self.snap = self.getSnapshot()
				self.snap = self.scaleImage(self.snap, 0.5)
			# snapshot convert
			elif self.rx3 <= event.x <= self.rx4 and self.ry3 <= event.y <= self.ry4:
				self.camFixed = False
				self.snap = self.getSnapshot()
				self.snap = self.scaleImage(self.snap, 0.5)
				MyApp.dealSnap(self)
				self.cameraOn = False
				self.draw = True
				MyApp.findSnapRange(self)
		elif self.dash:
			# edit back
			if self.lx1 <= event.x <= self.lx2 and self.ly1 <= event.y <= self.ly2:
				self.dash = False
				self.splash = True
				MyApp.checkSave(self)
			elif self.rx3 <= event.x <= self.rx4 and self.ry3 <= event.y <= self.ry4:
				self.saveMessage = True
		elif self.draw:
			# create a new line list
			if ((self.drx1+8) <= event.x <= (self.drx2-8) and (self.dry1+8) <= event.y <= (self.dry2-8)):
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
			elif (720 <= event.x <= 750 and self.height-30 <= event.y <= self.height-20): 
				self.erase = not self.erase
			elif (720 <= event.x <= 750 and self.height-70 <= event.y <= self.height-60): 
				self.retrieve = not self.retrieve
			elif (self.dpx1 <= event.x <= self.dpx2 and self.dpy1 <= event.y <= self.dpy2):
				self.moveMode = not self.moveMode
			elif (self.dpx3 <= event.x <= self.dpx4 and self.dpy3 <= event.y <= self.dpy4):
				self.resizeMode = not self.resizeMode
			elif (self.dpx5 <= event.x <= self.dpx6 and self.dpy5 <= event.y <= self.dpy6):
				self.rotateMode = not self.rotateMode
			elif (self.dpx7 <= event.x <= self.dpx8 and self.dpy7 <= event.y <= self.dpy8):
				self.flipH = not self.flipH
			elif (self.dpx9 <= event.x <= self.dpx10 and self.dpy9 <= event.y <= self.dpy10):
				self.flipV = not self.flipV
			else:
				MyApp.drawColorCheck(self, event.x, event.y)
				MyApp.resizeSnap(self, event.x, event.y)

	def moveSnap(self, x, y):
		if not self.moveMode: return
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
			self.drColor = 'firebrick1'
		elif self.cxI <= x <= self.cxI+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'IndianRed1'
		elif self.cxS <= x <= self.cxS+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'salmon1'
		elif self.cxC <= x <= self.cxC+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'chocolate1'
		elif self.cxOr <= x <= self.cxOr+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'orange'
		elif self.cxGo <= x <= self.cxGo+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'gold'
		elif self.cxY <= x <= self.cxY+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'yellow2'
		elif self.cxK <= x <= self.cxK+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'khaki1'
		elif self.cxA <= x <= self.cxA+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'antique white'
		elif self.cxG <= x <= self.cxG+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'green2'
		elif self.cxSg <= x <= self.cxSg+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'spring green'
		elif self.cxPg <= x <= self.cxPg+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'pale green'
		elif self.cxSn <= x <= self.cxSn+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'snow'
		elif self.cxS <= x <= self.cxS+30 and self.cfl <= y <= self.cfl+30:
			self.drColor = 'salmon1'
		elif self.cxAq <= x <= self.cxAq+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'aquamarine2'
		elif self.cxT <= x <= self.cxT+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'turquoise'
		elif self.cxDt <= x <= self.cxDt+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'dark turquoise'
		elif self.cxDs <= x <= self.cxDs+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'DeepSkyBlue2'
		elif self.cxDo <= x <= self.cxDo+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'DodgerBlue2'
		elif self.cxSb <= x <= self.cxSb+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'SlateBlue1'
		elif self.cxMp <= x <= self.cxMp+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'MediumPurple1'
		elif self.cxMo <= x <= self.cxMo+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'medium orchid'
		elif self.cxHp <= x <= self.cxHp+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'HotPink1'
		elif self.cxPv <= x <= self.cxPv+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'PaleVioletRed1'
		elif self.cxOc <= x <= self.cxOc+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'orchid2'
		elif self.cxRb <= x <= self.cxRb+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'RosyBrown1'
		elif self.cxB <= x <= self.cxB+30 and self.csl <= y <= self.csl+30:
			self.drColor = 'black'

	def drawSplashPage(self, canvas):
		canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.img1))
		# canvas.create_rectangle(0, 0, self.width, self.height, fill='SkyBlue1')
		canvas.create_text(self.width/2, self.height/2-100, text='Drawing Black Box', font='Baloo 98', fill='steel blue')

		canvas.create_rectangle(self.bx1, self.by1, self.bx2, self.by2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx1+self.bx2)/2, (self.by1+self.by2)/2, text='Scan', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx3, self.by3, self.bx4, self.by4, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx3+self.bx4)/2, (self.by4+self.by3)/2, text='Upload', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx5, self.by5, self.bx6, self.by6, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx5+self.bx6)/2, (self.by5+self.by6)/2, text='Edit', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx7, self.by7, self.bx8, self.by8, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx7+self.bx8)/2, (self.by7+self.by8)/2, text='Draw', font='Baloo 38', fill='steel blue')

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

	def drawDashboard(self, canvas):
		# canvas.create_image(0, 0, anchor = NW, image = img)
		canvas.create_rectangle(0, 0, self.width, self.height, fill='SkyBlue1')
		canvas.create_rectangle(self.tx1, self.ty1, self.tx2, self.ty2, fill='lavender', width=8, outline='steel blue')
		# back button & save button
		canvas.create_rectangle(self.lx1, self.ly1, self.lx2, self.ly2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.lx1+self.lx2)/2, (self.ly1+self.ly2)/2, text='Back', font='Baloo 28', fill='steel blue')
		canvas.create_rectangle(self.rx3, self.ry3, self.rx4, self.ry4, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.rx3+self.rx4)/2, (self.ry3+self.ry4)/2, text='Save', font='Baloo 28', fill='steel blue')
		MyApp.drawText(self)

	def drawDrawPage(self, canvas):
		canvas.create_rectangle(0, 0, self.width, self.height, fill='SkyBlue1')
		canvas.create_rectangle(self.drx1, self.dry1, self.drx2, self.dry2, fill='lavender', width=8, outline='steel blue')
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

		if self.erase:
			canvas.create_rectangle(720, self.height-30, 750, self.height-20, fill=color2, width=0)
		if not self.erase:
			canvas.create_rectangle(720, self.height-30, 750, self.height-20, fill=color1, width=0)
		if self.retrieve:
			canvas.create_rectangle(720, self.height-70, 750, self.height-60, fill=color2, width=0)
		if not self.retrieve:
			canvas.create_rectangle(720, self.height-70, 750, self.height-60, fill=color1, width=0)

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
		elif self.dash:
			MyApp.drawDashboard(self, canvas)
		elif self.draw:
			MyApp.drawDrawPage(self, canvas)
			MyApp.drawSnap(self, canvas)
			MyApp.drawAllLines(self, canvas)
			MyApp.drawColors(self, canvas)

if __name__ == "__main__":
	MyApp(width=1300, height=800)
	os._exit(0)
