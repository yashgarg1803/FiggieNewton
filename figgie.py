from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer
from agents.human import HumanPlayer
from agents.figgie_newton import FiggieNewton

import learn


parameters = [
    {
        "min": 0,
        "max": 1,
        "step_size": 0.1
    },
    {
        "min": 0,
        "max": 1,
        "step_size": 0.1
    },
    {
        "min": 1,
        "max": 100,
        "step_size": 5
    }
]
print(learn.hill_climbing(FiggieNewton, parameters, iterations=10))

# g = Game(show_messages=False)
# p1 = FiggieNewton("F1", [1, 1, 10])
# p2 = FiggieNewton("F2", [1, 1, 10])
# p3 = FiggieNewton("F3", [1, 1, 10])
# p4 = FiggieNewton("F4", [1, 1, 10])
# g.add_player(p1)
# g.add_player(p2)
# g.add_player(p3)
# g.add_player(p4)
# num_rounds = 100
# g.start_game(num_rounds)
# print([g.balances[player_id]/num_rounds for player_id in g.players])