from tkinter import Tk, Frame, Canvas, messagebox, Button
from math import sqrt
from random import randint
from time import time

MAX_AMMO = 5
MAX_HEALTH = 2

def calcDistanceVector(point1, point2):
	return (point2[0] - point1[0], point2[1] - point1[1])

def createCoordsFromCenter(xy, size):
	return [xy[0]-size/2, xy[1]+size/2, xy[0]+size/2, xy[1]-size/2]


class Pause():
	PAUSE_WINDOW = 0
	def resume(self):
		Pause.PAUSE_WINDOW.quit()
		Pause.PAUSE_WINDOW.destroy()
		Pause.PAUSE_WINDOW = 0
	def __init__(self, event):
		if Pause.PAUSE_WINDOW == 0: # not paused
			Pause.PAUSE_WINDOW = Tk()
			Pause.PAUSE_WINDOW.geometry("200x100+500+300")
			Pause.PAUSE_WINDOW.overrideredirect(True)
			canvas = Canvas(Pause.PAUSE_WINDOW)
			canvas.pack()
			canvas.create_text(100, 32, text="PAUSED", font=("Arial", 32))
			resume_button = Button(canvas, text='Resume', command=self.resume)
			resume_button.place(relx=0.3, rely=0.7)
			Pause.PAUSE_WINDOW.lift()
			Pause.PAUSE_WINDOW.mainloop()

def outOfBounds(obj, bounds):
		# horizontal
		if obj.getXY()[0] > bounds[0] or obj.getXY()[2] < 0:
			return True
		elif obj.getXY()[1] < 0 or obj.getXY()[3] > bounds[1]:
			return True
		else:
			return False


def collision(obj1, obj2):
	coords1 = obj1.getCenter()
	coords2 = obj2.getCenter()
	dist_vec = calcDistanceVector(coords1, coords2)
	dist = sqrt(dist_vec[0]**2+dist_vec[1]**2)
	if dist < obj1.SIZE/2 + obj2.SIZE/2:
		return True
	else:
		return False


def shortenVector(vector, max_size):
	return [(i*max_size)/(sqrt(vector[0]**2 + vector[1]**2)) for i in vector]

class Object:
	CANVAS = 0
	ID = 0
	def __init__(self, canvas):
		self.CANVAS = canvas

	def distanceBetweenSelfAndPoint(self, point):
		center_coords = self.getCenter()
		dist = calcDistanceVector(center_coords, point)
		return dist

	def getCenter(self):
		coords = self.getXY()
		x_mid = (coords[2] - coords[0])/2 + coords[0]
		y_mid = (coords[3] - coords[1])/2 + coords[1]
		output = [x_mid, y_mid]
		return output


	def getXY(self): # return dimensions of an object
		return self.CANVAS.coords(self.ID)

class Reticle(Object):
	SIZE = 50
	OBJECT_WHERE_IT_STARTS = 0 # usually the player
	LAST_AIM_SPOT = [SIZE, 0]

	def aim(self, event=None):
		if event != None:
			dist_vec = self.OBJECT_WHERE_IT_STARTS.distanceBetweenSelfAndPoint([event.x, event.y])
			self.LAST_AIM_SPOT = event
		else:
			dist_vec = self.OBJECT_WHERE_IT_STARTS.distanceBetweenSelfAndPoint([self.LAST_AIM_SPOT.x, self.LAST_AIM_SPOT.y])
		dist_vec = shortenVector(dist_vec, self.SIZE)
		if dist_vec[0] > 0:
			player_coords = self.OBJECT_WHERE_IT_STARTS.getCenter()
			new_xy = (player_coords[0], player_coords[1], player_coords[0]+dist_vec[0], player_coords[1]+dist_vec[1])
			self.CANVAS.coords(self.ID, new_xy)
			

	def create(self, starting_object):
		self.OBJECT_WHERE_IT_STARTS = starting_object
		self.ID = self.CANVAS.create_line(0, 0, 0, 0, fill='red')
		self.CANVAS.bind("<Motion>", self.aim)

