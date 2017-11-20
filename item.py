class item():
    PASSIVE, ACTIVE = 0, 1
    ATKPOWER, CRIT = 0, 1
    TIMESTOP, MOVE = 0, 1

    item_data = None

    def __init__(self, id, pointXY):
        if self.item_data == None:
            self.item_data = [
                [{0: ("sword", self.PASSIVE, self.ATKPOWER, 2, './src/item_sword')},
                 {1: ("glass", self.PASSIVE, self.CRIT, 5, './src/item_glass')}],
                [{2: ("clock", self.ACTIVE, self.TIMESTOP, 3, './src/item_clock')},
                 {3: ("shoose", self.ACTIVE, self.MOVE, 1.5, './src/item_shoose')}]
            ]

        self.id = id
        self.name = self.item_data[id][0]
        self.part = self.item_data[id][2]  # value가 어디에 사용될껀지
        self.value = self.item_data[id][3]
        self.image = self.item_data[id][4]
        self.type = self.item_data[id][1]
        self.x = 0
        self.y = 0

    def hitbox(self):
        return self.x - self.image.w//2, self.y - self.image.h//2, self.x + self.image.w//2, self.y + self.image.h//2

    def draw(self):
        self.image.draw(self.x, self.y)
