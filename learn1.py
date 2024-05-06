from engine.game import Game
from util.classes import Player
from util import constants
from agents.random import RandomPlayer
from agents.mle import MLEPlayer
from agents.human import HumanPlayer
from agents.figgienewton import FiggieNewton
from agents.card_counter import CardCounter
import copy
import random

TEST_SUITE = [
    {
        "name": "All Random",
        "players": [
            FiggieNewton("FiggieBlind", [0]),
            # CardCounter("CC1", [3, 1]),
            MLEPlayer("M2"),
            MLEPlayer("M3"),
        ],
    }
]

def evaluate_player(player, num_rounds=100):
    sum = 0
    sum2 = 0
    for test in TEST_SUITE:
        g = Game(show_messages=False)
        
        i = 2
        for test_class in test["players"]:
            g.add_player(test_class)
            i += 1
        g.add_player(player)
        g.start_game(num_rounds)
        sum += g.balances[player.player_id]
        sum2 += g.balances["FiggieBlind"]
    print("Figgie C:", player.c)
    print(sum2 / (len(TEST_SUITE) * num_rounds))
    score = sum / (len(TEST_SUITE) * num_rounds)
    print(score)
    return score

# parameters = min, max, initial, for each parameter
def hill_climbing(player_class, parameters, iterations=10, num_rounds=100):
    initial_parameters = []
    prev_diffs = {}
    step_sizes = []
    for parameter in parameters:
        tempmin = parameter["min"]
        tempmax = parameter["max"]
        initial = parameter["initial"]
        step_size = parameter["step_size"]
        initial_parameters.append(initial)
        step_sizes.append(step_size)
    player = player_class("TEST PLAYER", initial_parameters)

    cur_score = evaluate_player(player, num_rounds)

    for i in range(iterations):
        temperature = 1.0 - i / iterations
        print("Iteration: ", i, cur_score)
        print(initial_parameters)
        print("Steps Sizes: ")
        print(step_sizes)
        new_parameters = copy.deepcopy(initial_parameters)
        scores = []
        for j in range(0, len(new_parameters)):
            #step right for parameter j
            increment = min(parameters[j]["max"], new_parameters[j] + step_sizes[j]) - new_parameters[j]
            new_parameters[j] += increment
            test_player1 = player_class("TEST PLAYER", new_parameters)
            test_score1 = evaluate_player(test_player1, num_rounds)
            if(test_score1 > cur_score):
                scores.append((test_score1, j, 1, increment)) # tuple (score, parameter index, direction)
            new_parameters[j] -= increment

            #step left for parameter j
            decrement = new_parameters[j] - max(parameters[j]["min"], new_parameters[j] - step_sizes[j])
            new_parameters[j] -= decrement
            test_player2 = player_class("TEST PLAYER", new_parameters)
            test_score2 = evaluate_player(test_player2, num_rounds)
            if(test_score2 > cur_score):
                scores.append((test_score2, j, -1, decrement))
            new_parameters[j] += decrement
        
        #simple hill climbing
        if(len(scores) > 0):
            scores = sorted(scores, key=lambda x : x[0])
            best = scores[-1]  

            cur_diff = abs(best[0] - cur_score)
            cur_score = best[0] 
            new_parameters[best[1]] += best[2] * best[3]
            try:
                step_sizes[best[1]] *= abs(cur_diff/prev_diffs[best[1]])
            except:
                pass
            prev_diffs[best[1]] = cur_diff
        #stochastic version
        #best = random.choice(scores, weights=[x - cur_score for x in scores])
        # else:
        #     cur_score = evaluate_player(player_class("TEST PLAYER", new_parameters), num_rounds)
        
        initial_parameters = copy.deepcopy(new_parameters)
    
    print(cur_score)
    return initial_parameters     

