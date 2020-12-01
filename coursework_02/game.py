from tkinter import Tk, Frame, Canvas, messagebox, Button, W, E
from math import sqrt
from random import randint
from time import time
from json import load, dumps

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

	def quit(self):
		Pause.PAUSE_WINDOW.quit()
		Pause.PAUSE_WINDOW.destroy()
		Pause.PAUSE_WINDOW = 0
		self.game.breakToSave() # this way we quit after the while loop without deleting any needed variables

	def __init__(self, event, game):
		self.game = game
		if Pause.PAUSE_WINDOW == 0: # not paused
			Pause.PAUSE_WINDOW = Tk()
			Pause.PAUSE_WINDOW.geometry("200x200+500+300")
			Pause.PAUSE_WINDOW.overrideredirect(True)
			canvas = Canvas(Pause.PAUSE_WINDOW)
			canvas.pack()
			canvas.create_text(100, 32, text="PAUSED", font=("Arial", 32))
			resume_button = Button(canvas, text='Resume', command=self.resume)
			resume_button.place(relx=0.3, rely=0.5)
			quit_button = Button(canvas, text='Save and Quit', command=self.quit)
			quit_button.place(relx=0.2, rely=0.7)
			# usually the try block errors because the window gets destroyed
			# and while loop is not finished yet so it tries to call it a destroyed window
			try:
				while Pause.PAUSE_WINDOW != 0:
					Pause.PAUSE_WINDOW.lift()
					Pause.PAUSE_WINDOW.update()
				Pause.PAUSE_WINDOW.mainloop()
			except Exception as e:
				print("PROBABLY FINE?: ", e)



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
	OBJECT_WHERE_IT_STARTS = 0
	LAST_AIM_SPOT = [SIZE, 0]

	def aim(self, event=None):
		if event != None:
			dist_vec = self.OBJECT_WHERE_IT_STARTS.distanceBetweenSelfAndPoint([event.x, event.y])
			self.LAST_AIM_SPOT = [event.x, event.y]
		else:
			dist_vec = self.OBJECT_WHERE_IT_STARTS.distanceBetweenSelfAndPoint([self.LAST_AIM_SPOT[0], self.LAST_AIM_SPOT[1]])
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
	SEC_TO_RELOAD = 0.5

	OBJ = 0 # id of the object whose ammo we are tracking


	def __init__(self, obj):
		self.OBJ = obj
		self.reload_started_at = time()
		self.current_ammo = MAX_AMMO


	def tryToReload(self):
		if self.current_ammo < MAX_AMMO:
			if time() - self.reload_started_at > self.SEC_TO_RELOAD:
				self.current_ammo += 1
				self.reload_started_at = time()


	def shoot(self, event):
		if self.current_ammo > 0:
			self.reload_started_at = time()
			self.current_ammo -= 1
			ProjectileManager.createProjectile(self.OBJ.getCenter(), goal_xy=[self.OBJ.RETICLE.getXY()[2], self.OBJ.RETICLE.getXY()[3]])


class Player(Object):
	SIZE = 45
	SPEED = 10

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
		self.AMMO_TRACKER = AmmoTracker(self)

class HealthTracker:
	hp = 1
	def __init__(self):
		HealthTracker.hp = MAX_HEALTH


class ScoreTracker:
	score = 0
	def __init__(self):
		ScoreTracker.score = 0


class UI:
	def __init__(self, canvas, player):
		self.canvas = canvas
		self.player = player
		self.score = self.canvas.create_text(640, 20, text="Score: 0", font=("Arial", 20, 'bold'))
		self.ammo = self.canvas.create_text(1260, 20, text="Ammo: 0", font=("Arial", 20, 'bold'), anchor=E)
		self.health = self.canvas.create_text(10, 20, text="Health: 0", font=("Arial", 20, 'bold'), anchor=W)

	def update(self):	
		self.canvas.itemconfig(self.score, text="Score: " + str(ScoreTracker.score))
		self.canvas.itemconfig(self.ammo, text="Ammo: " + str(self.player.AMMO_TRACKER.current_ammo))
		self.canvas.itemconfig(self.health, text="Health: " + str(HealthTracker.hp))



class Game:
	# game consts
	TIME_BETWEEN_FRAMES = 3#ms

	def __init__(self, frame, windowManager, loadSave=False):
		self.BREAK_TO_SAVE = False
		self.windowManager = windowManager
		self.frame = frame
		self.initialAssetLoad()
		if loadSave:
			self.loadFromFile()
		self.loop()

	def pause(self, event):
		Pause(event, self)

	def breakToSave(self):
		self.BREAK_TO_SAVE = True

	def initialAssetLoad(self):
		self.sky = Canvas(self.frame, width=self.windowManager.getResolution()[0], height=self.windowManager.getResolution()[1], background='sky blue')
		self.sky.pack()

		starting_point = (50, self.windowManager.getResolution()[1]/2)
		self.player = Player(self.sky)
		self.player.create(starting_point)

		# order of operations is very important
		# some of them depent of the definitions of other
		with open("options.json", 'r') as f:
			options = load(f)
		print(options)
		window = self.frame.master
		window.bind(options['up'], self.player.up)
		window.bind(options['down'], self.player.down)
		window.bind("<Escape>", self.pause)

		ProjectileManager(self.sky)
		self.player.CANVAS.bind("<ButtonRelease-1>", self.player.AMMO_TRACKER.shoot)
		HealthTracker()
		ScoreTracker()
		EnemyManager(self.sky)
		self.ui = UI(self.sky, self.player)


	def saveGameToFile(self):
		data = {"player": self.player.getCenter(), "ENEMIES":[e.getCenter() for e in EnemyManager.ENEMIES], "hp":HealthTracker.hp, "score":ScoreTracker.score, "ammo": self.player.AMMO_TRACKER.current_ammo}
		with open("save.json", 'w') as f:
			f.write(dumps(data))


	def loadFromFile(self):
		with open("save.json", 'r') as f:
			data = load(f)
		xy = createCoordsFromCenter(data['player'], self.player.SIZE)
		self.sky.coords(self.player.ID, xy[0],xy[1],xy[2],xy[3])
		HealthTracker.hp = data['hp']
		ScoreTracker.score = data['score']
		self.player.AMMO_TRACKER.current_ammo = data['ammo']

	def loop(self):
		while HealthTracker.hp > 0 and not self.BREAK_TO_SAVE:
			self.player.AMMO_TRACKER.tryToReload()
			ProjectileManager.manage()
			EnemyManager.manage()
			self.ui.update()
			self.frame.update()
			self.frame.after(self.TIME_BETWEEN_FRAMES)

		if self.BREAK_TO_SAVE:
			self.frame.master.unbind("<Escape>")
			self.saveGameToFile()
			self.windowManager.saveAndQuit()
		else:
			leaderboard = open('leaderboard.txt', 'a')
			leaderboard.write("Jonas:" + str(ScoreTracker.score) + '\n')
			leaderboard.close()
			self.windowManager.gameOver()


	def save(self):
		pass
