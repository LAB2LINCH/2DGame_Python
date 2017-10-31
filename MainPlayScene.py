from pico2d import *
from random import *
import game_framework
import body


name = "MainPlayScene"
Character = None
Map = None
Monster = None
Regenpoint = None
Monster = None
Stage = 1
gametime = 0
regentime = 10
running = False
Rp = None

def enter():
    global Character, Map, Stage, Regenpoint, Monster, running
    Character = body.character()
    Map = body.map()
    Rp =  body.regenPoint()
    Stage = 1

    Regenpoint = Rp.regenpoint[Stage-1]
    Monster = [body.monster_sub(20, Regenpoint[randint(0,4)])]
    #test
    #Monster = [body.monster_sub(20, Regenpoint[randint(0,4)]) for i in range(200)]
    running = True

def exit():
    pass

def pause():
    running = False

def resume():
    running = True

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_z:
                Character.skill_z()
            elif event.key == SDLK_x:
                Character.skill_x()
            elif event.key == SDLK_c:
                Character.skill_c()
            elif event.key == SDLK_v:
                Character.skill_v()
            elif event.key == SDLK_LEFT:
                Character.seeside = -1
                Character.frame = 0
                Character.state = 'R'
            elif event.key == SDLK_RIGHT:
                Character.seeside = 1
                Character.frame = 0
                Character.state = 'R'
            elif event.key == SDLK_SPACE:
                Character.isground = False
        elif event.type == SDL_KEYUP:
            if ((event.key == SDLK_LEFT) and (Character.seeside == -1)):
                Character.frame = 0
                Character.state = 'I'
            if ((event.key == SDLK_RIGHT) and (Character.seeside == 1)):
                Character.frame = 0
                Character.state = 'I'



def update():
    global Character, Monster, running, gametime, regentime
    Character.update()
    for monster in Monster:
        monster.update((Character.x, Character.y))
    if running == True:
        gametime += 1/60
        if gametime >= regentime:
            Monster.append(body.monster_sub(20, Regenpoint[randint(0,4)]))
            gametime = 0


def draw():
    global Character, Map, Regenpoint, Monster
    clear_canvas()
    Map.draw()
    Character.draw()
    for mon in Monster:
        mon.draw()
    update_canvas()