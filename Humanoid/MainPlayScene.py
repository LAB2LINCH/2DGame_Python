from pico2d import *
import game_framework
import body

name = "MainPlayScene"
Character = None
Map = None
Monster = None
regenpoint = None

def enter():
    global Character, Map
    Character = body.character()
    Map = body.map()


def exit():
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT:
                Character.seeside = -1
                Character.state = 'R'
            elif event.key == SDLK_RIGHT:
                Character.seeside = 1
                Character.state = 'R'
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT or event.key == SDLK_RIGHT:
                Character.state = 'I'



def update():
    global Character
    Character.update()
    pass


def draw():
    global Character, Map
    clear_canvas()
    Map.draw()
    Character.draw()
    update_canvas()
