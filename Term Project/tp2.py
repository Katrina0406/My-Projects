# cited from http://www.cs.cmu.edu/~112/index.html
from cmu_112_graphics import *

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

class MyApp(App):
	def appStarted(self):
		self.width = 1300
		self.height = 800
		self.cameraOn = False
		self.splash = True
		self.dash = False
		self.load = None
		self.buttonCam = False
		self.messages = ''
		self.saveMessage = False

		MyApp.drawParas(self)
		MyApp.buttonParas(self)
		MyApp.colorParas(self)

		self.img1 = self.loadImage('dash.jpeg')
		self.img1 = self.scaleImage(self.img1, 2.2)

		# textbox parameters
		self.tx1, self.ty1, self.tx2, self.ty2 = self.width/2-100, self.height/2-330, self.width/2+600, self.height/2+270

	def drawParas(self):
		self.drx1, self.dry1, self.drx2, self.dry2 = 35, 100, 850, 650
		self.drSize = 5
		self.drColor = 'black'
		self.pencolors = []
		self.draw = False
		self.drawLine = []
		self.trackLine = -1
		self.saveDraw = False

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

	def mouseDragged(self, event):
		MyApp.drawPen(self, event.x, event.y)

	def drawPen(self, x, y):
		if not (self.drx1+8) <= x <= (self.drx2-8): return
		if not (self.dry1+8) <= y <= (self.dry2-8): return
		# fill up all the gaps between the last dot and the current dot
		if self.drawLine[self.trackLine] != []:
			x0, y0 = self.drawLine[self.trackLine][-1]
			xr = (x - x0)/45
			yr = (y - y0)/45
			xi, yi = x0+xr, y0+yr
			while not almostEqual(xi, x):
				self.drawLine[self.trackLine].append((xi, yi))
				xi, yi = xi+xr, yi+yr
				self.pencolors.append(self.drColor)
		else:
			self.drawLine[self.trackLine].append((x, y))

	def timerFired(self):
		if self.cameraOn:
			self.cameraFired()

	def getSnapshot(self):
		x1, y1 = 80, 100
		self._showRootWindow()
		x0 = self._root.winfo_rootx() + self._canvas.winfo_x()
		y0 = self._root.winfo_rooty() + self._canvas.winfo_y()
		result = ImageGrabber.grab((x0+x1,y0+y1,self.width-x1, self.height-y1))
		return result

	def keyReleased(self, event):
		if event.key == 'Space':
			self.messages += ' '
		elif event.key == 'Enter':
			self.messages += '\n'
		elif event.key == 'Delete':
			self.messages = self.messages[:-1]
		else:
			self.messages += event.key

	def mousePressed(self, event):
		if self.splash:
			# camera page
			if self.bx1 <= event.x <= self.bx2 and self.by1 <= event.y <= self.by2:
				self.buttonCam = True
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
			# draw back
			elif self.lx1 <= event.x <= self.lx2 and self.ly1 <= event.y <= self.ly2:
				self.draw = False
				self.splash = True
				if not self.saveDraw:
					self.drawLine = []
					self.trackLine = -1
					self.pencolors = []
			# draw save
			elif self.rx3 <= event.x <= self.rx4 and self.ry3 <= event.y <= self.ry4:
				self.saveDraw = True
			else:
				MyApp.drawColorCheck(self, event.x, event.y)

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

	def checkSave(self):
		if not self.saveMessage:
			self.load = None
			self.messages = ''

	def drawSplashPage(self, canvas):
		canvas.create_image(self.width/2, self.height/2, image=ImageTk.PhotoImage(self.img1))
		# canvas.create_rectangle(0, 0, self.width, self.height, fill='SkyBlue1')
		canvas.create_text(self.width/2, self.height/2-100, text='Magic Converter', font='Baloo 98', fill='steel blue')

		canvas.create_rectangle(self.bx1, self.by1, self.bx2, self.by2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx1+self.bx2)/2, (self.by1+self.by2)/2, text='Scan', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx3, self.by3, self.bx4, self.by4, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx3+self.bx4)/2, (self.by4+self.by3)/2, text='Upload', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx5, self.by5, self.bx6, self.by6, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx5+self.bx6)/2, (self.by5+self.by6)/2, text='Edit', font='Baloo 38', fill='steel blue')
		canvas.create_rectangle(self.bx7, self.by7, self.bx8, self.by8, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.bx7+self.bx8)/2, (self.by7+self.by8)/2, text='Draw', font='Baloo 38', fill='steel blue')

	def drawCameraPage(self, canvas):
		if not self.buttonCam:
			return
		marginH, marginW = 100,80
		canvas.create_rectangle(0, 0, self.width, marginH, fill='SkyBlue1', width=0)
		canvas.create_rectangle(0, self.height, self.width, self.height-marginH, fill='SkyBlue1', width=0)
		canvas.create_rectangle(0, 0, marginW, self.height, fill='SkyBlue1', width=0)
		canvas.create_rectangle(self.width-marginW, 0, self.width, self.height, fill='SkyBlue1', width=0)
		canvas.create_rectangle(self.lx1, self.ly1, self.lx2, self.ly2, fill='lavender', width=8, outline='steel blue')
		canvas.create_text((self.lx1+self.lx2)/2, (self.ly1+self.ly2)/2, text='Back', font='Baloo 28', fill='steel blue')

	# def drawText(self):
	# 	canvas.create_text(self.tx1+20, self.ty1+20, text=self.messages, font='Arial 18', anchor='nw')

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
		
		i = 0
		if self.drawLine != []:
			for line in self.drawLine:
				for x, y in line:
					canvas.create_oval(x-self.drSize, y-self.drSize, x+self.drSize, y+self.drSize, fill=self.pencolors[i], width=0)
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
			MyApp.drawColors(self, canvas)

if __name__ == "__main__":
	MyApp(width=1300, height=800)
	os._exit(0)