from pico2d import *
import monster_body

class monster_sub(monster_body.monster_body):
    monster1_image = None

    def __init__(self, hp, pointXY):
        monster_body.monster_body.__init__(self, hp, pointXY)
        self.type = 0
        if monster_sub.monster1_image == None:
            monster_sub.monster1_image = load_image('./src/mon_sub1.png')

    def draw(self):
        if self.type == 0:
            self.monster1_image.clip_draw(24+(24*self.seeside), 0, 48, 52, self.x, self.y)

    # state = i ready to atk, w wait to atktime
    def update(self, pointXY):
        if self.state == 'I':
            if ((math.fabs(pointXY[1] - self.y) <= 120) and (math.fabs(pointXY[0] - self.x) <= 500)):
                if (pointXY[0] - self.x) >= 0 :
                    self.seeside = 1
                else:
                    self.seeside = -1
                self.x += (self.seeside * self.spd)
                # atktime
                if (math.fabs(pointXY[0] - self.x) <= 20):
                    self.state = 'W'
        elif self.state == 'W':
            self.time += 1
            if self.time >= self.nextatktime:
                self.time = 0
                self.state = 'I'

    def move(self):
        pass