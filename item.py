from pico2d import *

class item():
    PASSIVE, ACTIVE = 0, 1
    ATKPOWER, CRIT = 0, 1
    TIMESTOP, COOLTIME = 0, 1

    item_data = None

    def __init__(self, id, pointXY):
        if self.item_data == None:
            self.item_data = [
                ("sword", self.PASSIVE, self.ATKPOWER, 2, './src/item_sword.png'),
                ("glasses", self.PASSIVE, self.CRIT, 5, './src/item_glasses.png'),
                ("frizon", self.ACTIVE, self.TIMESTOP, 3, './src/item_frizon.png'),
                ("resetball", self.ACTIVE, self.COOLTIME, 1.5, './src/item_resetball.png')
            ]

        self.spd = 8
        self.reverse_time = 1
        self.id = id
        self.name = self.item_data[id][0]
        self.part = self.item_data[id][2]  # value가 어디에 사용될껀지
        self.value = self.item_data[id][3]
        self.image = load_image(self.item_data[id][4])
        self.type = self.item_data[id][1]
        self.x = pointXY[0]
        self.y = pointXY[1]

    def hitbox(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self, frame_time):
        self.y += self.spd * frame_time
        self.reverse_time -= frame_time
        if self.reverse_time <= 0:
            self.spd *= -1
            self.reverse_time = 1
