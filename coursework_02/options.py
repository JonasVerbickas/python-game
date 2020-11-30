from tkinter import Canvas, Button
import json

class Options():
	def __init__(self, frame, windowManager):
		self.frame= frame
		self.windowManager = windowManager
		self.create()


	def getOptions(self):
		f = open('options.json', 'r')
		data = json.load(f)
		f.close()
		return data

	def writeOptions(self):
		f = open('options.json', 'w')
		print(json.dumps(self.options))
		f.write(json.dumps(self.options))
		f.close()		

	def changeUp(self, event):
		print(event.char)
		self.options['up'] = event.char
		self.frame.master.unbind("<Key>")
		self.writeOptions()
		self.windowManager.options()

	def waitForNewUp(self):
		self.frame.master.bind("<Key>", self.changeUp)

	def create(self):
		canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
		canvas.pack()

		canvas.create_text(self.windowManager.getResolution()[0]/2, 32, text="OPTIONS", font=("Arial", 32), fill='white')
		self.options = self.getOptions()
		
		up_button = Button(canvas, text=("Move Up: '%s'" % (self.options['up'])), command=self.waitForNewUp)
		up_button.place(x=self.windowManager.getResolution()[0]/2-50, y=200)
