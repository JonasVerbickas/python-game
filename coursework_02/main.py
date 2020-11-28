from tkinter import Tk, Frame
import menu
from rewrite import Game


RESOLUTION = (1280, 720)


def clearWindow(window):
	print(window.winfo_children())
	for widget in window.winfo_children():
		print(widget.winfo_children())
		widget.destroy()

if __name__ == "__main__":
	window = Tk()
	window.title("PEW PEW")
	window.geometry(str(RESOLUTION[0]) + 'x' + str(RESOLUTION[1]))
	game = Game(window, RESOLUTION)
	game.loadMap()
	# clearWindow(window)
	window.mainloop()