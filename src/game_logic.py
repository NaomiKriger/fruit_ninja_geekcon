import random
import sys
from pathlib import Path
from typing import Tuple

import pygame
from pygame.surface import Surface

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
missed_count = 5
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
missed_text = font.render(str(missed_count), True, (255, 0, 0), WHITE)


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
    surface.blit(GLARE_SPRITE, (position[0] - 59, position[1] - 50))


data = {}
for fruit in FRUITS:
    generate_random_fruit(fruit)

pygame.display.update()


def game_loop():
    global score_text, score, missed_count, missed_text

    keep_going = True
    while keep_going:
        gameDisplay.fill(WHITE)
        gameDisplay.blit(score_text, (0, 0))
        gameDisplay.blit(missed_text, (0, 50))
        for key, value in data.items():
            if value['throw']:
                value['x'] = value['x'] + value['speed_x']
                value['y'] = value['y'] + value['speed_y']
                value['speed_y'] += (g * value['t'])
                value['t'] += 1

                if value['x'] < 0 or value['x'] > WIDTH:
                    generate_random_fruit(key)
                if value['y'] <= 800:
                    gameDisplay.blit(value['img'], (value['x'], value['y']))
                else:
                    if not value['hit']:
                        missed_count -= 1
                    if missed_count == 0:
                        pygame.display.update()
                        keep_going = False
                    missed_text = font.render(str(missed_count), True, (255, 0, 0), WHITE)
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
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    game_over_text = font.render('GAME OVER', True, BLACK, WHITE)
    game_over_x = gameDisplay.get_width() // 2 - game_over_text.get_width() // 2
    game_over_y = gameDisplay.get_height() // 2 - game_over_text.get_height() // 2
    gameDisplay.blit(game_over_text, (game_over_x, game_over_y))


def is_hit(current_position, value):
    return all([
        not value['hit'],
        current_position[0] > value['x'],
        current_position[0] < value['x'] + 60,
        current_position[1] > value['y'],
        current_position[1] < value['y'] + 60,
    ])
