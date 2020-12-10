from tkinter import Frame, Canvas, Button, Toplevel, PhotoImage
from math import sqrt
from random import randint
from time import time
from json import load, dumps
from os import remove
from os.path import isfile, dirname

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


class Pause():
    window = 0

    def resume(self):
        self.game.bindKeys()
        Pause.window.quit()
        Pause.window.destroy()
        Pause.window = 0

    def quit(self):
        Pause.window.quit()
        Pause.window.destroy()
        Pause.window = 0
        # we quit after the while loop cleanly
        # without deleting any needed variables
        self.game.saveAndMenu()

    def __init__(self, event, game):
        self.game = game
        self.game.unbindKeys()
        Pause.window = Toplevel(self.game.windowManager.window)
        Pause.window.overrideredirect(True)  # removes borders
        canvas = Canvas(Pause.window, bg='white')
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
            while Pause.window != 0:
                x_offset = self.game.windowManager.window.winfo_rootx()+535
                y_offset = self.game.windowManager.window.winfo_rooty()+230
                geometry_string = ("200x200+%d+%d") % (x_offset, y_offset)
                Pause.window.geometry(geometry_string)
                Pause.window.lift()
                Pause.window.update()
            Pause.window.mainloop()
        except Exception as e:
            pass


def outOfBounds(obj, bounds):
    mult = 2
    bounds = [mult*b for b in bounds]
    # horizontal
    if obj.getXY()[0] > bounds[0] or obj.getXY()[0] < -bounds[0]:
        return True
    elif obj.getXY()[1] < -bounds[1] or obj.getXY()[1] > bounds[1]:
        return True
    else:
        return False


def collision(obj1, obj2):
    coords1 = obj1.getXY()
    coords2 = obj2.getXY()
    dist_vec = calcDistanceVector(coords1, coords2)
    dist = sqrt(dist_vec[0]**2+dist_vec[1]**2)
    if dist < obj1.SIZE/2 + obj2.SIZE/2:
        return True
    else:
        return False


def shortenVector(vector, max_size):
    return [(i*max_size)/(sqrt(vector[0]**2 + vector[1]**2)) for i in vector]


class Sprite:
    ID = 0
    SIZE = 0

    def __init__(self, canvas, sprite_file, coords):
        self.canvas = canvas
        sprite_location = "assets/" + sprite_file
        self.img = PhotoImage(file=sprite_location)
        self.ID = self.canvas.create_image(coords[0], coords[1],
                                           image=self.img)
        # radius/hitbox
        self.SIZE = sqrt((self.getSize()[0]/2)**2 + (self.getSize()[1]/2)**2)

    def distanceToAPoint(self, point):
        center_coords = self.getXY()
        dist = calcDistanceVector(center_coords, point)
        return dist

    def getXY(self):  # return dimensions of an object
        return self.canvas.coords(self.ID)

    def getSize(self):
        return (self.img.width(), self.img.height())


class Projectile(Sprite):
    SPEED = 32
    SIZE = 14
    vector = []

    def goal2AdjustedtedVector(self, starting_xy, goal_xy):
        dist = calcDistanceVector(starting_xy, goal_xy)
        vector = shortenVector(dist, self.SPEED)
        return vector

    def __init__(self, canvas, starting_xy, goal_xy):
        super().__init__(canvas, "bullet.gif", starting_xy)
        self.vector = self.goal2AdjustedtedVector(starting_xy, goal_xy)
        global TENET
        if TENET:
            self.vector = [-self.vector[0], -self.vector[1]]


class Enemy(Sprite):
    WORTH = 10
    SPEED = 8
    MAX_SPEED = 12
    MULT = 1.02  # 20 to reach max

    def __init__(self, canvas, coords):
        super().__init__(canvas, "zombie.gif", coords)
        if Enemy.SPEED < Enemy.MAX_SPEED:
            Enemy.SPEED *= Enemy.MULT


class Player(Sprite):
    SIZE = 45
    SPEED = 10

    def __init__(self, canvas, coords):
        super().__init__(canvas, "player.gif", coords)
        self.ammo_tracker = AmmoTracker(self)

    def up(self):
        if self.getXY()[1] > self.SIZE:
            self.canvas.move(self.ID, 0, -self.SPEED)

    def down(self):
        h = self.canvas.winfo_height()
        if self.getXY()[1] < h-self.SIZE:
            self.canvas.move(self.ID, 0, self.SPEED)


