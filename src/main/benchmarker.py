from algorithms import qlearning
from algorithms import sarsa
from algorithms import first_visit_monte_carlo
from algorithms import every_visit_monte_carlo
from maze_generator import MazeGenerator

from time import time

def benchmark_single(width, height):
    # Generate maze
    maze_creation_t0 = time()
    maze = MazeGenerator(height=height, width=width)
    R, P, STA = maze.DFT()
    maze_creation_t1 = time()
    time_maze_creation = maze_creation_t1 - maze_creation_t0
    print(time_maze_creation)

    #test algorithms

    qlearning_t0 = time()
    #algorithm
    qlearning_t1 = time()
    time_qlearning = qlearning_t1 - qlearning_t0

    sarsa_t0 = time()
    #algorithm
    sarsa_t1 = time()
    time_sarsa = sarsa_t1 - sarsa_t0

    first_visit_monte_carlo_t0 = time()
    #algorithm
    first_visit_monte_carlo_t1 = time()
    time_first_visit_monte_carlo = first_visit_monte_carlo_t1 - first_visit_monte_carlo_t0

    every_visit_monte_carlo_t0 = time()
    #algorithm
    every_visit_monte_carlo_t1 = time()
    time_every_visit_monte_carlo = every_visit_monte_carlo_t1 - every_visit_monte_carlo_t0

def benchmark_multiple():
    maximum_size = 10000
    step = 200
    initial = 200

    for size in range(initial, maximum_size, step):
        benchmark_single(size, size)


if __name__ == '__main__':
    benchmark_single(100,100)
    #benchmark_multiple()
