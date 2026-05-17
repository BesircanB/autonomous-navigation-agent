import pygame


CELL_SIZE = 80
PURPLE = (180, 100, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
GREEN = (80, 200, 120)
RED = (220, 80, 80)
BLUE = (100, 160, 255)
YELLOW = (255, 220, 100)
GRAY = (180, 180, 180)


def draw_grid(screen, environment, path=None, visited=None):
    if path is None:
        path = []

    if visited is None:
        visited = set()

    for row in range(environment.rows):
        for col in range(environment.cols):
            position = (row, col)

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            color = WHITE

            if environment.grid[row][col] == 1:
                color = BLACK

            if position in visited:
                color = BLUE

            if position in path:
                color = YELLOW

            if position == environment.start:
                color = GREEN

            if position == environment.goal:
                color = RED

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)


def draw_legend(screen, environment, title):
    font = pygame.font.SysFont("Arial", 22)

    y = environment.rows * CELL_SIZE + 15

    title_text = font.render(title, True, BLACK)
    screen.blit(title_text, (20, y))

    legend_items = [
        ("Start", GREEN),
        ("Goal", RED),
        ("Obstacle", BLACK),
        ("Visited", BLUE),
        ("Path", YELLOW),
    ]

    x = 20
    y += 45

    for label, color in legend_items:
        pygame.draw.rect(screen, color, (x, y, 25, 25))
        text = font.render(label, True, BLACK)
        screen.blit(text, (x + 35, y))
        x += 140


def visualize(environment, path, visited, title="Autonomous Navigation"):
    pygame.init()

    width = environment.cols * CELL_SIZE
    height = environment.rows * CELL_SIZE + 120

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_grid(screen, environment, path, visited)
        draw_legend(screen, environment, title)

        pygame.display.flip()

    pygame.quit()


def animate_search(environment, path, visited, title="Search Animation"):
    pygame.init()

    width = environment.cols * CELL_SIZE
    height = environment.rows * CELL_SIZE + 120

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    visited_list = list(visited)
    visible_visited = set()

    running = True
    index = 0
    show_path = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if index < len(visited_list):
            visible_visited.add(visited_list[index])
            index += 1
        else:
            show_path = True

        screen.fill(WHITE)

        if show_path:
            draw_grid(screen, environment, path, visible_visited)
        else:
            draw_grid(screen, environment, [], visible_visited)

        draw_legend(screen, environment, title)

        pygame.display.flip()
        clock.tick(4)

    pygame.quit()


def animate_multiple_agents(environment, agents, title="Multi-Agent System"):
    pygame.init()

    width = environment.cols * CELL_SIZE
    height = environment.rows * CELL_SIZE + 120

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    running = True

    max_steps = max(len(agent.path) for agent in agents)

    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        draw_grid(screen, environment)

        colors = [PURPLE, ORANGE]

        for index, agent in enumerate(agents):
            if step < len(agent.path):
                row, col = agent.path[step]
            else:
                row, col = agent.path[-1]

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, colors[index], rect)

        draw_legend(screen, environment, title)

        pygame.display.flip()

        if step < max_steps - 1:
            step += 1

        clock.tick(2)

    pygame.quit()

def animate_multiple_agents_with_collision_avoidance(environment, agents, title="Collision Avoidance"):
    pygame.init()

    width = environment.cols * CELL_SIZE
    height = environment.rows * CELL_SIZE + 120

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    colors = [PURPLE, ORANGE, GREEN, RED]

    max_steps = max(len(agent.path) for agent in agents)

    agent_positions = {agent.name: agent.start for agent in agents}

    running = True
    step = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        desired_positions = {}

        for agent in agents:
            desired_positions[agent.name] = agent.get_position_at_step(step)

        occupied_positions = set()
        new_positions = {}

        for agent in agents:
            desired_position = desired_positions[agent.name]

            if desired_position in occupied_positions:
                new_positions[agent.name] = agent_positions[agent.name]
            else:
                new_positions[agent.name] = desired_position
                occupied_positions.add(desired_position)

        agent_positions = new_positions

        screen.fill(WHITE)
        draw_grid(screen, environment)

        for index, agent in enumerate(agents):
            row, col = agent_positions[agent.name]

            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            pygame.draw.rect(screen, colors[index % len(colors)], rect)

        draw_legend(screen, environment, title)

        pygame.display.flip()

        if step < max_steps - 1:
            step += 1

        clock.tick(2)

    pygame.quit()