import random
import sys
from pathlib import Path
from typing import Tuple

import pygame
from pygame.surface import Surface

from entities import Fruit

MEDIA_PATH = Path(__file__).parent / 'media'
GLARE_SPRITE = pygame.transform.scale(
    pygame.image.load(MEDIA_PATH / 'sprites' / 'glare.png'),
    (118, 101)
)
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CURSOR_COLOR = (209, 238, 239)
clock = pygame.time.Clock()
g = 1
score = 0
FPS = 13
FRUITS = ['watermelon', 'orange', 'apple']

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
gameDisplay.fill(WHITE)
font = pygame.font.Font(
    MEDIA_PATH / 'fonts' / 'comic.ttf',
    32,
)
score_text = font.render(str(score), True, BLACK, WHITE)


def generate_random_fruit(fruit_type: str) -> None:
    path = MEDIA_PATH / 'sprites' / (fruit_type + '.png')
    data[fruit_type] = Fruit(ftype=fruit_type, img_path=path)

    if random.random() >= 0.75:
        data[fruit_type].throw = True
    else:
        data[fruit_type].throw = False


def paint_cursor(surface: Surface, position: Tuple[int, int]) -> None:
    surface.blit(GLARE_SPRITE, (position[0] - 59, position[1] - 50))


data = {}
for fruit in FRUITS:
    generate_random_fruit(fruit)

pygame.display.update()


def game_loop():
    global score_text, score
    gameDisplay.fill(WHITE)
    gameDisplay.blit(score_text, (0, 0))
    for key, value in data.items():
        if value.throw:
            value.x = value.x + value.speed_x
            value.y = value.y + value.speed_y
            value.speed_y += (g * value.t)
            value.t += 1

            if value.y <= 800:
                gameDisplay.blit(value.img, (value.x, value.y))
            else:
                generate_random_fruit(key)

            current_position = pygame.mouse.get_pos()
            paint_cursor(gameDisplay, current_position)

            if is_hit(current_position, value):
                path = MEDIA_PATH / 'sprites' / ('half_' + key + '.png')
                value.img = pygame.image.load(path)
                value.speed_x += 10
                score += 1
                score_text = font.render(str(score), True, BLACK, WHITE)
                value.hit = True

        else:
            generate_random_fruit(key)

    pygame.display.update()
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def is_hit(current_position, value):
    return all([
        not value.hit,
        current_position[0] > value.x,
        current_position[0] < value.x + 60,
        current_position[1] > value.y,
        current_position[1] < value.y + 60,
    ])
