Agents:

Agents perform actions through returning an action through get_action.
They receive information from the controller (game.py) through send_update.action

Game:

All the functions of the game are contained in the game.py file.

Learning:

learn.py contains the hillclimbing implementation. To try testing against specific sets of agents, you can add to the Test_Suite
defined in learn.py. To run the hillclimbing, you can run figgie_part1.py, and modify the parameters as you see fit.

To compare how the FiggieNewton does with the hillclimbed variables, you can run figgie_part2.py.