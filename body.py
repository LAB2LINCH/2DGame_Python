from pico2d import *

class body:
    def __init__(self):
        #see side left = -1, right = 1
        self.state = 0
        self.seeside = 1
        self.isground = True
        self.spd = 4
        self.frame = 0

