import body

class monster_body(body.body):
    def __init__(self, hp, pointXY):
        body.body.__init__(self)
        self.hp = hp
        self.x , self.y = pointXY
        self.nextatktime = 2.5
        self.atkdelay = 0.25 #frame
        self.atktime = 0.5
        self.time = 0
        self.c_block = False

    def damage(self, x):
        self.hp -= x
        if self.hp <= 0:
            return True

    def update(self, frame_time):
        pass