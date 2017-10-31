from pico2d import *

class body:
    def __init__(self):
        #idle = I, run = R, atk or use skill = A
        #see side left = -1, right = 1
        self.state = 'I'
        self.seeside = 1
        self.isground = True
        self.spd = 4


class character(body):
    def __init__(self):
        body.__init__(self)
        self.image_char = load_image('./src/char.png')
        self.image_idle = load_image('./src/char_idle.png')
        self.image_run = load_image('./src/char_run.png')
        #update later
        #self.image_jump = load_image('./res/char_idle.png')
        #self.image_skil1 = load_image('./res/char_idle.png')
        #self.image_skil2 = load_image('./res/char_idle.png')
        #self.image_skil3 = load_image('./res/char_idle.png')
        #self.image_skil4 = load_image('./res/char_idle.png')
        self.x, self.y = 210, 163
        self.jumpheight = 90
        self.spdy = self.jumpheight/15
        #gamefps / 4
        self.gravity = self.spdy / 15
        self.frame = 0
        self.framesec = 0
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
            self.framesec += 1
            if self.framesec >= 3:
                self.frame = (self.frame + 1) % 8
                self.framesec = 0
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
    def __init__(self, hp, pointXY):
        body.__init__(self)
        self.hp = hp
        self.x , self.y = pointXY
        self.nextatktime = 150
        self.atkdelay = 15 #frame
        self.time = 0

class monster_sub(monster_body):
    monster1_image = None

    def __init__(self, hp, pointXY):
        monster_body.__init__(self, hp, pointXY)
        self.type = 0
        if monster_sub.monster1_image == None:
            monster_sub.monster1_image = load_image('./src/mon_sub1.png')

    def draw(self):
        if self.type == 0:
            self.monster1_image.clip_draw(24+(24*self.seeside), 0, 48, 52, self.x, self.y)

    # state = i ready to atk, w wait to atktime
    def update(self, pointXY):
        if self.state == 'I':
            if ((math.fabs(pointXY[1] - self.y) <= 120) and (math.fabs(pointXY[0] - self.x) <= 500)):
                if (pointXY[0] - self.x) >= 0 :
                    self.seeside = 1
                else:
                    self.seeside = -1
                self.x += (self.seeside * self.spd)
                # atktime
                if (math.fabs(pointXY[0] - self.x) <= 20):
                    self.state = 'W'
        elif self.state == 'W':
            self.time += 1
            if self.time >= self.nextatktime:
                self.time = 0
                self.state = 'I'

    def move(self):
        pass

class monster_main(monster_body):
    def __init__(self, hp, pointXY):
        monster_body.__init__(self, hp, pointXY)
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
        self.image_bgi = load_image('./src/bgi_1.png')
        self.image_ground = load_image('./src/ground_1_G.png')
        self.image_groundbig = load_image('./src/ground_1_S1.png')
        self.image_groundsmall = load_image('./src/ground_1_S2.png')

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

class regenPoint():
    def __init__(self):
        self.regenpoint = [[(800,171), (1300,171), (600,369), (900,719), (1200,459)]]