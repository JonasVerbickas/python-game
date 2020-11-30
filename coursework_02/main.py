from tkinter import Tk
from WindowManager import WindowManager


RESOLUTION = (1280, 720)


if __name__ == "__main__":
	window = Tk()
	window.title("PEW PEW")
	window.geometry(str(RESOLUTION[0]) + 'x' + str(RESOLUTION[1]))
	window.configure(bg='black')
	windowManager = WindowManager(window, RESOLUTION)
	window.mainloop()