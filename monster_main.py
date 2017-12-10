from pico2d import *

class monster_main():
    PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 40 cm
    RUN_SPEED_KMPH = 35  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    JUMP_HEIGHT = 8  # max Meter
    JUMP_HEIGHT_P = (JUMP_HEIGHT * PIXEL_PER_METER)
    JUMP_TIME = 0.8

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    JUMP_START = ((JUMP_HEIGHT_P * 2) / (JUMP_TIME / 2))
    GRAVITY_P = (JUMP_START / (JUMP_TIME / 2))

    IDLE, RUN, ATKWAIT, ATK, SKILL1, SKILL2 = 0, 1, 2, 3, 4, 5
    LEFTSIDE, RIGHTSIDE = -1, 1
    BODY, NORMALATK, RANGEATK = 0, 1, 2

    XSIZE, YSIZE, ROOT, FRAME_COUNT = 0,1,2, 3

    monster_main_data = [
        (102, 210, './src/mon_main1.png', 3),
        (108, 278, './src/mon_main2.png', 4),
        (108, 168, './src/mon_main3.png', 4)
    ]

    sound_atk = None
    sound_buf = None

    def hp_percentage(self):
        return self.hp / self.max_hp

    def __init__(self, hp, pointXY, monster_type):
        self.hp = hp
        self.max_hp = hp
        self.x , self.y = pointXY
        self.nextatktime = 2.5
        self.atkdelay = 0.25 #frame
        self.atktime = 0.5
        self.time = 0
        self.state = 0
        self.seeside = self.RIGHTSIDE
        self.isground = True
        self.frame = 0
        self.down_spd = 10
        self.canmove = [True, True]
        self.l_block = None
        self.r_block = None
        self.d_block = None
        self.monster_type = monster_type
        self.monster_image = load_image(self.monster_main_data[monster_type][self.ROOT])
        self.image_size_x = self.monster_main_data[monster_type][self.XSIZE]
        self.image_size_y = self.monster_main_data[monster_type][self.YSIZE]
        self.how_many_frames = self.monster_main_data[monster_type][self.FRAME_COUNT]
        self.c_skill1 = 10
        self.c_skill2 = 5
        self.t_skill1 = 5
        self.skilltime = 0
        self.skilltime2 = 0
        self.framesec = 0
        self.framesec2 = 0
        self.atk_wait_time = 0.5
        self.actionspd = 1
        self.level = 1
        self.action_time = 1
        self.sx = -100

        if monster_main.sound_atk == None:
            monster_main.sound_atk = load_wav("./src/boss_at.wav")
            monster_main.sound_atk.set_volume(32)
        if monster_main.sound_buf == None:
            monster_main.sound_buf = load_wav("./src/boss_sk.wav")
            monster_main.sound_buf.set_volume(32)

        self.is_sound_on = True

    def onground(self, y):
        self.isground = True
        self.down_spd = 0
        self.y = (y + (self.image_size_y//2))

    def damage(self, x):
        self.hp -= x
        if self.hp <= 0:
            return True

    def idle(self, frame_time, pointXY):
        if ((math.fabs(pointXY[1] - self.y) <= 233) and (math.fabs(800 - self.sx) <= 500)):
            self.state = self.RUN
            if (800 - self.sx) >= 0:
                self.seeside = self.RIGHTSIDE
            else:
                self.seeside = self.LEFTSIDE

    def run(self, frame_time, pointXY):
        if (800 - self.sx) >= 0:
            self.seeside = self.RIGHTSIDE
        else:
            self.seeside = self.LEFTSIDE
        self.x += (self.seeside * self.RUN_SPEED_PPS * self.actionspd * frame_time)
        # atktime
        if (math.fabs(800 - self.sx) <= 20):
            self.state = self.ATKWAIT
            self.frame = 0

    def atkwait(self, frame_time, pointXY):
        self.framesec2 +=  frame_time
        if self.framesec2 >= (self.atk_wait_time / self.actionspd):
            self.framesec2 = 0
            if self.skilltime >= self.c_skill1:
                self.skilltime = 0
                self.state = self.SKILL1
            elif self.skilltime2 >= self.c_skill2:
                self.skilltime2 = 0
                self.state = self.SKILL2
            else:
                self.state = self.ATK

    def atk(self, frame_time, pointXY):
        self.framesec2 += frame_time
        if self.is_sound_on:
            monster_main.sound_atk.play()
            self.is_sound_on = False
        if self.framesec2 >= (self.action_time / self.actionspd):
            self.framesec2 = 0
            self.is_sound_on = True
            self.state = self.IDLE


    def skill1(self, frame_time, pointXY):
        self.framesec2 += frame_time
        if self.framesec2 >= (self.action_time / self.actionspd):
            self.framesec2 = 0
            self.actionspd = 2
            self.skilltime = 0
            self.state = self.IDLE
            self.is_sound_on = True
        if self.is_sound_on:
            monster_main.sound_buf.play()
            self.is_sound_on = False

    def skill2(self, frame_time, pointXY):
        self.framesec2 += frame_time
        if self.is_sound_on:
            monster_main.sound_atk.play()
            self.is_sound_on = False
        if self.framesec2 >= (self.action_time*2 / self.actionspd):
            self.is_sound_on = True
            self.framesec2 = 0
            self.state = self.IDLE

    stateset = {
        RUN: run,
        IDLE: idle,
        ATKWAIT: atkwait,
        ATK: atk,
        SKILL1: skill1,
        SKILL2: skill2
    }

    def hitbox(self, type):
        if type == self.BODY:
            return (self.sx - self.image_size_x//2, self.y - self.image_size_y//2, self.sx + self.image_size_x//2, self.y)
        elif type == self.NORMALATK:
            return (self.sx - self.image_size_x*3//4, self.y - self.image_size_y//2, self.sx + self.image_size_x*3//4, self.y)
        elif type == self.RANGEATK and self.seeside == -1:
            return (self.sx - self.image_size_x*3, self.y - self.image_size_y//3, self.sx + self.image_size_x//2, self.y)
        elif type == self.RANGEATK and self.seeside == 1:
            return (self.sx - self.image_size_x//2, self.y - self.image_size_y//3, self.sx + self.image_size_x*3, self.y)

    def draw(self):
        if self.monster_type == 1:
            if self.state >= self.ATKWAIT:
                x = (self.ATKWAIT * self.image_size_y*2) + (self.seeside * self.image_size_y//2) + self.image_size_y//2
            else:
                x = (self.state * self.image_size_y*2) + (self.seeside * self.image_size_y//2) + self.image_size_y//2
        else:
            if self.state >= self.ATK:
                x = (self.ATK * self.image_size_y*2) + (self.seeside * self.image_size_y//2) + self.image_size_y//2
            else:
                x = (self.state * self.image_size_y*2) + (self.seeside * self.image_size_y//2) + self.image_size_y//2
        self.monster_image.clip_draw((self.frame*self.image_size_x), x, self.image_size_x, self.image_size_y, self.sx, self.y)

    def draw_hitbox(self):
        draw_rectangle(*self.hitbox(0))
        draw_rectangle(*self.hitbox(1))
        draw_rectangle(*self.hitbox(2))

    def update(self, frame_time, pointXY): #state 0=walk, wait / 1 = atkwait, 2=atk, 3=pattern
        self.sx = self.x-pointXY[0]
        self.framesec += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = (int)(self.framesec) % self.how_many_frames

        if self.isground == False:
            self.down_spd -= self.GRAVITY_P * frame_time
            self.y += self.down_spd * frame_time

        self.skilltime += frame_time
        self.skilltime2 += frame_time
        if (self.actionspd > 1 and self.skilltime >= self.t_skill1):
            self.actionspd = 1

        self.stateset[self.state](self, frame_time, pointXY)