class Projectile(Object):
	SPEED = 15
	SIZE = 14
	VECTOR = []
	def goal2AdjustedtedVector(self, starting_xy, goal_xy):
		dist = calcDistanceVector(starting_xy, goal_xy)
		vector = shortenVector(dist, self.SPEED)
		return vector
	def create(self, starting_xy, goal_xy):
		self.VECTOR = self.goal2AdjustedtedVector(starting_xy, goal_xy)
		xy = createCoordsFromCenter(starting_xy, self.SIZE)
		self.ID = self.CANVAS.create_rectangle(xy, fill='black', outline='red')

class Enemy(Object):
	WORTH = 10
	SIZE = 50
	SPEED = 4
	def create(self):
		h = self.CANVAS.winfo_height()
		w = self.CANVAS.winfo_width()
		xy = createCoordsFromCenter([w, randint(0,h)], self.SIZE)
		self.ID = self.CANVAS.create_oval(xy, fill='dark green')

class ProjectileManager():
	CANVAS = 0
	PROJECTILES = []
	def __init__(self,canvas):
		ProjectileManager.CANVAS = canvas
		ProjectileManager.PROJECTILES = []
	@staticmethod
	def createProjectile(starting_xy, goal_xy):
		p = Projectile(ProjectileManager.CANVAS)
		p.create(starting_xy, goal_xy)
		ProjectileManager.PROJECTILES.append(p)
	@staticmethod
	def killProjectile(e):
		ProjectileManager.CANVAS.delete(e.ID)
		ProjectileManager.PROJECTILES.remove(e)
	@staticmethod
	def moveAllProjectiles():
		w = ProjectileManager.CANVAS.winfo_width()
		h = ProjectileManager.CANVAS.winfo_height()
		for p in list(ProjectileManager.PROJECTILES):
			if outOfBounds(p, [w, h]):
				ProjectileManager.CANVAS.delete(p.ID)
				ProjectileManager.PROJECTILES.remove(p)
			else:
				ProjectileManager.CANVAS.move(p.ID, p.VECTOR[0], p.VECTOR[1])
	@staticmethod
	def manage():
		ProjectileManager.moveAllProjectiles()

class EnemyManager():
	CANVAS = 0
	ENEMIES = []
	SPAWN_INTERVAL = 2#seconds
	LAST_SPAWN=0
	def __init__(self, canvas):
		EnemyManager.CANVAS = canvas
		EnemyManager.LAST_SPAWN = time()
		EnemyManager.ENEMIES = []
	@staticmethod
	def spawnEnemy():
		if time()-EnemyManager.LAST_SPAWN > EnemyManager.SPAWN_INTERVAL:
			e = Enemy(EnemyManager.CANVAS)
			e.create()
			EnemyManager.ENEMIES.append(e)
			EnemyManager.LAST_SPAWN = time()

	@staticmethod
	def killEnemy(e):
		EnemyManager.CANVAS.delete(e.ID)
		EnemyManager.ENEMIES.remove(e)

	@staticmethod
	def moveEnemies():
		w = EnemyManager.CANVAS.winfo_width()
		h = EnemyManager.CANVAS.winfo_height()
		for e in list(EnemyManager.ENEMIES):
			if outOfBounds(e, [w+(e.SIZE*2), h]):
				EnemyManager.killEnemy(e)
			elif e.getXY()[0] < e.SIZE:
				HealthTracker.hp -= 1
				EnemyManager.killEnemy(e)

			else:
				for p in list(ProjectileManager.PROJECTILES):
					if collision(p, e):
						ScoreTracker.score += e.WORTH
						EnemyManager.killEnemy(e)
						ProjectileManager.killProjectile(p)
						break
				else:
					EnemyManager.CANVAS.move(e.ID, -e.SPEED, 0)
	@staticmethod
	def manage():
		EnemyManager.spawnEnemy()
		EnemyManager.moveEnemies()


