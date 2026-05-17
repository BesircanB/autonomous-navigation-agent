import csv
import matplotlib.pyplot as plt


def plot_comparison(results, filename_prefix="comparison"):
    algorithm_names = [result["algorithm"] for result in results]
    path_lengths = [result["path_length"] for result in results]
    visited_nodes = [result["visited_nodes"] for result in results]
    execution_times = [result["execution_time"] for result in results]

    plt.figure()
    plt.bar(algorithm_names, path_lengths)
    plt.title("Path Length Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Path Length")
    plt.savefig(f"{filename_prefix}_path_length.png")
    plt.show()

    plt.figure()
    plt.bar(algorithm_names, visited_nodes)
    plt.title("Visited Nodes Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Visited Nodes")
    plt.savefig(f"{filename_prefix}_visited_nodes.png")
    plt.show()

    plt.figure()
    plt.bar(algorithm_names, execution_times)
    plt.title("Execution Time Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Execution Time (seconds)")
    plt.savefig(f"{filename_prefix}_execution_time.png")
    plt.show()


def save_results_to_csv(results, filename="results.csv"):
    with open(filename, mode="w", newline="") as file:
        fieldnames = ["map_name", "algorithm", "path_length", "visited_nodes", "execution_time"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for result in results:
            writer.writerow(result)