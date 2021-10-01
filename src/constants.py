from pathlib import Path

import pygame

MEDIA_PATH = Path(__file__).parent / 'media'
GLARE_SPRITE = pygame.transform.scale(
    pygame.image.load(MEDIA_PATH / 'sprites' / 'glare.png'),
    (118, 101)
)
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CLOCK = pygame.time.Clock()
g = 1

FPS = 13
FRUITS = ['watermelon', 'orange', 'apple']