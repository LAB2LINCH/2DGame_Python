from pico2d import *
import monster_body

class monster_sub(monster_body.monster_body):

    PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    monster1_image = None

    RUN, IDLE, ATK = 0, 1, 2

    def __init__(self, hp, pointXY):
        monster_body.monster_body.__init__(self, hp, pointXY)
        self.type = 0
        if monster_sub.monster1_image == None:
            monster_sub.monster1_image = load_image('./src/mon_sub1.png')

    def draw(self):
        if self.type == 0:
            self.monster1_image.clip_draw(24+(24*self.seeside), 0, 48, 52, self.x, self.y)

    def hitbox(self, type):
        if type == 0:
            return (self.x + 24, self.y + 26, self. x - 24, self.y - 26)
        if type == 1:
            if self.seeside == -1:
                return (self.x - 24, self.y + 26, self.x - 48, self.y - 26)
            else:
                return (self.x + 24, self.y + 26, self.x + 48, self.y - 26)

    # state = i ready to atk, w wait to atktime
    def update(self, frame_time, pointXY):
        if self.state == self.RUN:
            if ((math.fabs(pointXY[1] - self.y) <= 120) and (math.fabs(pointXY[0] - self.x) <= 500)):
                if (pointXY[0] - self.x) >= 0 :
                    self.seeside = 1
                else:
                    self.seeside = -1
                self.x += (self.seeside * self.RUN_SPEED_PPS * frame_time)
                # atktime
                if (math.fabs(pointXY[0] - self.x) <= 20):
                    self.state = self.ATK
        elif self.state == self.ATK:
            self.time += frame_time
            if self.time >= self.nextatktime:
                self.time = 0
                self.state = self.RUN

    def move(self):
        pass