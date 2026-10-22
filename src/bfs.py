
from collections import deque
from typing import Any, Dict, List, Optional

from src.graph import Graph


def solve_bfs(graph: Graph, start: str, destination: str) -> Dict[str, Any]:
    """
    Find a path using Breadth-First Search.

    BFS finds a path with the fewest edges, not necessarily the
    minimum total weight.

    Returns:
        path: Ordered list of locations from start to destination.
        found: Whether a path exists.
        explored: Locations visited in exploration order.
        events: Step-by-step events for future animation.
        path_cost: Sum of weights along the returned path.
    """
    if not graph.has_location(start):
        raise ValueError(f"Unknown start location: {start!r}")

    if not graph.has_location(destination):
        raise ValueError(f"Unknown destination: {destination!r}")

    events: List[Dict[str, Any]] = [
        {"type": "start", "node": start, "message": f"Starting BFS at {start}"}
    ]

    if start == destination:
        events.append({
            "type": "destination_found",
            "node": destination,
            "message": "Start and destination are the same location.",
        })
        return {
            "algorithm": "BFS",
            "found": True,
            "path": [start],
            "explored": [start],
            "path_cost": 0.0,
            "events": events,
        }

    queue = deque([start])
    visited = {start}
    parent: Dict[str, Optional[str]] = {start: None}
    explored: List[str] = []

    while queue:
        current = queue.popleft()
        explored.append(current)

        events.append({
            "type": "explore",
            "node": current,
            "message": f"Exploring {current}",
        })

        if current == destination:
            events.append({
                "type": "destination_found",
                "node": destination,
                "message": f"Destination {destination} found.",
            })
            break

        for neighbor, weight in graph.get_neighbors(current):
            events.append({
                "type": "edge_check",
                "node": neighbor,
                "parent": current,
                "weight": weight,
                "already_visited": neighbor in visited,
            })

            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)

                events.append({
                    "type": "discover",
                    "node": neighbor,
                    "parent": current,
                    "weight": weight,
                    "message": f"Discovered {neighbor} from {current}",
                })

    if destination not in parent:
        events.append({
            "type": "unreachable",
            "node": destination,
            "message": f"No route exists from {start} to {destination}.",
        })
        return {
            "algorithm": "BFS",
            "found": False,
            "path": [],
            "explored": explored,
            "path_cost": None,
            "events": events,
        }

    path: List[str] = []
    current: Optional[str] = destination

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    path_cost = sum(
        graph.get_weight(path[i], path[i + 1])
        for i in range(len(path) - 1)
    )

    events.append({
        "type": "path_found",
        "path": path.copy(),
        "path_cost": path_cost,
        "message": f"BFS found a path with {len(path) - 1} edges.",
    })

    return {
        "algorithm": "BFS",
        "found": True,
        "path": path,
        "explored": explored,
        "path_cost": path_cost,
        "events": events,
    }
