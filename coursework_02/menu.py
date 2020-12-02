from tkinter import Canvas, Button, DISABLED, NW, Entry
from os.path import isfile

class Menu():
	def __init__(self, frame, windowManager):
		self.frame= frame
		self.windowManager = windowManager
		self.create()


	def startGameAndSaveName(self):
		self.windowManager.player_name = self.name_field.get()
		self.windowManager.game()

	def loadGameAndSaveName(self):
		self.windowManager.player_name = self.name_field.get()
		self.windowManager.loadSavedGame()


	def create(self):
		canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
		canvas.pack()

		canvas.create_image(0, 0, image=self.windowManager.menu_image, anchor=NW)

		self.name_field = Entry(self.frame)
		self.name_field.place(relx=0.4, rely=0.1)
		self.name_field.insert(0, 'ENTER NAME')

		resume_button = Button(canvas, text="RESUME", padx=60, pady=30, bg='sky blue', fg='black', command=self.loadGameAndSaveName)
		resume_button.place(relx=0.4, rely=0.2)
		if not isfile('save.json'):
			resume_button['state'] = DISABLED

		start_new_button = Button(canvas, text="START", padx=60, pady=30, bg='sky blue', fg='black', command=self.startGameAndSaveName)
		start_new_button.place(relx=0.405, rely=0.35)

		leaderboard_button = Button(canvas, text="LEADERBOARD", padx=60, pady=30, bg='sky blue', fg='black', command=self.windowManager.leaderboard)
		leaderboard_button.place(relx=0.385, rely=0.5)

		options_button = Button(canvas, text="OPTIONS", padx=60, pady=30, bg='sky blue', fg='black', command=self.windowManager.options)
		options_button.place(relx=0.4, rely=0.65)

