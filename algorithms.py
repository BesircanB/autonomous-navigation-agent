from collections import deque
import heapq


def bfs(environment):
    start = environment.start
    goal = environment.goal

    queue = deque()
    queue.append(start)

    visited = set()
    visited.add(start)

    parent = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        neighbors = environment.get_neighbors(current)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

    path = reconstruct_path(parent, start, goal)

    return path, visited


def reconstruct_path(parent, start, goal):
    path = []

    current = goal

    while current != start:
        if current not in parent:
            return []

        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path

def dfs(environment):
    start = environment.start
    goal = environment.goal

    stack = [start]

    visited = set()
    visited.add(start)

    parent = {}

    while stack:
        current = stack.pop()

        if current == goal:
            break

        neighbors = environment.get_neighbors(current)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    path = reconstruct_path(parent, start, goal)

    return path, visited



def heuristic(a, b):
    row1, col1 = a
    row2, col2 = b

    return abs(row1 - row2) + abs(col1 - col2)


def astar(environment):
    start = environment.start
    goal = environment.goal

    open_list = []
    heapq.heappush(open_list, (0, start))

    visited = set()

    parent = {}

    g_cost = {}
    g_cost[start] = 0

    while open_list:
        current_f_cost, current = heapq.heappop(open_list)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            break

        neighbors = environment.get_neighbors(current)

        for neighbor in neighbors:
            new_cost = g_cost[current] + 1

            if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                g_cost[neighbor] = new_cost

                h_cost = heuristic(neighbor, goal)
                f_cost = new_cost + h_cost

                parent[neighbor] = current
                heapq.heappush(open_list, (f_cost, neighbor))

    path = reconstruct_path(parent, start, goal)

    return path, visited