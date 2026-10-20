
from math import inf, isfinite
from typing import Any, Dict, List, Optional

from src.graph import Graph


def solve_bellman_ford(
    graph: Graph,
    start: str,
    destination: str,
) -> Dict[str, Any]:
    """
    Find a minimum-cost path using Bellman-Ford.

    Supports negative edge weights if supplied by a compatible graph
    implementation. Detects negative cycles reachable from start.

    The current Graph class enforces positive road weights.

    Returns:
        algorithm, found, path, explored, path_cost, events,
        negative_cycle
    """
    if not graph.has_location(start):
        raise ValueError(f"Unknown start location: {start!r}")

    if not graph.has_location(destination):
        raise ValueError(f"Unknown destination location: {destination!r}")

    nodes = graph.get_locations()
    edges = []

    for u in nodes:
        for v, weight in graph.get_neighbors(u):
            # The graph is undirected, so each road appears in both directions.
            edges.append((u, v, weight))

    events: List[Dict[str, Any]] = [
        {
            "type": "start",
            "node": start,
            "message": f"Starting Bellman-Ford at {start}",
        }
    ]

    if start == destination:
        events.append({
            "type": "destination_found",
            "node": destination,
            "message": "Start and destination are the same location.",
        })
        return {
            "algorithm": "Bellman-Ford",
            "found": True,
            "path": [start],
            "explored": [start],
            "path_cost": 0.0,
            "events": events,
            "negative_cycle": False,
        }

    distances = {node: inf for node in nodes}
    parents: Dict[str, Optional[str]] = {start: None}
    distances[start] = 0.0

    explored = []
    explored_set = set()

    # Relax every edge up to |V| - 1 times.
    for iteration in range(len(nodes) - 1):
        changed = False

        events.append({
            "type": "iteration",
            "iteration": iteration + 1,
            "message": f"Relaxation pass {iteration + 1}",
        })

        for u, v, weight in edges:
            if distances[u] == inf:
                continue

            if u not in explored_set:
                explored_set.add(u)
                explored.append(u)

            new_distance = distances[u] + weight

            if new_distance < distances[v]:
                old_distance = distances[v]
                distances[v] = new_distance
                parents[v] = u
                changed = True

                events.append({
                    "type": "relax",
                    "node": v,
                    "parent": u,
                    "old_distance": old_distance,
                    "new_distance": new_distance,
                    "weight": weight,
                    "iteration": iteration + 1,
                    "message": (
                        f"Updated distance to {v}: "
                        f"{old_distance:g} → {new_distance:g}"
                    ),
                })

        if not changed:
            events.append({
                "type": "early_stop",
                "iteration": iteration + 1,
                "message": "No distances changed; stopping early.",
            })
            break

    # Detect a negative cycle reachable from the start.
    for u, v, weight in edges:
        if distances[u] != inf and distances[u] + weight < distances[v]:
            events.append({
                "type": "negative_cycle",
                "node": v,
                "message": "A reachable negative-weight cycle was detected.",
            })
            return {
                "algorithm": "Bellman-Ford",
                "found": False,
                "path": [],
                "explored": explored,
                "path_cost": None,
                "events": events,
                "negative_cycle": True,
            }

    if distances[destination] == inf:
        events.append({
            "type": "unreachable",
            "node": destination,
            "message": f"No route exists from {start} to {destination}.",
        })
        return {
            "algorithm": "Bellman-Ford",
            "found": False,
            "path": [],
            "explored": explored,
            "path_cost": None,
            "events": events,
            "negative_cycle": False,
        }

    path = []
    current: Optional[str] = destination

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()

    # Count the destination as explored when it is reachable.
    if destination not in explored_set:
        explored.append(destination)

    events.append({
        "type": "destination_found",
        "node": destination,
        "distance": distances[destination],
        "message": f"Destination {destination} reached.",
    })

    events.append({
        "type": "path_found",
        "path": path.copy(),
        "path_cost": distances[destination],
        "message": f"Minimum-cost route found: {distances[destination]:g}",
    })

    return {
        "algorithm": "Bellman-Ford",
        "found": True,
        "path": path,
        "explored": explored,
        "path_cost": distances[destination],
        "events": events,
        "negative_cycle": False,
    }
