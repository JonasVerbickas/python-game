from tkinter import Tk, Canvas
from time import sleep
from math import sin, cos, radians

WIDTH = 700
HEIGHT = 400
STARTING_POINT = (20, HEIGHT-50)
PLAYER_SIZE = 20
SHURIKEN_SIZE = 5
G = 0.0981

PROJECTILES = []

def throw(event):
	trajectory = [round(sin(radians(60)), 2), round(cos(radians(60)), 2)] # GET FROM MOUSE_POS LATER!!!
	power = 3 # GET FROM THE TIME MOUSE WAS HELD DOWN FOR
	vector = [direction * power for direction in trajectory]

	player_coords = sky.coords(player)
	xy = (player_coords[2]+PLAYER_SIZE+SHURIKEN_SIZE, player_coords[1]-PLAYER_SIZE-SHURIKEN_SIZE, player_coords[2]+PLAYER_SIZE, player_coords[1]-PLAYER_SIZE)
	projectile_id = sky.create_rectangle(xy, fill='red')
	projectile = {"id": projectile_id, "vector": vector}
	PROJECTILES.append(projectile)


def moveProjectiles():
	for projectile in PROJECTILES:
		if sky.coords(projectile['id'])[3] < HEIGHT:
			vector = projectile['vector']
			sky.move(projectile['id'], vector[0], -vector[1])
		else:
			sky.delete(projectile['id'])
			PROJECTILES.remove(projectile) # ar galime remove kol esam for loope?? 


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

window.bind("<Button-1>", throw)

while True:
	moveProjectiles()
	applyGravity()
	window.update()
	sleep(0.005)

window.mainloop()