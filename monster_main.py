from pico2d import *
import monster_body

class monster_main(monster_body.monster_body):
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