import numpy as np
from random import shuffle, randrange, seed
from enum import Enum
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('maze_generator')


class Direction(Enum):
    UP  = 0
    DOWN = 1
    LEFT  = 2
    RIGHT = 3

    @staticmethod
    def find_oppposite(direction):
        if direction == Direction.UP: return Direction.DOWN
        if direction == Direction.DOWN: return Direction.UP
        if direction == Direction.RIGHT: return Direction.LEFT
        if direction == Direction.LEFT: return Direction.RIGHT


class MazeGenerator():

    def __init__(self, height=0, width=0):
        if height <= 0 and width <= 0:
            raise Exception('Heigth and width must be greater than zero, found: height {}, width {}'.format(height, width))
        self.height        = height
        self.width         = width
        self.num_states    = self.height * self.width
        self.num_actions   = len(Direction)

        # Rewards for valid actions
        self.normal_reward = 0
        self.goal_reward   = 1

        logger.debug("Height {}; Width {}".format(self.height, self.width))
        self.start_state = randrange(self.height), randrange(self.width)
        self.goal_state  = self.generate_new_goal_state()

    # TODO: think about a better way of assigning reward values.
    # Perhaps add at the end?. Look at all possible actions for every state
    # and give 0 (or small negative value) for non goal state and positive
    # value for goal state..
    # Perhaps  np.Nan for invalid moves.
    def initialize_reward_matrix(self):
        R = np.full((self.num_states, self.num_actions), -1)
        return R

    def initialize_transition_probability_matrix(self):
        P = np.zeros((self.num_states, self.num_states))
        return P

    # Used for policies, possible actions that can be taken per state.
    def initialize_possible_actions_per_state(self):
        state_to_actions = [[] for _ in range(0, self.num_states)]
        return state_to_actions

    def DFT(self):
        '''
        Creates a maze contained in a grid of space self.height ad self.width.
        The following matrices are also generated
          - R: Reward matrix. Reward for moving to invalid position is -1.
                              Reward for moving to valid position is
                              self.normal_reward and self.goal_reward for moving into goal
          - P: Transition probability matrix.
          - STA: valid actions for each state.
        '''
        within_bounds = lambda y, x: (x >= 0 and x < self.width) and (y >= 0 and y < self.height)
        is_valid_direction = lambda y, x, _: within_bounds(y, x) and not visited[y][x]

        # Initialize all variables
        visited = np.full((self.height, self.width), False)
        stack = [] # Used to calculate which state to visit next

        # Variables used in reinforcement learning
        R = self.initialize_reward_matrix()
        P = self.initialize_transition_probability_matrix()
        STA = self.initialize_possible_actions_per_state()

        # Start depth first traversal
        stack.append((self.start_state[0], self.start_state[1], None))

        logger.debug('Start state: {} {}'.format(*self.start_state))
        logger.debug('Goal  state: {} {}'.format(*self.goal_state))
        while len(stack) > 0:
            # New tile to explore. dirc represents the previous direction taken to come to this tile.
            y, x, dirc = stack.pop()
            if visited[y][x]: continue # Not necessary, but speeds up computation
            visited[y][x] = True


            # All possible directions that can be taken.
            directions = [(y+1, x, Direction.DOWN), (y, x+1, Direction.RIGHT),
                          (y-1, x, Direction.UP), (y, x-1, Direction.LEFT)]
            # Filter directions to the ones we can actually take
            valid_directions = [(y, x, d) for y, x, d in directions if is_valid_direction(y, x, d)]

            # Shuffling possible directions ensures random walk
            shuffle(valid_directions)
            # add directions to be explored later
            stack.extend(valid_directions)

            # Update reinforcement learning variables
            if dirc != None:
                # Previous and current states in 1D format
                prev_state_number = self.coordinates_to_state_number(prev_y, prev_x)
                state_number = self.coordinates_to_state_number(y, x)

                # Set reward for possible transitions
                R[prev_state_number][dirc.value] = self.normal_reward if (y, x) != self.goal_state else self.goal_reward
                R[state_number][Direction.find_oppposite(dirc).value] = self.normal_reward if (prev_y, prev_x) != self.goal_state else self.goal_reward

                # Add transition probability
                P[prev_state_number][state_number] = 1
                P[state_number][prev_state_number] = 1

                # Add action to possible actions
                STA[prev_state_number].append(dirc)
                STA[state_number].append(Direction.find_oppposite(dirc))

            prev_y, prev_x = y, x # End of iteration

        # Normalize matrix P
        P = self.normalize_matrix(P)
        # Set all variables as part of object
        return R, P, STA

    # Normalizes a matrix so that each row sums up to one.
    # TODO: check if this can be done in place
    def normalize_matrix(self, matrix):
        row_sums = matrix.sum(axis=1)
        return matrix / row_sums[:, np.newaxis]

    # Defines the goal states as a random state.
    # Goal state can never be the same as start state.
    def generate_new_goal_state(self):
        goal_y, goal_x = randrange(self.height), randrange(self.width)
        while self.start_state == (goal_y, goal_x):
            goal_y, goal_x = randrange(self.height), randrange(self.width)
        return (goal_y, goal_x)

    def generate_new_start_state(self):
        '''
        Sets a new start_state for the maze, which must differ from goal_state
        used when resetting the environment with 'exploring_start' flag
        '''
        start_y, start_x = randrange(self.height), randrange(self.width)
        while self.goal_state == (start_y, start_x):
            start_y, start_x = randrange(self.height), randrange(self.width)
        return (start_y, start_x)

    def coordinates_to_state_number(self, y, x):
        '''
        Given a 2D  coordinate, it calculates the state number.
        i.e converts 2D array coordinate into 1D coordinate
        :param x,y: grid-coordinates to be translated to 1D coordinates
        '''
        return y * self.width + x


if __name__ == '__main__':
    seed(42)
    m = MazeGenerator(height=2, width=3)
    R, P, STA = m.DFT()
