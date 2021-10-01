from constants import WIDTH, HEIGHT
from entities import Player, PlayTime


def game_loop():
    player = Player('Player1')
    game = PlayTime(WIDTH, HEIGHT, player)

    game.init_game()
