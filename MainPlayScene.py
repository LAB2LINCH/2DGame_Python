from pico2d import *
from random import *
import game_framework
import GameOverScene
import character
import stage_controller


name = "MainPlayScene"
Character = None
Stage_ctrl = None
groundcheck = False

Stage = 1
UP, LEFT, RIGHT, DOWN, FALSE = 1, 2, 3, 4, 0

def collision(a, b): #body = 0
    a_LEFT, a_DOWN, a_RIGHT, a_UP = a
    b_LEFT, b_DOWN, b_RIGHT, b_UP = b

    if a_RIGHT < b_LEFT: return False
    if a_LEFT > b_RIGHT: return False
    if a_UP < b_DOWN: return False
    if a_DOWN > b_UP: return False

    return True

def collision_ADD(a, b): #body = 0
    a_LEFT, a_DOWN, a_RIGHT, a_UP = a
    b_LEFT, b_DOWN, b_RIGHT, b_UP = b

    if a_RIGHT < b_LEFT: return FALSE
    if a_LEFT > b_RIGHT: return FALSE
    if a_UP < b_DOWN: return FALSE
    if a_DOWN > b_UP: return FALSE

    a = math.fabs(a_RIGHT-b_LEFT)#LEFT
    b = math.fabs(a_LEFT-b_RIGHT)#RIGHT
    c = math.fabs(a_UP-b_DOWN)#UP
    d = math.fabs(a_DOWN-b_UP)#DOWN

    if (a<b) and (a<c) and (a<d): return RIGHT
    elif b<c and b<d: return LEFT
    elif c<d: return UP
    else: return DOWN


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
    global Character, running, Stage_ctrl, groundcheck
    Character.update(frame_time)
    Stage_ctrl.update(frame_time, (Character.x, Character.y))

    for monster in Stage_ctrl.Monster:
        if (monster.state == monster.ATK):
            if (collision(Character.hitbox(0), monster.hitbox(1))):#char - mon_atk
                pass
        elif monster.level == 0:
            if monster.state == monster.SKILL1:#char - mon_skill
                pass

        if (Character.state // 2) == 3:  # mon - char_atk
            if (collision(Character.hitbox(1), monster.hitbox(0))):
                print(monster.hp)
                if Character.ATK:
                    if(monster.damage(Character.damage())):
                        Stage_ctrl.Monster.remove(monster)
        elif (Character.state // 2) == 4:  # mon - char_skill1
            if (collision(Character.hitbox(2), monster.hitbox(0))):
                print(monster.hp)
                if Character.ATK:
                    if(monster.damage(Character.damage())):
                        Stage_ctrl.Monster.remove(monster)
        elif (Character.state // 2) == 5:  # mon - char_skill2
            if (collision(Character.hitbox(3), monster.hitbox(0))):
                print(monster.hp)
                if Character.ATK:
                    if(monster.damage(Character.damage())):
                        Stage_ctrl.Monster.remove(monster)
    Character.ATK = False

    groundcheck = False
    for block in Stage_ctrl._BLOCK:
        side = collision_ADD(Character.hitbox(0), block.hitbox())
        if side == FALSE:
            if block.collisionflag == DOWN:
                block.collisionflag = FALSE
                break
            elif block.collisionflag in (LEFT, RIGHT):
                Character.canmove[block.collisionflag-2] = True
                block.collisionflag = FALSE
                break
        elif side == DOWN:#char - block
            if math.fabs((block.return_ground_y() + (Character.imagesize_y // 2)) - Character.y) <= 5:
                block.collisionflag = DOWN
                Character.onground(block.return_ground_y())
                groundcheck = True
        elif side == LEFT:
            block.collisionflag = LEFT
            Character.canmove[LEFT-2] = False
        elif side == RIGHT:
            block.collisionflag = RIGHT
            Character.canmove[RIGHT-2] = False

    if not groundcheck:
        Character.isground = False
        Character.canmove[LEFT-2] = True
        Character.canmove[RIGHT-2] = True

    for monster in Stage_ctrl.Monster:
        monster.c_block = False

    for monster in Stage_ctrl.Monster:
        for block in Stage_ctrl._BLOCK:
            if math.fabs(monster.x - block.x) <= block.image.w\
                    and math.fabs(monster.y - block.y) <= block.image.h:
                if (collision(monster.hitbox(0), block.hitbox())):#mon - block
                    monster.isground == True
                    monster.c_block = True

    for monster in Stage_ctrl.Monster:
        if monster.c_block == False:
            monster.isground = False

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
