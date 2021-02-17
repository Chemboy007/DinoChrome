import pyglet
import time
from GeneticAlgo import *
import copy
import csv


class Record:

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "r+", newline="")

        # self.fields = ["Distance", "Speed"]
        # self.file_writer = csv.writer(self.file)

    def set_fields(self, fields):
        self.field = fields

    def reader(self):
        return csv.DictReader(self.file)

    def capture(self, rows):
        with open(self.filename, "w", newline='') as file:
            writer = csv.DictWriter(file, self.field)
            writer.writeheader()
            writer.writerows(rows)
        pass


class Dino:
    r = 255

    def __init__(self):
        self.x = 50
        self.y = 0
        self.height = 100
        self.width = 10
        self.rate = -5
        self.genes = []
        self.score = -5
        self.time = 0
        self.color = (Dino.r, 0, 0)
        self.jumpCount = 0
        Dino.r -= 10

    def think(self, dist):
        y = self.genes[0]*Cactus.speed + self.genes[1]*dist + self.genes[2]
        if y > 2:
            self.jump()

    def jump(self):
        if self.y <= 0:
            self.jumpCount += 1
            self.rate = 10

    def update(self):
        self.y += self.rate
        pyglet.shapes.Rectangle(x=self.x, y=self.y,
                                width=self.width, height=self.height,
                                color=self.color).draw()
        if self.y <= 0:
            self.rate = 0
        elif self.y >= 200:
            self.rate = -5


class Cactus:
    def __init__(self):
        self.x = 800 + Cactus.speed*200/5
        self.y = 0
        self.height = 100
        self.width = 50

    speed = 5

    def update_x(self):
        self.x -= Cactus.speed
        Cactus.speed += 0.001

    def draw(self):
        # print(Cactus.speed)
        pyglet.shapes.Rectangle(x=self.x, y=self.y,
                                width=self.width, height=self.height,
                                color=(55, 55, 255)).draw()


record = Record("results.csv")
record.set_fields(["Gen", "alpha=0.2", "best(0.2)", "alpha=0.5", "best(0.5)", "alpha=0.7",
                   "best(0.7)", "alpha=1", "best(1)"])
test = record.reader()
rows = []
for row in test:
    rows.append(row)
print(rows)


gen = 1
bots = []
size = 16
genes = populate(size)
for i in range(size):
    person = Dino()
    person.genes = genes[i]
    bots.append(person)
stack = []

start = time.time()
cac = Cactus()
# player = Dino()
window = pyglet.window.Window(height=800, width=800, resizable=True)

square = pyglet.shapes.Rectangle(x=700, y=0, width=50, height=100, color=(55, 55, 255))
score_label = pyglet.text.Label('score: ',
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width // 2, y=window.height ,
                              anchor_x='left', anchor_y='top')

game = 1


@window.event
def on_draw():
    global start, gen, stack
    # if game:
    window.clear()
    cac.draw()
    for b in bots:
        b.update()
    score = time.time() - start
    score_label.text = "Score: " + str(int(score))
    score_label.draw()
    # else:
    label = pyglet.text.Label('',
                              font_name='Times New Roman',
                              font_size=36,
                              x=window.width // 2, y=window.height // 2,
                              anchor_x='center', anchor_y='center')
    label.text = "Bots: " + str(len(bots))
    label.draw()

    if len(bots) == 0 or score > 200:
        if score > 200:
            for bot in bots:
                bot.score = int(time.time() - start) - bot.jumpCount / int(time.time() - start)
                bot.time = int(time.time() - start)
                stack.append(bot)
                bot.jumpCount = 0
                bots.remove(bot)

        Cactus.speed = 5
        new_cactus()
        start = time.time()
        stack.sort(key=lambda bot: bot.score)

        avg = 0
        for i in stack:
            # print(i.score)
            avg += int(i.time)
        avg /= len(stack)
        best = stack[len(stack) - 1]

        rows[gen-1]["alpha=1"] = avg
        rows[gen-1]["best(1)"] = best.score

        for _ in range(size//2):
            bots.append(stack.pop())
        stack.clear()
        temp = mutate(copy.deepcopy(bots))
        bots.extend(temp)
        print(" gen: ", gen)
        print("best: ", best.time, " avg: ", avg, " bscore: ", best.score)
        gen += 1


@window.event
def on_key_press(symbol, mod):
    global game
    if game:
        if symbol == pyglet.window.key.SPACE:
            player.jump()
    else:
        if symbol == pyglet.window.key.ENTER:
            global start, cac
            cac = Cactus()
            Cactus.speed = 5
            start = time.time()
            game = 1


def update(time):
    cac.update_x()
    if cac.x < 0:
        new_cactus()
    for b in bots:
        distance = cac.x - b.x
        b.think(distance)
        if collision_check(b):
            stack.append(b)
            b.jumpCount = 0
            bots.remove(b)


def collision_check(bot):
    global game
    if (bot.x > cac.x) and (bot.x < cac.x + cac.width):
        if bot.y < cac.height:
            bot.score = int(time.time() - start) - bot.jumpCount / int(time.time() - start)
            bot.time = int(time.time() - start)
            return 1
        else:
            return 0


def new_cactus():
    global cac
    cac = Cactus()


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()

record.capture(rows)
