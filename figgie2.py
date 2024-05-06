from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer
from agents.human import HumanPlayer
from agents.figgienewton import FiggieNewton
from agents.card_counter import CardCounter
from agents.mle import MLEPlayer
import learn


p1 = FiggieNewton("Figgie1", [3, 1, 1])
# p1 = CardCounter("CC", [3.5, 1])
# p1 = RandomPlayer("Random1")
# p2 = MLEPlayer("MLEPlayer2")
p2 = FiggieNewton("Figgie2", [3, 1, 0])
# p2 = CardCounter("CC2", [3, 1])
# p2 = RandomPlayer("Random2")
# p3 = RandomPlayer("Random3")   
p3 = MLEPlayer("MLEPlayer3")
# p3 = FiggieNewton("Figgie3", [16, 1])
# p3 = CardCounter("CC3", [1, 1]) 
# p4 = RandomPlayer("Random4")
p4 = MLEPlayer("MLEPlayer4")
# p4 = FiggieNewton("Figgie4", [64, 1])
# p4 = CardCounter("CC4", [3, 1])

g = Game(show_messages=False)
g.add_player(p1)
g.add_player(p2)
g.add_player(p3)
g.add_player(p4)
num_rounds = 100
g.start_game(num_rounds)
print([(player_id, g.balances[player_id]/num_rounds) for player_id in g.players])

g = Game(show_messages=False)
g.add_player(p1)
g.add_player(p2)
g.add_player(p3)
g.add_player(p4)
num_rounds = 1000
g.start_game(num_rounds)
print([(player_id, g.balances[player_id]/num_rounds) for player_id in g.players])
