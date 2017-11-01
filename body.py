from pico2d import *

class body:
    def __init__(self):
        #idle = I, run = R, atk or use skill = A
        #see side left = -1, right = 1
        self.state = 'I'
        self.seeside = 1
        self.isground = True
        self.spd = 4

