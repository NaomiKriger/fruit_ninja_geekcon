import random
import sys
from pathlib import Path
from typing import Tuple, List

import pygame
from pygame import image
from pygame.font import Font
from pygame.surface import Surface

from constants import MEDIA_PATH, WHITE, BLACK, FRUITS, CLOCK, FPS, WIDTH, HEIGHT, g


class Player:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.score = 0
        self.missed_count = 5

    def get_score(self) -> int:
        return self.score

    def set_score(self, value: int) -> None:
        self.score = value

    def get_missed_count(self) -> int:
        return self.missed_count

    def set_missed_count(self, value: int) -> None:
        self.missed_count = value


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

    def is_hit(self, current_position: Tuple[int, int]) -> bool:
        return all([
            not self.hit,
            current_position[0] > self.get_x(),
            current_position[0] < self.get_x() + 60,
            current_position[1] > self.get_y(),
            current_position[1] < self.get_y() + 60,
        ])

    @staticmethod
    def generate_random_fruit(collection: FruitCollection, ftype: str) -> None:
        path = MEDIA_PATH / 'sprites' / (ftype + '.png')
        collection.set_fruit(ftype, Fruit(ftype=ftype, img_path=path))

        if random.random() >= 0.75:
            collection.get_fruit(ftype).set_throw(True)
        else:
            collection.get_fruit(ftype).set_throw(False)


class Game:
    def __init__(
            self,
            width: int,
            height: int,
            player: Player
    ):
        self.width = width
        self.height = height
        self.player = player
        self.surface = None
        self.font = None
        self.fruit_collection = FruitCollection()
        self.cursor = None
        self.keep_going = True

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_display_size(self) -> Tuple[int, int]:
        return self.width, self.height

    def init_game(self):
        pygame.init()
        self.font = pygame.font.Font(
            MEDIA_PATH / 'fonts' / 'comic.ttf',
            32,
        )
        score_text = self.font.render(str(self.player.get_score()), True, BLACK, WHITE)
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))

        for fruit in FRUITS:
            Fruit.generate_random_fruit(self.fruit_collection, fruit)

        while self.keep_going:
            self.surface.fill(WHITE)
            self.surface.blit(score_text, (0, 0))
            self.throw_fruit()

            pygame.display.update()
            CLOCK.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def throw_fruit(self) -> None:
        for key, value in self.fruit_collection.get_all().items():
            if value.get_throw():
                value.set_x(value.get_x() + value.get_speed_x())
                value.set_y(value.get_y() + value.get_speed_y())
                value.speed_y += (g * value.t)
                value.t += 1

                if value.get_y() <= 800:
                    self.surface.blit(value.get_img(), value.get_position())
                else:
                    Fruit.generate_random_fruit(self.fruit_collection, key)

                current_position = pygame.mouse.get_pos()
                # paint_cursor(gameDisplay, current_position)

                if value.is_hit(current_position):
                    path = MEDIA_PATH / 'sprites' / ('half_' + key + '.png')
                    value.set_img(pygame.image.load(path))
                    value.set_speed_x(value.get_speed_x() + 10)
                    self.player.set_score(self.player.get_score() + 1)
                    score_text = self.font.render(str(self.player.get_score()), True, BLACK, WHITE)
                    value.hit = True

            else:
                Fruit.generate_random_fruit(self.fruit_collection, key)

