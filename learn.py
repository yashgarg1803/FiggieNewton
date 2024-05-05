from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer
from agents.human import HumanPlayer
from agents.figgie_newton import FiggieNewton
import copy
import random

TEST_SUITE = [
    {
        "name": "All Random",
        "players": [
            # FiggieNewton("testfiggie", [1, 1, 10]),
            RandomPlayer("R1"),
            RandomPlayer("R2"),
            RandomPlayer("R3"),
        ],
    }
]

def evaluate_player(player, num_rounds=100):
    sum = 0
    for test in TEST_SUITE:
        g = Game(show_messages=False)
        g.add_player(player)
        i = 2
        for test_class in test["players"]:
            g.add_player(test_class)
            i += 1
        g.start_game(num_rounds)
        sum += g.balances[player.player_id]
    score = sum / (len(TEST_SUITE) * num_rounds)
    return score

# parameters = min, max, initial, for each parameter
def hill_climbing(player_class, parameters, iterations=10, num_rounds=100):
    initial_parameters = []
    step_sizes = []
    for parameter in parameters:
        min = parameter["min"]
        max = parameter["max"]
        initial_parameters.append(random.uniform(min, max))
        step_sizes.append(parameter["step_size"])
    player = player_class("TEST PLAYER", initial_parameters)

    cur_score = evaluate_player(player, num_rounds)

    for i in range(iterations):
        print("Iteration: ", i, cur_score)
        print(initial_parameters)
        new_parameters = copy.deepcopy(initial_parameters)
        scores = []
        for j in range(0, len(new_parameters)):
            #step right for parameter j
            step_size = step_sizes[j]
            new_parameters[j] += step_size
            test_player1 = player_class("TEST PLAYER", new_parameters)
            test_score1 = evaluate_player(test_player1, num_rounds)
            if(test_score1 > cur_score):
                scores.append((test_score1, j, 1)) # tuple (score, parameter index, direction)
            new_parameters[j] -= step_size

            #step left for parameter j
            new_parameters[j] -= step_size
            test_player2 = player_class("TEST PLAYER", new_parameters)
            test_score2 = evaluate_player(test_player2, num_rounds)
            if(test_score2 > cur_score):
                scores.append((test_score2, j, -1))
            new_parameters[j] += step_size
        
        #simple hill climbing
        if(len(scores) > 0):
            sorted(scores, key=lambda x : x[0])
            best = scores[-1]  
            cur_score = best[0] 
            new_parameters[best[1]] += best[2] * step_sizes[best[1]]
            step_sizes[best[1]] *= 1.1

        else:
            cur_score = evaluate_player(player_class("TEST PLAYER", new_parameters), num_rounds)
            for j in range(0, len(step_sizes)):
                step_sizes[j] *= 0.9
        #stochastic version
        #best = random.choice(scores, weights=[x - cur_score for x in scores])
        
        
        initial_parameters = copy.deepcopy(new_parameters)
    
    print(cur_score)
    return initial_parameters     

