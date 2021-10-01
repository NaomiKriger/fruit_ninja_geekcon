import random
from pathlib import Path
from typing import Tuple

import pygame


class Game:
    pass


class Player:
    pass


class Cursor:
    pass


class Fruit:
    def __init__(self, ftype: str, img_path: Path,):
        self.ftype = ftype
        self.img = pygame.image.load(img_path)
        self.x = random.randint(100, 500)
        self.y = 800
        self.speed_x = random.randint(-10, 10)
        self.speed_y = random.randint(-80, -60)
        self.throw = False
        self.t = 0
        self.hit = False

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_position(self) -> Tuple[int, int]:
        return self.get_x(), self.get_y()


