# Autonomous Navigation Agent

A grid-based autonomous navigation system implemented in Python using BFS, DFS, and A* path planning algorithms. The project includes environment visualization, random map generation, multi-agent navigation, collision avoidance, and path replanning mechanisms.

---

## Features

* **Grid-Based Navigation:** Autonomous agent movement on discrete grids.
* **Path Planning:** Implementations of BFS, DFS, and A* search algorithms.
* **Procedural Generation:** Random and predefined map generation capabilities.
* **Multi-Agent Support:** Simultaneous multi-agent navigation.
* **Collision Avoidance System:** Advanced movement coordination to prevent asset collisions.
* **Dynamic Replanning:** Real-time path recalculation when deadlocks or blockages occur.
* **Data & Visualization:** Pygame-based GUI, Matplotlib performance comparison charts, CSV data export, and execution time analysis.

---

## Project Structure

```text
autonomous-navigation-agent/
│
├── agent.py
├── algorithms.py
├── collision_controller.py
├── environment.py
├── evaluation.py
├── experiments.py
├── main.py
├── maps.py
├── multi_agent_demo.py
├── visualizer.py
```
## Architecture Overview

The project is divided into modular components, each handling a specific domain of the system:

### 📄 `environment.py`
Implements the `GridEnvironment` class.
* **Responsibilities:** Environment representation, obstacle checking, boundary checking, neighbor generation, and movement validation.
* **Representation:** The grid environment is represented as a matrix where:
  * `0` → Free cell
  * `1` → Obstacle

### 📄 `algorithms.py`
Contains all path planning algorithms.
* **Algorithms:** BFS, DFS, and A* Search.
* **Responsibilities:** Pathfinding execution, visited node tracking, and final path reconstruction.

### 📄 `agent.py`
Implements the autonomous agent model.
* **Responsibilities:** Storing start and goal positions, selecting algorithms, path calculation, movement simulation, and path replanning.
* **Note:** Each agent can utilize a completely different path planning algorithm within the same map.

### 📄 `collision_controller.py`
Manages runtime coordination across multiple agents.
* **Responsibilities:** Multi-agent movement oversight, collision avoidance, deadlock detection, and path replanning triggers.
* **Safety Protocols:** The system actively prevents agents from occupying the same cell or performing position swapping (e.g., Agent A moving X→Y while Agent B moves Y→X). When agents become blocked, path replanning is instantly triggered.

### 📄 `visualizer.py`
Handles graphical visualization using Pygame.
* **Responsibilities:** Grid rendering, agent rendering, animation system updates, path visualization, and legend drawing.

### 📄 `maps.py`
Manages map configurations and layouts.
* **Predefined Maps:** Simple Map, Maze Map, Obstacle Dense Map, and Collision Test Map.
* **Procedural Generation:** Features a random map generation system to test arbitrary layout densities.

### 📄 `experiments.py`
Responsible for automated benchmarking.
* **Scenarios:** Runs core algorithm experiments, performance evaluations, collision avoidance scenarios, and random map stress-testing.
* **Metrics Tracked:** Path length, total visited nodes, and execution time.

### 📄 `evaluation.py`
Generates analytics and reporting data from experimental results.
* **Outputs:** Creates comparison charts, CSV exports, and performance plots using Matplotlib.

---

## Path Planning Algorithms

### Breadth-First Search (BFS)
* Explores the graph layer by layer (level order).
* Guarantees the shortest path on unweighted grids.
* **Characteristics:** Explores a large number of nodes before finding the target.

### Depth-First Search (DFS)
* Explores as deeply as possible along each branch before backtracking.
* May reach the goal quickly if the branching path favors the goal orientation.
* **Characteristics:** Does not guarantee the shortest path.

### A* Search Algorithm
* A heuristic-based, goal-oriented search algorithm.
* Generally explores significantly fewer nodes than BFS.
* **Characteristics:** Usually provides the best overall balance of performance and path optimality.

---

## Multi-Agent Navigation & Collision Avoidance

The project supports simultaneous navigation of multiple autonomous agents inside the same environment.

### Core Mechanics
* Random agent spawning generation.
* Independent algorithm selection per agent.
* Continuous deadlock detection and path replanning.

### Collision Scenarios Prevented
* **Same-Cell Collisions:** Two or more agents trying to step into identical coordinates at the same time step.
* **Swap Collisions:** Agent A moving from X→Y while Agent B tries to move from Y→X. The controller detects this overlap and pauses or diverts movement.

### Dynamic Replanning Function
When an agent becomes blocked by another agent's presence:
1. Other moving agents are temporarily flagged as static obstacles.
2. A new path is calculated from the current location to the original destination.
3. The agent resumes navigation smoothly using the newly calculated route, enhancing adaptability in tight, dynamic layouts.

---

## Performance Evaluation & Visualization

Experiments are systematically performed using predefined maps, randomly generated maps, collision test environments, and multi-agent simulations.

The following metrics are collected and evaluated:
* **Path Length:** Total steps taken to reach the destination.
* **Visited Nodes:** The algorithmic footprint and efficiency of map exploration.
* **Execution Time:** CPU runtime performance analyzed via the Python `time` module.

All gathered results are directly visualized using Matplotlib charts, exported to CSV files, and animated live through the Pygame visualization loop (showing explored cells, final paths, real-time replanning behavior, and agent interactions).

---

## Installation & Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/BesircanB/autonomous-navigation-agent.git
   cd autonomous-navigation-agent
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Project**
   ```bash
   python main.py
   ```

---

## Technologies Used

* **Core Language:** Python
* **Graphics & GUI:** Pygame
* **Data Visualizations:** Matplotlib
* **Standard Library Utilities:** `csv`, `time`, `random`

---

## Future Improvements

- [ ] Dynamic, moving obstacles (independent of agents).
- [ ] Support for irregular, continuous, or non-grid map structures.
- [ ] Adaptive algorithm selection (switching algorithms dynamically based on local clutter).
- [ ] Reinforcement learning integration for complex path prediction.
- [ ] Advanced multi-agent coordination (e.g., priority-based traffic assignment).
- [ ] Weighted movement costs for terrain variations.
- [ ] Diagonal movement support (8-way navigation connectivity).
