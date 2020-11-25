from tkinter import Tk, Canvas
from time import sleep
from math import sin, cos, atan, radians, degrees, pi

WIDTH = 700
HEIGHT = 400
PLAYER_SIZE = 20
STARTING_POINT = (20, HEIGHT-PLAYER_SIZE)
PROJECTILE_SIZE = 5
RETICLE_SIZE = 50
G = 0.0981

PROJECTILES = []

def getPlayerCenter():
	player_coords = sky.coords(player)
	# return point(x, y)
	return (player_coords[0] + PLAYER_SIZE/2, player_coords[1]+PLAYER_SIZE/2)

def calcAngle(mouse):
	player_center = getPlayerCenter()
	player2mouse = (mouse.x - player_center[0], mouse.y - player_center[1])
	# restricts the area where projectiles can be thrown
	if player2mouse[0] > 0 and player2mouse[1] < 0:
		return pi/2 - abs(atan(player2mouse[0]/player2mouse[1]))
	else:
		# dont throw
		return -1


def aim(event):
	player_center = getPlayerCenter()
	angle = calcAngle(event)
	if angle > 0:
		xy = (player_center[0], player_center[1], player_center[0]+cos(angle)*RETICLE_SIZE, player_center[1]-sin(angle)*RETICLE_SIZE)
		sky.coords(reticle, xy)


def throw(event):
	angle = calcAngle(event)
	if angle > 0:
		trajectory = [round(cos(angle), 2), round(sin(angle), 2)] # GET FROM MOUSE_POS LATER!!!
		power = 6 # GET FROM THE TIME MOUSE WAS HELD DOWN FOR
		vector = [direction * power for direction in trajectory]

		player_center = getPlayerCenter()
		xy = (player_center[0]-PROJECTILE_SIZE/2, player_center[1]+PROJECTILE_SIZE/2, player_center[0]+PROJECTILE_SIZE/2, player_center[1]-PROJECTILE_SIZE/2)
		projectile_id = sky.create_rectangle(xy, fill='red')
		projectile = {"id": projectile_id, "vector": vector}
		PROJECTILES.append(projectile)


def moveProjectiles():
	for projectile in list(PROJECTILES):
		# if not out of bounds
		if sky.coords(projectile['id'])[3] < HEIGHT:
			vector = projectile['vector']
			sky.move(projectile['id'], vector[0], -vector[1])
		else:
			sky.delete(projectile['id'])
			PROJECTILES.remove(projectile)


def applyGravity(): # rename later
	for projectile in PROJECTILES:
		projectile['vector'][1] -= G/2



window = Tk()
window.title("PEW PEW")
sky = Canvas(width=WIDTH, height=HEIGHT, background='sky blue')
sky.pack()
ground = Canvas(width=WIDTH, height=HEIGHT/2, background='pale green')
ground.pack()

player = sky.create_oval(STARTING_POINT[0], STARTING_POINT[1], STARTING_POINT[0] + PLAYER_SIZE, STARTING_POINT[1] + PLAYER_SIZE, fill="tomato")
reticle = sky.create_line(0, 0, 0, 0, fill='red')

sky.bind("<ButtonRelease-1>", throw)
sky.bind("<Motion>", aim)

while True:
	moveProjectiles()
	applyGravity()
	window.update()
	sleep(0.005)

window.mainloop()