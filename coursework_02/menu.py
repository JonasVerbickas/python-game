from tkinter import Canvas, Button, DISABLED
from os.path import isfile

class Menu():
	def __init__(self, frame, windowManager):
		self.frame= frame
		self.windowManager = windowManager
		self.create()


	def create(self):
		canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
		canvas.pack()


		resume_button = Button(canvas, text="RESUME", padx=60, pady=30, bg='black', fg='yellow', command=self.windowManager.loadSavedGame)
		resume_button.place(relx=0.4, rely=0.1)
		if not isfile('save.json'):
			resume_button['state'] = DISABLED

		start_new_button = Button(canvas, text="START", padx=60, pady=30, bg='black', fg='yellow', command=self.windowManager.game)
		start_new_button.place(relx=0.4, rely=0.3)

		leaderboard_button = Button(canvas, text="LEADERBOARD", padx=60, pady=30, bg='black', fg='yellow', command=self.windowManager.leaderboard)
		leaderboard_button.place(relx=0.4, rely=0.5)

		options_button = Button(canvas, text="OPTIONS", padx=60, pady=30, bg='black', fg='yellow', command=self.windowManager.options)
		options_button.place(relx=0.4, rely=0.7)

