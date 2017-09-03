from .mazeGenerator import MazeGenerator
from .mazeGenerator import Direction

import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('mazeEnvironment')

# Environment class are given an environment as an input.
# the main feature is that it contains the step function, described below
class MazeEnvironment():

    def __init__(self, height, width):
        self.maze = MazeGenerator(height, width)
        self.R, self.P, self.STA = self.maze.DFT()
        self.start_state = self.coordinates_to_state_number(self.maze.start_y, self.maze.start_x) # bad practice. Very similar attributes stored in different formats 
        self.goal_state  = self.coordinates_to_state_number(*self.maze.goal_state) # bad practice. Very similar attributes stored in different formats 

    # Takes a "step" in the sense that we take an action at a given state
    # returns the given state.
    # Params:
    #   - state: state at which action is going to be taken
    #   - action: action that is going to be taken
    def step(self, state, action):
        reward     = self.R[state][action.value]
        print("State {}. Reward {}".format(state, reward))
        if action == Direction.UP:    next_state = state - self.maze.width
        if action == Direction.DOWN:  next_state = state + self.maze.width
        if action == Direction.LEFT:  next_state = state - 1
        if action == Direction.RIGHT: next_state = state + 1
        done = self.get_goal_state() == next_state
        return next_state, reward, done

    
    # Resets the enviorment and returns the start state.
    def reset(self, exploring_start=False):
        if exploring_start: # updates starting state
            self.state_state = maze.set_start_state()
        return self.start_state
        
    # Initial state changes with exploring start
    def get_start_state(self):
        return self.start_state

    def get_goal_state(self):
        return self.goal_state

    # TODO: this function is duplicated from mazeGenerator
    # Given a 2D  coordinate, it calculates the state number.
    # i.e converts 2D array coordinate into 1D coordinate
    def coordinates_to_state_number(self,y,x):
        return self.maze.height*y + x
