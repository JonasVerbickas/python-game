from tkinter import Frame, Canvas, Button, Toplevel
from math import sqrt
from random import randint
from time import time
from json import load, dumps
from os import remove
from os.path import isfile

MAX_AMMO = 5
MAX_HEALTH = 2
TIME_BETWEEN_FRAMES = 25  # ms
FASTEST_SPAWNING = 0.3  # sec
INFINITE_AMMO = "kilburn"
BOOM = "boom"
LIFE = "life"
TENET = False
TENET_ACTIVATABLE = False


def calcDistanceVector(point1, point2):
    return (point2[0] - point1[0], point2[1] - point1[1])


def createCoordsFromCenter(xy, size):
    return [xy[0]-size/2, xy[1]+size/2, xy[0]+size/2, xy[1]-size/2]


class Pause():
    PAUSE_WINDOW = 0

    def resume(self):
        self.game.bindKeys()
        Pause.PAUSE_WINDOW.quit()
        Pause.PAUSE_WINDOW.destroy()
        Pause.PAUSE_WINDOW = 0

    def quit(self):
        Pause.PAUSE_WINDOW.quit()
        Pause.PAUSE_WINDOW.destroy()
        Pause.PAUSE_WINDOW = 0
        # we quit after the while loop cleanly
        # without deleting any needed variables
        self.game.saveAndMenu()

    def __init__(self, event, game):
        self.game = game
        self.game.unbindKeys()
        if Pause.PAUSE_WINDOW == 0:  # not paused
            Pause.PAUSE_WINDOW = Toplevel(self.game.windowManager.window)
            Pause.PAUSE_WINDOW.overrideredirect(True)  # removes borders
            canvas = Canvas(Pause.PAUSE_WINDOW, bg='white')
            canvas.pack()
            canvas.create_text(100, 32, text="PAUSED", font=("Arial", 32))
            resume_button = Button(canvas, text='Resume',
                                   command=self.resume,
                                   padx=15, pady=8, bg='white')
            resume_button.place(relx=0.5, rely=0.5, anchor="center")
            quit_button = Button(canvas, text='Save and Quit',
                                 command=self.quit,
                                 padx=15, pady=8, bg='white')
            quit_button.place(relx=0.5, rely=0.75, anchor="center")
            # updates the pause window if it isn't destroyed
            try:
                while Pause.PAUSE_WINDOW != 0:
                    x_offset = self.game.windowManager.window.winfo_rootx()+535
                    y_offset = self.game.windowManager.window.winfo_rooty()+230
                    geometry_string = ("200x200+%d+%d") % (x_offset, y_offset)
                    Pause.PAUSE_WINDOW.geometry(geometry_string)
                    Pause.PAUSE_WINDOW.lift()
                    Pause.PAUSE_WINDOW.update()
                Pause.PAUSE_WINDOW.mainloop()
            except Exception as e:
                print("PROBABLY FINE?: ", e)


def outOfBounds(obj, bounds):
    mult = 2
    bounds = [mult*b for b in bounds]
    # horizontal
    if obj.getXY()[0] > bounds[0] or obj.getXY()[2] < -bounds[0]:
        return True
    elif obj.getXY()[1] < -bounds[1] or obj.getXY()[3] > bounds[1]:
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

    def distanceToAPoint(self, point):
        center_coords = self.getCenter()
        dist = calcDistanceVector(center_coords, point)
        return dist

    def getCenter(self):
        coords = self.getXY()
        x_mid = (coords[2] - coords[0])/2 + coords[0]
        y_mid = (coords[3] - coords[1])/2 + coords[1]
        output = [x_mid, y_mid]
        return output

    def getXY(self):  # return dimensions of an object
        return self.CANVAS.coords(self.ID)


class Reticle(Object):
    SIZE = 50
    master = 0
    last_aimed_at = [SIZE, 0]

    def aim(self, event=None):
        if event is not None:
            dist_vec = self.master.distanceToAPoint([event.x, event.y])
            self.last_aimed_at = [event.x, event.y]
        else:
            dist_vec = self.master.distanceToAPoint(self.last_aimed_at)
        dist_vec = shortenVector(dist_vec, self.SIZE)
        if dist_vec[0] > 0:
            player_coords = self.master.getCenter()
            starting_xy = [player_coords[0], player_coords[1]]
            end_xy = [player_coords[i]+dist_vec[i] for i in range(2)]
            new_xy = starting_xy + end_xy
            self.CANVAS.coords(self.ID, new_xy)

    def create(self, starting_object):
        self.master = starting_object
        center = starting_object.getCenter()
        xy = (center[0], center[1], center[0]+self.SIZE, center[1])
        self.ID = self.CANVAS.create_line(xy, fill='red')


