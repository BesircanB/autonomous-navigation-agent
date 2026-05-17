class GridEnvironment:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows = len(grid)
        self.cols = len(grid[0])

    def is_inside_grid(self, position):
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_obstacle(self, position):
        row, col = position
        return self.grid[row][col] == 1

    def is_valid_position(self, position):
        return self.is_inside_grid(position) and not self.is_obstacle(position)

    def get_neighbors(self, position):
        row, col = position

        possible_moves = [
            (row - 1, col),  # up
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1),  # right
        ]

        valid_neighbors = []

        for move in possible_moves:
            if self.is_valid_position(move):
                valid_neighbors.append(move)

        return valid_neighbors