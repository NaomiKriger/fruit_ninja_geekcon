import random
import sys
from pathlib import Path
from typing import Tuple

import pygame
from pygame.surface import Surface

import tkinter as tk

root = tk.Tk()

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()


MEDIA_PATH = Path(__file__).parent / 'media'
GLARE_SPRITE = pygame.transform.scale(
    pygame.image.load(MEDIA_PATH / 'sprites' / 'glare.png'),
    (118, 101)
)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CURSOR_COLOR = (209, 238, 239)
clock = pygame.time.Clock()
g = 84
score = 0
FPS = 60
SPF = 1 / FPS

FRUITS = ['watermelon', 'orange', 'apple']

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
gameDisplay.fill(WHITE)
font = pygame.font.Font(
    MEDIA_PATH / 'fonts' / 'comic.ttf',
    32,
)
score_text = font.render(str(score), True, BLACK, WHITE)


def generate_random_fruit(fruit: str) -> None:
    path = MEDIA_PATH / 'sprites' / (fruit + '.png')
    seconds_till_top = 5
    data[fruit] = {
        'img': pygame.image.load(path),
        'x': random.randint(0, WIDTH),
        'y': 0,
        'speed_x': 0,#random.randint(-1000, 1000)*2/1000,
        'speed_y': -420,#-HEIGHT / seconds_till_top,
        # x[m] = x0[m] + v[m/s]*t[s] + 1/2(a[m/s^2]*t^2[s^2])
        # v = (x1 - x0) / dt
        # v = (0 - HEIGHT) / seconds_till_top
        # t=5, g=? v0=?, x0=1050, x1=0, v1=0,
        #
        # 0 = 1050 + -25g + g25/2
        # 0 = 2100 - 25g
        # v = -1050/5 +g*5/2
        # 0 = v0 + g*5


        'throw': False,
        't': 0,
        'hit': False,
    }

    if (random.random() >= 0.75):
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False


def paint_cursor(surface: Surface, position: Tuple[int, int]) -> None:
    surface.blit(GLARE_SPRITE, (position[0] - 59, position[1] - 50))


data = {}
for fruit in FRUITS:
    generate_random_fruit(fruit)
    break

pygame.display.update()


def game_loop():
    global score_text, score
    gameDisplay.fill(WHITE)
    gameDisplay.blit(score_text, (0, 0))
    for key, value in data.items():
        if value['throw']:
            value['x'] = int(value['x'] + value['speed_x'])
            value['y'] = int(HEIGHT + value['speed_y']*(SPF*value["t"]))
            value['speed_y'] = value['speed_y'] + (g * SPF * value["t"])
            value['t'] += 1
            print(f"{int(value['speed_y'])}, {value['t']}, {int(value['y'])}")

            if value['y'] <= HEIGHT:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruit(key)

            current_position = pygame.mouse.get_pos()
            paint_cursor(gameDisplay, current_position)

            if is_hit(current_position, value):
                path = MEDIA_PATH / 'sprites' / ('half_' + key + '.png')
                value['img'] = pygame.image.load(path)
                value['speed_x'] += 0
                score += 1
                score_text = font.render(str(score), True, BLACK, WHITE)
                value['hit'] = True

        else:
            generate_random_fruit(key)

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def is_hit(current_position, value):
    return all([
        not value['hit'],
        current_position[0] > value['x'],
        current_position[0] < value['x'] + 60,
        current_position[1] > value['y'],
        current_position[1] < value['y'] + 60,
    ])
