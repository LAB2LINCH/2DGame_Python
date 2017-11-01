import body

class monster_body(body.body):
    def __init__(self, hp, pointXY):
        body.body.__init__(self)
        self.hp = hp
        self.x , self.y = pointXY
        self.nextatktime = 150
        self.atkdelay = 15 #frame
        self.time = 0