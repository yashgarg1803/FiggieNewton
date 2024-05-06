from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer
from agents.human import HumanPlayer
from agents.figgienewton import FiggieNewton
from agents.card_counter import CardCounter
from matplotlib import pyplot as plt
import FiggieNewton.learn as learn


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
        "initial": 1.5,
        "step_size": .2
    },
]

points = 50
y = []
x = []

x1 = []
y1 = []


# temp = learn.hill_climbing(FiggieNewton, [{"min": 0.0, "max": 2.0, "initial": .5, "step_size": .1}], iterations=30, num_rounds=40)
# for i in range(0, len(temp[1])):
#     y = temp[1]
#     x.append(i)
# plt.plot(x, y)
# plt.title("Hill Climb Scores")
# plt.xlabel("Iteration Number")
# plt.ylabel("Score")
# ax = plt.gca()
# plt.show()

for i in range(0, points):
    increment = 2.0 / points
    temp = learn1.hill_climbing(FiggieNewton, [{"min": 0.0, "max": 2.0, "initial": increment * i, "step_size": .2}], iterations=1, num_rounds=50)
    y.append(temp[0])
    x.append(i * increment)
    y1.append(temp[1])
    x1.append(i * increment)
a = plt.scatter(x, y, label="Converge")
a.ylim([0, 60])
plt.show()
b = plt.scatter(x1, y1, label="Profit Attained")
plt.show()

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