import time

from environment import GridEnvironment
from algorithms import bfs, dfs, astar
from visualizer import animate_search
from evaluation import plot_comparison
from maps import maps, generate_random_map


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
    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("A*", astar),
    ]

    results = []
    paths = {}

    for algorithm_name, algorithm_function in algorithms:
        result, path, visited = run_single_algorithm(
            environment,
            algorithm_function,
            algorithm_name,
            map_name
        )

        results.append(result)
        paths[algorithm_name] = (path, visited)

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


def run_experiment_for_map(map_name, map_data):
    environment = GridEnvironment(
        map_data["grid"],
        map_data["start"],
        map_data["goal"]
    )

    results, paths = run_algorithms(environment, map_name)

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

    print_results(map_name, results)
    plot_comparison(results, filename_prefix=map_name.replace(" ", "_").lower())

    return results


def run_map_experiments():
    all_results = []

    for map_name, map_data in maps.items():
        results = run_experiment_for_map(map_name, map_data)
        all_results.extend(results)

    return all_results


def run_random_map_experiment():
    random_map = generate_random_map(8, 8, obstacle_probability=0.25)

    results = run_experiment_for_map("Random Map", random_map)

    return results