class ProjectileManager():
    canvas = 0
    projectiles = []

    def __init__(self, canvas, windowManager):
        ProjectileManager.canvas = canvas
        ProjectileManager.projectiles = []
        ProjectileManager.windowManager = windowManager

    @staticmethod
    def createProjectile(starting_xy, goal_xy):
        p = Projectile(ProjectileManager.canvas, starting_xy, goal_xy)
        ProjectileManager.projectiles.append(p)

    @staticmethod
    def killProjectile(e):
        ProjectileManager.canvas.delete(e.ID)
        ProjectileManager.projectiles.remove(e)

    @staticmethod
    def moveAllProjectiles():
        for p in list(ProjectileManager.projectiles):
            if outOfBounds(p, ProjectileManager.windowManager.getResolution()):
                ProjectileManager.canvas.delete(p.ID)
                ProjectileManager.projectiles.remove(p)
                continue
            global TENET
            if TENET:
                ProjectileManager.canvas.move(p.ID, -p.vector[0], -p.vector[1])
            else:
                ProjectileManager.canvas.move(p.ID, p.vector[0], p.vector[1])

    @staticmethod
    def manage():
        ProjectileManager.moveAllProjectiles()


class EnemyManager():
    def __init__(self, canvas, windowManager):
        EnemyManager.SPAWN_INTERVAL = 2  # seconds
        EnemyManager.canvas = canvas
        EnemyManager.last_spawn = time()
        EnemyManager.enemies = []
        EnemyManager.grave_img = PhotoImage(file="assets/grave.gif")
        EnemyManager.windowManager = windowManager

    @staticmethod
    def spawnEnemy(coords=[]):
        if time()-EnemyManager.last_spawn > EnemyManager.SPAWN_INTERVAL:
            w = EnemyManager.windowManager.getResolution()[0]
            h = EnemyManager.windowManager.getResolution()[1]
            xy = [w, randint(100, h-100)]
            e = Enemy(EnemyManager.canvas, xy)
            EnemyManager.enemies.append(e)
            EnemyManager.last_spawn = time()
            if EnemyManager.SPAWN_INTERVAL > FASTEST_SPAWNING:
                EnemyManager.SPAWN_INTERVAL *= 0.98

    @staticmethod
    def createTombstone(coords):
        grave = EnemyManager.canvas.create_image(coords[0], coords[1], 
                                         image=EnemyManager.grave_img)
        EnemyManager.canvas.after(2000,
                                  lambda : EnemyManager.canvas.delete(grave))

    @staticmethod
    def killEnemy(e):
        EnemyManager.createTombstone(e.getXY())
        EnemyManager.canvas.delete(e.ID)
        EnemyManager.enemies.remove(e)

    @staticmethod
    def moveEnemies():
        for e in list(EnemyManager.enemies):
            bounds = list(EnemyManager.windowManager.getResolution())
            bounds[0] += e.SIZE*2  # bounds depend on the enemy
            if outOfBounds(e, bounds):
                EnemyManager.killEnemy(e)
            elif e.getXY()[0] < e.SIZE:
                HealthTracker.hp -= 1
                EnemyManager.killEnemy(e)
            else:
                for p in list(ProjectileManager.projectiles):
                    if collision(p, e):
                        ScoreTracker.score += e.WORTH
                        EnemyManager.killEnemy(e)
                        ProjectileManager.killProjectile(p)
                        break
                else:
                    global TENET
                    if TENET:
                        EnemyManager.canvas.move(e.ID, e.SPEED, 0)
                    else:
                        EnemyManager.canvas.move(e.ID, -e.SPEED, 0)

    @staticmethod
    def manage():
        EnemyManager.spawnEnemy()
        EnemyManager.moveEnemies()


