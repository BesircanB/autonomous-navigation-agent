class Agent:
    def __init__(self, name, start, goal, algorithm):
        self.name = name
        self.start = start
        self.goal = goal
        self.algorithm = algorithm

        self.path = []
        self.visited = set()
        self.current_position = start

    def find_path(self, environment):
        original_start = environment.start
        original_goal = environment.goal

        environment.start = self.start
        environment.goal = self.goal

        self.path, self.visited = self.algorithm(environment)
        print(f"{self.name} path: {self.path}")

        if not self.path:
            print(f"{self.name} could not find a valid path.")

        environment.start = original_start
        environment.goal = original_goal

    def get_position_at_step(self, step):
        if not self.path:
            return self.start

        if step < len(self.path):
            return self.path[step]

        return self.path[-1]