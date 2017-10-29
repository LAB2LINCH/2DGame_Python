from pico2d import *

class body:
    def __init__(self):
        #idle = I, run = R, atk or use skill = A
        #see side left = -1, right = 1
        self.state = 'I'
        self.seeside = 1
        self.isground = True
        self.spd = 10


class character(body):
    def __init__(self):
        body.__init__(self)
        self.image_char = load_image('./res/char.png')
        self.image_idle = load_image('./res/char_idle.png')
        self.image_run = load_image('./res/char_run.png')
        #update later
        #self.image_jump = load_image('./res/char_idle.png')
        #self.image_skil1 = load_image('./res/char_idle.png')
        #self.image_skil2 = load_image('./res/char_idle.png')
        #self.image_skil3 = load_image('./res/char_idle.png')
        #self.image_skil4 = load_image('./res/char_idle.png')
        self.x, self.y = 210, 163
        self.jumpheight = 90
        self.spdy = self.jumpheight/15
        self.gravity = self.spdy / 15
        self.frame = 0
        self.skill = None
        self.c_skill_z = 0
        self.c_skill_c = 0
        self.c_skill_v = 0

    def update(self):
        if self.c_skill_z > 0:
            self.c_skill_z -= 1/60
        if self.c_skill_c > 0:
            self.c_skill_c -= 1/60
        if self.c_skill_v > 0:
            self.c_skill_v -= 1/60
        if self.isground == False:
            self.y += self.spdy
            self.spdy -= self.gravity
            if self.y < 163:
                self.y = 163
                self.spdy = self.jumpheight/15
                self.isground = True
        if self.state == 'R':
            self.frame = (self.frame + 1) % 8
            self.x += (self.spd * self.seeside)
        elif self.state == 'A':
            self.frame = (self.frame + 1) % 4
            pass

    def draw(self) :
        if self.state == 'A':
            self.image_idle.draw(self.x, self.y)
        elif self.state == 'I':
            if(self.seeside == -1):
                self.image_char.clip_draw(0,72,33,36,self.x,self.y)
            elif(self.seeside == 1):
                self.image_char.clip_draw(33,72,33,36,self.x,self.y)
            #self.image_idle.draw(self.x, self.y)
        elif self.state == 'R':
            if(self.seeside == 1):
                self.image_char.clip_draw((self.frame*33), 0, 33, 36, self.x, self.y)
            elif(self.seeside == -1):
                self.image_char.clip_draw((self.frame*33), 36, 33, 36, self.x, self.y)
            #self.image_run.clip_draw((self.frame*33),0,33,36,self.x,self.y)

    def skill_z(self): #move
        if self.c_skill_z <= 0:
            self.skill = 'Z'
            self.x += self.spd * 30 * self.seeside
            self.c_skill_z = 1.5

    def skill_x(self): #atk
        self.skill = 'X'
        self.x += self.spd * 30 * self.seeside

    def skill_c(self):  #6hit
        if self.c_skill_c <= 0:
            self.skill = 'C'
            self.x += self.spd * 30 * self.seeside
            self.c_skill_c = 3

    def skill_v(self):  #area 3hit
        if self.c_skill_v <= 0:
            self.skill = 'V'
            self.x += self.spd * 30 * self.seeside
            self.c_skill_v = 5

class monster_body(body):
    def __init__(self, root, hp, pointXY):
        body.__init__(self)
        self.image = load_image(root)
        self.hp = hp
        self.x , self.y = pointXY

    def draw(self):
        if self.seeside == -1:
            self.image.clip_draw(0, 0, 48, 52, self.x, self.y)
        elif self.seeside == 1:
            self.image.clip_draw(48, 0, 48, 52, self.x, self.y)

class monster_sub(monster_body):
    def __init__(self, root, hp, pointXY):
        monster_body.__init__(self, root, hp, pointXY)

class monster_main(monster_body):
    def __init__(self, root, hp, pointXY):
        monster_body.__init__(self, root, hp, pointXY)
        self.skill_state = 0

    def draw(self):
        if self.state == 'I':
            monster_body.draw(self)

    def update(self):
        pass

    def patern1(self):
        self.skill_state = 1

class map():
    def __init__(self):
        self.image_bgi = load_image('./res/bgi_1.png')
        self.image_ground = load_image('./res/ground_1_G.png')
        self.image_groundbig = load_image('./res/ground_1_S1.png')
        self.image_groundsmall = load_image('./res/ground_1_S2.png')

    def draw(self):
        self.image_bgi.draw(800,450)
        self.image_ground.draw(800,75)
        self.image_groundbig.draw(400,300)
        self.image_groundsmall.draw(140,340)
        self.image_groundsmall.draw(680,340)
        self.image_groundbig.draw(1050,390)
        self.image_groundsmall.draw(1330,430)
        self.image_groundsmall.draw(900,525)
        self.image_groundbig.draw(670,650)

class actionPoint():
    pass