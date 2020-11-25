from tkinter import Tk, Canvas
from time import sleep
from math import sin, cos, atan, radians, degrees 

WIDTH = 700
HEIGHT = 400
STARTING_POINT = (20, HEIGHT)
PLAYER_SIZE = 20
SHURIKEN_SIZE = 5
G = 0.0981

PROJECTILES = []

def calcAngle(mouse):
	player_pos = sky.coords(player)
	player_x = player_pos[2]
	player_y = player_pos[1]
	player2mouse = (mouse.x - player_x, mouse.y - player_y)
	# restricts the area where projectiles can be thrown
	if player2mouse[0] > 0 and player2mouse[1] < 0:
		return abs(atan(player2mouse[0]/player2mouse[1]))
	else:
		# dont throw
		return -1


def throw(event):
	angle = calcAngle(event)
	if angle > 0:
		trajectory = [round(sin(angle), 2), round(cos(angle), 2)] # GET FROM MOUSE_POS LATER!!!
		power = 6 # GET FROM THE TIME MOUSE WAS HELD DOWN FOR
		vector = [direction * power for direction in trajectory]

		player_coords = sky.coords(player)
		xy = (player_coords[0]+PLAYER_SIZE/2, player_coords[1]-PLAYER_SIZE/2-SHURIKEN_SIZE, player_coords[0]+PLAYER_SIZE/2+SHURIKEN_SIZE, player_coords[1]-PLAYER_SIZE/2)
		projectile_id = sky.create_rectangle(xy, fill='red')
		projectile = {"id": projectile_id, "vector": vector}
		PROJECTILES.append(projectile)


def moveProjectiles():
	for projectile in list(PROJECTILES):
		if sky.coords(projectile['id'])[3] < HEIGHT:
			vector = projectile['vector']
			sky.move(projectile['id'], vector[0], -vector[1])
		else:
			sky.delete(projectile['id'])
			# ar galime remove kol esam for loope?? 
			PROJECTILES.remove(projectile) # kazkodel veikia


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
#aim = sky.create_line(STARTING_POINT[0]+PLAYER_SIZE/1.2, STARTING_POINT[1], STARTING_POINT[0]+100, STARTING_POINT[1] - 75, fill='red')

sky.bind("<Button-1>", throw)

while True:
	moveProjectiles()
	applyGravity()
	window.update()
	sleep(0.005)

window.mainloop()