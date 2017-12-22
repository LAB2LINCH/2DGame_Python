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

    def stageChange(self, stage):
        self.stage = stage
        self.BOSS = False
        self.BOSS_Alive = True
        self.gen_count = 0
        self.regen_time = 0

        '''
        stage_data_file = open('./TXT/stage_data.txt', 'r')
        stage_data = json.load(stage_data_file)
        stage_data_file.close()

        regen_data_file = open('./TXT/regen_data.txt', 'r')
        regen_data = json.load(regen_data_file)
        regen_data_file.close()
        '''

        stage_data = [
            [(0, 1600, 450),
            (2, 800, 290),
            (2, 1200, 480),
            (2, 1880, 290),
            (2, 1770, 670),
            (3, 1470, 540),
            (3, 2080, 540),
            (3, 2180, 350),
            (4, 400, 450),
            (4, 2800, 450),
             (1, 1600, 75)],
            [(5, 1600, 450),
             (7, 800, 290),
             (7, 1200, 480),
             (7, 1880, 290),
             (7, 1770, 670),
             (8, 1470, 540),
             (8, 2080, 540),
             (8, 2180, 350),
             (9, 400, 450),
             (9, 2800, 450),
             (6, 1600, 75)],
            [(10, 1600, 450),
             (14, 400, 450),
             (14, 2800, 450),
             (11, 1600, 75)],
        ]

        regen_data = [
            {"NORMAL":[(1100, 530), (1350, 200), (1870, 720), (1920, 340), (2180, 200)],
             "BOSS":[(1350, 200), (2180, 200)]},
            {"NORMAL": [(1100, 530), (1350, 200), (1870, 720), (1920, 340), (2180, 200)],
             "BOSS": [(1350, 200), (2180, 200)] },
            {"NORMAL": [(1100, 530), (1350, 200), (1870, 720), (1920, 340), (2180, 200)],
             "BOSS": [(1350, 200), (2180, 200)]},
        ]

        self.env = stage_data[self.stage-1]
        self.regenpoint = regen_data[self.stage-1]['NORMAL']
        self.regenpoint_b = regen_data[self.stage-1]['BOSS']

        self.Monster = []
        self._BGI = None
        self._BLOCK = []
        self._USEABLE = []
        self._item = []
        self.font = load_font('./src/ENCR10B.TTF')

        for e in self.env:
            if e[0]%5 == self.BGI:
                self._BGI = environment.env(e[0], (e[1], e[2]))
            elif e[0]%5 == self.USEABLE:
                self._USEABLE.append(environment.env(e[0], (e[1], e[2])))
            else:
                self._BLOCK.append(environment.env(e[0], (e[1], e[2])))


    def __init__(self, stage, character):
        self.timer = 0
        self.stage = stage
        self.gametime = 0
        self.regen_time = 0
        self.stageChange(stage)
        self.center_object = character
        self.boss_hp_percentage = 1

        self.item_drop_list = [[
            (0, 50),
            (1, 50)
        ],[
            (2, 50),
            (3, 50)
        ]]
        self.passive_item = self.item_drop_list[self.PASSIVE]
        self.active_item = self.item_drop_list[self.ACTIVE]
        self.bgm = load_music('./src/bgm.mp3')
        self.bgm.set_volume(50)
        self.bgm.repeat_play()

        self.cooltime_check = self.center_object.skill_cooltime_check()

        self._UI = load_image('./src/bgi_ui.png')
        self._UI_skill_cooltime = load_image('./src/skill_cooltime.png')
        self._UI_boss_hp = load_image('./src/boss_hp.png')

        self.active_item_image = [load_image('./src/item_frizon.png'), load_image('./src/item_resetball.png')]
        self.active_item_id = self.center_object.get_active_item_id() - len(self.passive_item)

        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = 3200

    def draw(self):
        self._BGI.image.draw(self.canvas_width//2, self.canvas_height//2)
        for e in self._BLOCK:
            e.draw()
        for u in self._USEABLE:
            u.draw()
        for monster in self.Monster:
            monster.draw()

        self._UI.draw(800, 450)
        if self.active_item_id >= 0:
            self.active_item_image[self.active_item_id].draw(929, 192)
        self.font.draw(1520, 846, "%d:%d:%d" % (self.timer/3600, (self.timer/60)%60, self.timer%60), (255,255,255))

        for i in range(5):
            if self.cooltime_check[i] >= 0:
                self._UI_skill_cooltime.draw(673+(64*i), 192)

        if self.BOSS and self.BOSS_Alive:
            self._UI_boss_hp.clip_draw_to_origin(0, 0, (int)(self._UI_boss_hp.w * self.boss_hp_percentage), self._UI_boss_hp.h, 5, 873,
                                                 (int)(self._UI_boss_hp.w * self.boss_hp_percentage), self._UI_boss_hp.h)
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

    def stage_check(self):
        if len(self.Monster)+len(self._item) <= 0 and not self.BOSS_Alive:
            return True
        return False

    def drop_item(self, level, pointXY):
        value = randrange(1,100)
        if level == 0:
            if randrange(1,20) <= 1:
                i=0
                while value >= self.passive_item[i][1]:
                    i+=1
                    value -= self.passive_item[i][1]
                self._item.append(item.item(i, pointXY))
        elif level == 1:
            if randrange(1,10) <= 5:
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
                self._item.append(item.item(i+len(self.passive_item), pointXY))#패시브아이템 개수 -1

    def drop_item_test(self, type):
        self._item.append(item.item(type, (1000, 350)))

    def monster_gen(self):
        self.Monster.append(monster_sub.monster_sub(self.stage * 30 - 10, self.regenpoint[randint(0, 4)], self.stage - 1))

    def update(self, frame_time, pointXY):
        self.window_left = clamp(0, int(self.center_object.x) - self.canvas_width//2, self.w - self.canvas_width)
        self.timer += frame_time

        for e in self._BLOCK:
            e.update(pointXY[0])
        for u in self._USEABLE:
            u.update(pointXY[0])

        self.cooltime_check = self.center_object.skill_cooltime_check()
        self.active_item_id = self.center_object.get_active_item_id() - len(self.passive_item)

        if self.BOSS and self.BOSS_Alive:
            self.boss_hp_percentage = self.BOSS_Monster.hp_percentage()

        self.Playtime += frame_time
        for monster in self.Monster:
            monster.update(frame_time, pointXY)
        self.gametime += frame_time
        self.regen_time += frame_time
        if self.stage < 3:
            if self.regen_time >= self._Regen_time and self.BOSS_Alive:
                self.Monster.append(monster_sub.monster_sub(self.stage * 30 - 10, self.regenpoint[randint(0, 4)], self.stage-1))
                self.regen_time = 0
                self.gen_count += 1
            if self.gen_count >= 1  and not self.BOSS:
                self.BOSS_Monster = monster_main.monster_main(self.stage * 300 - 100, self.regenpoint_b[1],
                                                              self.stage - 1)
                self.Monster.append(self.BOSS_Monster)
                self.BOSS = True
        elif self.stage == 3:
            if not self.BOSS and self.BOSS_Alive:
                self.BOSS_Monster = monster_main.monster_main(self.stage * 300 - 100, self.regenpoint_b[1],
                                                                self.stage - 1)
                self.Monster.append(self.BOSS_Monster)
                self.BOSS = True
        for item in self._item:
            item.update(frame_time, pointXY)

