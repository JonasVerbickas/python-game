from tkinter import Canvas, Button, messagebox
from json import dumps, load


class Options():
    def __init__(self, frame, windowManager):
        self.frame = frame
        self.windowManager = windowManager
        self.create()

    def getOptions(self):
        option_file = open('options.json', 'r')
        data = load(option_file)
        option_file.close()
        return data

    def writeOptions(self):
        option_file = open('options.json', 'w')
        option_file.write(dumps(self.options))
        option_file.close()     

    def changeKeyPopUp(self):
        width = 300
        height = 250
        self.popup = Canvas(self.frame, width=width, height=height, bg='black')
        self.popup.place(relx=0.5, rely=0.4, anchor="center")
        self.popup.create_text(width/2, height/2, text="Press a key that you want to use", fill='white', font=("Arial", 20))
        self.popup.create_text(width/2, height/2+20, text="(Has to be alphanumeric)", fill='white', font=("Arial", 12))
        self.back_button.destroy()

    def changeUp(self, event):
        if event.char in self.options.values() and event.char != self.options['up']:
            messagebox.showwarning("Warning", "Key already in use!")
        elif event.char.isalnum():
            self.options['up'] = event.char
            self.frame.master.unbind("<Key>")
            self.writeOptions()
            self.windowManager.options()

    def waitForNewUp(self):
        self.changeKeyPopUp()
        self.frame.master.bind("<Key>", self.changeUp)

    def changeDown(self, event):
        if event.char in self.options.values() and event.char != self.options['down']:
            messagebox.showwarning("Warning", "Key already in use!")
        elif event.char.isalnum():
            self.options['down'] = event.char
            self.frame.master.unbind("<Key>")
            self.writeOptions()
            self.windowManager.options()

    def waitForNewDown(self):
        self.changeKeyPopUp()
        self.frame.master.bind("<Key>", self.changeDown)

    def changeBossKey(self, event):
        if event.char in self.options.values() and event.char != self.options['bosskey']:
            messagebox.showwarning("Warning", "Key already in use!")
        elif event.char.isalnum():
            self.options['bosskey'] = event.char
            self.windowManager.window.bind(self.options['bosskey'], self.windowManager.pressedBossKey)
            self.frame.master.unbind("<Key>")
            self.writeOptions()
            self.windowManager.options()

    def waitForNewBossKey(self):
        self.windowManager.window.unbind(self.options['bosskey'])
        self.changeKeyPopUp()
        self.frame.master.bind("<Key>", self.changeBossKey)

    def create(self):
        self.canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1])
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.windowManager.menu_image, anchor="nw")
        self.canvas.create_text(self.windowManager.getResolution()[0]/2, 60, text="OPTIONS", font=("Arial", 40, 'bold'))

        self.options = self.getOptions()

        self.options_grid = Canvas(self.canvas, width=500, height=500)
        self.options_grid.place(relx=0.5, rely=0.4, anchor="center")

        up_button = Button(self.options_grid, text=("Move Up: '%s'" % (self.options['up'])), bg='white', command=self.waitForNewUp, padx=60, pady=25)
        up_button.grid(row=0,pady=10, padx=10, sticky="nsew")

        down_button = Button(self.options_grid, text=("Move Down: '%s'" % (self.options['down'])), bg='white', command=self.waitForNewDown, padx=60, pady=25)
        down_button.grid(row=1,pady=5, padx=10, sticky="nsew")

        boss_button = Button(self.options_grid, text=("Boss Key: '%s'" % (self.options['bosskey'])), bg='white', command=self.waitForNewBossKey, padx=60, pady=25)
        boss_button.grid(row=2,pady=10, padx=10, sticky="nsew")

        self.back_button = Button(self.canvas, text="BACK", command=self.windowManager.menu, bg='white', padx=30, pady=20)
        self.back_button.place(relx=0.2, rely=0.15)
