import numpy as np
from random import shuffle, randrange
from enum import Enum

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

    def __init__(self, heigth=0, width=0):
        if heigth <= 0 and width <= 0:
            raise Exception('Heigth and width must be greater than zero, found: heigth {}, width {}'.format(heigth,width))
        self.heigth        = heigth
        self.width         = width
        self.num_states = heigth * width
        self.num_actions   = len(Direction)

    def initialize_reward_matrix(self):
        R = np.full((self.num_states, self.num_actions), -1)
        return R

    def initialize_transition_probability_matrix(self):
        P = np.zeros((self.num_states, self.num_states))
        return P
    
    # Will need to convert from 2D coordinate to state number
    def initialize_possible_actions_per_state(self):
        state_to_actions = [[]] * self.num_states
        return state_to_actions 

    # Carve maze.
    def DFT(self):
        within_bounds = lambda y,x: (x >= 0 and x < self.width) and (y >= 0 and y < self.heigth)
        is_valid_direction = lambda y,x,_: within_bounds(y,x) and not visited[y][x]
        


        # Initialize all variables
        visited = np.full((self.heigth, self.width), False)
        stack = [] # Used to calculate which state to visit next

        start_y, start_x = randrange(self.heigth), randrange(self.width)
        goal_state = self.set_goal_state(start_y, start_x)

        # Variables used in reinforcement learning
        R = self.initialize_reward_matrix()
        P = self.initialize_transition_probability_matrix()
        STA = self.initialize_possible_actions_per_state()

        # Start depth first traversal
        stack.append((start_y, start_x, None))
        print('Start state: {} {}'.format(start_y,start_x))
        print('Goal  state: {} {}'.format(*goal_state))
        while len(stack) > 0:
            print()
            y, x, dirc = stack.pop()
            if visited[y][x]: continue

            print("We have gone {}".format(dirc))
            visited[y][x] = True
            print(visited)
            directions = [(y+1,x,Direction.DOWN),(y,x+1,Direction.RIGHT),
                          (y-1,x,Direction.UP),(y,x-1,Direction.LEFT)]

            valid_directions = [(y,x,d) for y,x,d in directions if is_valid_direction(y,x,d)]

            # Shuffling possible directions ensures random walk
            shuffle(valid_directions)
            stack.extend(valid_directions)

            # Update reinforcement learning variables
            if dirc != None:
                prev_state_number = self.coordinates_to_state_number(prev_y,prev_x)
                state_number = self.coordinates_to_state_number(y,x)

                # Set reward for possible transitions
                print(prev_dirc)
                R[prev_state_number][dirc.value] = 0 if (y,x) != goal_state else 5
                R[state_number][Direction.find_oppposite(dirc).value] = 0 if (prev_y,prev_x) != goal_state else 5

                # Add transition probability

                # Add action to possible actions
                pass
            

            prev_y, prev_x, prev_dirc = y, x, dirc # End of iteration
        return R

    # Defines the goal states as a random state.
    # Goal state can never be the same as start state.
    def set_goal_state(self, start_y, start_x):
        goal_y, goal_x = randrange(self.heigth),randrange(self.width)
        while (start_y, start_x) == (goal_y, goal_x):
            goal_y, goal_x = randrange(self.heigth),randrange(self.width)
        return (goal_y, goal_x)

    # Given a 2D  coordinate, it calculates the state number.
    # i.e converts 2D array coordinate into 1D coordinate
    def coordinates_to_state_number(self,y,x):
        return self.heigth*y + x

if __name__ == '__main__':
    m = MazeGenerator(heigth=3, width=3)
    R = m.DFT()
    print()
    print("R: U,D,L,R")
    for l in R:
        print(l)
