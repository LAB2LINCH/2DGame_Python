import game_framework
import MainPlayScene
from pico2d import *

name = "MenuScene"

UP, DOWN, SPACE = 0, 1, 2
select = 0
bgi = None
select_arrow = None
delta_time = 0
sound = None

def enter():
    global select, bgi, select_arrow, sound
    select = 0
    bgi = load_image('./src/bgi_menu.png')
    select_arrow = load_image('./src/menu_select_arrow.png')
    sound = load_wav('./src/button_click.wav')
    sound.set_volume(50)

def exit():
    pass

def pause():
    pass

def resume():
    pass

def menu(input_key):#MENU 0 == continue, 1 == intro, 2 == EXIT
    global select
    if input_key == UP:
        select -= 1
        if select <= -1:
            select = 1
    elif input_key == DOWN:
        select = (select + 1) % 2
    elif input_key == SPACE:
        if select == 0:
            game_framework.pop_state()
        else:
            game_framework.quit()


def handle_events(frame_time):
    global sound
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_state()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            sound.play()
            menu(UP)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            sound.play()
            menu(DOWN)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            sound.play()
            menu(SPACE)

def update(frame_time):
    global delta_time
    delta_time += frame_time
    if delta_time >= 0.5:
        delta_time = 0

def draw(frame_time):
        clear_canvas()
        bgi.draw(800, 450)
        select_arrow.draw(672, 450-(select*78))
        update_canvas()