class Projectile(Object):
    SPEED = 26
    SIZE = 14
    VECTOR = []

    def goal2AdjustedtedVector(self, starting_xy, goal_xy):
        dist = calcDistanceVector(starting_xy, goal_xy)
        vector = shortenVector(dist, self.SPEED)
        return vector

    def create(self, starting_xy, goal_xy):
        self.VECTOR = self.goal2AdjustedtedVector(starting_xy, goal_xy)
        global TENET
        if TENET:
            self.VECTOR = [-self.VECTOR[0], -self.VECTOR[1]]
        xy = createCoordsFromCenter(starting_xy, self.SIZE)
        self.ID = self.CANVAS.create_rectangle(xy, fill='black', outline='red')


class Enemy(Object):
    WORTH = 10
    SIZE = 55
    SPEED = 8
    MAX_SPEED = 12
    MULT = 1.02  # 20 to reach max

    def create(self, xy):
        self.ID = self.CANVAS.create_oval(xy, fill='dark green')
        if Enemy.SPEED < Enemy.MAX_SPEED:
            Enemy.SPEED *= Enemy.MULT


class ProjectileManager():
    CANVAS = 0
    PROJECTILES = []

    def __init__(self, canvas, windowManager):
        ProjectileManager.CANVAS = canvas
        ProjectileManager.PROJECTILES = []
        ProjectileManager.windowManager = windowManager

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
        for p in list(ProjectileManager.PROJECTILES):
            if outOfBounds(p, ProjectileManager.windowManager.getResolution()):
                ProjectileManager.CANVAS.delete(p.ID)
                ProjectileManager.PROJECTILES.remove(p)
                continue
            global TENET
            if TENET:
                ProjectileManager.CANVAS.move(p.ID, -p.VECTOR[0], -p.VECTOR[1])
            else:
                ProjectileManager.CANVAS.move(p.ID, p.VECTOR[0], p.VECTOR[1])

    @staticmethod
    def manage():
        ProjectileManager.moveAllProjectiles()


class EnemyManager():
    def __init__(self, canvas, windowManager):
        EnemyManager.SPAWN_INTERVAL = 2  # seconds
        EnemyManager.CANVAS = canvas
        EnemyManager.LAST_SPAWN = time()
        EnemyManager.ENEMIES = []
        EnemyManager.windowManager = windowManager

    @staticmethod
    def spawnEnemy(coords=[]):
        if time()-EnemyManager.LAST_SPAWN > EnemyManager.SPAWN_INTERVAL:
            w = EnemyManager.windowManager.getResolution()[0]
            h = EnemyManager.windowManager.getResolution()[1]
            e = Enemy(EnemyManager.CANVAS)
            xy = createCoordsFromCenter([w, randint(0, h-e.SIZE)], e.SIZE)
            e.create(xy)
            EnemyManager.ENEMIES.append(e)
            EnemyManager.LAST_SPAWN = time()
            if EnemyManager.SPAWN_INTERVAL > FASTEST_SPAWNING:
                EnemyManager.SPAWN_INTERVAL *= 0.98

    @staticmethod
    def killEnemy(e):
        EnemyManager.CANVAS.delete(e.ID)
        EnemyManager.ENEMIES.remove(e)

    @staticmethod
    def moveEnemies():
        for e in list(EnemyManager.ENEMIES):
            bounds = list(EnemyManager.windowManager.getResolution())
            bounds[0] += e.SIZE*2  # bounds depend on the enemy
            if outOfBounds(e, bounds):
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
                    global TENET
                    if TENET:
                        EnemyManager.CANVAS.move(e.ID, e.SPEED, 0)
                    else:
                        EnemyManager.CANVAS.move(e.ID, -e.SPEED, 0)

    @staticmethod
    def manage():
        EnemyManager.spawnEnemy()
        EnemyManager.moveEnemies()


