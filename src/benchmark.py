
from statistics import median
from time import perf_counter
from typing import Any, Callable, Dict, List

from src.bfs import solve_bfs
from src.bellman_ford import solve_bellman_ford
from src.dfs import solve_dfs
from src.dijkstra import solve_dijkstra
from src.graph import Graph


Solver = Callable[[Graph, str, str], Dict[str, Any]]

SOLVERS: Dict[str, Solver] = {
    "BFS": solve_bfs,
    "DFS": solve_dfs,
    "Dijkstra": solve_dijkstra,
    "Bellman-Ford": solve_bellman_ford,
}


def benchmark_algorithms(
    graph: Graph,
    start: str,
    destination: str,
    repetitions: int = 5,
) -> List[Dict[str, Any]]:
    """
    Benchmark all pathfinding algorithms on the same graph and query.

    Timing includes each solver call but excludes graph drawing and UI
    work. The median of repeated runs is reported to reduce noise.

    Note:
        Event recording is currently part of each solver's execution,
        so measured time includes event creation.
    """
    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1.")

    if not graph.has_location(start):
        raise ValueError(f"Unknown start location: {start!r}")

    if not graph.has_location(destination):
        raise ValueError(f"Unknown destination location: {destination!r}")

    results: List[Dict[str, Any]] = []

    for algorithm_name, solver in SOLVERS.items():
        run_times = []
        result = None

        for _ in range(repetitions):
            begin = perf_counter()
            result = solver(graph, start, destination)
            elapsed = perf_counter() - begin
            run_times.append(elapsed)

        assert result is not None

        events = result.get("events", [])

        edges_examined = sum(
            1 for event in events
            if event.get("type") == "edge_check"
        )

        successful_relaxations = sum(
            1 for event in events
            if event.get("type") == "relax"
        )

        results.append({
            "algorithm": algorithm_name,
            "execution_time_ms": median(run_times) * 1000,
            "repetitions": repetitions,
            "found": result["found"],
            "path": result["path"],
            "path_cost": result["path_cost"],
            "explored_vertices": len(result["explored"]),
            "edges_examined": edges_examined,
            "successful_relaxations": successful_relaxations,
            "event_count": len(events),
            "explored_order": result["explored"],
            "theoretical_time_complexity": {
                "BFS": "O(V + E)",
                "DFS": "O(V + E)",
                "Dijkstra": "O((V + E) log V)",
                "Bellman-Ford": "O(VE)",
            }[algorithm_name],
        })

    return results
