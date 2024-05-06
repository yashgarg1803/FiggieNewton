from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer
from agents.human import HumanPlayer
from agents.figgienewton import FiggieNewton
from agents.card_counter import CardCounter
import learn
import learn1


parameters = [
    # {
    #     "min": 1.1,
    #     "max": 100.0,
    #     "initial": 15.0,
    #     "step_size": 10.0
    # },
    # {
    #     "min": 0.01,
    #     "max": 50.0,
    #     "initial": 5.0,
    #     "step_size": 5.0
    # },
    {
        "min": 0.0,
        "max": 2.0,
        "initial": .25,
        "step_size": .2
    },
]
print(learn1.hill_climbing(FiggieNewton, parameters, iterations=100, num_rounds=1000))

# g = Game(show_messages=False)
# p1 = FiggieNewton("FiggieNewton", [3.5, 2])
# # p1 = RandomPlayer("Random1")
# # p2 = CardCounter("CountingPlayer")
# p2 = RandomPlayer("Random2")
# p3 = RandomPlayer("Random3")
# p4 = RandomPlayer("Random4")
# g.add_player(p1)
# g.add_player(p2)
# g.add_player(p3)
# g.add_player(p4)
# num_rounds = 100
# g.start_game(num_rounds)
# print([(player_id, g.balances[player_id]/num_rounds) for player_id in g.players])