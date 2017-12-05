from pico2d import *
from random import *
import environment
import monster_main
import monster_sub
import item

class stage_controller():
    BGI, GROUND, LONG, SHORT, USEABLE = 0, 1, 2, 3, 4
    PASSIVE, ACTIVE = 0, 1

    _BGI = None
    _BLOCK = []
    _USEABLE = []
    Monster = []
    item_drop_list = []
    _item = []

    _Regen_time = 3
    Playtime = 0


    def stopbgm(self):
        self.bgm.play()

    def stageChange(self, stage):
        self.stage = stage
        self.BOSS = False
        self.BOSS_Alive = True
        self.gen_count = 0

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
            (3, 900, 550),
            (2, 670, 675)],
            [(0, 800, 450),
             (1, 800, 75),
             (2, 400, 300),
             (3, 140, 340),
             (3, 680, 340),
             (2, 1050, 390),
             (3, 1330, 430),
             (3, 900, 550),
             (2, 670, 675)],
            [(0, 800, 450),
             (1, 800, 75),
             (2, 400, 300),
             (3, 140, 340),
             (3, 680, 340),
             (2, 1050, 390),
             (3, 1330, 430),
             (3, 900, 550),
             (2, 670, 675)],
        ]

        regen_data = [
            {"NORMAL":[(800,171), (1300,171), (600,369), (900,719), (1200,459)],
             "BOSS":[(800, 284), (1300, 284)]},
            {"NORMAL": [(800, 171), (1300, 171), (600, 369), (900, 719), (1200, 459)],
             "BOSS": [(800, 284), (1300, 284)]},
            {"NORMAL": [(800, 171), (1300, 171), (600, 369), (900, 719), (1200, 459)],
             "BOSS": [(800, 284), (1300, 284)]}
        ]

        self.env = stage_data[self.stage-1]
        self.regenpoint = regen_data[self.stage-1]['NORMAL']
        self.regenpoint_b = regen_data[self.stage-1]['BOSS']

        self._BGI = None
        self._BLOCK = []
        self._USEABLE = []

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

        self.item_drop_list = [[
            (0, 50),
            (1, 50)
        ],[
            (2, 50),
            (3, 50)
        ]]
        self.passive_item = self.item_drop_list[self.PASSIVE]
        self.active_item = self.item_drop_list[self.ACTIVE]
        self.bgm = load_wav('./src/bgm.wav')
        self.bgm.repeat_play()

    def draw(self):
        self._BGI.image.draw(self._BGI.x, self._BGI.y)
        for e in self._BLOCK:
            e.image.draw(e.x, e.y)
        for u in self._USEABLE:
            u.image.draw(u.x, u.y)
        for monster in self.Monster:
            monster.draw()

        '''
        for e in self._BLOCK:
            e.draw_hitbox()
        for u in self._USEABLE:
            u.draw_hitbox()
        for monster in self.Monster:
            monster.draw_hitbox()
        '''

        for item in self._item:
            item.draw()

    def drop_item(self, level, pointXY):
        value = randrange(1,100)
        if level == 0:
            if True: # randrange(1,20) <= 1
                i=0
                while value >= self.passive_item[i][1]:
                    i+=1
                    value -= self.passive_item[i][1]
                self._item.append(item.item(i, pointXY))
        elif level == 1:
            if randrange(1,10) <= 9:
                i=0
                while value >= self.passive_item[i][1]:
                    i+=1
                    value -= self.passive_item[i][1]
                self._item.append(item.item(i, pointXY))
            else:
                i=0
                while value >= self.active_item[i][1]:
                    i+=1
                    value -= self.active_item[i][1]
                self._item.append(item.item(i+self.passive_item.len-1, pointXY))#패시브아이템 개수 -1


    def update(self, frame_time, pointXY):
        self.Playtime += frame_time
        for monster in self.Monster:
            monster.update(frame_time, pointXY)
        self.gametime += frame_time
        self.regen_time += frame_time
        if self.regen_time >= self._Regen_time and self.BOSS_Alive:
            self.Monster.append(monster_sub.monster_sub(20, self.regenpoint[randint(0, 4)], self.stage-1))
            self.regen_time = 0
            self.gen_count += 1
        if self.gen_count >= 1  and not self.BOSS:
            self.Monster.append(monster_main.monster_main(200, self.regenpoint_b[1], self.stage-1))
            self.BOSS = True

        for item in self._item:
            item.update(frame_time)

