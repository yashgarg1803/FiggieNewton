from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer

g = Game(show_messages=False)
p1 = RandomPlayer("Player 1")
p2 = RandomPlayer("Player 2")
p3 = RandomPlayer("Player 3")
p4 = RandomPlayer("Player 4")
g.add_player(p1)
g.add_player(p2)
g.add_player(p3)
g.add_player(p4)
g.start_game(1000)
print(g.balances)
