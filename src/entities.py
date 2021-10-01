import random
from pathlib import Path
from typing import Tuple

import pygame
from pygame import image
from pygame.surface import Surface

from constants import MEDIA_PATH


class Game:
    def __init__(
            self,
            surface: Surface,
            width: int,
            height: int,
            score: int = 0,
            missed_count: int = 5
    ):
        pass


class Player:
    pass


class Cursor:

    def get_current_position(self) -> Tuple[int, int]:
        pass


class FruitCollection:

    def __init__(self, *args):
        for ftype in args:
            self.__dict__[ftype] = None

    def get_fruit(self, ftype: str):
        return self.__dict__[ftype]

    def set_fruit(self, ftype: str, value) -> None:
        self.__dict__[ftype] = value

    def get_all(self) -> dict:
        return self.__dict__


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

    def set_x(self, value: int) -> None:
        self.x = value

    def get_y(self) -> int:
        return self.y

    def set_y(self, value: int) -> None:
        self.y = value

    def get_position(self) -> Tuple[int, int]:
        return self.get_x(), self.get_y()

    def get_speed_x(self) -> int:
        return self.speed_x

    def set_speed_x(self, value: int) -> None:
        self.speed_x = value

    def get_speed_y(self) -> int:
        return self.speed_y

    def get_img(self) -> image:
        return self.img

    def set_img(self, value: image) -> None:
        self.img = value

    def get_throw(self) -> bool:
        return self.throw

    def set_throw(self, value: bool) -> None:
        self.throw = value

    @staticmethod
    def generate_random_fruit(collection: FruitCollection, ftype: str) -> None:
        path = MEDIA_PATH / 'sprites' / (ftype + '.png')
        collection.set_fruit(ftype, Fruit(ftype=ftype, img_path=path))

        if random.random() >= 0.75:
            collection.get_fruit(ftype).set_throw(True)
        else:
            collection.get_fruit(ftype).set_throw(False)