class AmmoTracker():
    SEC_TO_RELOAD = 0.4
    OBJ = 0  # id of the object whose ammo we are tracking

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
            starting_pos = self.OBJ.getCenter()
            goal = [self.OBJ.RETICLE.getXY()[2], self.OBJ.RETICLE.getXY()[3]]
            ProjectileManager.createProjectile(starting_pos, goal_xy=goal)


class Player(Object):
    SIZE = 45
    SPEED = 10

    def up(self):
        if self.getXY()[1] > self.SIZE:
            self.CANVAS.move(self.ID, 0, -self.SPEED)
            self.RETICLE.aim()  # refresh aim

    def down(self):
        h = self.CANVAS.winfo_height()
        if self.getXY()[1] < h-self.SIZE*2:
            self.CANVAS.move(self.ID, 0, self.SPEED)
            self.RETICLE.aim()

    def create(self, starting_pont):
        xy = createCoordsFromCenter(starting_pont, self.SIZE)
        self.ID = self.CANVAS.create_oval(xy, fill="tomato")
        self.RETICLE = Reticle(self.CANVAS)
        self.RETICLE.create(self)
        self.ammo_tracker = AmmoTracker(self)


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
        self.score = self.canvas.create_text(640, 20, text="Score: 0",
                                             font=("Arial", 20, 'bold'))
        self.ammo = self.canvas.create_text(1260, 20, text="Ammo: 0",
                                            font=("Arial", 20, 'bold'),
                                            anchor='e')
        self.health = self.canvas.create_text(10, 20, text="Health: 0",
                                              font=("Arial", 20, 'bold'),
                                              anchor='w')

    def update(self):
        score_str = "Score: " + str(ScoreTracker.score)
        ammo_str = "Ammo: %d/%d" % (self.player.ammo_tracker.current_ammo,
                                    MAX_AMMO)
        health_str = "Health: " + str(HealthTracker.hp)
        self.canvas.itemconfig(self.score, text=score_str)
        self.canvas.itemconfig(self.ammo, text=ammo_str)
        self.canvas.itemconfig(self.health, text=health_str)


