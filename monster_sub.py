from pico2d import *
import random
import monster_body

class monster_sub(monster_body.monster_body):

    monster1_image = None

    IDLE, RUN, ATK, ATKWAIT, SKILL1 = 0, 1, 2, 3, 4
    SLEEP = 8

    def __init__(self, hp, pointXY):
        monster_body.monster_body.__init__(self, hp, pointXY)
        self.type = 0
        self.level = 0
        self.randomx = random.randint(0,10)
        self.runtime = 2.5
        self.sleeptime = random.randint(5,15) / 10
        if monster_sub.monster1_image == None:
            monster_sub.monster1_image = load_image('./src/mon_sub1.png')

    def draw(self):
        if self.type == 0:
            self.monster1_image.clip_draw(24+(24*self.seeside), 0, 48, 52, self.x, self.y)

    def hitbox(self, type):
        if type == 0:
            return (self.x - 24, self.y - 26, self. x + 24, self.y + 26)
        if type == 1:
            if self.seeside == -1:
                return (self.x - 24, self.y - 26, self.x - 48, self.y + 26)
            else:
                return (self.x + 24, self.y - 26, self.x + 48, self.y + 26)

    def draw_hitbox(self):
        draw_rectangle(*self.hitbox(0))

    # state = i ready to atk, w wait to atktime
    def update(self, frame_time, pointXY):
        if self.isground == False:
            self.down_spd -= self.GRAVITY_P * frame_time
            self.y += self.down_spd * frame_time

        if self.state == self.IDLE:
            if ((math.fabs(pointXY[1] - self.y) <= 120) and (math.fabs(pointXY[0] - self.x) <= 500)):
                if (pointXY[0] - self.x) >= 0 :
                    self.seeside = 1
                else:
                    self.seeside = -1
                self.state = self.RUN
        elif self.state == self.RUN:
            self.time += frame_time
            if (pointXY[0] - self.x) >= 0:
                self.seeside = 1
            else:
                self.seeside = -1
            if self.time >= self.runtime:
                self.time = 0
                self.state = self.SLEEP
            self.x += (self.seeside * self.RUN_SPEED_PPS * frame_time)
            if (math.fabs(pointXY[0] - self.x) <= (15 + self.randomx*2)):
                self.time = 0
                self.state = self.ATKWAIT
        elif self.state == self.SLEEP:
            self.time += frame_time
            if self.time >= self.sleeptime:
                self.time = 0
                self.sleeptime = random.randint(5,15) / 10
                self.state == self.RUN
            if (math.fabs(pointXY[0] - self.x) <= (20 + self.randomx)):
                self.time = 0
                self.state = self.ATKWAIT
        elif self.state == self.ATKWAIT:
            self.time += frame_time
            if self.time >= self.atkdelay:
                self.time = 0
                self.state = self.ATK
        elif self.state == self.ATK:
            self.time += frame_time
            if self.time >= self.atktime:
                self.time = 0
                self.state = self.IDLE

    def move(self):
        pass