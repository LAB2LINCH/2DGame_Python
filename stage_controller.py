from pico2d import *
from random import *
import environment
import monster_main
import monster_sub

class stage_controller():
    BGI, GROUND, LONG, SHORT, USEABLE = 0, 1, 2, 3, 4

    _BGI = None
    _BLOCK = []
    _USEABLE = []
    Monster = None

    _Regen_time = 8

    def stageChange(self, stage):
        self.stage = stage

        '''
        stage_data_file = open('./TXT/stage_data.txt', 'r')
        stage_data = json.load(stage_data_file)
        stage_data_file.close()

        regen_data_file = open('./TXT/regen_data.txt', 'r')
        regen_data = json.load(regen_data_file)
        regen_data_file.close()
        '''

        stage_data = [
            [(0, 800, 450),
            (1, 800, 75),
            (2, 400, 300),
            (3, 140, 340),
            (3, 680, 340),
            (2, 1050, 390),
            (3, 1330, 430),
            (3, 900, 525),
            (2, 670, 650)]]

        regen_data = [
            {"NORMAL":[(800,171), (1300,171), (600,369), (900,719), (1200,459)],
             "BOSS":[(800, 284), (1300, 284)]}
        ]

        self.env = stage_data[self.stage-1]
        self.regenpoint = regen_data[self.stage-1]['NORMAL']
        self.regenpoint_b = regen_data[self.stage-1]['BOSS']

        for e in self.env:
            if e[0] == self.BGI:
                self._BGI = environment.env(e[0], (e[1], e[2]))
            elif e[0] == self.USEABLE:
                self._USEABLE.append(environment.env(e[0], (e[1], e[2])))
            else:
                self._BLOCK.append(environment.env(e[0], (e[1], e[2])))


    def __init__(self, stage):
        self.stage = stage
        self.gametime = 0
        self.regen_time = 0

        self.stageChange(stage)

        self.Monster = [monster_sub.monster_sub(20, self.regenpoint[randint(0, 4)])]
        self.Monster.append(monster_main.monster_main(200, self.regenpoint_b[1]))

    def draw(self):
        self._BGI.image.draw(self._BGI.x, self._BGI.y)
        for e in self._BLOCK:
            e.image.draw(e.x, e.y)
        for u in self._USEABLE:
            u.image.draw(u.x, u.y)
        for monster in self.Monster:
            monster.draw()

        for e in self._BLOCK:
            e.draw_hitbox()
        for u in self._USEABLE:
            u.draw_hitbox()
        for monster in self.Monster:
            monster.draw_hitbox()



    def update(self, frame_time, pointXY):
        for monster in self.Monster:
            monster.update(frame_time, pointXY)
        self.gametime += frame_time
        self.regen_time += frame_time
        if self.regen_time >= self._Regen_time:
            self.Monster.append(monster_sub.monster_sub(20, self.regenpoint[randint(0, 4)]))
            self.regen_time = 0

