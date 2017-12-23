import game_framework
import StartScene
from pico2d import *

Image = None
sound = None

def enter():
    global Image, sound
    Image = load_image("./src/bgi_clear.png")
    sound = load_wav("./src/game_win.wav")
    sound.set_volume(50)
    sound.play()

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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_g):
            game_framework.change_state(StartScene)

def update(frame_time):
    pass

def draw(frame_time):
    global Image
    clear_canvas()
    Image.draw(get_canvas_width()//2, get_canvas_height()//2)
    update_canvas()