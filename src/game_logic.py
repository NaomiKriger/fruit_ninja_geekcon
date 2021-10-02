import pygame
from pygame import QUIT

from constants import WIDTH, HEIGHT, CLOCK, FPS
from entities import PlayScene


def game_loop():
    pygame.init()

    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    running = True

    scene = PlayScene()

    while running:
        if pygame.event.get(QUIT):
            running = False
        scene.handle_events(pygame.event.get())
        scene.render(surface)
        scene.update(surface)

        pygame.display.update()
        CLOCK.tick(FPS)