class AmmoTracker():
    SEC_TO_RELOAD = 0.5
    master = 0  # id of the object whose ammo we are tracking

    def __init__(self, obj):
        self.master = obj
        self.reload_started_at = time()
        self.current_ammo = MAX_AMMO

    def tryToReload(self):
        if self.current_ammo < MAX_AMMO:
            if time() - self.reload_started_at > self.SEC_TO_RELOAD:
                self.current_ammo += 1
                self.reload_started_at = time()

    def moveAllChildren(self, parent, direction):
        for child in parent.find_all():
            self.master.canvas.move(child, direction, 0)
        self.master.canvas.master.update()

    def shakeCamera(self):
        self.moveAllChildren(self.master.canvas, 4)
        self.master.canvas.master.after(4)
        self.moveAllChildren(self.master.canvas, -4)
        self.master.canvas.master.after(4)
        self.moveAllChildren(self.master.canvas, 4)
        self.master.canvas.master.after(4)
        self.moveAllChildren(self.master.canvas, -4)   

    def shoot(self, event):
        if self.current_ammo > 0:
            self.reload_started_at = time()
            self.current_ammo -= 1
            starting_pos = self.master.getXY()
            starting_pos[0] = starting_pos[0] + self.master.getSize()[0]/2
            starting_pos[1] = starting_pos[1] + self.master.getSize()[1]/4
            goal = [event.x,
                    event.y]
            ProjectileManager.createProjectile(starting_pos, goal_xy=goal)
            self.shakeCamera()


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
                                             font=("Arial", 24, 'bold'),
                                             fill='linen')
        self.ammo = self.canvas.create_text(1260, 20, text="Ammo: 0",
                                            font=("Arial", 21, 'bold'),
                                            anchor='e',
                                            fill='linen')
        self.health = self.canvas.create_text(10, 20, text="Health: 0",
                                              font=("Arial", 21, 'bold'),
                                              anchor='w',
                                              fill='linen')

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
        ProjectileManager(self.canvas, self.windowManager)
        HealthTracker()
        ScoreTracker()
        EnemyManager(self.canvas, self.windowManager)

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
                self.canvas.configure(bg='salmon1')
            else:
                self.canvas.configure(bg='dark olive green')

    def cheatLife(self):
        HealthTracker.hp = 100

    def cheatBoom(self):
        resolution = self.windowManager.getResolution()
        # top and bottom
        y = resolution[1]
        for x in range(0, resolution[0], Projectile.SIZE):
            ProjectileManager.createProjectile(self.player.getXY(), [x, 0])
            ProjectileManager.createProjectile(self.player.getXY(), [x, y])
        # right
        x = resolution[0]
        for y in range(0, resolution[1], Projectile.SIZE//2):
            ProjectileManager.createProjectile(self.player.getXY(), [x, y])

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
        self.canvas = Canvas(self.frame,
                             width=self.windowManager.getResolution()[0],
                             height=self.windowManager.getResolution()[1],
                             background='dark olive green')
        self.canvas.pack()

        # background reduces framerate immensly
        # to the point where it isn't worth it
        # self.background = PhotoImage(file="assets/game_bg_2.gif")
        # self.canvas.create_image(0, 0, image=self.background, anchor='nw')

        starting_point = (60,
                          self.windowManager.getResolution()[1]/2)
        self.player = Player(self.canvas, starting_point)

        self.createGlobalStatTrackers()
        self.ui = UI(self.canvas, self.player)

        self.bindKeys()

    def saveGameToFile(self):
        data = {"player": self.player.getXY(),
                "enemies": [e.getXY() for e in EnemyManager.enemies],
                "hp": HealthTracker.hp,
                "score": ScoreTracker.score,
                "ammo": self.player.ammo_tracker.current_ammo}
        with open("save.json", 'w') as save_file:
            save_file.write(dumps(data))

    def loadFromFile(self):
        with open("save.json", 'r') as save_file:
            data = load(save_file)
        xy = data['player']
        self.canvas.coords(self.player.ID, xy[0], xy[1])
        HealthTracker.hp = data['hp']
        ScoreTracker.score = data['score']
        self.player.ammo_tracker.current_ammo = data['ammo']
        for e_coords in data['enemies']:
            e = Enemy(self.canvas, "zombie.gif")
            xy = createCoordsFromCenter(e_coords, e.SIZE)
            e.create(xy)
            EnemyManager.enemies.append(e)

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
            need_to_save = self.SAVE_AND_MENU or self.SAVE_AND_BOSSKEY

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
