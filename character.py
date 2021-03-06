from pico2d import *
import item
import random

class character():

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

    RIGHT_RUN, LEFT_RUN, RIGHT_IDLE, LEFT_IDLE = 0, 1, 2, 3
    R_Z_SKILL, L_Z_SKILL, R_X_SKILL, L_X_SKILL, R_C_SKILL, L_C_SKILL, R_V_SKILL, L_V_SKILL = 4, 5, 6, 7, 8, 9, 10, 11

    LEFTSIDE, RIGHTSIDE = -1, 1

    LEFT, RIGHT = 0, 1

    PASSIVE, ACTIVE = 0, 1
    sound_skill_v = None
    sound_normal_atk = None
    sound_skill_z = None
    sound_jump = None

    def pause(self):
        self.keydown = 0
        self.leftinput = False
        self.rightinput = False
        self.change_state()

    def get_active_item_id(self):
        return self.itemlist[self.itemvalue-1][0]

    def skill_cooltime_check(self):
        return (1.5-self.c_skill_z, 0.5-self.c_skill_x, 3-self.c_skill_c, 5-self.c_skill_v,
                self.itemlist[self.itemvalue-1][1]-self.item_cooldown)

    def handle_run(self, frame_time):
        if self.seeside == -1:
            if not self.canmove[self.LEFT]:
                return
        if self.seeside == 1:
            if not self.canmove[self.RIGHT]:
                return
        self.x = clamp(20, self.x + (self.RUN_SPEED_PPS * self.seeside * frame_time), 1580)
        self.skill_x -= (self.RUN_SPEED_PPS * self.seeside * frame_time)

    def handle_idle(self, frame_time):
        pass

    def handle_jump(self, frame_time):
        self.down_spd = self.JUMP_START
        character.sound_jump.play()
        self.isground = False
        self.y += 3

    def is_down(self):
        if(self.down_spd <= 0):
            return True
        else:
            return False

    def change_state(self):
        if self.seeside == self.LEFTSIDE:
            if self.leftinput:
                self.state = self.LEFT_RUN
            else:
                self.state = self.LEFT_IDLE
        elif self.seeside == self.RIGHTSIDE:
            if self.rightinput:
                self.state = self.RIGHT_RUN
            else:
                self.state = self.RIGHT_IDLE

    def handle_z_skill(self, frame_time): # move
        if self.aniemelock:
            self.skillsec += frame_time
            if self.skillsec >= self.t_skill_z:
                self.skillsec = 0
                self.aniemelock = False
                self.change_state()
        elif self.c_skill_z >= 1.5:
            self.x = clamp(2, self.x +self.RUN_SPEED_PPS * self.seeside * 0.5, 1580)
            self.skill_x -= (self.RUN_SPEED_PPS * self.seeside * 0.5)
            character.sound_skill_z.play()
            self.ATK = True
            self.c_skill_z = 0
            self.aniemelock = True
        else:
            self.change_state()

    def handle_x_skill(self, frame_time): # atk
        if self.aniemelock:
            self.skillsec += frame_time
            if self.skillsec >= self.t_skill_x:
                self.skillsec = 0
                self.aniemelock = False
                self.change_state()
        elif self.c_skill_x >= 0.5:
            self.ATK = True
            self.c_skill_x = 0
            self.aniemelock = True
            character.sound_normal_atk.play()
        else:
            self.change_state()

    def handle_c_skill(self, frame_time): # 6hit
        if self.aniemelock:
            self.skillsec += frame_time
            if self.skillsec >= self.t_skill_c:
                self.skillsec = 0
                self.aniemelock = False
                self.change_state()
                self.atk_count2 = 0
            self.atk_count = (int)((self.atk_count + (frame_time * 10)) % 4)
            if self.atk_count == 0 and self.atk_count2 < 6:
                self.atk_count2 += 1
                character.sound_normal_atk.play()
        elif self.c_skill_c >= 3:
            self.ATK = True
            self.c_skill_c = 0
            self.aniemelock = True
        else:
            self.change_state()

    def handle_v_skill(self, frame_time): # area
        if self.aniemelock:
            self.skillsec += frame_time
            if self.skillsec >= self.t_skill_v:
                self.skillsec = 0
                self.aniemelock = False
                self.change_state()
        elif self.c_skill_v >= 5:
            self.ATK = True
            self.c_skill_v = 0
            self.aniemelock = True
            character.sound_skill_v.play()
        else:
            self.change_state()

    def use_active_item(self):
        if self.itemlist[self.itemvalue-1][0] == 0:
            return
        if self.item_cooldown >= self.itemlist[self.itemvalue-1][1]:
            if self.itemlist[self.itemvalue-1][0] == 2:
                self.immortal = True
            if self.itemlist[self.itemvalue-1][0] == 3:
                self.c_skill_z = 5
                self.c_skill_x = 5
                self.c_skill_c = 5
                self.c_skill_v = 5
            self.item_cooldown = 0


    handle_state = {
        RIGHT_RUN: handle_run,
        LEFT_RUN: handle_run,
        RIGHT_IDLE: handle_idle,
        LEFT_IDLE: handle_idle,
        L_Z_SKILL: handle_z_skill,
        R_Z_SKILL: handle_z_skill,
        L_X_SKILL: handle_x_skill,
        R_X_SKILL: handle_x_skill,
        L_C_SKILL: handle_c_skill,
        R_C_SKILL: handle_c_skill,
        L_V_SKILL: handle_v_skill,
        R_V_SKILL: handle_v_skill
    }
    def down(self):
        self.isground = False

    def hit(self):
        if self.immortal:
            return False
        else:
            return True

    def hitbox(self, type): #idle, atk, skillc, skillv
        if type == 0: return (self.canvas_x - 16, self.y - 18, self.canvas_x + 16, self. y + 18)
        elif type == 1:
            if self.seeside == -1:
               return (self.canvas_x  -32, self.y - 18, self.canvas_x -16, self.y + 18)
            else:
               return (self.canvas_x + 16, self.y - 18, self.canvas_x + 32, self.y + 18)
        elif type == 2: return (self.canvas_x - 50, self.y - 54, self.canvas_x + 50, self.y + 54)
        elif type == 3: return (self.canvas_x - 240, self.y - 20, self.canvas_x + 240, self.y + 20)

    def draw_hitbox(self):
        draw_rectangle(*self.hitbox(0))
        draw_rectangle(*self.hitbox(1))
        draw_rectangle(*self.hitbox(2))
        draw_rectangle(*self.hitbox(3))

    def damage(self, pointXY):
        self.skill_x, self.skill_y = pointXY
        if self.state in (self.L_C_SKILL, self.R_C_SKILL):
            self.anime_time = 0.5
            self.anime_state = 1
        elif self.state in (self.L_X_SKILL, self.R_X_SKILL):
            self.anime_time = 0.5
            self.anime_state = 0
        if(random.randrange(0,100) <= self.critchance):
            return (self._damage * 2)
        else:
            return self._damage

    def stage_Change(self):
        #see side left = -1, right = 1
        self.state = 0
        self.seeside = 1
        self.isground = False
        self.frame = 0
        self.down_spd = 10
        self.canmove = [True, True]
        self.l_block = None
        self.r_block = None
        self.d_block = None
        self.x, self.y = 800, 1000
        self.framesec = 0
        self.skillsec = 0
        self.anime_time = 0
        self.anime_state = 0
        self.skill_x, self.skill_y = 0, 0
        self.c_skill_z = 0
        self.c_skill_x = 0
        self.c_skill_c = 0
        self.c_skill_v = 0
        self.atk_count = 0
        self.atk_count2 = 0
        self.state = 2
        self.keydown = 0
        self.aniemelock = False
        self.leftinput = False
        self.rightinput = False
        self.ATK = False
        self.item_cooldown = 0
        self.immortal = False
        self.immortal_time = 0


    def __init__(self, itemvalue):
        #see side left = -1, right = 1
        self.state = 0
        self.seeside = 1
        self.isground = True
        self.frame = 0
        self.down_spd = 10
        self.imagesize_y = 0
        self.canmove = [True, True]
        self.l_block = None
        self.r_block = None
        self.d_block = None

        self.image_char = load_image('./src/char.png')
        self.image_skill_x = load_image('./src/char_atk.png')
        self.image_skill_c = load_image('./src/char_skill_c.png')
        self.image_skill_v = load_image('./src/char_skill_v.png')
        self.x, self.y = 800, 1000
        self.item_cooldown = 0
        self.framesec = 0
        self.skillsec = 0
        self.c_skill_z = 0
        self.c_skill_x = 0
        self.c_skill_c = 0
        self.c_skill_v = 0
        self.t_skill_z = 0.25
        self.t_skill_x = 1/15
        self.t_skill_c = 0.25
        self.t_skill_v = 0.5
        self.anime_time = 0
        self.anime_state = 0
        self.skill_x, self.skill_y = 0, 0
        self._damage = 10
        self.atk_count = 0
        self.atk_count2 = 0
        self.state = 2
        self.keydown = 0
        self.critchance = 5
        self.aniemelock = False
        self.leftinput = False
        self.rightinput = False
        self.imagesize_y = 34
        self.ATK = False
        self.itemlist = []
        self.itemvalue = itemvalue
        self.canvas_x = get_canvas_width()//2
        self.immortal = False
        self.immortal_time = 0
        for i in range(itemvalue): # PASSIVE 아이템
            self.itemlist.append([i, 0])
        self.itemlist[itemvalue-1][0] = 0

        if character.sound_skill_z == None:
            character.sound_skill_z = load_wav('./src/char_blink.wav')
            character.sound_skill_z.set_volume(50)
        if character.sound_jump == None:
            character.sound_jump = load_wav('./src/char_jump.wav')
            character.sound_jump.set_volume(50)
        if character.sound_skill_v == None:
            character.sound_skill_v = load_wav('./src/earth_skill.wav')
            character.sound_skill_v.set_volume(100)
        if character.sound_normal_atk == None:
            character.sound_normal_atk = load_wav('./src/normal_atk.wav')
            character.sound_skill_v.set_volume(32)

    def onground(self, y):
        self.isground = True
        self.down_spd = 0
        self.y = (y + (self.imagesize_y//2))

    def getitem(self, item):
        if item.type == 0:
            self.itemlist[item.id][1] = self.itemlist[item.id][1] + 1
            if item.part == item.ATKPOWER:
                self._damage += item.value
            elif item.part == item.CRIT:
                self.critchance += item.value
        else:
            self.itemlist[self.itemvalue-1][0] = item.id
            self.itemlist[self.itemvalue-1][1] = item.value
            self.item_cooldown = 0

    def cooldown(self, frame_time):
        self.c_skill_z += frame_time
        self.c_skill_x += frame_time
        self.c_skill_c += frame_time
        self.c_skill_v += frame_time

    def update(self, frame_time):
        self.item_cooldown += frame_time
        if self.anime_time > 0:
            self.anime_time -= frame_time
        if self.immortal:
            self.immortal_time += frame_time
            if self.immortal_time >= 1.5:
                self.immortal = False
                self.immortal_time = 0
        self.cooldown(frame_time)
        #if self.state <= 3:
        self.handle_state[self.state](self, frame_time)
        self.framesec += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = (int)(self.framesec) % 8
        if self.isground == False:
            self.down_spd -= self.GRAVITY_P * frame_time
            self.y += self.down_spd * frame_time


    def draw(self):
        if self.anime_time > 0:
            if self.anime_state == 0:
                self.image_skill_x.clip_draw(0, (self.frame*36), 33, 36, self.skill_x, self.skill_y)
            elif self.anime_state == 1:
                self.image_skill_c.clip_draw(0, (self.frame*36), 33, 36, self.skill_x, self.skill_y)

        if self.state in (self.LEFT_IDLE, self.LEFT_RUN, self.RIGHT_IDLE, self.RIGHT_RUN):
            self.image_char.clip_draw((self.frame*33), (self.state * 36), 33, 36, self.canvas_x, self.y)
        elif self.state in (self.L_Z_SKILL, self.L_C_SKILL, self.L_X_SKILL):
            self.image_char.clip_draw((self.frame*33), 180, 33, 36, self.canvas_x, self.y)
        elif self.state in (self.R_Z_SKILL, self.R_C_SKILL, self.R_X_SKILL):
            self.image_char.clip_draw((self.frame*33), 144, 33, 36, self.canvas_x, self.y)
        elif self.state in (self.L_V_SKILL, self.R_V_SKILL):
            self.image_char.clip_draw((self.frame * 33), 144+((self.state-10) * 36), 33, 36, self.canvas_x, self.y)
            self.image_skill_v.clip_draw(0, (self.frame * 36), 240, 36, self.canvas_x, self.y)


    def handle_events(self, frame_time, event):
        if((event.type == SDL_KEYDOWN) and (self.aniemelock)):
            if event.key == SDLK_LEFT:
                self.seeside = self.LEFTSIDE
                self.leftinput = True
            elif event.key == SDLK_RIGHT:
                self.seeside = 1
                self.rightinput = True
            elif event.key == SDLK_g:
                self.use_active_item()
        elif((event.type == SDL_KEYUP) and (self.aniemelock)):
            if event.key == SDLK_LEFT:
                self.leftinput = False
                if self.rightinput == True:
                    self.seeside = 1
            elif event.key == SDLK_RIGHT:
                self.rightinput = False
                if self.leftinput == True:
                    self.seeside = self.LEFTSIDE
        elif((event.type == SDL_KEYDOWN) and not(self.aniemelock)):
            if (event.key == SDLK_z):
                self.frame = 0
                if self.seeside == self.RIGHTSIDE:
                    self.state = self.R_Z_SKILL
                else:
                    self.state = self.L_Z_SKILL
            elif (event.key == SDLK_x):
                self.frame = 0
                if self.seeside == self.RIGHTSIDE:
                    self.state = self.R_X_SKILL
                else:
                    self.state = self.L_X_SKILL
            elif (event.key == SDLK_c):
                self.frame = 0
                if self.seeside == self.RIGHTSIDE:
                    self.state = self.R_C_SKILL
                else:
                    self.state = self.L_C_SKILL
            elif (event.key == SDLK_v):
                self.frame = 0
                if self.seeside == self.RIGHTSIDE:
                    self.state = self.R_V_SKILL
                else:
                    self.state = self.L_V_SKILL
            elif event.key == SDLK_SPACE:
                if self.isground:
                    self.handle_jump(frame_time)
            elif event.key == SDLK_LEFT:
                self.leftinput = True
                self.seeside = self.LEFTSIDE
                self.frame = 0
                self.state = self.LEFT_RUN
            elif event.key == SDLK_RIGHT:
                self.rightinput = True
                self.seeside = 1
                self.frame = 0
                self.state = self.RIGHT_RUN
            elif event.key == SDLK_DOWN:
                if self.y >= 300:
                    self.down()
            elif event.key == SDLK_g:
                self.use_active_item()
        elif ((event.type == SDL_KEYUP) and not(self.aniemelock)):
            if event.key == SDLK_LEFT:
                self.leftinput = False
                if self.seeside == self.LEFTSIDE:
                    if self.rightinput:
                        self.seeside = 1
                        self.state = self.RIGHT_RUN
                    else:
                        self.state = self.LEFT_IDLE
            elif event.key == SDLK_RIGHT:
                self.rightinput = False
                if self.seeside == self.RIGHTSIDE:
                    if self.leftinput:
                        self.seeside = self.LEFTSIDE
                        self.state = self.LEFT_RUN
                    else:
                        self.state = self.RIGHT_IDLE
