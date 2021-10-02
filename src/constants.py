from pathlib import Path

import pygame
import tkinter as tk

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
RED = (255, 0, 0)
CLOCK = pygame.time.Clock()
g = 35

DEV_MODE = True

FPS = 40
SPF = 1 / FPS
FRUITS = ['watermelon', 'orange', 'apple']