class AmmoTracker():
	CURRENT_AMMO = 0
	SEC_TO_RELOAD = 0.5
	RELOAD_START = 0

	OBJ = 0 # id of the object whose ammo we are tracking

	def __init__(self, obj):
		self.OBJ = obj
		self.CURRENT_AMMO = MAX_AMMO


	def tryToReload(self):
		if self.CURRENT_AMMO < MAX_AMMO:
			if time() - self.RELOAD_START > self.SEC_TO_RELOAD:
				self.CURRENT_AMMO += 1
				self.RELOAD_START = time()


	def shoot(self, event):
		if self.CURRENT_AMMO > 0:
			self.RELOAD_START = time()
			self.CURRENT_AMMO -= 1
			ProjectileManager.createProjectile(self.OBJ.getCenter(), goal_xy=[self.OBJ.RETICLE.getXY()[2], self.OBJ.RETICLE.getXY()[3]])


class Player(Object):
	SIZE = 45
	RETICLE = 0
	SPEED = 8

	AMMO_TRACKER = 0

	def up(self, event):
		if self.getXY()[1] > self.SIZE:
			self.CANVAS.move(self.ID, 0, -self.SPEED)
			self.RETICLE.aim() # refresh aim

	def down(self, event):
		h = self.CANVAS.winfo_height()
		if self.getXY()[1] < h-self.SIZE*2:
			self.CANVAS.move(self.ID, 0, self.SPEED)
			self.RETICLE.aim()

	def create(self, starting_pont):
		xy = createCoordsFromCenter(starting_pont, self.SIZE)
		self.ID = self.CANVAS.create_oval(xy, fill="tomato")
		self.RETICLE = Reticle(self.CANVAS)
		self.RETICLE.create(self)
		window = self.CANVAS.master.master
		print(window)
		self.AMMO_TRACKER = AmmoTracker(self)
		self.CANVAS.bind("<ButtonRelease-1>", self.AMMO_TRACKER.shoot)
		window.bind("w", self.up)
		window.bind("s", self.down)
		window.bind("<Escape>", Pause)


class HealthTracker:
	hp = 1
	def __init__(self):
		HealthTracker.hp = MAX_HEALTH


class ScoreTracker:
	score = 0
	def __init__(self):
		ScoreTracker.score = 0


class UI:
	# from global
	CANVAS = 0
	PLAYER = 0

	# only local
	score = 0
	ammo = 0
	health = 0

	def __init__(self, canvas, player):
		self.CANVAS = canvas
		self.PLAYER = player
		self.score = self.CANVAS.create_text(500, 20, text="Score: 0", font=("Arial", 20, 'bold'))
		self.ammo = self.CANVAS.create_text(500, 50, text="Ammo: 0", font=("Arial", 20, 'bold'))
		self.health = self.CANVAS.create_text(500, 80, text="Health: 0", font=("Arial", 20, 'bold'))

	def update(self):	
		self.CANVAS.itemconfig(self.score, text="Score: " + str(ScoreTracker.score))
		self.CANVAS.itemconfig(self.ammo, text="Ammo: " + str(self.PLAYER.AMMO_TRACKER.CURRENT_AMMO))
		self.CANVAS.itemconfig(self.health, text="Health: " + str(HealthTracker.hp))



class Game:
	# game consts
	TIME_BETWEEN_FRAMES = 3#ms

	# assets
	sky = 0
	player = 0
	reticle = 0
	ui = 0

	def __init__(self, frame, resolution):
		self.RESOLUTION = resolution
		self.frame = frame
		self.create()

	def loadAssets(self):
		self.sky = Canvas(self.frame, width=self.RESOLUTION[0], height=self.RESOLUTION[1], background='sky blue')
		self.sky.pack()

		starting_point = (50, self.RESOLUTION[1]/2)
		self.player = Player(self.sky)
		self.player.create(starting_point)

		HealthTracker()
		ScoreTracker()
		ProjectileManager(self.sky)
		EnemyManager(self.sky)
		self.ui = UI(self.sky, self.player)


	def loop(self):
		while HealthTracker.hp > 0:
			self.player.AMMO_TRACKER.tryToReload()
			ProjectileManager.manage()
			EnemyManager.manage()
			self.ui.update()
			self.frame.update()
			self.frame.after(self.TIME_BETWEEN_FRAMES)

		leaderboard = open('leaderboard.txt', 'a')
		leaderboard.write("Jonas:" + str(ScoreTracker.score) + '\n')
		leaderboard.close()

	def create(self):
		self.loadAssets()
		self.loop()

