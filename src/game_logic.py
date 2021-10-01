import sys
from typing import Tuple

import pygame
from pygame.surface import Surface

from constants import WIDTH, HEIGHT, WHITE, MEDIA_PATH, BLACK, GLARE_SPRITE, FRUITS, CLOCK, FPS, g
from entities import Fruit, FruitCollection, Player

score = 0
player = Player('Player1')

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
gameDisplay.fill(WHITE)
font = pygame.font.Font(
    MEDIA_PATH / 'fonts' / 'comic.ttf',
    32,
)
score_text = font.render(str(player.get_score()), True, BLACK, WHITE)

fruit_collection = FruitCollection()


def paint_cursor(surface: Surface, position: Tuple[int, int]) -> None:
    surface.blit(GLARE_SPRITE, (position[0] - 59, position[1] - 50))


for fruit in FRUITS:
    Fruit.generate_random_fruit(fruit_collection, fruit)

pygame.display.update()


def game_loop():
    global score_text, player
    gameDisplay.fill(WHITE)
    gameDisplay.blit(score_text, (0, 0))
    for key, value in fruit_collection.get_all().items():
        if value.get_throw():
            value.set_x(value.get_x() + value.get_speed_x())
            value.set_y(value.get_y() + value.get_speed_y())
            value.speed_y += (g * value.t)
            value.t += 1

            if value.get_y() <= 800:
                gameDisplay.blit(value.get_img(), value.get_position())
            else:
                Fruit.generate_random_fruit(fruit_collection, key)

            current_position = pygame.mouse.get_pos()
            paint_cursor(gameDisplay, current_position)

            if is_hit(current_position, value):
                path = MEDIA_PATH / 'sprites' / ('half_' + key + '.png')
                value.set_img(pygame.image.load(path))
                value.set_speed_x(value.get_speed_x() + 10)
                player.set_score(player.get_score() + 1)
                score_text = font.render(str(player.get_score()), True, BLACK, WHITE)
                value.hit = True

        else:
            Fruit.generate_random_fruit(fruit_collection, key)

    pygame.display.update()
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def is_hit(current_position, value):
    return all([
        not value.hit,
        current_position[0] > value.get_x(),
        current_position[0] < value.get_x() + 60,
        current_position[1] > value.get_y(),
        current_position[1] < value.get_y() + 60,
    ])
