# Emergency Evacuation & Route Planner

A Python-based graph algorithms project that simulates an emergency evacuation network, finds routes between campus locations, visualizes algorithm execution, simulates road closures, and compares algorithm performance.

## Overview

The Emergency Evacuation & Route Planner models a campus as a weighted graph. Locations are represented by vertices, and roads are represented by weighted edges. Users select a starting location, destination, and pathfinding algorithm to explore how different algorithms find routes through the network.

The application is designed for educational use in Design and Analysis of Algorithms (DAA). It provides step-by-step algorithm visualization and a benchmark interface for comparing algorithm behavior.

## Features

- **Four pathfinding algorithms:** BFS, DFS, Dijkstra, and Bellman–Ford.
- **Interactive campus network:** Visualize locations and connecting roads.
- **Road closures:** Block and reopen roads to simulate disruptions.
- **Animated algorithm execution:** Step through recorded algorithm events with Play/Pause, Previous, Next, Restart, and playback-speed controls.
- **Decision explanations:** View edge examinations, node discoveries, and distance updates during execution.
- **Performance benchmarking:** Compare execution time, vertices explored, route availability, route cost, and recorded operation counts.
- **Automated tests:** Validate graph behavior, algorithm results, animation, visualization, and benchmarking.

## Implemented Algorithms

| Algorithm | Purpose | Time Complexity |
|---|---|---|
| Breadth-First Search (BFS) | Finds a route with the fewest edges in an unweighted graph | O(V + E) |
| Depth-First Search (DFS) | Explores paths depth-first and finds a valid route when one exists | O(V + E) |
| Dijkstra's Algorithm | Finds a minimum-cost route with non-negative edge weights | O((V + E) log V) with a binary heap |
| Bellman–Ford Algorithm | Finds minimum-cost routes and detects reachable negative-weight cycles | O(VE) |

Here, **V** is the number of vertices and **E** is the number of edges. The stated complexities are standard bounds; actual behavior depends on the implementation and graph representation.

### Important distinctions

- BFS minimizes the number of edges, not necessarily the total road cost.
- DFS does not guarantee a minimum-edge or minimum-cost route.
- Dijkstra requires non-negative edge weights.
- Bellman–Ford supports negative edge weights and can detect reachable negative-weight cycles.

## Technology Stack

- **Language:** Python
- **User interface:** Streamlit
- **Graph visualization:** Plotly
- **Testing:** pytest
- **Version control:** Git and GitHub

## Project Structure

```text
Emergency-Evacuation-Route-Planner/
├── app.py
├── src/
│   ├── graph.py
│   ├── bfs.py
│   ├── dfs.py
│   ├── dijkstra.py
│   ├── bellman_ford.py
│   ├── benchmark.py
│   ├── animation.py
│   └── visualization.py
├── tests/
│   ├── test_graph.py
│   ├── test_bfs.py
│   ├── test_dfs.py
│   ├── test_dijkstra.py
│   ├── test_bellman_ford.py
│   ├── test_animation.py
│   ├── test_visualization.py
│   └── test_benchmark.py
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/harshkdm31/Emergency-Evacuation-Route-Planner.git
cd Emergency-Evacuation-Route-Planner
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the project's required packages. Run:

```bash
pip install -r requirements.txt
```


## Running the Application

From the project root, run:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal by Streamlit.

### Using the application

1. Select a starting location and destination.
2. Choose BFS, DFS, Dijkstra, or Bellman–Ford.
3. Optionally block roads using the sidebar controls.
4. Inspect the calculated route and its cost.
5. Use the animation controls to examine the algorithm's execution.
6. Run the benchmark to compare the algorithms under the same graph and route configuration.

## Running Tests

Run the complete test suite from the project root:

```bash
python -m pytest -v
```

The tests cover graph operations, route finding, blocked roads, unreachable destinations, animation events, visualization, and benchmark behavior.

## Benchmarking

The benchmark runs each algorithm multiple times for the selected route and reports the median execution time to reduce the influence of individual timing fluctuations.

The benchmark interface includes:

- Execution time in milliseconds
- Vertices explored
- Edges examined through recorded `edge_check` events
- Successful distance relaxations recorded through `relax` events
- Total recorded algorithm events
- Whether a route was found and its path cost

**Interpreting the results:** event-based operation counts describe the events recorded by this implementation. They are useful for educational comparison but are not perfectly equivalent measures of computational work across all four algorithms. Execution time also includes the overhead of recording events.

## Limitations

- The application uses a predefined campus graph rather than live maps or GPS.
- Road costs are modeled as edge weights; real-world traffic and changing emergency conditions are not simulated.
- BFS optimizes the number of edges, whereas Dijkstra and Bellman–Ford optimize total path cost.
- Benchmark timings can vary with the execution environment and graph size.
- The application is an academic simulation, not a real-world emergency dispatch or navigation system.

## Future Improvements

Potential extensions include configurable graph generation, larger benchmark datasets, additional performance metrics, downloadable benchmark results, and support for more route-planning algorithms.
