from constants import WIDTH, HEIGHT
from entities import Player, Game


def game_loop():
    player = Player('Player1')
    game = Game(WIDTH, HEIGHT, player)

    game.init_game()
