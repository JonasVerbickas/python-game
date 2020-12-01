from tkinter import Frame, Canvas, Button, NW

class LeaderBoard():
	def getSortedListOfLeaders(self):
		list_of_leaders = []
		f = open("leaderboard.txt", 'r')
		for key_val in f.read().strip().split('\n'):
			key_val_split = key_val.split(':')
			for combo in list(list_of_leaders):
				if int(key_val_split[1]) > int(combo[1]):
					insert_index = list_of_leaders.index(combo)
					list_of_leaders.insert(insert_index, key_val_split)
					break
			else:
				list_of_leaders.append(key_val_split)
		f.close()
		return list_of_leaders

	def leaderList2String(self, leader_list):
		output = ""
		for i in range(len(leader_list)): # only the TOP 9
			if i >= 9:
				break
			output += ("%d %s\n") % (i+1, " ".join(leader_list[i]))
		return output


	def __init__(self, frame, windowManager):
		self.frame = frame
		self.windowManager = windowManager
		self.create()


	def create(self):
		canvas = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], bg='black')
		canvas.pack()

		canvas.create_image(0, 0, image=self.windowManager.menu_image, anchor=NW)

		back_button = Button(canvas, text="BACK", command=self.windowManager.menu)
		back_button.place(relx=0.15, rely=0.05)

		list_of_leaders = self.getSortedListOfLeaders()
		string_of_leaders = self.leaderList2String(list_of_leaders)
		title = canvas.create_text(self.windowManager.getResolution()[0]/2, 50, text="LEADERBOARD", font=('Arial', 32))
		leaderboard_text = canvas.create_text(self.windowManager.getResolution()[0]/2, self.windowManager.getResolution()[1]/2, text=string_of_leaders, font=('Arial', 32))

