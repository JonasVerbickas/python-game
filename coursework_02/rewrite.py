from tkinter import Frame, Canvas
from math import sin, cos, atan, pi, sqrt, radians

def calcDistanceVector(point1, point2):
	return (point2[0] - point1[0], point2[1] - point1[1])

class Object:
	SIZE = 28
	CANVAS = 0
	XY = []

	def __init__(self, canvas):
		self.CANVAS = canvas

	def distanceBetweenSelfAndPoint(self, point):
		center_coords = self.getCenter()
		dist = calcDistanceVector(center_coords, point)
		return dist

	def getCenter(self):
		coords = self.XY
		x_mid = (coords[2] - coords[0])/2 + coords[0]
		y_mid = (coords[3] - coords[1])/2 + coords[1]
		output = [x_mid, y_mid]
		return output


class Reticle(Object):
	ID = 0
	SIZE = 50
	PLAYER_CONTROLLING = 0

	def aim(self, event):
		dist_vec = self.PLAYER_CONTROLLING.distanceBetweenSelfAndPoint([event.x, event.y])
		print(dist_vec)
		if dist_vec[0] > 0:
			player_coords = self.PLAYER_CONTROLLING.getCenter()
			new_xy = (player_coords[0], player_coords[1], player_coords[0]+dist_vec[0], player_coords[1]+dist_vec[1])
			self.CANVAS.coords(self.ID, new_xy)

	def create(self, player_controlling):
		self.PLAYER_CONTROLLING = player_controlling
		self.ID = self.CANVAS.create_line(0, 0, 0, 0, fill='red')
		self.CANVAS.bind("<Motion>", self.aim)


class Player(Object):
	SIZE = 28
	ID = 0

	RETICLE = 0

	def create(self, starting_pont):
		self.XY = (starting_pont[0], starting_pont[1], starting_pont[0] + self.SIZE, starting_pont[1] + self.SIZE)
		self.ID = self.CANVAS.create_oval(self.XY, fill="tomato")
		self.RETICLE = Reticle(self.CANVAS)
		self.RETICLE.create(self)


class Game:
	# consts after init
	RESOLUTION = (0, 0)
	WINDOW = 0

	# assets
	sky = 0
	player = 0
	reticle = 0
	wall1 = 0

	def __init__(self, window, resolution):
		self.RESOLUTION = resolution
		self.window = window

	def loadMap(self):
		new_frame = Frame(self.window)
		new_frame.pack()
		self.sky = Canvas(new_frame, width=self.RESOLUTION[0], height=self.RESOLUTION[1], background='sky blue')
		self.sky.pack()


		starting_pont = (50, self.RESOLUTION[1]/2)
		self.player = Player(self.sky)
		self.player.create(starting_pont)

		# self.wall1 = SKY.create_rectangle(90, HEIGHT, 90+WALL_DIMEN[0], HEIGHT-WALL_DIMEN[1], fill='brown4')