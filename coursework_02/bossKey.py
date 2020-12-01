from tkinter import Canvas, Button

class BossKey():
	def __init__(self, frame, windowManager):
		self.frame= frame
		self.windowManager = windowManager
		self.create()


	def create(self):
		canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
		canvas.pack()
		canvas.create_text(500, 500, text='BOSS', font=('Arial', 32), fill='white')

