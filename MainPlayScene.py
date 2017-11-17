from pico2d import *
from random import *
import game_framework
import GameOverScene
import character
import stage_controller


name = "MainPlayScene"
Character = None
Stage_ctrl = None

Stage = 1

def collision(a, b): #body = 0
    a_LEFT, a_DOWN, a_RIGHT, a_UP = a
    b_LEFT, b_DOWN, b_RIGHT, b_UP = b

    if a_RIGHT < b_LEFT: return False
    if a_LEFT > b_RIGHT: return False
    if a_UP < b_DOWN: return False
    if a_DOWN > b_UP: return False
    return True

def collision_G(a, b): #a = moveable
    a_DOWN= a[1]
    b_UP = b[3]

    if a_DOWN > b_UP: return False
    return True

def enter():
    global Character, Map, Stage, running, Stage_ctrl
    Character = character.character()
    Stage_ctrl = stage_controller.stage_controller(Stage)

    Stage = 1
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
    global Character, running, Stage_ctrl
    Character.update(frame_time)
    Stage_ctrl.update(frame_time, (Character.x, Character.y))

    if (Character.state // 2) in (3, 4, 5):
            #mon - char_atk
            #mon - char_skill1
            #mon - char_skill2
        pass

    for monster in Stage_ctrl.Monster:
        if (monster.state == monster.ATK):
            if (collision(Character.hitbox(0), monster.hitbox(1))):#char - mon_atk
                pass
        elif monster.level == 0:
            if monster.state == monster.SKILL1:#char - mon_skill
                pass

    for block in Stage_ctrl._BLOCK:
        if Character.isground == False:
            if (collision(Character.hitbox(0), block.hitbox())):#char - block
                Character.onground()

    for monster in Stage_ctrl.Monster:
        if monster.isground == False:
            for block in Stage_ctrl._BLOCK:
                if (collision(monster.hitbox(0), block.hitbox())):#mon - block
                    monster.isground == True
                    break;

    for useable in Stage_ctrl._USEABLE:
        if (collision(Character.hitbox(0), useable.hitbox())):#char - ladder
                pass

def draw(frame_time):
    global Character
    clear_canvas()

    Stage_ctrl.draw()
    Character.draw()

    Character.draw_hitbox()

    update_canvas()
