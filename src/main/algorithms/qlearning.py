import sys
sys.path.append('..')
import numpy as np
import random

from maze_generator import MazeGenerator
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('qlearning')


def has_converged(epsilon=1e-4):
    '''
    Convergence check with respect to epsilon threshold
    :param epsilon: convergence threshold
    '''
    pass


def create_q_matrix():
    '''
    Matrix representing action-value function Q(state, action)
    Initialized at zero, values will change throughout the algorithm.
    '''
    return np.zeros((number_of_states, number_of_actions))

def qlearning(R, P, STA, discount_factor, learning_rate, num_of_episodes=100):
    
    Q = create_q_matrix()
    episode = 0 # Current episode

    number_of_states = len(R)

    while episode < num_of_episodes:
        
        initial_state = random.randint(0, number_of_states - 1) 
        cur_state     = initial_state
        while not is_goal_reached(cur_state):
            action          = select_random_action_from_state(cur_state) #TODO: adapt
            successor_state = P[cur_state, action]

            Q[cur_state, action] = (1 - learning_rate) * Q[cur_state, action] + \
                                   learning_rate * (R[cur_state, action] + discount_factor * max(Q[successor_state, :]))
            cur_state = successor_state
        episode += 1
        if has_converged(Q, prev(Q)): break
    return episodes, Q
