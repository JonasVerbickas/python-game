from tkinter import Canvas, Button

class Menu():
	def __init__(self, frame, windowManager):
		self.frame= frame
		self.windowManager = windowManager
		self.create()


	def create(self):
		canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
		canvas.pack()

		start_button = Button(canvas, text="START", padx=60, pady=30, bg='black', fg='yellow', command=self.windowManager.game)
		start_button.place(relx=0.4, rely=0.2)

		leaderboard_button = Button(canvas, text="LEADERBOARD", padx=60, pady=30, bg='black', fg='yellow', command=self.windowManager.leaderboard)
		leaderboard_button.place(relx=0.4, rely=0.4)

		options_button = Button(canvas, text="OPTIONS", padx=60, pady=30, bg='black', fg='yellow')
		options_button.place(relx=0.4, rely=0.6)

