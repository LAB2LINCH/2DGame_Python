from pico2d import *
import monster_body

class monster_main(monster_body.monster_body):
    monster1_image = None

    IDLE, RUN, ATKWAIT, ATK, SKILL1 = 0, 1, 2, 3, 4

    def __init__(self, hp, pointXY):
        monster_body.monster_body.__init__(self, hp, pointXY)
        if monster_main.monster1_image == None:
            monster_main.monster1_image = load_image('./src/mon_main1.png')
        self.c_skill1 = 600
        self.t_skill1 = 300
        self.skilltime = 0
        self.framesec = 0
        self.framesec2 = 0
        self.atkwaitframe = 30
        self.actionspd = 1

    def idle(self, pointXY):
        if ((math.fabs(pointXY[1] - self.y) <= 233) and (math.fabs(pointXY[0] - self.x) <= 500)):
            self.state = 1
            if (pointXY[0] - self.x) >= 0:
                self.seeside = 1
            else:
                self.seeside = -1

    def run(self, pointXY):
        if (pointXY[0] - self.x) >= 0:
            self.seeside = 1
        else:
            self.seeside = -1
        self.x += (self.seeside * self.spd * self.actionspd)
        # atktime
        if (math.fabs(pointXY[0] - self.x) <= 20):
            self.state = 2
            self.frame = 0

    def atkwait(self, pointXY):
        self.framesec2 = (self.framesec2 + 1) % (self.atkwaitframe / self.actionspd)
        if self.framesec2 == 0:
            self.framesec2 = 0
            if self.skilltime >= self.c_skill1:
                self.skilltime = 0
                self.state = 4
            else:
                self.state = 3

    def atk(self, pointXY):
        self.framesec2 = (self.framesec2 + 1) % (60 / self.actionspd)
        if self.framesec2 == 0:
            self.state = 0


    def skill1(self, pointXY):
        self.framesec2 = (self.framesec2 + 1) % (60 / self.actionspd)
        if self.framesec2 == 0:
            self.actionspd = 2
            self.skilltime = 0
            self.state = 0

    stateset = {
        RUN: run,
        IDLE: idle,
        ATKWAIT: atkwait,
        ATK: atk,
        SKILL1: skill1
    }

    def draw(self):
        x = (self.state * 556) + (self.seeside * 139) + 139
        monster_main.monster1_image.clip_draw((self.frame*108), x, 108, 278, self.x, self.y)

    def update(self, pointXY): #state 0=walk, wait / 1 = atkwait, 2=atk, 3=pattern
        self.framesec = (self.framesec + 1) % 3
        if self.framesec == 0:
            self.frame = (self.frame + 1) % 4

        self.skilltime += 1
        if (self.actionspd > 1 and self.skilltime >= self.t_skill1):
            self.actionspd = 1

        self.stateset[self.state](self, pointXY)