import os
import random
import sys

import pygame

WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
g = 1
score = 0
fps = 13
fruits = ['watermelon', 'orange', 'apple']

pygame.init()
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
gameDisplay.fill(WHITE)
font = pygame.font.Font(os.path.join(os.getcwd(), 'src', 'media', 'fonts', 'comic.ttf'), 32)
score_text = font.render(str(score), True, BLACK, WHITE)


def generate_random_fruit(fruit: str) -> None:
    path = os.path.join(os.getcwd(), 'src', 'media', 'sprites', fruit + '.png')
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


data = {}
for fruit in fruits:
    generate_random_fruit(fruit)

pygame.display.update()

while True:
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
            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 60 and \
                    current_position[1] > value['y'] and current_position[1] < value['y'] + 60:
                path = os.path.join(os.getcwd(), 'src', 'media', 'sprites', 'half_' + key + '.png')
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
