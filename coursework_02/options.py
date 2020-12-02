from tkinter import Canvas, Button, NW
from json import dumps, load

class Options():
	def __init__(self, frame, windowManager):
		self.frame= frame
		self.windowManager = windowManager
		self.create()

	def getOptions(self):
		f = open('options.json', 'r')
		data = load(f)
		f.close()
		return data

	def writeOptions(self):
		f = open('options.json', 'w')
		f.write(dumps(self.options))
		f.close()		

	def changeKeyPopUp(self):
		width = 300
		height = 250
		self.popup = Canvas(self.frame, width=width, height=height, bg='black')
		self.popup.place(relx=0.38, rely=0.25)
		self.popup.create_text(width/2, height/2, text="Press a key that you want to use", fill='white', font=("Arial", 20))
		self.popup.create_text(width/2, height/2+20, text="(Has to be alphanumeric)", fill='white', font=("Arial", 12))

		self.back_button.destroy()


	def changeUp(self, event):
		if event.char.isalnum():
			self.options['up'] = event.char
			self.frame.master.unbind("<Key>")
			self.writeOptions()
			self.windowManager.options()

	def waitForNewUp(self):
		self.changeKeyPopUp()
		self.frame.master.bind("<Key>", self.changeUp)

	def changeDown(self, event):
		if event.char.isalnum():
			self.options['down'] = event.char
			self.frame.master.unbind("<Key>")
			self.writeOptions()
			self.windowManager.options()

	def waitForNewDown(self):
		self.changeKeyPopUp()
		self.frame.master.bind("<Key>", self.changeDown)

	def changeBossKey(self, event):
		if event.char.isalnum():
			self.options['bosskey'] = event.char
			self.windowManager.window.bind(self.options['bosskey'], self.windowManager.pressedBossKey)
			self.frame.master.unbind("<Key>")
			self.writeOptions()
			self.windowManager.options()

	def waitForNewBossKey(self):
		self.windowManager.window.unbind(self.options['bosskey'])
		self.changeKeyPopUp()
		self.frame.master.bind("<Key>", self.changeBossKey)

	def create(self):
		self.canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1])
		self.canvas.pack()
		self.canvas.create_image(0, 0, image=self.windowManager.menu_image, anchor=NW)
		self.canvas.create_text(self.windowManager.getResolution()[0]/2, 32, text="OPTIONS", font=("Arial", 32))

		self.options = self.getOptions()
		
		up_button = Button(self.canvas, text=("Move Up: '%s'" % (self.options['up'])), command=self.waitForNewUp, bg="sky blue", padx=10, pady=20)
		up_button.place(relx=0.456, rely=0.3)

		down_button = Button(self.canvas, text=("Move Down: '%s'" % (self.options['down'])), command=self.waitForNewDown, bg="sky blue", padx=10, pady=20)
		down_button.place(relx=0.45, rely=0.4)

		down_button = Button(self.canvas, text=("Boss Key: '%s'" % (self.options['bosskey'])), command=self.waitForNewBossKey, bg="sky blue", padx=10, pady=20)
		down_button.place(relx=0.458, rely=0.5)

		self.back_button = Button(self.canvas, text="BACK", command=self.windowManager.menu, bg="sky blue", padx=30, pady=20)
		self.back_button.place(relx=0.2, rely=0.15)