from tkinter import Canvas, Button, Entry, DISABLED
from os.path import isfile


class Menu():
    def __init__(self, frame, windowManager):
        self.frame = frame
        self.windowManager = windowManager
        self.create()

    def startGameAndSaveName(self):
        self.windowManager.player_name = self.name_field.get()
        self.windowManager.game()

    def loadGameAndSaveName(self):
        self.windowManager.player_name = self.name_field.get()
        self.windowManager.loadSavedGame()

    def create(self):
        canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
        canvas.pack()

        canvas.create_image(0, 0, image=self.windowManager.menu_image, anchor="nw")

        self.name_field = Entry(self.frame)
        self.name_field.place(relx=0.5, rely=0.1, anchor="center")
        self.name_field.insert(0, 'ENTER NAME')

        resume_button = Button(canvas, text="RESUME", padx=60, pady=25, bg='white', fg='black', command=self.loadGameAndSaveName)
        resume_button.place(relx=0.5, rely=0.2, anchor="center")

        if not isfile('save.json'):
            resume_button['state'] = DISABLED

        start_new_button = Button(canvas, text="START", padx=60, pady=25, bg='white', fg='black', command=self.startGameAndSaveName)
        start_new_button.place(relx=0.5, rely=0.34, anchor="center")

        leaderboard_button = Button(canvas, text="LEADERBOARD", padx=60, pady=25, bg='white', fg='black', command=self.windowManager.leaderboard)
        leaderboard_button.place(relx=0.5, rely=0.48, anchor="center")

        options_button = Button(canvas, text="OPTIONS", padx=60, pady=25, bg='white', fg='black', command=self.windowManager.options)
        options_button.place(relx=0.5, rely=0.62, anchor="center")

        quit_button = Button(canvas, text="QUIT", padx=60, pady=25, bg='white', fg='black', command=self.windowManager.quit)
        quit_button.place(relx=0.5, rely=0.76, anchor="center")
