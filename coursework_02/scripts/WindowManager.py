from tkinter import Frame, messagebox, PhotoImage
from scripts.game import Game
from scripts.menu import Menu
from scripts.leaderboard import LeaderBoard
from scripts.options import Options
from scripts.bossKey import BossKey
from json import load


class WindowManager():
    def __init__(self, window, resolution):
        self.player_name = "ANON"
        self.window= window
        self.resolution = resolution
        self.boss_image = PhotoImage(file='assets/bosskey.gif')
        self.menu_image = PhotoImage(file='assets/newbackground.gif')
        self.createHiddenBossKey()
        option_file = open('options.json', 'r')
        self.window.bind(load(option_file)['bosskey'], self.pressedBossKey)
        option_file.close()
        self.menu()

    def getResolution(self):
        return self.resolution

    def clearWindow(self):
        for widget in self.window.winfo_children():
            if widget.winfo_ismapped():
                widget.destroy()

    def createCleanFrame(self):
        self.clearWindow()
        new_frame = Frame(self.window)
        new_frame.pack()
        return new_frame

    def gameOver(self):
        ans = messagebox.askquestion("GAME OVER!", "Do you want to try again?")
        if ans.lower() == 'yes':
            self.game()
        else:
            self.menu()

    def game(self):
        self.game_frame = self.createCleanFrame()
        game = Game(self.game_frame, self)

    def loadSavedGame(self):
        self.game_frame = self.createCleanFrame()
        game = Game(self.game_frame, self, True)

    def menu(self):
        new_frame = self.createCleanFrame()
        Menu(new_frame, self)

    def leaderboard(self):
        new_frame = self.createCleanFrame()
        leaderboard = LeaderBoard(new_frame, self)

    def options(self):
        new_frame = self.createCleanFrame()
        options = Options(new_frame, self)

    def openBossKeyInGame(self):
        new_frame = self.createCleanFrame()
        boss_key = BossKey(new_frame, self, True)

    def createHiddenBossKey(self):
        hidden_frame = BossKey(Frame(self.window), self)
        hidden_frame = hidden_frame.frame
        hidden_frame.pack_forget()

    def pressedBossKey(self, event):
        for frame in self.window.winfo_children():
            if frame.winfo_ismapped():
                frame.pack_forget()
            else:
                frame.pack()

    def quit(self):
        self.window.quit()
        self.window.destroy()
