from tkinter import Canvas, Button
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

	def changeUp(self, event):
		if event.char.isalnum():
			self.options['up'] = event.char
			self.frame.master.unbind("<Key>")
			self.writeOptions()
			self.windowManager.options()

	def waitForNewUp(self):
		self.frame.master.bind("<Key>", self.changeUp)

	def changeDown(self, event):
		if event.char.isalnum():
			self.options['down'] = event.char
			self.frame.master.unbind("<Key>")
			self.writeOptions()
			self.windowManager.options()

	def waitForNewDown(self):
		self.frame.master.bind("<Key>", self.changeDown)

	def create(self):
		canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
		canvas.pack()

		canvas.create_text(self.windowManager.getResolution()[0]/2, 32, text="OPTIONS", font=("Arial", 32), fill='white')
		self.options = self.getOptions()
		
		up_button = Button(canvas, text=("Move Up: '%s'" % (self.options['up'])), command=self.waitForNewUp)
		up_button.place(relx=0.45, rely=0.3)

		down_button = Button(canvas, text=("Move Down: '%s'" % (self.options['down'])), command=self.waitForNewDown)
		down_button.place(relx=0.45, rely=0.4)

		back_button = Button(canvas, text="BACK", command=self.windowManager.menu)
		back_button.place(relx=0.05, rely=0.05)