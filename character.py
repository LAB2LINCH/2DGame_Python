from pico2d import *
import body

class character(body.body):

    RIGHT_RUN, LEFT_RUN, RIGHT_IDLE, LEFT_IDLE = 0, 1, 2, 3
    R_Z_SKILL, L_Z_SKILL, R_X_SKILL, L_X_SKILL, R_C_SKILL, L_C_SKILL, R_V_SKILL, L_V_SKILL = 4, 5, 6, 7, 8, 9, 10, 11


    def handle_run(self):
        self.x += (self.spd * self.seeside)

    def handle_idle(self):
        pass

    def handle_z_skill(self): # move
        if self.c_skill_z >= 1.5:
            #self.aniemelock = True
            self.x += self.spd * 30 * self.seeside
            self.c_skill_z = 0
        elif self.frame == 7:
            pass#self.animelock = False

    def handle_x_skill(self): # atk
        if self.c_skill_x >= 0:
            self.x += self.spd * 30 * self.seeside
            self.c_skill_x = 0
        elif self.frame == 7:
            pass#self.animelock = False

    def handle_c_skill(self): # 6hit
        if self.c_skill_c >= 3:
            self.x += self.spd * 30 * self.seeside
            self.c_skill_c = 0
        elif self.frame == 7:
            pass#self.animelock = False

    def handle_v_skill(self): # area
        if self.c_skill_v >= 5:
            self.x += self.spd * 30 * self.seeside
            self.c_skill_v = 0
        elif self.frame == 7:
            pass#self.animelock = False

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

    def __init__(self):
        global C_SKILL_Z, C_SKILL_X, C_SKILL_C, C_SKILL_V
        body.body.__init__(self)
        self.image_char = load_image('./src/char.png')
        self.x, self.y = 210, 163
        self.jumpheight = 90
        self.spdy = self.jumpheight / 15
        self.gravity = self.spdy / 15
        self.frame = 0
        self.framesec = 0
        self.c_skill_z = 0
        self.c_skill_x = 0
        self.c_skill_c = 0
        self.c_skill_v = 0
        self.state = 2
        self.keydown = 0
        self.aniemelock = False
        self.fps = 60

    def cooldown(self):
        self.c_skill_z += 1 / self.fps
        self.c_skill_c += 1 / self.fps
        self.c_skill_v += 1 / self.fps

    def gravitydrop(self):
        if self.isground == False:
            self.y += self.spdy
            self.spdy -= self.gravity
            if self.y < 163:
                self.y = 163
                self.spdy = self.jumpheight/15
                self.isground = True

    def update(self):
        self.cooldown()
        self.gravitydrop()
        if self.state <= 3:
            self.handle_state[self.state](self)
        self.framesec += 1
        if self.framesec >= 3:
            self.frame = (self.frame + 1) % 8
            self.framesec = 0

    def draw(self) :
        self.image_char.clip_draw((self.frame*33), (self.state * 36), 33, 36, self.x, self.y)

    def handle_events(self, event):
        if event.type == SDL_KEYDOWN:
            if (event.key == SDLK_z):
                self.frame = 0
                if self.seeside == 1:
                    self.handle_state[5](self)
                else:
                    self.handle_state[4](self)
            elif (event.key == SDLK_x):
                self.frame = 0
                if self.seeside == 1:
                    self.handle_state[7](self)
                else:
                    self.handle_state[6](self)
            elif (event.key == SDLK_c):
                self.frame = 0
                if self.seeside == 1:
                    self.handle_state[9](self)
                else:
                    self.handle_state[8](self)
            elif (event.key == SDLK_v):
                self.frame = 0
                if self.seeside == 1:
                    self.handle_state[11](self)
                else:
                    self.handle_state[10](self)
            elif event.key == SDLK_LEFT:
                #self.keydown += 1
                self.seeside = -1
                self.frame = 0
                self.state = 1
            elif event.key == SDLK_RIGHT:
                #self.keydown += 1
                self.seeside = 1
                self.frame = 0
                self.state = 0
            elif event.key == SDLK_SPACE:
                self.isground = False
        elif event.type == SDL_KEYUP:
            if ((event.key == SDLK_LEFT) and (self.seeside == -1)):
                #self.keydown -= 1
                #if (self.keydown <= 0):
                    self.state = 2
            if ((event.key == SDLK_RIGHT) and (self.seeside == 1)):
                #self.keydown -= 1
                #if (self.keydown <= 0):
                    self.state = 3