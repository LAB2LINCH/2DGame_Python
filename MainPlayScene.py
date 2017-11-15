from pico2d import *
from random import *
import game_framework
import GameOverScene
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
regentime = 3
Rp = None


def collision(a, b): #body = 0
    a_RIGHT, a_DOWN, a_LEFT, a_UP = a
    b_RIGHT, b_DOWN, b_LEFT, b_UP = b

    if a_RIGHT > b_LEFT: return False
    if a_LEFT < b_RIGHT: return False
    if a_UP < b_DOWN: return False
    if a_DOWN > b_UP: return False
    return True

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

def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        else:
            Character.handle_events(frame_time, event)



def update(frame_time):
    global Character, Monster, running, gametime, regentime
    Character.update(frame_time)
    for monster in Monster:
        monster.update(frame_time, (Character.x, Character.y))
    if running == True:
        gametime += frame_time
        if gametime >= regentime:
            Monster.append(monster_sub.monster_sub(20, Regenpoint[randint(0,4)]))
            gametime = 0
#char - mon_skill
#char - block
#char - ladder
#mon - block

        if (Character.state // 2) in (3, 4, 5):
            #mon - char_atk
            #mon - char_skill1
            #mon - char_skill2
            pass
        for monster in Monster: #char - mon_atk
            if (monster.state == monster.ATK):
                collision(Character.hitbox(0), monster.hitbox(1))



def draw(frame_time):
    global Character, Map, Regenpoint, Monster
    clear_canvas()
    Map.draw()
    Character.draw()
    for mon in Monster:
        mon.draw()
    update_canvas()
