import sys
sys.path.append('..')
import environments
from environments.mazeEnvironment import MazeEnvironment

from random import choice

import logging
logging.basicConfig(level=logging.debug)
logger = logging.getLogger("first_visit_MC")

# Calculates the return for the given state list.
# each element of that state list is (state, reward)
# Gamma is the discount factor
def get_return(state_list, gamma):
    pass


# Run an episode. Obtain the list of all states and rewards per state.
# Then go through every element of the state list and calculate the return for
# every state. Don't check again if the return state has already been seen.

# Run an episode starting at start_state.
# Params:
#   - envirnonment: contains a maze object containing:
#       - start_state: (initial_y, initial_x)
#       - goal_state: (end_y, end_x)
#       - STA: contains the list of actions for each state
#       - reward_matrix: matrix containing reward per state and action
def generate_episode(environment, policy):
    maximum_number_of_moves = 1000
    # Sequence of states and rewards format (state, reward)
    episode_list = list()
    
    observation  = environment.get_start_state()
    print("Start state {}".format(observation))
    print("Goal state {}".format(environment.get_goal_state()))
    for _ in range(0,maximum_number_of_moves):
        # Take action from policy for current state (observation)
        # we are currently only looking at RANDOM policy.
        action = choice(policy[observation]) 

        # Take_action and retrieve information 
        observation, reward, done = environment.step(observation, action)

        # Add move and reward to list
        episode_list.append((observation, reward, action.name))
        if done: break
    print("Episode {}".format('SUCCESS' if done else 'FAIL'))
    return episode_list
