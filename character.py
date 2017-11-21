from pico2d import *
import body
import item

class character(body.body):

    RIGHT_RUN, LEFT_RUN, RIGHT_IDLE, LEFT_IDLE = 0, 1, 2, 3
    R_Z_SKILL, L_Z_SKILL, R_X_SKILL, L_X_SKILL, R_C_SKILL, L_C_SKILL, R_V_SKILL, L_V_SKILL = 4, 5, 6, 7, 8, 9, 10, 11

    LEFTSIDE, RIGHTSIDE = -1, 1

    LEFT, RIGHT = 0, 1

    PASSIVE, ACTIVE = 0, 1

    def handle_run(self, frame_time):
        if self.seeside == -1:
            if not self.canmove[self.LEFT]:
                return
        if self.seeside == 1:
            if not self.canmove[self.RIGHT]:
                return
        self.x += (self.RUN_SPEED_PPS * self.seeside * frame_time)

    def handle_idle(self, frame_time):
        pass

    def handle_jump(self, frame_time):

        self.down_spd = self.JUMP_START
        self.isground = False
        self.y += 3

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
            self.x += self.RUN_SPEED_PPS * self.seeside * 0.5
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
        else:
            self.change_state()

    def handle_c_skill(self, frame_time): # 6hit
        if self.aniemelock:
            self.skillsec += frame_time
            if self.skillsec >= self.t_skill_c:
                self.skillsec = 0
                self.aniemelock = False
                self.change_state()
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
        else:
            self.change_state()

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

    def hitbox(self, type): #idle, atk, skillc, skillv
        if type == 0: return (self.x - 16, self.y - 18, self.x + 16, self. y + 18)
        elif type == 1:
            if self.seeside == -1:
               return (self.x  -32, self.y - 18, self.x -16, self.y + 18)
            else:
               return (self.x + 16, self.y - 18, self.x + 32, self.y + 18)
        elif type == 2: return (self.x - 50, self.y - 54, self.x + 50, self.y + 54)
        elif type == 3: return (self.x - 240, self.y - 20, self.x + 240, self.y + 20)

    def draw_hitbox(self):
        draw_rectangle(*self.hitbox(0))
        draw_rectangle(*self.hitbox(1))
        draw_rectangle(*self.hitbox(2))
        draw_rectangle(*self.hitbox(3))

    def damage(self):
        return self._damage



    def __init__(self, itemvalue):
        body.body.__init__(self)
        self.image_char = load_image('./src/char.png')
        self.x, self.y = 210, 800
        self.framesec = 0
        self.skillsec = 0
        self.c_skill_z = 0
        self.c_skill_x = 0
        self.c_skill_c = 0
        self.c_skill_v = 0
        self.t_skill_z = 0.25
        self.t_skill_x = 1/15
        self.t_skill_c = 0.25
        self.t_skill_v = 2
        self._damage = 10
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
        for i in range(itemvalue): # PASSIVE 아이템
            self.itemlist.append([i, 0])

    def getitem(self, item):
        if item.type == 0:
            self.itemlist[item.id][1] = self.itemlist[item.id][1] + 1
            if item.part == item.ATKPOWER:
                self._damage += item.value
            elif item.part == item.CRIT:
                self.critchance += item.value
        else:
            self.itemlist[self.itemvalue][0] = item.id



    def cooldown(self, frame_time):
        self.c_skill_z += frame_time
        self.c_skill_x += frame_time
        self.c_skill_c += frame_time
        self.c_skill_v += frame_time

    def update(self, frame_time):
        self.cooldown(frame_time)
        #if self.state <= 3:
        self.handle_state[self.state](self, frame_time)
        self.framesec += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * frame_time
        self.frame = (int)(self.framesec) % 8
        if self.isground == False:
            self.down_spd -= self.GRAVITY_P * frame_time
            self.y += self.down_spd * frame_time

    def draw(self):
        if self.state in (self.L_Z_SKILL, self.L_C_SKILL, self.L_X_SKILL, self.L_V_SKILL):
            self.image_char.clip_draw((self.frame*33), 108, 33, 36, self.x, self.y)
        elif self.state in (self.R_Z_SKILL, self.R_C_SKILL, self.R_X_SKILL, self.R_V_SKILL):
            self.image_char.clip_draw((self.frame*33), 72, 33, 36, self.x, self.y)
        else:
            self.image_char.clip_draw((self.frame*33), (self.state * 36), 33, 36, self.x, self.y)

    def handle_events(self, frame_time, event):
        if((event.type == SDL_KEYDOWN) and (self.aniemelock)):
            if event.key == SDLK_LEFT:
                self.seeside = self.LEFTSIDE
                self.leftinput = True
            elif event.key == SDLK_RIGHT:
                self.seeside = 1
                self.rightinput = True
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
                if self.x >= 300:
                    self.down()
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
