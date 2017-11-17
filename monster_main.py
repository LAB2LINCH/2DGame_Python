from pico2d import *
import monster_body

class monster_main(monster_body.monster_body):
    monster1_image = None

    PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 30 cm
    RUN_SPEED_KMPH = 30  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    IDLE, RUN, ATKWAIT, ATK, SKILL1 = 0, 1, 2, 3, 4

    LEFTSIDE, RIGHTSIDE = -1, 1

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
        self.level = 1

    def idle(self, frame_time, pointXY):
        if ((math.fabs(pointXY[1] - self.y) <= 233) and (math.fabs(pointXY[0] - self.x) <= 500)):
            self.state = self.RUN
            if (pointXY[0] - self.x) >= 0:
                self.seeside = self.RIGHTSIDE
            else:
                self.seeside = self.LEFTSIDE

    def run(self, frame_time, pointXY):
        if (pointXY[0] - self.x) >= 0:
            self.seeside = self.RIGHTSIDE
        else:
            self.seeside = self.LEFTSIDE
        self.x += (self.seeside * self.RUN_SPEED_PPS * self.actionspd * frame_time)
        # atktime
        if (math.fabs(pointXY[0] - self.x) <= 20):
            self.state = self.ATKWAIT
            self.frame = 0

    def atkwait(self, frame_time, pointXY):
        self.framesec2 = (self.framesec2 + 1) % (self.atkwaitframe / self.actionspd)
        if self.framesec2 == 0:
            self.framesec2 = 0
            if self.skilltime >= self.c_skill1:
                self.skilltime = 0
                self.state = self.SKILL1
            else:
                self.state = self.ATK

    def atk(self, frame_time, pointXY):
        self.framesec2 = (self.framesec2 + 1) % (60 / self.actionspd)
        if self.framesec2 == 0:
            self.state = self.IDLE


    def skill1(self, frame_time, pointXY):
        self.framesec2 = (self.framesec2 + 1) % (60 / self.actionspd)
        if self.framesec2 == 0:
            self.actionspd = 2
            self.skilltime = 0
            self.state = self.IDLE

    stateset = {
        RUN: run,
        IDLE: idle,
        ATKWAIT: atkwait,
        ATK: atk,
        SKILL1: skill1
    }
    def hitbox(self, type):
        if type == 0:
            return (self.x - 24, self.y - 26, self. x + 24, self.y + 26)
        if type == 1:
            if self.seeside == -1:
                return (self.x - 24, self.y - 26, self.x - 48, self.y + 26)
            else:
                return (self.x + 24, self.y - 26, self.x + 48, self.y + 26)

    def draw(self):
        x = (self.state * 556) + (self.seeside * 139) + 139
        monster_main.monster1_image.clip_draw((self.frame*108), x, 108, 278, self.x, self.y)

    def draw_hitbox(self):
        draw_rectangle(*self.hitbox(0))

    def update(self, frame_time, pointXY): #state 0=walk, wait / 1 = atkwait, 2=atk, 3=pattern
        monster_body.monster_body.update(self, frame_time)
        self.framesec = (self.framesec + 1) % 3
        if self.framesec == 0:
            self.frame = (self.frame + 1) % 4

        self.skilltime += 1
        if (self.actionspd > 1 and self.skilltime >= self.t_skill1):
            self.actionspd = 1

        self.stateset[self.state](self, frame_time, pointXY)