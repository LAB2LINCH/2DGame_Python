from pico2d import *
from random import *
import game_framework
import character
import monster_main
import monster_sub
import stage_controller
import stage


name = "MainPlayScene"
Character = None
Map = None
Monster = None
Regenpoint = None
Regenpoint_b = None
Monster = None
Stage = 1
gametime = 0
regentime = 10
Rp = None

def enter():
    global Character, Map, Stage, Regenpoint, Monster, running, Regenpoint_b
    Character = character.character()
    Map = stage.ground()
    Rp =  stage_controller.stage_controller()
    Stage = 1

    Regenpoint = Rp.regenpoint[Stage-1]
    Regenpoint_b = Rp.regenpoint_b[Stage-1]
    Monster = [monster_sub.monster_sub(20, Regenpoint[randint(0,4)])]
    Monster = [monster_main.monster_main(200, Regenpoint_b[1])]
    #test
    #Monster = [body.monster_sub(20, Regenpoint[randint(0,4)]) for i in range(200)]
    running = True

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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            Character.handle_events(event)



def update():
    global Character, Monster, running, gametime, regentime
    Character.update()
    for monster in Monster:
        monster.update((Character.x, Character.y))
    if running == True:
        gametime += 1/60
        if gametime >= regentime:
            Monster.append(monster_sub.monster_sub(20, Regenpoint[randint(0,4)]))
            gametime = 0


def draw():
    global Character, Map, Regenpoint, Monster
    clear_canvas()
    Map.draw()
    Character.draw()
    for mon in Monster:
        mon.draw()
    update_canvas()
