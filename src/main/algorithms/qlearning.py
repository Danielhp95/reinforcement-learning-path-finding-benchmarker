import sys
sys.path.append('..')
from tqdm import tqdm
import numpy as np
import random

from environments import mazeEnvironment

from rlutils import create_q_table, derive_policy_from_q_table

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('qlearning')


def Qlearning(environment, learning_rate=1e-2, number_of_episodes=2000):

    Q_table = create_q_table(environment)
    for _ in tqdm(range(number_of_episodes)):
        observation = environment.reset(exploring_start=True)
        done = False
        while not done:
            policy = derive_policy_from_q_table(Q_table)
            action = policy[observation] if np.random.uniform(0, 1) < 5e-2 else random.choice(environment.STA[observation])
            successor_obvservation, reward, done = environment.step(observation, action)
            Q_table[observation][action.value] = (1 - learning_rate) * Q_table[observation][action.value] + \
                                     learning_rate * (reward + environment.discount_factor * max([x for x in Q_table[successor_obvservation] if x is not None]))
            observation = successor_obvservation
    return Q_table


if __name__ == '__main__':
    random.seed(42)
    environment = mazeEnvironment.MazeEnvironment(height=3, width=3)
    logger.info('Environment initialized')
    Q_table = Qlearning(environment)
    logger.info('Q table: {}'.format(Q_table))
    logger.info('Policy: {}'.format(derive_policy_from_q_table(Q_table)))
