import random
import sys
from pathlib import Path
from typing import Tuple, List
import cv2


import numpy
import pygame
from pygame import image
from pygame.event import Event
from pygame.surface import Surface

from constants import MEDIA_PATH, WHITE, BLACK, FRUITS, CLOCK, FPS, WIDTH, HEIGHT, g, GLARE_SPRITE, SPF, RED


class Player:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self.score = 0
        self.missed_count = 5

    def get_score(self) -> int:
        return self.score

    def set_score(self, value: int) -> None:
        self.score = value



class Cursor:
    def __init__(self):
        self.cap = cv2.VideoCapture(1)  # (0) is the laptop's cam, (1) is the external webcam

    def get_blue_blob_position(self):
        ret, frame = self.cap.read()
        frame_2 = frame * [1, 0, 0]

        gray_full = cv2.cvtColor(numpy.uint8(frame_2), cv2.COLOR_BGR2GRAY)
        gray_full_final = cv2.GaussianBlur(gray_full, (31, 31), 0)
        _, _, _, (x_coor, y_coor) = cv2.minMaxLoc(gray_full_final)


        return WIDTH - x_coor, y_coor


    def draw(self, surface: Surface) -> None:
        x_coor, y_coor = self.mouse_obj.get_pos()
        center_x, center_y = GLARE_SPRITE.get_width() // 2, GLARE_SPRITE.get_height() // 2
        surface.blit(GLARE_SPRITE, (x_coor - center_x, y_coor - center_y))


class FruitCollection:
    def __init__(self, *args):
        for fruit_type in args:
            self.__dict__[fruit_type] = None

    def get_fruit(self, fruit_type: str):
        return self.__dict__[fruit_type]

    def set_fruit(self, fruit_type: str, value) -> None:
        self.__dict__[fruit_type] = value

    def get_all(self) -> dict:
        return self.__dict__


class Fruit:
    def __init__(self, fruit_type: str, img_path: Path):
        self.fruit_type = fruit_type
        self.img = pygame.transform.scale(pygame.image.load(img_path), (160, 160))
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT
        self.speed_x = self.get_speed_x_random()
        self.speed_y = -1600 + random.randint(-300, 300)
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

    def get_speed_x(self) -> float:
        return self.speed_x

    def set_speed_x(self, value: float) -> None:
        self.speed_x = value

    def get_speed_y(self) -> int:
        return self.speed_y

    def set_speed_y(self, value: float) -> None:
        self.speed_y = value

    def get_img(self) -> image:
        return self.img

    def set_img(self, value: image) -> None:
        self.img = value

    def get_throw(self) -> bool:
        return self.throw

    def set_throw(self, value: bool) -> None:
        self.throw = value

    def is_hit(self, current_position: Tuple[int, int]) -> bool:
        current_x, current_y = current_position
        range_x, range_y = self.img.get_width(), self.img.get_height()
        return all([
            not self.hit,
            current_x > self.get_x(),
            current_x < self.get_x() + range_x,
            current_y > self.get_y(),
            current_y < self.get_y() + range_y,
        ])

    def get_x_location(self):
        current_x = int(self.get_x() + self.get_speed_x())
        if current_x > WIDTH or current_x < 0:
            self.set_speed_x(-1 * self.get_speed_x() * 0.9)
            current_x = int(self.get_x() + self.get_speed_x())
            self.set_speed_y(self.get_speed_y() - 10)
        return current_x

    @staticmethod
    def get_speed_x_random():
        speed_x_random = random.randint(-1000, 1000) * 10 / 1000

        while -0.1 < speed_x_random < 0.1:
            speed_x_random = random.randint(-1000, 1000) * 10 / 1000

        return speed_x_random

    @staticmethod
    def generate_random_fruit(collection: FruitCollection, fruit_type: str) -> None:
        path = MEDIA_PATH / 'sprites' / (fruit_type + '.png')
        collection.set_fruit(fruit_type, Fruit(fruit_type=fruit_type, img_path=path))

        if random.random() >= 0.75:
            collection.get_fruit(fruit_type).set_throw(True)
        else:
            collection.get_fruit(fruit_type).set_throw(False)


class PlayTime:
    def __init__(
            self,
            player: Player
    ):
        self.player = player
        self.font = None
        self.score_text = None
        self.missed_text = None
        self.fruit_collection = FruitCollection()
        self.cursor = None
        self.keep_going = True
        self.init_game()
        self.populate_fruit_collection()

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def get_display_size(self) -> Tuple[int, int]:
        return self.width, self.height

    def populate_fruit_collection(self):
        for fruit in FRUITS:
            Fruit.generate_random_fruit(self.fruit_collection, fruit)

    def init_game(self):
        self.cursor = Cursor(pygame.mouse)
        self.font = pygame.font.Font(
            MEDIA_PATH / 'fonts' / 'comic.ttf',
            32,
        )

    def throw_fruit(self, surface: Surface) -> bool:
        for fruit_name, fruit in self.fruit_collection.get_all().items():
            if fruit.get_throw():
                dt = SPF * fruit.t
                fruit.set_x(fruit.get_x_location())
                fruit.set_y(int(HEIGHT + fruit.get_speed_y() * dt))
                fruit.set_speed_y(fruit.speed_y + (g * dt))
                fruit.t += 1

                if fruit.get_x() < 0 or fruit.get_x() > WIDTH:
                    Fruit.generate_random_fruit(self.fruit_collection, fruit_name)
                if fruit.get_y() <= HEIGHT:
                    surface.blit(fruit.get_img(), fruit.get_position())
                else:
                    if not fruit.hit:
                        self.player.missed_count -= 1
                    if self.player.missed_count <= 0:
                        self.keep_going = False
                    self.missed_text = self.font.render(str(self.player.missed_count), True, (255, 0, 0), WHITE)
                    Fruit.generate_random_fruit(self.fruit_collection, fruit_name)

                current_position = self.cursor.get_current_position()
                self.cursor.draw(surface)

                if fruit.is_hit(current_position):
                    path = MEDIA_PATH / 'sprites' / ('half_' + fruit_name + '.png')
                    fruit.set_img(pygame.transform.scale(pygame.image.load(path), (160, 160)))
                    fruit.set_speed_x(fruit.get_speed_x() + fruit.get_speed_x_random())
                    self.player.set_score(self.player.get_score() + 1)
                    self.score_text = self.font.render(str(self.player.get_score()), True, BLACK, WHITE)
                    fruit.hit = True

            else:
                Fruit.generate_random_fruit(self.fruit_collection, fruit_name)


# Scenes management

class Scene(object):
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.cursor = None
        self.player = Player('Player1')

    def render(self, surface: Surface):
        pass

    def update(self, surface: Surface):
        pass

    def handle_events(self, events: List[Event]):
        pass


class PlayScene(Scene):
    def __init__(self):
        super().__init__()
        self.score_text = None
        self.missed_text = None
        self.font = None
        self.play_time = PlayTime(self.player)
        self.keep_going = True

    def render(self, surface):
        self.font = pygame.font.Font(
            MEDIA_PATH / 'fonts' / 'comic.ttf',
            32,
        )
        self.score_text = self.font.render(str(self.player.get_score()), True, BLACK, WHITE)
        self.missed_text = self.font.render(str(self.player.missed_count), True, RED, WHITE)

        surface.fill(WHITE)
        surface.blit(self.score_text, (0, 0))
        surface.blit(self.missed_text, (0, 50))

    def update(self, surface: Surface):
        self.play_time.throw_fruit(surface)




    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()


class SceneManager:
    def __init__(self):
        self.go_to(PlayScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self
