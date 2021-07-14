from tkinter import Label
from json import load


class BossKey():

    def loadGameFromBossKey(self, event):
        self.windowManager.loadSavedGame()

    def __init__(self, frame, windowManager, loadGame=False):
        self.frame = frame
        self.windowManager = windowManager
        self.create()
        if loadGame:
            with open('options.json', 'r') as f:
                keybind = load(f)['bosskey']
                self.frame.master.bind(keybind, self.loadGameFromBossKey)

    def create(self):
        self.label = Label(self.frame, image=self.windowManager.boss_image)
        self.label.pack()
