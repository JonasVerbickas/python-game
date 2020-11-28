from tkinter import Tk, Canvas, Frame
from math import sin, cos, atan, pi, sqrt, radians
from time import time
from random import randint

"""ARTILERY SIM?!?!??!?!"""

WIDTH = 0
HEIGHT = 0

PLAYER_SIZE = 28
STARTING_POINT = (40, HEIGHT-PLAYER_SIZE*1.75)
WALL_DIMEN = (16, 25)

PROJECTILES = []
PROJECTILE_SIZE = 12
POWER = 6
MAX_SHRAPNEL_COUNT = 5
SHRAPNEL = []
SHRAPNEL_POWER_MULT = 0.5
RETICLE_SIZE = 50
G = 0.0981

ZOMBIES = []
Z_SIZE = PLAYER_SIZE
Z_SPEED = 2.5
TIME_BETWEEN_SPAWNS = 2000
LAST_SPAWN_TIME = 0 
TIME_DECREMENT = 0.95 # makes spawns more often as time goes by
FASTEST_SPAWING = 300
FLYING_SPAWNING_START = 10000 #ms

SCORE = 0
SCORE_PER_Z = 100

MAX_AMMO = 5
CURRENT_AMMO = MAX_AMMO
TIME_TO_RELOAD = 500
RELOAD_START_TIME = 0

HP = 5

# assets
SKY = 0
GROUND = 0

txt_score = 0
txt_ammo = 0
txt_health = 0
player = 0
reticle = 0
wall1 = 0


def getCenter(coords):
	x_mid = (coords[2] - coords[0])/2 + coords[0]
	y_mid = (coords[3] - coords[1])/2 + coords[1]
	output = [x_mid, y_mid]
	return output


def calcDistanceVector(point1, point2):
	return (point2[0] - point1[0], point2[1] - point1[1])


def pythagoras(xy):
	return sqrt(xy[0]**2 + xy[1]**2)

def angleBetweenPointAndPlayer(point):
	player_center = getCenter(SKY.coords(player))
	dist = calcDistanceVector(player_center, point)
	if dist[0] > 0 and dist[1] < 0:
		return pi/2 - abs(atan(dist[0]/dist[1]))
	else:
		# dont throw
		return -1

def coordsFromBottomLeft(xy, size):
	return [xy[0], xy[1], xy[0]+size, xy[1]+size]


def coordsFromCenter(xy, size):
	return [xy[0]-size/2, xy[1]+size/2, xy[0]+size/2, xy[1]-size/2]


def aim(event):
	player_center = getCenter(SKY.coords(player))
	angle = angleBetweenPointAndPlayer([event.x, event.y])
	if angle > 0:
		xy = (player_center[0], player_center[1], player_center[0]+cos(angle)*RETICLE_SIZE, player_center[1]-sin(angle)*RETICLE_SIZE)
		SKY.coords(reticle, xy)


def createProjectile(starting_xy, angle, power=POWER):
	trajectory = [round(cos(angle), 2), round(sin(angle), 2)] # GET FROM MOUSE_POS LATER!!!
	vector = [direction * power for direction in trajectory]
	xy = coordsFromCenter(starting_xy, PROJECTILE_SIZE)
	projectile_id = SKY.create_rectangle(xy, fill='black', outline='red')
	projectile = {"id": projectile_id, "vector": vector}
	return projectile

def shoot(event):
	# shoot based on reticle and not mouse
	# thus being able to shoot when out of bounds
	reticle_coords = SKY.coords(reticle)
	angle = angleBetweenPointAndPlayer([reticle_coords[2], reticle_coords[3]])
	global CURRENT_AMMO
	global RELOAD_START_TIME
	if angle > 0 and CURRENT_AMMO > 0:
		player_center = getCenter(SKY.coords(player))
		projectile = createProjectile(player_center, angle)
		PROJECTILES.append(projectile)
		CURRENT_AMMO -= 1
		RELOAD_START_TIME = time()


def createShrapnel(startintg_xy):
	if startintg_xy < HEIGHT-5:  # this ensures that shrapnel always spawns
		startintg_xy[1] = HEIGHT-5 # even when i should be below the GROUND
	for i in range(MAX_SHRAPNEL_COUNT - randint(0, 1)): # randomize number of shrapnel
		angle = randint(50, 130)
		angle = radians(angle)
		shrapnel = createProjectile(startintg_xy, angle, power=POWER*SHRAPNEL_POWER_MULT)
		SHRAPNEL.append(shrapnel)

def BOOM(projectile, kill_id=-1, is_shrapnel=False):
	if is_shrapnel:
		projectile_center = getCenter(SKY.coords(projectile['id']))
		createShrapnel(projectile_center)
		SKY.delete(projectile['id'])
		PROJECTILES.remove(projectile)
	else:
		SKY.delete(projectile['id'])
		SHRAPNEL.remove(projectile)

	if kill_id > 0:
		SKY.delete(kill_id)
		ZOMBIES.remove(kill_id)
		global SCORE
		SCORE += SCORE_PER_Z


