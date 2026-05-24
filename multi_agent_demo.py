import random

from environment import GridEnvironment
from algorithms import bfs, dfs, astar
from maps import generate_random_map
from agent import Agent
from collision_controller import run_collision_avoidance_simulation


def create_agents_from_configs(environment, agent_configs):
    agents = []

    for config in agent_configs:
        agent = Agent(
            config["name"],
            config["start"],
            config["goal"],
            config["algorithm"]
        )

        agent.find_path(environment)

        if agent.path:
            agents.append(agent)
        else:
            print(f"{agent.name} could not find a path and was skipped.")

    return agents


def generate_random_agent_positions(grid, number_of_agents):
    rows = len(grid)
    cols = len(grid[0])

    free_cells = []

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                free_cells.append((row, col))

    random.shuffle(free_cells)

    required_cells = number_of_agents * 2

    if len(free_cells) < required_cells:
        raise ValueError("Not enough free cells for agents.")

    starts = free_cells[:number_of_agents]
    goals = free_cells[number_of_agents:required_cells]

    return starts, goals


def create_random_agents(grid, environment, number_of_agents):
    starts, goals = generate_random_agent_positions(
        grid,
        number_of_agents
    )

    algorithms = [astar, bfs, dfs]

    agent_configs = []

    for index in range(number_of_agents):
        agent_configs.append(
            {
                "name": f"Agent {index + 1}",
                "start": starts[index],
                "goal": goals[index],
                "algorithm": algorithms[index % len(algorithms)],
            }
        )

    agents = create_agents_from_configs(
        environment,
        agent_configs
    )

    return agents


def run_multi_agent_demo():
    number_of_agents = 3

    while True:
        random_map = generate_random_map(
            8,
            8,
            obstacle_probability=0.25
        )

        grid = random_map["grid"]

        environment = GridEnvironment(
            grid,
            random_map["start"],
            random_map["goal"]
        )

        agents = create_random_agents(
            grid,
            environment,
            number_of_agents
        )

        if len(agents) == number_of_agents:
            break

        print("Some agents could not find paths. Generating a new map...")

    run_collision_avoidance_simulation(
        environment,
        agents,
        "Random Multi-Agent Navigation with Collision Avoidance"
    )