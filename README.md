# Emergency-Evacuation-Route-Planner
A Python-based emergency route planner using graph algorithms to find and visualize routes, simulate blocked roads, and compare algorithm performance.


## Implemented Algorithms

The project currently includes four graph algorithms:

- **Breadth-First Search (BFS):** Finds a route with the fewest edges.
- **Depth-First Search (DFS):** Finds a route using depth-first exploration.
- **Dijkstra's Algorithm:** Finds a minimum-cost route for non-negative road weights.
- **Bellman–Ford Algorithm:** Finds minimum-cost routes and supports negative-cycle detection.

## Running Tests

Install the dependencies and run the complete test suite:

```bash
python -m pytest -v
```

## Road Closures

Roads can be blocked or reopened in the graph model. The pathfinding algorithms ignore blocked roads when searching for a route.
