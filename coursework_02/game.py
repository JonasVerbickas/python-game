from tkinter import Tk, Canvas
from math import sin, cos, atan, pi, sqrt, radians
from time import time
from random import randint

"""ARTILERY SIM?!?!??!?!"""

WIDTH = 700
HEIGHT = 400
PLAYER_SIZE = 20
STARTING_POINT = (40, HEIGHT-PLAYER_SIZE*1.75)
WALL_DIMEN = (10, 12)

PROJECTILES = []
PROJECTILE_SIZE = 8
POWER = 6
MAX_SHRAPNEL_COUNT = 4
SHRAPNEL = []
SHRAPNEL_POWER_MULT = 0.5
RETICLE_SIZE = 50
G = 0.0981

ZOMBIES = []
Z_SIZE = PLAYER_SIZE
Z_SPEED = 2.5
TIME_BETWEEN_SPAWNS = 4000

SCORE = 0
SCORE_PER_Z = 100

MAX_AMMO = 5
CURRENT_AMMO = MAX_AMMO
TIME_TO_RELOAD = 1000
RELOAD_START_TIME = 0

HP = 5

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
	player_center = getCenter(sky.coords(player))
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
	player_center = getCenter(sky.coords(player))
	angle = angleBetweenPointAndPlayer([event.x, event.y])
	if angle > 0:
		xy = (player_center[0], player_center[1], player_center[0]+cos(angle)*RETICLE_SIZE, player_center[1]-sin(angle)*RETICLE_SIZE)
		sky.coords(reticle, xy)


def createProjectile(starting_xy, angle, power=POWER):
	trajectory = [round(cos(angle), 2), round(sin(angle), 2)] # GET FROM MOUSE_POS LATER!!!
	vector = [direction * power for direction in trajectory]
	xy = coordsFromCenter(starting_xy, PROJECTILE_SIZE)
	projectile_id = sky.create_rectangle(xy, fill='red')
	projectile = {"id": projectile_id, "vector": vector}
	return projectile

def shoot(event):
	# shoot based on reticle and not mouse
	# thus being able to shoot when out of bounds
	reticle_coords = sky.coords(reticle)
	angle = angleBetweenPointAndPlayer([reticle_coords[2], reticle_coords[3]])
	global CURRENT_AMMO
	global RELOAD_START_TIME
	if angle > 0 and CURRENT_AMMO > 0:
		player_center = getCenter(sky.coords(player))
		projectile = createProjectile(player_center, angle)
		PROJECTILES.append(projectile)
		CURRENT_AMMO -= 1
		RELOAD_START_TIME = time()


def createShrapnel(startintg_xy):
	startintg_xy[1] = HEIGHT # this ensures that shrapnel always spawns
	for i in range(MAX_SHRAPNEL_COUNT - randint(0, 1)): # randomize number of shrapnel
		angle = randint(50, 100)
		angle = radians(angle)
		shrapnel = createProjectile(startintg_xy, angle, power=POWER*SHRAPNEL_POWER_MULT)
		SHRAPNEL.append(shrapnel)

def BOOM(projectile, kill_id=-1, is_shrapnel=False):
	if is_shrapnel:
		projectile_center = getCenter(sky.coords(projectile['id']))
		createShrapnel(projectile_center)
		sky.delete(projectile['id'])
		PROJECTILES.remove(projectile)
	else:
		sky.delete(projectile['id'])
		SHRAPNEL.remove(projectile)

	if kill_id > 0:
		sky.delete(kill_id)
		ZOMBIES.remove(kill_id)
		global SCORE
		SCORE += SCORE_PER_Z


def moveProjectile(projectile):
	# if not out of bounds
	vector = projectile['vector']
	sky.move(projectile['id'], vector[0], -vector[1])


def applyGravity(projectile): # rename later
	projectile['vector'][1] -= G/2


def outOfBounds(coords):
	# vertical
	if coords[1] > HEIGHT: # or coords[3] < 0: # no top bounds to allow projectiles to fall from the sky
		return True
	else:
		return False

def checkForCollision(projectile, is_shrapnel=False):
	p_coords = sky.coords(projectile['id'])
	if outOfBounds(p_coords):
		BOOM(projectile, is_shrapnel=is_shrapnel)
	else:
		p_center = getCenter(p_coords)
		for z in ZOMBIES:
			z_center = getCenter(sky.coords(z))
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


def createZombie():
	xy = coordsFromBottomLeft([WIDTH, STARTING_POINT[1]], Z_SIZE)
	z = sky.create_oval(xy, fill='dark green')
	ZOMBIES.append(z)


def moveEnemies():
	global HP
	for z in list(ZOMBIES):
		sky.move(z, -Z_SPEED, 0)
		if sky.coords(z)[0] <= STARTING_POINT[0]:
			HP -= 1
			print(HP)
			sky.delete(z)
			ZOMBIES.remove(z)


def updateText():
	sky.itemconfig(txt_score, text="Score:" + str(SCORE))
	sky.itemconfig(txt_ammo, text="Ammo:" + str(CURRENT_AMMO))
	sky.itemconfig(txt_health, text="Health:" + str(HP))


def tryToReload():
	global RELOAD_START_TIME
	global CURRENT_AMMO
	time_elapsed = (time() - RELOAD_START_TIME) * 1000
	if time_elapsed > TIME_TO_RELOAD:
		RELOAD_START_TIME = time()
		CURRENT_AMMO += 1


window = Tk()
window.title("PEW PEW")
sky = Canvas(width=WIDTH, height=HEIGHT, background='sky blue')
sky.pack()

ground = Canvas(width=WIDTH, height=HEIGHT/2, background='pale green')
ground.pack()

txt_score = sky.create_text(WIDTH/2, 20, text="Score: 0", font=("Arial", 20, 'bold'))
txt_ammo = sky.create_text(WIDTH/2, 50, text="Ammo: 0", font=("Arial", 20, 'bold'))
txt_health = sky.create_text(WIDTH/2, 80, text="Health: 0", font=("Arial", 20, 'bold'))
player = sky.create_oval(STARTING_POINT[0], STARTING_POINT[1], STARTING_POINT[0] + PLAYER_SIZE, STARTING_POINT[1] + PLAYER_SIZE, fill="tomato")
reticle = sky.create_line(0, 0, 0, 0, fill='red')
wall1 = sky.create_rectangle(70, HEIGHT, 70+WALL_DIMEN[0], HEIGHT-WALL_DIMEN[1], fill='brown4')

sky.bind("<ButtonRelease-1>", shoot)
sky.bind("<Motion>", aim)


LAST_SPAWN_TIME = TIME_BETWEEN_SPAWNS # instant spawn
while True:
	everythingProjectiles()
	if time() - LAST_SPAWN_TIME > TIME_BETWEEN_SPAWNS/1000:
		createZombie()
		LAST_SPAWN_TIME = time()
	moveEnemies()
	if CURRENT_AMMO < MAX_AMMO:
		tryToReload()
	updateText()
	window.update()
	window.after(3)

window.mainloop()