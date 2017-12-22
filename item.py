from pico2d import *

class item():
    PASSIVE, ACTIVE = 0, 1
    ATKPOWER, CRIT = 0, 1
    TIMESTOP, COOLTIME = 0, 1

    item_count = 4

    item_data = None
    item_image = []

    item_data = [
                ("sword", PASSIVE, ATKPOWER, 2, './src/item_sword.png'),
                ("glasses", PASSIVE, CRIT, 5, './src/item_glasses.png'),
                ("frizon", ACTIVE, TIMESTOP, 4, './src/item_frizon.png'),
                ("resetball", ACTIVE, COOLTIME, 1.5, './src/item_resetball.png')
            ]

    def __init__(self, id, pointXY):
        if len(item.item_image) == 0:
            for i in range(item.item_count):
                item.item_image.append(load_image(item.item_data[i][4]))
        self.spd = 8
        self.reverse_time = 1
        self.id = id
        self.name = item.item_data[id][0]
        self.part = item.item_data[id][2]  # value가 어디에 사용될껀지
        self.value = item.item_data[id][3]
        self.type = item.item_data[id][1]
        self.x = pointXY[0]
        self.y = pointXY[1]
        self.sx = -100

    def hitbox(self):
        return self.sx - 25, self.y - 25, self.sx + 25, self.y + 25

    def draw(self):
        item.item_image[self.id].draw(self.sx, self.y)

    def update(self, frame_time, pointXY):
        self.sx = self.x - pointXY[0]
        self.y += self.spd * frame_time
        self.reverse_time -= frame_time
        if self.reverse_time <= 0:
            self.spd *= -1
            self.reverse_time = 1
