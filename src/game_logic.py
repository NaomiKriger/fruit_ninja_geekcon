import os
import random
import sys
from typing import Tuple

import pygame
from pygame.surface import Surface

from pathlib import Path

MEDIA_PATH = Path(__file__).parent / 'media'

WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CURSOR_COLOR = (209, 238, 239)
clock = pygame.time.Clock()
g = 1
score = 0
fps = 13
fruits = ['watermelon', 'orange', 'apple']

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
    data[fruit] = {
        'img': pygame.image.load(path),
        'x': random.randint(100, 500),
        'y': 800,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -60),
        'throw': False,
        't': 0,
        'hit': False,
    }

    if (random.random() >= 0.75):
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False


def paint_cursor(surface: Surface, position: Tuple[int, int]) -> None:
    glare_sprite = pygame.image.load(os.path.join(os.getcwd(), 'src', 'media', 'sprites', 'glare.png'))
    glare_sprite = pygame.transform.scale(glare_sprite, (118, 101))

    surface.blit(glare_sprite, (position[0] - 59, position[1] - 50))


data = {}
for fruit in fruits:
    generate_random_fruit(fruit)

pygame.display.update()


def game_loop():
    global score_text, score
    gameDisplay.fill(WHITE)
    gameDisplay.blit(score_text, (0, 0))
    for key, value in data.items():
        if value['throw']:
            value['x'] = value['x'] + value['speed_x']
            value['y'] = value['y'] + value['speed_y']
            value['speed_y'] += (g * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruit(key)

            current_position = pygame.mouse.get_pos()
            paint_cursor(gameDisplay, current_position)

            if is_hit(current_position, value):
                path = MEDIA_PATH / 'sprites' / ('half_' + key + '.png')
                value['img'] = pygame.image.load(path)
                value['speed_x'] += 10
                score += 1
                score_text = font.render(str(score), True, BLACK, WHITE)
                value['hit'] = True

        else:
            generate_random_fruit(key)

    pygame.display.update()
    clock.tick(fps)

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
