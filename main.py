import time

from environment import GridEnvironment
from algorithms import bfs, dfs, astar
from visualizer import animate_search, animate_multiple_agents_with_collision_avoidance
from evaluation import plot_comparison, save_results_to_csv
from maps import maps
from agent import Agent
from random_map import generate_random_map


all_results = []


def run_single_algorithm(environment, algorithm_function, algorithm_name, map_name):
    start_time = time.perf_counter()

    path, visited = algorithm_function(environment)

    end_time = time.perf_counter()
    execution_time = end_time - start_time

    result = {
        "map_name": map_name,
        "algorithm": algorithm_name,
        "path_length": len(path),
        "visited_nodes": len(visited),
        "execution_time": execution_time,
    }

    return result, path, visited


def run_algorithms(environment, map_name):
    bfs_result, bfs_path, bfs_visited = run_single_algorithm(environment, bfs, "BFS", map_name)
    dfs_result, dfs_path, dfs_visited = run_single_algorithm(environment, dfs, "DFS", map_name)
    astar_result, astar_path, astar_visited = run_single_algorithm(environment, astar, "A*", map_name)

    results = [
        bfs_result,
        dfs_result,
        astar_result,
    ]

    paths = {
        "BFS": (bfs_path, bfs_visited),
        "DFS": (dfs_path, dfs_visited),
        "A*": (astar_path, astar_visited),
    }

    return results, paths


def print_results(map_name, results):
    print(f"\n--- {map_name} ---")
    print("Algorithm | Path Length | Visited Nodes | Execution Time")
    print("--------------------------------------------------------")

    for result in results:
        print(
            f"{result['algorithm']:<9} | "
            f"{result['path_length']:<11} | "
            f"{result['visited_nodes']:<13} | "
            f"{result['execution_time']:.6f} sec"
        )


def run_map_experiments():
    for map_name, map_data in maps.items():
        environment = GridEnvironment(
            map_data["grid"],
            map_data["start"],
            map_data["goal"]
        )

        results, paths = run_algorithms(environment, map_name)

        all_results.extend(results)

        print_results(map_name, results)
        plot_comparison(results, filename_prefix=map_name.replace(" ", "_").lower())

        for algorithm_name, data in paths.items():
            path, visited = data

            if path:
                animate_search(
                    environment,
                    path,
                    visited,
                    f"{map_name} - {algorithm_name}"
                )
            else:
                print(f"{algorithm_name} could not find a path in {map_name}.")


def run_random_map_experiment():
    random_map = generate_random_map(8, 8, obstacle_probability=0.25)

    random_environment = GridEnvironment(
        random_map["grid"],
        random_map["start"],
        random_map["goal"]
    )

    map_name = "Random Map"

    results, paths = run_algorithms(random_environment, map_name)

    all_results.extend(results)

    print_results(map_name, results)
    plot_comparison(results, filename_prefix="random_map")

    for algorithm_name, data in paths.items():
        path, visited = data

        if path:
            animate_search(
                random_environment,
                path,
                visited,
                f"Random Map - {algorithm_name}"
            )
        else:
            print(f"{algorithm_name} could not find a path in Random Map.")


def run_multi_agent_demo():
    random_map = generate_random_map(8, 8, obstacle_probability=0.25)

    multi_agent_environment = GridEnvironment(
        random_map["grid"],
        random_map["start"],
        random_map["goal"]
    )

    agent1 = Agent(
        "Agent A",
        (0, 0),
        (7, 7),
        astar
    )

    agent2 = Agent(
        "Agent B",
        (7, 0),
        (0, 7),
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


def main():
 #   run_map_experiments()
  #  run_random_map_experiment()

   # save_results_to_csv(all_results, "algorithm_results.csv")

    run_multi_agent_demo()


if __name__ == "__main__":
    main()