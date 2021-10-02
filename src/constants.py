import tkinter as tk
from pathlib import Path

import pygame

root = tk.Tk()

MEDIA_PATH = Path(__file__).parent / 'media'
GLARE_SPRITE = pygame.transform.scale(
    pygame.image.load(MEDIA_PATH / 'sprites' / 'glare.png'),
    (118, 101)
)

WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CLOCK = pygame.time.Clock()
g = 5

FPS = 40
SPF = 1 / FPS
FRUITS = ['hershko', 'shahar', 'ariel']
