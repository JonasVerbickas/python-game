from tkinter import Tk, Canvas
from math import sin, cos, atan, pi, sqrt, radians
from time import time
from random import randint

"""ARTILERY SIM?!?!??!?!"""

WIDTH = 700
HEIGHT = 400
PLAYER_SIZE = 20
STARTING_POINT = (20, HEIGHT-PLAYER_SIZE*1.75)
WALL_DIMEN = (8, 12)

PROJECTILES = []
PROJECTILE_SIZE = 8
POWER = 6
MAX_SHRAPNEL_COUNT = 5
SHRAPNEL = []
RETICLE_SIZE = 50
G = 0.0981

ZOMBIES = []
Z_SIZE = PLAYER_SIZE
Z_SPEED = 2.5
TIME_BETWEEN_SPAWNS = 4000

SCORE = 0
SCORE_PER_Z = 100

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
	print(angle)
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
	if angle > 0:
		player_center = getCenter(sky.coords(player))
		projectile = createProjectile(player_center, angle)
		PROJECTILES.append(projectile)


def createShrapnel(startintg_xy):
	for i in range(randint(2, MAX_SHRAPNEL_COUNT)):
		angle = randint(30, 100)
		angle = radians(angle)
		shrapnel = createProjectile(startintg_xy, angle, power=POWER/1.5)
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
	for z in ZOMBIES:
		sky.move(z, -Z_SPEED, 0)


def updateText():
	sky.itemconfig(txt, text="Score:" + str(SCORE))


window = Tk()
window.title("PEW PEW")
sky = Canvas(width=WIDTH, height=HEIGHT, background='sky blue')
sky.pack()
ground = Canvas(width=WIDTH, height=HEIGHT/2, background='pale green')
ground.pack()

txt = sky.create_text(WIDTH/2, 20, text="Score: 0", font=("Arial", 20, 'bold'))
player = sky.create_oval(STARTING_POINT[0], STARTING_POINT[1], STARTING_POINT[0] + PLAYER_SIZE, STARTING_POINT[1] + PLAYER_SIZE, fill="tomato")
reticle = sky.create_line(0, 0, 0, 0, fill='red')
wall1 = sky.create_rectangle(60, HEIGHT, 60+WALL_DIMEN[0], HEIGHT-WALL_DIMEN[1], fill='brown4')

sky.bind("<ButtonRelease-1>", shoot)
sky.bind("<Motion>", aim)


LAST_SPAWN_TIME = TIME_BETWEEN_SPAWNS # instant spawn
while True:
	everythingProjectiles()
	if time() - LAST_SPAWN_TIME > TIME_BETWEEN_SPAWNS/1000:
		createZombie()
		LAST_SPAWN_TIME = time()
	moveEnemies()
	updateText()
	window.update()
	window.after(3)

window.mainloop()