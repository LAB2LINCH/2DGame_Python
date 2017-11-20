import game_framework
import MainPlayScene

name = "MenuScene"

UP, DOWN = 0, 1
select = 0

def enter():
    global select
    select = 0
    pass

def exit():
    pass

def pause():
    pass

def resume():
    pass

def menu(ud):#MENU 0 == continue, 1 == intro, 2 == EXIT
    global select
    if ud == UP:
        select -= 1
        if select <= -1:
            select = 2
    elif ud == DOWN:
        select = (select + 1) % 3


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.pop_state()
        elif (event.type, event.key) == (SDL_KEWDOWN, SDLK_UP):
            menu(UP)
        elif (event.type, event.key) == (SDL_KEWDOWN, SDLK_DOWN):
            menu(DOWN)

def update(frame_time):

    pass

def draw(frame_time):
    MainPlayScene.draw(frame_time)
    #image 4
    #arrow 1 -> move to select
    pass