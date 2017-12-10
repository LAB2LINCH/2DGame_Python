from pico2d import *
import random

class monster_sub():
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

    item_drop_list = None

    IDLE, RUN, ATK, ATKWAIT, SKILL1 = 0, 1, 2, 3, 4
    SLEEP = 8

    XSIZE, YSIZE, ROOT = 0,1,2

    sound_die = None
    sound_atk = None
    font = None
    hp_bar = None
    hp_bar_back = None

    monster_sub_data = [
        (48, 52, './src/mon_sub1.png'),
        (45, 42, './src/mon_sub2.png')
    ]

    def __init__(self, hp, pointXY, monster_type):
        self.hp = hp
        self.x , self.y = pointXY
        self.nextatktime = 2.5
        self.atkdelay = 0.25 #frame
        self.atktime = 0.5
        self.time = 0
        self.c_block = False
        self.sx = -100

        #see side left = -1, right = 1
        self.state = 0
        self.seeside = 1
        self.isground = True
        self.frame = 0
        self.down_spd = 10
        self.canmove = [True, True]
        self.l_block = None
        self.r_block = None
        self.d_block = None
        self.type = 0
        self.level = 0
        self.randomx = random.randint(0,10)
        self.runtime = 2.5
        self.sleeptime = random.randint(5,15) / 10
        self.image_size_x = self.monster_sub_data[monster_type][self.XSIZE]
        self.image_size_y = self.monster_sub_data[monster_type][self.YSIZE]
        self.monster_image = load_image(self.monster_sub_data[monster_type][self.ROOT])
        if monster_sub.hp_bar_back == None:
            monster_sub.hp_bar_back = load_image('./src/mon_hp_bar.png')
        if monster_sub.hp_bar == None:
            monster_sub.hp_bar = load_image('./src/mon_hp.png')
        if monster_sub.font == None:
            monster_sub.font = load_font('./src/ENCR10B.TTF')
        if monster_sub.sound_die == None:
            monster_sub.sound_die = load_wav("./src/mon_die.wav")
            monster_sub.sound_die.set_volume(100)
        if monster_sub.sound_atk == None:
            monster_sub.sound_atk = load_wav("./src/mon_atk.wav")
            monster_sub.sound_atk.set_volume(100)
        self.damaged = 0
        self.damaged_show_time = 1.5
        self.hp_percentage = 1.0
        self.max_hp = hp

    def damage(self, x):
        self.hp -= x
        if self.hp <= 0:
            monster_sub.sound_die.play()
            return True

    def onground(self, y):
        self.isground = True
        self.down_spd = 0
        self.y = (y + (self.image_size_y//2))

    def draw(self):
        if self.type == 0:
            self.monster_image.clip_draw(self.image_size_x//2 + (self.image_size_x//2 * self.seeside), 0, self.image_size_x, self.image_size_y, self.sx, self.y)
        self.hp_bar_back.draw(self.sx, self.y + 60)
        self.hp_bar.clip_draw_to_origin(0, 0, (int)(self.hp_bar.w * self.hp_percentage), self.hp_bar.h, self.sx-46, self.y+52,
                                                (int)(self.hp_bar.w * self.hp_percentage), self.hp_bar.h)

    def hitbox(self, type):
        if type == 0:
            return (self.sx - self.image_size_x//2, self.y - self.image_size_y//2, self. sx + self.image_size_x//2, self.y
                    + self.image_size_y//2)
        if type == 1:
            if self.seeside == -1:
                return (self.sx - self.image_size_x, self.y - self.image_size_y//2, self.sx - self.image_size_x//2, self.y
                        + self.image_size_y//2)
            else:
                return (self.sx + self.image_size_x//2, self.y - self.image_size_y//2, self.sx + self.image_size_x, self.y
                        + self.image_size_y//2)

    def draw_hitbox(self):
        draw_rectangle(*self.hitbox(0))

    # state = i ready to atk, w wait to atktime
    def update(self, frame_time, pointXY):
        self.sx = self.x-pointXY[0]
        if self.isground == False:
            self.down_spd -= self.GRAVITY_P * frame_time
            self.y += self.down_spd * frame_time
        self.hp_percentage = self.hp / self.max_hp

        if self.state == self.IDLE:
            if ((math.fabs(pointXY[1] - self.y) <= 120) and (math.fabs(800 - self.sx) <= 500)):
                if (800 - self.sx) >= 0 :
                    self.seeside = 1
                else:
                    self.seeside = -1
                self.state = self.RUN
        elif self.state == self.RUN:
            self.time += frame_time
            if (800 - self.sx) >= 0:
                self.seeside = 1
            else:
                self.seeside = -1
            if self.time >= self.runtime:
                self.time = 0
                self.state = self.SLEEP
            if self.seeside == -1 and self.canmove[0]:
                self.x += (self.seeside * self.RUN_SPEED_PPS * frame_time)
            elif self.seeside == 1 and self.canmove[1]:
                self.x += (self.seeside * self.RUN_SPEED_PPS * frame_time)
            if (math.fabs(800 - self.sx) <= (15 + self.randomx*2)):
                self.time = 0
                self.state = self.ATKWAIT
        elif self.state == self.SLEEP:
            self.time += frame_time
            if self.time >= self.sleeptime:
                self.time = 0
                self.sleeptime = random.randint(5,15) / 10
                self.state = self.RUN
            if (math.fabs(800 - self.sx) <= (20 + self.randomx)):
                self.time = 0
                self.state = self.ATKWAIT
        elif self.state == self.ATKWAIT:
            self.time += frame_time
            if self.time >= self.atkdelay:
                self.time = 0
                monster_sub.sound_atk.play()
                self.state = self.ATK
        elif self.state == self.ATK:
            self.time += frame_time
            if self.time >= self.atktime:
                self.time = 0
                self.state = self.IDLE

    def move(self):
        pass