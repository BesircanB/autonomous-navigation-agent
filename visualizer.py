import pygame

CELL_SIZE = 80
LEGEND_HEIGHT = 170
MIN_WINDOW_WIDTH = 760

PURPLE = (180, 100, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
GREEN = (80, 200, 120)
RED = (220, 80, 80)
BLUE = (100, 160, 255)
YELLOW = (255, 220, 100)
GRAY = (180, 180, 180)


def get_window_size(environment):
    grid_width = environment.cols * CELL_SIZE
    grid_height = environment.rows * CELL_SIZE

    width = max(grid_width, MIN_WINDOW_WIDTH)
    height = grid_height + LEGEND_HEIGHT

    return width, height


def draw_grid(screen, environment, path=None, visited=None, show_start_goal=True):
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

            if show_start_goal:
                if position == environment.start:
                    color = GREEN
                elif position == environment.goal:
                    color = RED



            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)


def draw_legend(screen, environment, title):
    font_title = pygame.font.SysFont("Arial", 24)
    font = pygame.font.SysFont("Arial", 20)

    y = environment.rows * CELL_SIZE + 20

    title_text = font_title.render(title, True, BLACK)
    screen.blit(title_text, (25, y))

    legend_items = [
        ("Start", GREEN),
        ("Goal", RED),
        ("Obstacle", BLACK),
        ("Visited", BLUE),
        ("Path", YELLOW),
    ]

    x = 25
    y += 55

    for index, (label, color) in enumerate(legend_items):
        if index == 3:
            x = 25
            y += 50

        pygame.draw.rect(screen, color, (x, y, 25, 25))
        text = font.render(label, True, BLACK)
        screen.blit(text, (x + 35, y))

        x += 180


def handle_quit_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True


def draw_agent(screen, agent, position, color):
    row, col = position

    rect = pygame.Rect(
        col * CELL_SIZE,
        row * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )

    pygame.draw.rect(screen, color, rect)

    font = pygame.font.SysFont("Arial", 18)
    agent_label = font.render(agent.name[-1], True, BLACK)

    screen.blit(
        agent_label,
        (col * CELL_SIZE + 30, row * CELL_SIZE + 25)
    )


def visualize(environment, path, visited, title="Autonomous Navigation"):
    pygame.init()

    width, height = get_window_size(environment)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    running = True

    while running:
        running = handle_quit_events()

        screen.fill(WHITE)

        draw_grid(screen, environment, path, visited)
        draw_legend(screen, environment, title)

        pygame.display.flip()

    pygame.quit()


def animate_search(environment, path, visited, title="Search Animation"):
    pygame.init()

    width, height = get_window_size(environment)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    visited_list = list(visited)
    visible_visited = set()

    running = True
    index = 0
    show_path = False

    while running:
        running = handle_quit_events()

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

    width, height = get_window_size(environment)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    colors = [PURPLE, ORANGE, GREEN, RED]

    max_steps = max(len(agent.path) for agent in agents)
    step = 0
    running = True

    while running:
        running = handle_quit_events()

        screen.fill(WHITE)
        draw_grid(screen, environment)

        for index, agent in enumerate(agents):
            if step < len(agent.path):
                position = agent.path[step]
            else:
                position = agent.path[-1]

            draw_agent(
                screen,
                agent,
                position,
                colors[index % len(colors)]
            )

        draw_legend(screen, environment, title)

        pygame.display.flip()

        if step < max_steps - 1:
            step += 1

        clock.tick(2)

    pygame.quit()


def draw_multi_agent_frame(screen, environment, agents, agent_positions, title, show_paths=False):
    colors = [PURPLE, ORANGE, GREEN, RED]

    screen.fill(WHITE)

    # Draw base grid without environment start/goal colors
    draw_grid(screen, environment, show_start_goal=False)

    # Draw paths only when show_paths=True
    if show_paths:
        for index, agent in enumerate(agents):
            path_color = colors[index % len(colors)]

            for row, col in agent.path:
                path_rect = pygame.Rect(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(screen, path_color, path_rect)
                pygame.draw.rect(screen, GRAY, path_rect, 1)

    # Draw each agent's goal
    for index, agent in enumerate(agents):
        goal_row, goal_col = agent.goal
        goal_color = colors[index % len(colors)]

        goal_rect = pygame.Rect(
            goal_col * CELL_SIZE,
            goal_row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )

        pygame.draw.rect(screen, goal_color, goal_rect)
        pygame.draw.rect(screen, GRAY, goal_rect, 1)

        font = pygame.font.SysFont("Arial", 18)
        goal_label = font.render(f"G{index + 1}", True, BLACK)

        screen.blit(
            goal_label,
            (goal_col * CELL_SIZE + 20, goal_row * CELL_SIZE + 25)
        )

    # Draw current agent positions on top
    for index, agent in enumerate(agents):
        draw_agent(
            screen,
            agent,
            agent_positions[agent.name],
            colors[index % len(colors)]
        )

    draw_legend(screen, environment, title)

    pygame.display.flip()