def moveProjectile(projectile):
	# if not out of bounds
	vector = projectile['vector']
	SKY.move(projectile['id'], vector[0], -vector[1])


def applyGravity(projectile): # rename later
	projectile['vector'][1] -= G/2


def outOfBounds(coords):
	# vertical
	if coords[1] > HEIGHT: # or coords[3] < 0: # no top bounds to allow projectiles to fall from the SKY
		return True
	else:
		return False

def checkForCollision(projectile, is_shrapnel=False):
	p_coords = SKY.coords(projectile['id'])
	if outOfBounds(p_coords):
		BOOM(projectile, is_shrapnel=is_shrapnel)
	else:
		p_center = getCenter(p_coords)
		for z in ZOMBIES:
			z_center = getCenter(SKY.coords(z))
			dist_vector = calcDistanceVector(p_center, z_center)
			absolute_dist = pythagoras(dist_vector)
			if absolute_dist < (PROJECTILE_SIZE/2 + Z_SIZE/2):
				BOOM(projectile, z, is_shrapnel=is_shrapnel)


def everythingProjectiles():
	for projectile in list(PROJECTILES):
		moveProjectile(projectile)
		applyGravity(projectile)
		checkForCollision(projectile, is_shrapnel=True)

	for shrapnel in list(SHRAPNEL):
		moveProjectile(shrapnel)
		applyGravity(shrapnel)
		checkForCollision(shrapnel, is_shrapnel=False)


def createZombie(flying=False):
	global TIME_BETWEEN_SPAWNS
	if flying:
		xy = coordsFromBottomLeft([WIDTH, 250], Z_SIZE)
	else:
		xy = coordsFromBottomLeft([WIDTH, STARTING_POINT[1]], Z_SIZE)
	z = SKY.create_oval(xy, fill='dark green')
	ZOMBIES.append(z)
	if TIME_BETWEEN_SPAWNS > FASTEST_SPAWING:
		TIME_BETWEEN_SPAWNS *= TIME_DECREMENT


def moveEnemies():
	global HP
	for z in list(ZOMBIES):
		SKY.move(z, -Z_SPEED, 0)
		if SKY.coords(z)[0] <= STARTING_POINT[0]:
			HP -= 1
			print(HP)
			SKY.delete(z)
			ZOMBIES.remove(z)


def updateText():
	global txt_score
	SKY.itemconfig(txt_score, text="Score:" + str(SCORE))
	SKY.itemconfig(txt_ammo, text="Ammo:" + str(CURRENT_AMMO))
	SKY.itemconfig(txt_health, text="Health:" + str(HP))


def tryToReload():
	global RELOAD_START_TIME
	global CURRENT_AMMO
	time_elapsed = (time() - RELOAD_START_TIME) * 1000
	if time_elapsed > TIME_TO_RELOAD:
		RELOAD_START_TIME = time()
		CURRENT_AMMO += 1


def startGame(window, resolution):
	global WIDTH
	global HEIGHT
	global LAST_SPAWN_TIME
	global SKY
	global GROUND
	global txt_score
	global txt_ammo
	global txt_health
	global player
	global reticle
	global wall1

	HEIGHT = resolution[0]
	print(HEIGHT)
	WIDTH = resolution[1]
	new_frame = Frame(window)
	new_frame.pack()
	SKY = Canvas(new_frame, width=WIDTH, height=HEIGHT*0.4, background='sky blue')
	SKY.pack()

	GROUND = Canvas(new_frame, width=WIDTH, height=HEIGHT*0.4, background='pale green')
	GROUND.pack()

	txt_score = SKY.create_text(WIDTH/2, 20, text="Score: 0", font=("Arial", 20, 'bold'))
	txt_ammo = SKY.create_text(WIDTH/2, 50, text="Ammo: 0", font=("Arial", 20, 'bold'))
	txt_health = SKY.create_text(WIDTH/2, 80, text="Health: 0", font=("Arial", 20, 'bold'))
	player = SKY.create_oval(STARTING_POINT[0], STARTING_POINT[1], STARTING_POINT[0] + PLAYER_SIZE, STARTING_POINT[1] + PLAYER_SIZE, fill="tomato")
	reticle = SKY.create_line(0, 0, 0, 0, fill='red')
	wall1 = SKY.create_rectangle(90, HEIGHT, 90+WALL_DIMEN[0], HEIGHT-WALL_DIMEN[1], fill='brown4')

	SKY.bind("<ButtonRelease-1>", shoot) # shoot when in window
	SKY.bind("<Motion>", aim) # only aim in when SKY


	TIME_STARTED = time()

	while HP > 0:
		everythingProjectiles()
		if time() - LAST_SPAWN_TIME > TIME_BETWEEN_SPAWNS/1000:
			if time() - TIME_STARTED > FLYING_SPAWNING_START/1000:
				createZombie(flying=randint(0, 1))
			else:
				createZombie()
			LAST_SPAWN_TIME = time()
		moveEnemies()
		if CURRENT_AMMO < MAX_AMMO:
			tryToReload()
		updateText()
		new_frame.update()
		new_frame.after(3) # cant go lower/makes framerate too unstable

	return new_frame
