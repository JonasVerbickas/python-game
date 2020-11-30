from tkinter import messagebox
from rewrite import Game
from menu import Menu
from leaderboard import LeaderBoard

class WindowManager():
	def __init__(self, window, resolution):
		self.window= window
		self.resolution = resolution
		self.menu()

	def clearWindow(self):
		for widget in self.window.winfo_children():
			widget.destroy()

	def gameOver(self):
		ans = messagebox.askquestion("GAME OVER!", "Do you want to try again?")
		if ans.lower() == 'yes':
			self.game()
		else:
			self.menu()

	def game(self):
		self.clearWindow()
		game = Game(self.window, self.resolution)
		self.gameOver()


	def menu(self):
		self.clearWindow()
		menu = Menu(self.window, self.resolution, self)


	def leaderboard(self):
		self.clearWindow()
		leaderboard = LeaderBoard(self.window, self.resolution, self)
		leaderboard.create()