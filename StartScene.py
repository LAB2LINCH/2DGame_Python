import game_framework
import MainPlayScene
from pico2d import *

name = "StartScene"

UP, DOWN, SPACE = 0, 1, 2
select = 0
bgi = None
select_arrow = None

def enter():
    global select, bgi, select_arrow
    select = 0
    bgi = load_image('./src/bgi_main_menu.png')
    select_arrow = load_image('./src/menu_select_arrow.png')

def exit():
    pass

def pause():
    pass

def resume():
    pass

def menu(input_key):#MENU 0 == start, 1 == exit
    global select
    if input_key == UP:
        select -= 1
        if select <= -1:
            select = 1
    elif input_key == DOWN:
        select = (select + 1) % 2
    elif input_key == SPACE:
        if select == 0:
            game_framework.change_state(MainPlayScene)
        else:
            game_framework.quit()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            menu(UP)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            menu(DOWN)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            menu(SPACE)

def update(frame_time):
    pass

def draw(frame_time):
    clear_canvas()
    bgi.draw(800, 450)
    select_arrow.draw(672, 450-(select*78))
    update_canvas()