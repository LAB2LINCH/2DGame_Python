from pico2d import *
import monster_body

class monster_main(monster_body.monster_body):
    monster1_image = None

    def __init__(self, hp, pointXY):
        monster_body.monster_body.__init__(self, hp, pointXY)
        if monster_main.monster1_image == None:
            monster_main.monster1_image = load_image('./src/mon_main1.png')
        self.skill_state = 0
        self.framesec = 0

    def draw(self):
        monster_main.monster1_image.clip_draw((self.frame*108), 139 + (self.seeside * 139), 108, 278, self.x, self.y)

    def update(self, pointXY):
        self.framesec = (self.framesec + 1) % 3
        if self.framesec == 0:
            self.frame = (self.frame + 1) % 4
        if self.state == 'I':
            if ((math.fabs(pointXY[1] - self.y) <= 233) and (math.fabs(pointXY[0] - self.x) <= 500)):
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

    def patern1(self):
        self.skill_state = 1