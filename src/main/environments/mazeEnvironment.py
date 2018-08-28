from .mazeGenerator import MazeGenerator
from .mazeGenerator import Direction


# Environment class are given an environment as an input.
# the main feature is that it contains the step function, described below
class MazeEnvironment():

    def __init__(self, height, width, discount_factor=0.99):
        self.maze = MazeGenerator(height, width)
        self.discount_factor = discount_factor
        self.R, self.P, self.STA = self.maze.DFT()
        self.start_state = self.maze.coordinates_to_state_number(*self.maze.start_state) # bad practice. Very similar attributes stored in different formats
        self.goal_state  = self.maze.coordinates_to_state_number(*self.maze.goal_state) # bad practice. Very similar attributes stored in different formats
        self.num_states  = self.maze.num_states
        self.num_actions = self.maze.num_actions

    def step(self, state, action):
        '''
        Takes a "step" in the sense that we take an action at a given state
        returns the given state.
        :param state: state where action takes place
        :param action: action taken by the agent
        '''
        reward     = self.R[state][action.value]
        if action == Direction.UP:    next_state = state - self.maze.width
        if action == Direction.DOWN:  next_state = state + self.maze.width
        if action == Direction.LEFT:  next_state = state - 1
        if action == Direction.RIGHT: next_state = state + 1
        done = self.get_goal_state() == next_state
        return next_state, reward, done

    def reset(self, exploring_start=False):
        '''
        Returns the start state of the environment
        :param exploring_start: flag that determines if new start state is generated for this episode
        '''
        if exploring_start: # updates starting state
            self.start_state = self.maze.coordinates_to_state_number(*self.maze.generate_new_start_state())
        return self.start_state

    def get_goal_state(self):
        return self.goal_state
