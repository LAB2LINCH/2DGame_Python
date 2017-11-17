from pico2d import *

class body:
    PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 40 cm
    DOWN_GRAVITY = 30
    DOWN_SPD = (DOWN_GRAVITY * PIXEL_PER_METER)

    def __init__(self):
        #see side left = -1, right = 1
        self.state = 0
        self.seeside = 1
        self.isground = True
        self.frame = 0
        self.down_spd = 10

    def update(self, frame_time):
        if self.isground == False:
            self.down_spd += (int)(self.DOWN_SPD * frame_time)
            self.y -= (int)(self.down_spd * frame_time)

    def onground(self):
        self.isground = True
        self.down_spd = 0