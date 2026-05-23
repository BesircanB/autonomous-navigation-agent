import random

from environment import GridEnvironment
from algorithms import astar


maps = {
    "Simple Map": {
        "grid": [
            [0, 0, 0, 1, 0],
            [1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ],
        "start": (0, 0),
        "goal": (4, 4),
    },

    "Maze Map": {
        "grid": [
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0],
        ],
        "start": (0, 0),
        "goal": (5, 5),
    },

    "Obstacle Dense Map": {
        "grid": [
            [0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0],
            [1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
        ],
        "start": (0, 0),
        "goal": (5, 5),
    },
}


def generate_random_map(rows, cols, obstacle_probability=0.25, max_attempts=100):
    for _ in range(max_attempts):
        grid = []

        for row in range(rows):
            grid_row = []

            for col in range(cols):
                if random.random() < obstacle_probability:
                    grid_row.append(1)
                else:
                    grid_row.append(0)

            grid.append(grid_row)

        start = (0, 0)
        goal = (rows - 1, cols - 1)

        grid[start[0]][start[1]] = 0
        grid[goal[0]][goal[1]] = 0

        environment = GridEnvironment(grid, start, goal)
        path, visited = astar(environment)

        if path:
            return {
                "grid": grid,
                "start": start,
                "goal": goal,
            }

    raise ValueError("Could not generate a valid random map.")