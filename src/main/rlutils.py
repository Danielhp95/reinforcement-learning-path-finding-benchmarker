
import sys
sys.path.append('..')

from environments import mazeEnvironment


def create_q_table(environment):
    '''
    Creates a Q table representing action-value function Q(state, action)
    Initialized at zero, values will change throughout the algorithm.
    :param environment:
    :returns: Q table where valid state-action paris are initialized to 0 and
              invalid ones are initialized to None.
    '''
    action_space_size = 4
    Q_table = [[0.0] * action_space_size for _ in range(environment.num_states)]
    for i in range(len(Q_table)):
        valid_action_values_for_state = list(map(lambda x: x.value, environment.STA[i]))
        for k in range(action_space_size):
            Q_table[i][k] = 0.0 if k in valid_action_values_for_state else None

    return Q_table


# TODO decouple this from mazeEnvironment
def derive_policy_from_q_table(Q_table):
    policy = [None] * len(Q_table)
    for state, action_values in enumerate(Q_table):
        policy[state] = mazeEnvironment.Direction(Q_table[state].index(max([x for x in Q_table[state] if x is not None])))
    return policy


def deterministic_random_policy(environment):
    '''
    Creates a deterministic policy that returns random actions
    for a given environment
    :param environment: Markov decision process that the policy will act on
    :returns: random mapping from environment states to actions
    '''
    return [random.choice(valid_actions) for valid_actions in environment.STA]
