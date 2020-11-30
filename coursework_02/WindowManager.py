from rewrite import Game
from menu import Menu

class WindowManager():
	window = 0
	resolution = 0
	usable_frames = ['menu', 'game']
	current_frame = 0

	def __init__(self, window, resolution):
		self.window= window
		self.resolution = resolution

	def clearWindow(self):
		for widget in self.window.winfo_children():
			widget.destroy()


	def load(frame_name):
		if frame_name in usable_frames:
			self.clearWindow()
			if frame_name == 'game':
				current_frame = Game(wi)
		else:
			raise ValueError("No such frame can be created!")
