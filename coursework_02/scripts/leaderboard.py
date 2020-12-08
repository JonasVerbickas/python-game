from tkinter import Frame, Canvas, Button, Label
from os.path import isfile


class LeaderBoard():
    def getSortedListOfLeaders(self):
        list_of_leaders = []
        if isfile("leaderboard.txt"):
            leaderboard_file = open("leaderboard.txt", 'r')
            leaderboard_list = leaderboard_file.read().strip().split('\n')
            for key_val in leaderboard_list:
                key_val_split = key_val.split(':')
                for combo in list(list_of_leaders):
                    if int(key_val_split[1]) > int(combo[1]):
                        insert_index = list_of_leaders.index(combo)
                        list_of_leaders.insert(insert_index, key_val_split)
                        break
                else:
                    list_of_leaders.append(key_val_split)
            leaderboard_file.close()
        return list_of_leaders[:10]  # only the TOP 10

    def leaderList2String(self, leader_list):
        output = ""
        for i in range(len(leader_list)):
            output += ("%d. %s\n") % (i+1, ":  ".join(leader_list[i]))
        return output

    def __init__(self, frame, windowManager):
        self.frame = frame
        self.windowManager = windowManager
        self.create()

    def create(self):
        canvas = Canvas(self.frame,
                        width=self.windowManager.getResolution()[0],
                        height=self.windowManager.getResolution()[1])
        canvas.pack()

        canvas.create_image(0, 0, image=self.windowManager.menu_image,
                            anchor="nw")
        title = canvas.create_text(self.windowManager.getResolution()[0]/2,
                                   60, text="LEADERBOARD",
                                   font=('Arial', 40, 'bold'))

        back_button = Button(canvas, text="BACK",
                             command=self.windowManager.menu,
                             bg='white', fg='black', padx=30, pady=20)
        back_button.place(relx=0.2, rely=0.15)

        list_of_leaders = self.getSortedListOfLeaders()
        grid_of_leaders = Canvas(canvas, width=500, height=500, bg='white')
        grid_of_leaders.place(relx=0.5, rely=0.45, anchor="center")
        for leader_i in range(len(list_of_leaders)):
            placed = Label(grid_of_leaders, text=str(leader_i+1),
                           font=("Arial", 24), bg='white')
            placed.grid(row=leader_i, column=0, padx=5, sticky='e')
            name = Label(grid_of_leaders, text=list_of_leaders[leader_i][0],
                         font=("Arial", 24), bg='white')
            name.grid(row=leader_i, column=1, sticky='w')
            score = Label(grid_of_leaders, text=list_of_leaders[leader_i][1],
                          font=("Arial", 24), bg='white')
            score.grid(row=leader_i, column=2, padx=15)
