from pico2d import *
from random import *
import game_framework
import GameOverScene
import character
import stage_controller
import MenuScene


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
    Character = character.character(2)
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
            game_framework.push_state(MenuScene)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            Stage_ctrl.stageChange(2)
            Character.stage_Change()
        else:
            Character.handle_events(frame_time, event)

def update(frame_time):
    global Character, running, Stage_ctrl, groundcheck
    Character.update(frame_time)
    Stage_ctrl.update(frame_time, (Character.x, Character.y))

    for monster in Stage_ctrl.Monster:
        if (monster.state == monster.ATK):
            if (collision(Character.hitbox(0), monster.hitbox(1))):#char - mon_atk
                print("AAAAAA")
        elif monster.level == 0:
            if monster.state == monster.SKILL1:#char - mon_skill
                pass

        if (Character.state // 2) == 3:  # mon - char_atk
            if (collision(Character.hitbox(1), monster.hitbox(0))):
                print(monster.hp)
                if Character.ATK:
                    if(monster.damage(Character.damage())):
                        Stage_ctrl.drop_item(monster.level, (monster.x, monster.y))
                        Stage_ctrl.Monster.remove(monster)
        elif (Character.state // 2) == 4:  # mon - char_skill1
            if (collision(Character.hitbox(2), monster.hitbox(0))):
                print(monster.hp)
                if Character.ATK:
                    if(monster.damage(Character.damage())):
                        Stage_ctrl.drop_item(monster.level, (monster.x, monster.y))
                        Stage_ctrl.Monster.remove(monster)
        elif (Character.state // 2) == 5:  # mon - char_skill2
            if (collision(Character.hitbox(3), monster.hitbox(0))):
                print(monster.hp)
                if Character.ATK:
                    if(monster.damage(Character.damage())):
                        Stage_ctrl.drop_item(monster.level, (monster.x, monster.y))
                        Stage_ctrl.Monster.remove(monster)
    Character.ATK = False

    for block in Stage_ctrl._BLOCK:
        side = collision_ADD(Character.hitbox(0), block.hitbox())  # mon - block
        if side == FALSE:
            if block == Character.d_block:
                Character.d_block = None
            elif block == Character.l_block:
                Character.l_block = None
            elif block == Character.r_block:
                Character.r_block = None
        elif side == DOWN and Character.d_block != block and Character.is_down() == True:
            Character.onground(block.return_ground_y())
            Character.d_block = block
            if Character.l_block == block: Character.l_block = None
            elif Character.r_block == block: Character.r_block = None
        elif side == LEFT and Character.l_block != block:
            Character.canmove[LEFT - 2] = False
            Character.l_block = block
            if Character.d_block == block: Character.d_block = None
            elif Character.r_block == block: Character.r_block = None
        elif side == RIGHT and Character.r_block != block:
            Character.canmove[RIGHT - 2] = False
            Character.r_block = block
            if Character.l_block == block: Character.l_block = None
            elif Character.d_block == block: Character.d_block = None
        if Character.d_block == None: Character.isground = False
        if Character.l_block == None: Character.canmove[LEFT - 2] = True
        if Character.r_block == None: Character.canmove[RIGHT - 2] = True

    # 벽 - 몬스터 바닥 충돌 시 onground, 옆 충돌시 off, 부딪히면 각 배열에 저장해서 다음 비교에 빠지면 빼줌

    for monster in Stage_ctrl.Monster:
        for block in Stage_ctrl._BLOCK:
            side = collision_ADD(monster.hitbox(0), block.hitbox())  # mon - block
            if side == FALSE:
                if block == monster.d_block:
                    monster.d_block = None
                elif block == monster.l_block:
                    monster.l_block = None
                elif block == monster.r_block:
                    monster.r_block = None
            elif side == DOWN and monster.d_block != block:
                monster.onground(block.return_ground_y())
                monster.d_block = block
                if monster.l_block == block: monster.l_block = None
                elif monster.r_block == block: monster.r_block = None
            elif side == LEFT and monster.l_block != block:
                monster.canmove[LEFT - 2] = False
                monster.l_block = block
                if monster.d_block == block: monster.d_block = None
                elif monster.r_block == block: monster.r_block = None
            elif side == RIGHT and monster.r_block != block:
                monster.canmove[RIGHT - 2] = False
                monster.r_block = block
                if monster.l_block == block: monster.l_block = None
                elif monster.d_block == block: monster.d_block = None
            if monster.d_block == None: monster.isground = False
            if monster.l_block == None: monster.canmove[LEFT - 2] = True
            if monster.r_block == None: monster.canmove[RIGHT - 2] = True

    for useable in Stage_ctrl._USEABLE:
        if (collision(Character.hitbox(0), useable.hitbox())):#char - ladder
                pass

    for item in Stage_ctrl._item:
        if (collision(Character.hitbox(0), item.hitbox())):
            Character.getitem(item)
            Stage_ctrl._item.remove(item)

def draw(frame_time):
    global Character
    clear_canvas()

    Stage_ctrl.draw()
    Character.draw()

    #Character.draw_hitbox()

    update_canvas()
