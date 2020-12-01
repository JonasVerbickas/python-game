from tkinter import Tk
from WindowManager import WindowManager


RESOLUTION = (1280, 720)


if __name__ == "__main__":
	window = Tk()
	window.title("PEW PEW")
	window.geometry(str(RESOLUTION[0]) + 'x' + str(RESOLUTION[1]))
	window.configure(bg='black')
	windowManager = WindowManager(window, RESOLUTION)
	while True: # makes sure that we stay in the main loop while in between menu pages (when old frame is being replace by the new one)
		window.update()
	window.mainloop()