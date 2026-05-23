from environment import GridEnvironment
from algorithms import bfs, astar
from visualizer import animate_multiple_agents_with_collision_avoidance
from maps import generate_random_map
from agent import Agent


def run_multi_agent_demo():
    random_map = generate_random_map(8, 8, obstacle_probability=0.25)

    grid = random_map["grid"]

    agent1_start = (0, 0)
    agent1_goal = (7, 7)

    agent2_start = (7, 0)
    agent2_goal = (0, 7)

    important_positions = [
        agent1_start,
        agent1_goal,
        agent2_start,
        agent2_goal,
    ]

    for row, col in important_positions:
        grid[row][col] = 0

    multi_agent_environment = GridEnvironment(
        grid,
        random_map["start"],
        random_map["goal"]
    )

    agent1 = Agent(
        "Agent A",
        agent1_start,
        agent1_goal,
        astar
    )

    agent2 = Agent(
        "Agent B",
        agent2_start,
        agent2_goal,
        bfs
    )

    agent1.find_path(multi_agent_environment)
    agent2.find_path(multi_agent_environment)

    agents = [agent1, agent2]

    animate_multiple_agents_with_collision_avoidance(
        multi_agent_environment,
        agents,
        "Random Multi-Agent Navigation with Collision Avoidance"
    )