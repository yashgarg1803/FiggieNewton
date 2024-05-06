from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer
from agents.human import HumanPlayer
from agents.figgienewton import FiggieNewton
from agents.card_counter import CardCounter
from agents.mle import MLEPlayer
import FiggieNewton.learn_v0 as learn_v0
import time

c1 = 1

start_time = time.time()
p1 = FiggieNewton("FiggieNewton", [c1])
# p1 = CardCounter("CC", [3.5, 1])
# p1 = RandomPlayer("Random1")
# p2 = MLEPlayer("MLEPlayer2")
# p2 = FiggieNewton("FiggieNewton2", [c1])
p2 = CardCounter("CC2", [3, 1])
# p2 = RandomPlayer("Random2")
p3 = RandomPlayer("Beginner3")   
# p3 = MLEPlayer("MLEPlayer3")
# p3 = FiggieNewton("FiggieNewton3", [c1])
# p3 = CardCounter("CC3", [3, 1]) 
# p4 = RandomPlayer("Random4")
p4 = MLEPlayer("MLEPlayer4")
# p4 = FiggieNewton("FiggieNewton4", [c1])
# p4 = CardCounter("CC4", [3, 1])

g = Game(show_messages=False)
g.add_player(p1)
g.add_player(p2)
g.add_player(p3)
g.add_player(p4)
num_rounds = 10
g.start_game(num_rounds)
print("num rounds: ", num_rounds)
print(c1)
print([(player_id, g.balances[player_id]/num_rounds) for player_id in g.players])
print("--- %s seconds ---" % (time.time() - start_time))

# p1 = FiggieNewton("Figgie1", [3, 1, 0])
# # p1 = CardCounter("CC", [3.5, 1])
# # p1 = RandomPlayer("Random1")
# # p2 = MLEPlayer("MLEPlayer2")
# p2 = FiggieNewton("Figgie2", [3, 1, 2])
# # p2 = CardCounter("CC2", [3, 1])
# # p2 = RandomPlayer("Random2")
# # p3 = RandomPlayer("Random3")   
# p3 = MLEPlayer("MLEPlayer3")
# # p3 = FiggieNewton("Figgie3", [16, 1])
# # p3 = CardCounter("CC3", [1, 1]) 
# # p4 = RandomPlayer("Random4")
# p4 = MLEPlayer("MLEPlayer4")
# # p4 = FiggieNewton("Figgie4", [64, 1])
# # p4 = CardCounter("CC4", [3, 1])


# g = Game(show_messages=False)
# g.add_player(p1)
# g.add_player(p2)
# g.add_player(p3)
# g.add_player(p4)
# num_rounds = 1000
# g.start_game(num_rounds)
# print([(player_id, g.balances[player_id]/num_rounds) for player_id in g.players])