class Game:
    def __init__(self, frame, windowManager, loadSave=False):
        self.input_sequence = ""
        self.SAVE_AND_MENU = False
        self.SAVE_AND_BOSSKEY = False
        self.windowManager = windowManager
        self.frame = frame
        self.frame.focus_force()
        self.initialAssetLoad()
        if loadSave:
            self.loadFromFile()
        self.loop()

    def bindKeys(self):
        with open("options.json", 'r') as option_file:
            self.options = load(option_file)
        window = self.frame.master
        window.bind("<Escape>", self.pause)
        window.bind("<ButtonRelease-1>", self.player.ammo_tracker.shoot)
        window.bind("<Motion>", self.player.RETICLE.aim)
        window.bind("<Key>", self.recordInput)
        window.bind("<space>", self.tenet)
        # we unbind and use <key> instead
        window.unbind(self.options['bosskey'])

    def unbindKeys(self):
        with open('options.json', 'r') as option_file:
            options = load(option_file)
        window = self.frame.master
        window.unbind("<Escape>")
        window.unbind("<ButtonRelease-1>")
        window.unbind("<Motion>")
        window.unbind("<Key>")
        window.unbind("<space>")

    def createGlobalStatTrackers(self):
        global TENET_ACTIVATABLE
        TENET_ACTIVATABLE = False
        ProjectileManager(self.sky, self.windowManager)
        HealthTracker()
        ScoreTracker()
        EnemyManager(self.sky, self.windowManager)

    def pause(self, event):
        Pause(event, self)

    def saveAndMenu(self):
        self.SAVE_AND_MENU = True

    def saveAndBosskey(self):
        self.SAVE_AND_BOSSKEY = True

    def tenet(self, event):
        global TENET_ACTIVATABLE
        if TENET_ACTIVATABLE:
            global TENET
            TENET = not TENET
            if TENET:
                self.sky.configure(bg='salmon1')
            else:
                self.sky.configure(bg='SlateGray1')

    def cheatLife(self):
        HealthTracker.hp = 100

    def cheatBoom(self):
        resolution = self.windowManager.getResolution()
        # top and bottom
        y = resolution[1]
        for x in range(0, resolution[0], Projectile.SIZE):
            ProjectileManager.createProjectile(self.player.getCenter(), [x, 0])
            ProjectileManager.createProjectile(self.player.getCenter(), [x, y])
        # right
        x = resolution[0]
        for y in range(0, resolution[1], Projectile.SIZE//2):
            ProjectileManager.createProjectile(self.player.getCenter(), [x, y])

    def cheatAmmo(self):
        self.player.ammo_tracker.current_ammo = 9999

    def cheatTenet(self):
        global TENET_ACTIVATABLE
        TENET_ACTIVATABLE = True

    def checkForCheats(self, input_sequence, event):
        input_sequence += event.char
        for cheat in [INFINITE_AMMO, BOOM, LIFE, "tenet"]:
            if cheat[0:len(input_sequence)] == input_sequence:
                if input_sequence == INFINITE_AMMO:
                    self.cheatAmmo()
                elif input_sequence == BOOM:
                    self.cheatBoom()
                elif input_sequence == LIFE:
                    self.cheatLife()
                elif input_sequence == "tenet":
                    self.cheatTenet()
                break
        # no cheat begins with these chars
        else:
            input_sequence = event.char
        return input_sequence

    def recordInput(self, event):
        if event.char.isalnum():
            # check if the button does something
            if event.char in self.options.values():
                if self.options['up'] == event.char:
                    self.player.up()
                elif self.options['down'] == event.char:
                    self.player.down()
                elif self.options['bosskey'] == event.char:
                    self.saveAndBosskey()

            # add to cheat string
            self.input_sequence = self.checkForCheats(self.input_sequence,
                                                      event)

    def initialAssetLoad(self):
        self.sky = Canvas(self.frame,
                          width=self.windowManager.getResolution()[0],
                          height=self.windowManager.getResolution()[1],
                          background='SlateGray1')
        self.sky.pack()

        starting_point = (50, self.windowManager.getResolution()[1]/2)
        self.player = Player(self.sky)
        self.player.create(starting_point)

        self.createGlobalStatTrackers()
        self.ui = UI(self.sky, self.player)

        self.bindKeys()

    def saveGameToFile(self):
        data = {"player": self.player.getCenter(),
                "ENEMIES": [e.getCenter() for e in EnemyManager.ENEMIES],
                "hp": HealthTracker.hp,
                "score": ScoreTracker.score,
                "ammo": self.player.ammo_tracker.current_ammo}
        with open("save.json", 'w') as save_file:
            save_file.write(dumps(data))

    def loadFromFile(self):
        with open("save.json", 'r') as save_file:
            data = load(save_file)
        xy = createCoordsFromCenter(data['player'], self.player.SIZE)
        self.sky.coords(self.player.ID, xy[0], xy[1], xy[2], xy[3])
        HealthTracker.hp = data['hp']
        ScoreTracker.score = data['score']
        self.player.ammo_tracker.current_ammo = data['ammo']
        for e_coords in data['ENEMIES']:
            e = Enemy(self.sky)
            xy = createCoordsFromCenter(e_coords, e.SIZE)
            e.create(xy)
            EnemyManager.ENEMIES.append(e)

    def loop(self):
        need_to_save = self.SAVE_AND_MENU or self.SAVE_AND_BOSSKEY
        while HealthTracker.hp > 0 and not need_to_save:
            frame_start_time = time()
            self.player.ammo_tracker.tryToReload()
            ProjectileManager.manage()
            EnemyManager.manage()
            self.ui.update()
            self.frame.update()
            # adjust the delay between frames depending on
            # how long the operations needed took
            delay = TIME_BETWEEN_FRAMES - (time()-frame_start_time) * 1000
            delay = int(round(delay, 0))
            if delay < 0:
                delay = 0
            self.frame.after(delay)

        self.unbindKeys()
        if self.SAVE_AND_MENU:
            self.saveGameToFile()
            self.windowManager.menu()
        elif self.SAVE_AND_BOSSKEY:
            self.saveGameToFile()
            self.windowManager.openBossKeyInGame()
        else:
            if isfile("save.json"):
                remove("save.json")
            leaderboard_file = open('leaderboard.txt', 'a')
            score_string = "%s:%d\n" % (self.windowManager.player_name,
                                        ScoreTracker.score)
            leaderboard_file.write(score_string)
            leaderboard_file.close()
            self.windowManager.gameOver()

    def save(self):
        pass
