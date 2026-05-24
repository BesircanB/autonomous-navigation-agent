
import pygame

from visualizer import get_window_size, handle_quit_events, draw_multi_agent_frame


def get_desired_positions(agents, agent_positions, path_indices):
    desired_positions = {}

    for agent in agents:
        current_index = path_indices[agent.name]
        next_index = current_index + 1

        if agent.path and next_index < len(agent.path):
            desired_positions[agent.name] = agent.path[next_index]
        else:
            desired_positions[agent.name] = agent_positions[agent.name]

    return desired_positions


def has_collision(agent, agents, agent_positions, desired_positions):
    agent_name = agent.name
    current_position = agent_positions[agent_name]
    desired_position = desired_positions[agent_name]

    for other_agent in agents:
        other_name = other_agent.name

        if other_name == agent_name:
            continue

        other_current = agent_positions[other_name]
        other_desired = desired_positions[other_name]

        same_cell_collision = desired_position == other_desired

        swap_collision = (
            desired_position == other_current
            and other_desired == current_position
        )

        if same_cell_collision or swap_collision:
            return True

    return False


def move_agents(agents, agent_positions, desired_positions, path_indices):
    new_positions = {}
    moved_any_agent = False

    for agent in agents:
        agent_name = agent.name

        current_position = agent_positions[agent_name]
        desired_position = desired_positions[agent_name]

        collision_detected = has_collision(
            agent,
            agents,
            agent_positions,
            desired_positions
        )

        if collision_detected:
            print(f"Collision avoided: {agent_name} waited at {current_position}")
            new_positions[agent_name] = current_position
        else:
            new_positions[agent_name] = desired_position

            if desired_position != current_position:
                path_indices[agent_name] += 1
                moved_any_agent = True

    return new_positions, path_indices, moved_any_agent


def replan_second_agent_if_stuck(
    environment,
    agents,
    agent_positions,
    path_indices
):
    for agent in agents[1:]:
        current_position = agent_positions[agent.name]

        blocked_positions = []

        for other_agent in agents:
            if other_agent.name != agent.name:
                blocked_positions.append(
                    agent_positions[other_agent.name]
                )

        agent.replan_path_with_temporary_obstacles(
            environment,
            current_position,
            blocked_positions
        )

        path_indices[agent.name] = 0

        print(f"{agent.name} new path: {agent.path}")

    return path_indices


def all_agents_reached_goals(agents, agent_positions):
    for agent in agents:
        if agent_positions[agent.name] != agent.goal:
            return False

    return True


def run_collision_avoidance_simulation(environment, agents, title="Collision Avoidance"):
    pygame.init()

    width, height = get_window_size(environment)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    agent_positions = {agent.name: agent.start for agent in agents}
    path_indices = {agent.name: 0 for agent in agents}

    stuck_counter = 0
    replanning_attempts = 0
    max_replanning_attempts = 3
    max_stuck_steps = 3

    running = True

    # Show initial starting positions before movement begins
    draw_multi_agent_frame(
        screen,
        environment,
        agents,
        agent_positions,
        title
    )

    pygame.time.delay(1000)

    while running:
        running = handle_quit_events()

        desired_positions = get_desired_positions(
            agents,
            agent_positions,
            path_indices
        )

        agent_positions, path_indices, moved_any_agent = move_agents(
            agents,
            agent_positions,
            desired_positions,
            path_indices
        )

        if moved_any_agent:
            stuck_counter = 0
        else:
            stuck_counter += 1

        if stuck_counter >= max_stuck_steps and replanning_attempts < max_replanning_attempts:
            print("Agents are stuck. Re-planning paths...")

            path_indices = replan_second_agent_if_stuck(
                environment,
                agents,
                agent_positions,
                path_indices
            )

            replanning_attempts += 1
            stuck_counter = 0

        elif stuck_counter >= max_stuck_steps and replanning_attempts >= max_replanning_attempts:
            print("Deadlock detected after re-planning. Simulation stopped.")
            running = False

        draw_multi_agent_frame(
            screen,
            environment,
            agents,
            agent_positions,
            title
        )

        if all_agents_reached_goals(agents, agent_positions):
            print("All agents reached their goals.")

            draw_multi_agent_frame(
                screen,
                environment,
                agents,
                agent_positions,
                title,
                show_paths=True
            )

            pygame.time.delay(5000)
            running = False

        clock.tick(1)

    pygame.quit()