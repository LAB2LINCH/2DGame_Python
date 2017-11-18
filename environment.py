from pico2d import *

class env():
    image = None

    UP, LEFT, RIGHT, DOWN, FALSE = 1, 2, 3, 4, 0

    def __init__(self, type, pointXY):
        global image
        self.x = pointXY[0]
        self.y = pointXY[1]
        self.collisionflag = self.FALSE

        '''
        env_data_file = open('./TXT/env_data.txt', 'r')
        env_data = json.load(env_data_file)
        env_data_file.close()
        '''
        env_data = [
            './src/bgi_1.png',
            './src/ground_1_G.png',
            './src/ground_1_S1.png',
            './src/ground_1_S2.png',
            './src/ground_1_1.png'
        ]

        self.image = load_image(env_data[type])
        #type 0=bg, 1=ground, 2=long, 3=short, 4=usealbe // stage*5 +

        self.w = self.image.w
        self.h = self.image.h

    def hitbox(self):
        return ((self.x - (self.w//2)), (self.y - (self.h//2)), (self.x + (self.w//2)), (self.y + (self.h//2)))

    def return_ground_y(self):
        return (self.y + (self.h//2))

    def draw_hitbox(self):
        draw_rectangle(*self.hitbox())

    def draw(self):
        self.image.draw(self.x, self.y)
