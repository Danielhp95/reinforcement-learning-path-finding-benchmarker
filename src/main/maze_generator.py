import numpy as np
from random import shuffle, randrange
from enum import Enum

class Directions(Enum):
    UP  = 0
    DOWN = 1
    LEFT  = 2
    RIGHT = 3

class MazeGenerator():

    def __init__(self, heigth=0, width=0):
        if heigth <= 0 and width <= 0:
            raise Exception('Heigth and width must be greater than zero, found: heigth {}, width {}'.format(heigth,width))
        self.heigth        = heigth
        self.width         = width
        self.num_states = heigth * width
        self.num_actions   = len(Directions)

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
        print(visited)
        stack = [] # Used to calculate which state to visit next

        start_y, start_x = randrange(self.heigth), randrange(self.width)

        # Variables used in reinforcement learning
        R = self.initialize_reward_matrix()
        P = self.initialize_transition_probability_matrix()
        STA = self.initialize_possible_actions_per_state()

        # Start depth first traversal
        stack.append((start_y, start_x, None))
        print('{} {}'.format(start_x,start_y))
        while len(stack) > 0:
            print()
            y, x, dirc = stack.pop()
            if visited[y][x]: continue

            print("We have gone {}".format(dirc))
            visited[y][x] = True
            print(visited)
            directions = [(y+1,x,Directions.DOWN),(y,x+1,Directions.RIGHT),
                          (y-1,x,Directions.UP),(y,x-1,Directions.LEFT)]

            valid_directions = [(y,x,d) for y,x,d in directions if is_valid_direction(y,x,d)]

            print(valid_directions)
            
            shuffle(valid_directions)
            stack.extend(valid_directions)



    # TODO: not implemented
    def state_number_to_coordinates(self,state_num):
        return (-1,-1)


    def coordinates_to_state_number(self,y,x):
        return self.heigth*y + x

if __name__ == '__main__':
    m = MazeGenerator(heigth=3, width=3)
    m.DFT()
    print("Boop")
