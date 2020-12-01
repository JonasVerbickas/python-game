from tkinter import Frame, messagebox
from game import Game
from menu import Menu
from leaderboard import LeaderBoard
from options import Options

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
		self.game_frame = self.createCleanFrame()
		game = Game(self.game_frame, self)

	def menu(self):
		new_frame = self.createCleanFrame()
		Menu(new_frame, self)

	def saveAndQuit(self):
		self.menu()

	def leaderboard(self):
		new_frame = self.createCleanFrame()
		leaderboard = LeaderBoard(new_frame, self)

	def options(self):
		new_frame = self.createCleanFrame()
		options = Options(new_frame, self)


	def boss_key(self):
		pass # needs saving to be implemented