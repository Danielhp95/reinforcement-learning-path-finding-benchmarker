import sys
sys.path.append('..')

from environments import mazeEnvironment

from rlutils import create_q_table, deterministic_random_policy

import numpy as np
import random

from tqdm import tqdm

import logging
logging.basicConfig(level=logging.info)
logger = logging.getLogger("Monte_carlo_for_control")


def get_return(remaining_episode, discount_factor):
    '''
    Calculates the discounted return for the remaining of the episode
    experience replay
    :param experience_replay: experience replay for the episode
    :param discount_factor: environment's discount factor
    :returns: discounted return for the remaining of episode
    '''
    returns = 0
    for i, (state, action, reward, successor_state) in enumerate(remaining_episode):
        returns += (discount_factor**i) * reward
    return returns


def generate_episode(environment, policy, maximum_number_of_moves=1000):
    '''
    Run an episode starting at start_state.
    :param environment: contains a maze object containing:
          - start_state: (initial_y, initial_x)
          - goal_state: (end_y, end_x)
          - STA: contains the list of actions for each state
          - reward_matrix: matrix containing reward per state and action
    :param maximum_number_of_moves: maximum number of moves to be carried out before ending episode
    :returns: experience replay for a newly generated episod with format (state, action, reward, state)
    '''
    experience_replay = []

    observation  = environment.reset(exploring_start=True)
    for current_step in range(maximum_number_of_moves):
        action = policy[observation] if np.random.uniform(0, 1) < 5e-2 else random.choice(environment.STA[observation]) # Carry out random action, soft greedy policy
        successor_obvservation, reward, done = environment.step(observation, action)          # Take_action and retrieve information
        experience_replay.append((observation, action.value, reward, successor_obvservation)) # Add move and reward to list
        observation = successor_obvservation
        if done: break
    return experience_replay


def update_Q_table(Q_table, experience_replay, discount_factor, every_visit):
    '''
    Updates the parameter Q_table to approximate the true Q table of the current policy
    :param Q_table: Q table being approximated for the current policy
    :param experience_replay: experience replay generated for the last completed episode
    :param discount_factor: discount factor of the MDP
    :param every_visit: flag to differentiate from first visit MC and every visit MC
    :returns: Closer approximation to true Q table for the current policy
    '''
    visited_states_action_pairs = []
    for i, experience in enumerate(experience_replay):
        state, action, reward, successor_state = experience

        if every_visit and (state, action) in visited_states_action_pairs:
                continue
        visited_states_action_pairs.append((state, action))

        return_after_state_action = get_return(experience_replay[i::], discount_factor)
        Q_table[state][action] = (Q_table[state][action] + return_after_state_action) / 2
    return Q_table


def policy_evaluation(environment, policy, every_visit, number_of_episodes=100):
    '''
    Approximates Q_table for :param: policy:
    :param environment: TODO
    :param policy TODO
    :param every_visit TODO
    :param num_of_episodes TODO
    :returns: Q_table for the parameter policy
    '''
    Q_table = create_q_table(environment)
    for episode in range(number_of_episodes):
        experience_replay = generate_episode(environment, policy)
        Q_table = update_Q_table(Q_table, experience_replay, environment.discount_factor, every_visit)
    return Q_table


def policy_improvement(Q_table, policy, epsilon=5e-1):
    '''
    Improves policy e-greedily with respect to Q_table
    :param Q_table:
    :param policy: mapping between states and actions
    :returns: e-greedily improved policy
    '''
    for state in range(len(Q_table)):
        if np.random.uniform(0, 1) > epsilon:
            e_greedy_best_action = max([x for x in Q_table[state] if x is not None])
        else:
            e_greedy_best_action = random.choice([x for x in Q_table[state] if x is not None])
        policy[state] = mazeEnvironment.Direction(Q_table[state].index(e_greedy_best_action)) # Turns action into an enum
    return policy


def monte_carlo_for_control(environment, every_visit=False, policy_evaluation_improvement_loop_iterations=100):
    '''
    Algorithm description:
    Run an episode. Obtain the list of all states and rewards per state.
    Then go through every element of the state list and calculate the return for
    every state. Don't check again if the return state has already been seen.

    Calculates Q*(s,a), the optimal Q table.
    The algorithm starts with a random policy, and performs
    e-greedy policy improvment
    :params every_visit: Flag to switch from every visit MC to first visit MC
    :returns: Approximated optimal policy and approximated Q table for said policy
    '''
    policy  = deterministic_random_policy(environment)
    for iteration in tqdm(range(policy_evaluation_improvement_loop_iterations)):
        Q_table = policy_evaluation(environment, policy, every_visit)
        policy  = policy_improvement(Q_table, policy)
    return Q_table, policy


if __name__ == '__main__':
    random.seed(42)
    environment = mazeEnvironment.MazeEnvironment(height=3, width=3)
    logger.info('Environment initialized')
    q_table, policy = monte_carlo_for_control(environment, every_visit=False)
    logger.info('Q table: {}'.format(q_table))
    logger.info('Policy: {}'.format(policy))
