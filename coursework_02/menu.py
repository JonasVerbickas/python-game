from tkinter import Canvas, Button, Frame

def create(window):
	new_frame = Frame(window)
	new_frame.pack()

	start_button = Button(new_frame, text="START", width="300", height="300")
	start_button.pack()

	options_button = Button(new_frame, text="OPTIONS")
	options_button.pack()

	exit_button = Button(new_frame, text="EXIT")
	exit_button.pack()

	return new_frame