from tkinter import Canvas, Button, Frame, messagebox
from rewrite import Game

class Menu():
	window = 0
	resolution = 0

	def __init__(self, window, resolution):
		self.window= window
		self.resolution = resolution
		self.create()


	def clearWindow(self):
		for widget in self.window.winfo_children():
			widget.destroy()


	def gameOver(self):
		ans = messagebox.askquestion("GAME OVER!", "Do you want to try again?")
		if ans.lower() == 'yes':
			self.startGame()
			

	def startGame(self):
		self.clearWindow()
		game = Game(self.window, self.resolution)
		game.create()
		self.gameOver()


	def create(self):
		new_frame = Frame(self.window)
		new_frame.pack()

		canvas = Canvas(new_frame, width=self.resolution[0], height=self.resolution[1], bg='black')
		canvas.pack()


		start_button = Button(canvas, text="START", padx=60, pady=30, bg='black', fg='yellow', command=self.startGame)
		start_button.place(relx=0.4, rely=0.2)

		options_button = Button(canvas, text="OPTIONS", padx=60, pady=30, bg='black', fg='yellow')
		options_button.place(relx=0.4, rely=0.4)

		exit_button = Button(canvas, text="EXIT", padx=60, pady=30, bg='black', fg='yellow')
		exit_button.place(relx=0.4, rely=0.6)

		return new_frame

