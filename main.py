from experiments import run_collision_avoidance_experiment, run_map_experiments, run_random_map_experiment
from multi_agent_demo import run_multi_agent_demo
from evaluation import save_results_to_csv


def main():
    all_results = []

    all_results.extend(run_map_experiments())
    all_results.extend(run_random_map_experiment())

    save_results_to_csv(all_results, "algorithm_results.csv")

    run_collision_avoidance_experiment()

    run_multi_agent_demo()


if __name__ == "__main__":
    main()