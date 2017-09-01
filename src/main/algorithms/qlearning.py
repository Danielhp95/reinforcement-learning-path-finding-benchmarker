import sys
sys.path.append('..')

from maze_generator import MazeGenerator
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('qlearning')

def has_converged():
    pass
    

# Matrix representing action-value function Q(state, action)
# Initialized at zero, values will change throughout the algorithm.
def create_q_matrix():
    return np.zeros((number_of_states, number_of_actions))

def qlearning(R, P, STA, discount_factor, learning_rate, num_of_episodes=100):
    
    Q = create_q_matrix()
    episode = 0 # Current episode

    while episode < num_of_episodes:
        
        initial_state = random.randint(0,number_of_states - 1) 
        cur_state     = initial_state
        while not is_goal_reached(cur_state):
            action          = select_random_action_from_state(cur_state) #TODO: adapt
            successor_state = P[cur_state, action]

            Q[cur_state, action] = R[cur_state, action] + d_f * max(Q[successor_state,:])
            cur_state = successor_state
        episode +=1
        if has_converged(Q,prev(Q)): break
    return episodes, Q

#MazeGenerator(heigth=10, width=10)
