from tkinter import Tk
from menu import Menu


RESOLUTION = (1280, 720)


if __name__ == "__main__":
	window = Tk()
	window.title("PEW PEW")
	window.geometry(str(RESOLUTION[0]) + 'x' + str(RESOLUTION[1]))
	current_frame = Menu(window, RESOLUTION)
	window.mainloop()