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
        self.image_idle = load_image('./res/char_idle.png')
        self.image_run = load_image('./res/char_run.png')
        #update later
        #self.image_jump = load_image('./res/char_idle.png')
        #self.image_skil1 = load_image('./res/char_idle.png')
        #self.image_skil2 = load_image('./res/char_idle.png')
        #self.image_skil3 = load_image('./res/char_idle.png')
        #self.image_skil4 = load_image('./res/char_idle.png')
        self.x, self.y = 210, 163
        self.jumpheight = 40
        self.gravity = 2
        self.spdy = 20
        self.frame = 0

    def update(self):
        if self.isground == False:
            self.y += self.spdy
            self.spdy -= self.gravity
        if self.state == 'R':
            self.frame = (self.frame + 1) % 8
            self.x += (self.spd * self.seeside)
        elif self.state == 'A':
            pass

    def draw(self) :
        if self.isground == False:
            self.image_idle.draw(self.x, self.y)
        elif self.state == 'I':
            self.image_idle.draw(self.x, self.y)
        elif self.state == 'R':
            self.image_run.clip_draw
            self.image_run.clip_draw((self.frame*33),0,33,36,self.x,self.y)
        elif self.state == 'A':
            self.image_idle.draw(self.x, self.y)

class monster(body):
    pass

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