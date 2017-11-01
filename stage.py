from pico2d import *

class ground():
    image_bgi = None
    image_ground = None
    image_ground2 = None
    image_ground3 = None

    def __init__(self):
        global image_bgi, image_ground, image_ground2, image_ground3
        self.image_bgi = load_image('./src/bgi_1.png')
        self.image_ground = load_image('./src/ground_1_G.png')
        self.image_ground2 = load_image('./src/ground_1_S1.png')
        self.image_ground3 = load_image('./src/ground_1_S2.png')

    def draw(self):
        self.image_bgi.draw(800,450)
        self.image_ground.draw(800,75)
        self.image_ground2.draw(400,300)
        self.image_ground3.draw(140,340)
        self.image_ground3.draw(680,340)
        self.image_ground2.draw(1050,390)
        self.image_ground3.draw(1330,430)
        self.image_ground3.draw(900,525)
        self.image_ground2.draw(670,650)