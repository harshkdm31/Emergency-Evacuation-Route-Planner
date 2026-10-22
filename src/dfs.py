
from typing import Any, Dict, List, Optional

from src.graph import Graph


def solve_dfs(graph: Graph, start: str, destination: str) -> Dict[str, Any]:
    """
    Find a path using iterative Depth-First Search.

    DFS returns the first path it finds, not necessarily the shortest
    or least-cost path.

    Returns a dictionary containing:
        algorithm, found, path, explored, path_cost, events
    """
    if not graph.has_location(start):
        raise ValueError(f"Unknown start location: {start!r}")

    if not graph.has_location(destination):
        raise ValueError(f"Unknown destination location: {destination!r}")

    events: List[Dict[str, Any]] = [
        {"type": "start", "node": start, "message": f"Starting DFS at {start}"}
    ]

    if start == destination:
        events.append({
            "type": "destination_found",
            "node": destination,
            "message": "Start and destination are the same location.",
        })
        return {
            "algorithm": "DFS",
            "found": True,
            "path": [start],
            "explored": [start],
            "path_cost": 0.0,
            "events": events,
        }

    # Each stack entry stores the current node and its path from the start.
    stack = [(start, [start])]
    visited = set()
    explored: List[str] = []
    found_path: Optional[List[str]] = None

    while stack:
        current, current_path = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        explored.append(current)

        events.append({
            "type": "explore",
            "node": current,
            "path": current_path.copy(),
            "message": f"Exploring {current}",
        })

        if current == destination:
            found_path = current_path
            events.append({
                "type": "destination_found",
                "node": destination,
                "message": f"Destination {destination} found.",
            })
            break

        neighbors = graph.get_neighbors(current)

        # Reverse insertion order because the stack is LIFO.
        # This makes the first inserted neighbor explored first.
        
        for neighbor, weight in reversed(neighbors):
            already_visited = neighbor in visited

            events.append({
                "type": "edge_check",
                "node": neighbor,
                "parent": current,
                "weight": weight,
                "already_visited": already_visited,
                "message": (
                    f"Checking edge {current} → {neighbor}. "
                    + (
                        "Neighbor already visited."
                        if already_visited
                        else "Neighbor not yet visited; adding it to the DFS stack."
                    )
                ),
            })

            if not already_visited:
                stack.append((neighbor, current_path + [neighbor]))

                events.append({
                    "type": "discover",
                    "node": neighbor,
                    "parent": current,
                    "weight": weight,
                    "message": f"Added {neighbor} to the DFS stack.",
                })


    if found_path is None:
        events.append({
            "type": "unreachable",
            "node": destination,
            "message": f"No route exists from {start} to {destination}.",
        })
        return {
            "algorithm": "DFS",
            "found": False,
            "path": [],
            "explored": explored,
            "path_cost": None,
            "events": events,
        }

    path_cost = sum(
        graph.get_weight(found_path[i], found_path[i + 1])
        for i in range(len(found_path) - 1)
    )

    events.append({
        "type": "path_found",
        "path": found_path.copy(),
        "path_cost": path_cost,
        "message": f"DFS found a path with {len(found_path) - 1} edges.",
    })

    return {
        "algorithm": "DFS",
        "found": True,
        "path": found_path,
        "explored": explored,
        "path_cost": path_cost,
        "events": events,
    }
