import platform
import os

if platform.architecture()[0] == '32bit':
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x86"
else:
    os.environ["PYSDL2_DLL_PATH"] = "./SDL2/x64"

import StartScene
from pico2d import *
import game_framework

start_data_file = open('start_data.txt', 'r')
start_data = start_data_file.readlines()
start_data_file.close()

if start_data[2][13:] == 'True':
    open_canvas(1600,900,False,True)
    game_framework.run(StartScene)
    close_canvas()
elif start_data[2][13:] == 'False':
    open_canvas(1600,900,False,False)
    game_framework.run(StartScene)
    close_canvas()
