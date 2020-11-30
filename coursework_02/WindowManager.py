from tkinter import Frame, messagebox
from game import Game
from menu import Menu
from leaderboard import LeaderBoard

class WindowManager():
	def __init__(self, window, resolution):
		self.window= window
		self.resolution = resolution
		self.menu()

	def getResolution(self):
		return self.resolution

	def clearWindow(self):
		for widget in self.window.winfo_children():
			widget.destroy()

	def createCleanFrame(self):
		self.clearWindow()
		new_frame = Frame(self.window)
		new_frame.pack()
		return new_frame

	def gameOver(self):
		ans = messagebox.askquestion("GAME OVER!", "Do you want to try again?")
		if ans.lower() == 'yes':
			self.game()
		else:
			self.menu()

	def game(self):
		new_frame = self.createCleanFrame()
		game = Game(new_frame, self.resolution)
		self.gameOver()


	def menu(self):
		new_frame = self.createCleanFrame()
		Menu(new_frame, self.resolution, self)


	def leaderboard(self):
		new_frame = self.createCleanFrame()
		leaderboard = LeaderBoard(self.window, self)
		leaderboard.create()