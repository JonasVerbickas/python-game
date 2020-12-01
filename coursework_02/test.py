from tkinter import Tk, Canvas, Button, PhotoImage, NW

window = Tk()
img = PhotoImage("bosskey.gif")
b = Button(window, image=img, width=1000, height=1000)
b.pack()
window.mainloop()