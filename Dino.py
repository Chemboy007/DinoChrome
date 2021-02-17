import pyglet
import time
import csv


class Record:
    fields = ["Distance", "Speed"]

    def __init__(self):
        self.file = open("data.csv", "w", newline="")
        self.file_writer = csv.writer(self.file)
        self.file_writer.writerow(Record.fields)

    def record(self, distance, speed):
        self.file_writer.writerow([distance, speed])


class Dino:
    def __init__(self):
        self.x = 50
        self.y = 0
        self.height = 100
        self.width = 10
        self.rate = -5

    def jump(self):
        if self.y <= 0:
            self.rate = 10

    def update(self):
        self.y += self.rate
        pyglet.shapes.Rectangle(x=self.x, y=self.y,
                                width=self.width, height=self.height,
                                color=(255, 0, 0)).draw()
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


records = Record()
start = time.time()
cac = Cactus()
player = Dino()
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
    if game:
        window.clear()
        cac.draw()
        player.update()
        score = time.time() - start
        score_label.text = "Score: " + str(int(score))
        score_label.draw()
    else:
        label = pyglet.text.Label('Game over',
                                  font_name='Times New Roman',
                                  font_size=36,
                                  x=window.width // 2, y=window.height // 2,
                                  anchor_x='center', anchor_y='center')
        label.draw()



@window.event
def on_key_press(symbol, mod):
    global game

    if game:
        if symbol == pyglet.window.key.SPACE:
            player.jump()
            capture()
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
    collision_check()


def collision_check():
    global game
    if (player.x > cac.x) and (player.x < cac.x + cac.width):
        if player.y < cac.height:
            # print("collide")
            game = 0


def capture():
     distance = cac.x - player.x
     records.record(distance, cac.speed)



def new_cactus():
    global cac
    cac = Cactus()


pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()

