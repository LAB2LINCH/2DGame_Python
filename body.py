from pico2d import *

class body:
    PIXEL_PER_METER = (10.0 / 0.4)  # 10 pixel 40 cm
    RUN_SPEED_KMPH = 35  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    JUMP_HEIGHT = 8 #max Meter
    JUMP_HEIGHT_P = (JUMP_HEIGHT * PIXEL_PER_METER)
    JUMP_TIME = 0.8

    JUMP_START = ((JUMP_HEIGHT_P * 2) / (JUMP_TIME / 2))

    GRAVITY_P = (JUMP_START / (JUMP_TIME/ 2))

    def __init__(self):
        #see side left = -1, right = 1
        self.state = 0
        self.seeside = 1
        self.isground = True
        self.frame = 0
        self.down_spd = 10
        self.x, self.y = 0, 0
        self.imagesize_y = 0
