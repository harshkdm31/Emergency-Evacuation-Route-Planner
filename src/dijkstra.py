
import heapq
from itertools import count
from typing import Any, Dict, List, Optional

from src.graph import Graph


def solve_dijkstra(
    graph: Graph,
    start: str,
    destination: str,
) -> Dict[str, Any]:
    """
    Find a minimum-cost path using Dijkstra's algorithm.

    Requires non-negative edge weights. The Graph class currently
    enforces strictly positive road weights.

    Returns:
        algorithm, found, path, explored, path_cost, events
    """
    if not graph.has_location(start):
        raise ValueError(f"Unknown start location: {start!r}")

    if not graph.has_location(destination):
        raise ValueError(f"Unknown destination location: {destination!r}")

    events: List[Dict[str, Any]] = [
        {
            "type": "start",
            "node": start,
            "message": f"Starting Dijkstra at {start}",
        }
    ]

    if start == destination:
        events.append({
            "type": "destination_found",
            "node": destination,
            "message": "Start and destination are the same location.",
        })
        return {
            "algorithm": "Dijkstra",
            "found": True,
            "path": [start],
            "explored": [start],
            "path_cost": 0.0,
            "events": events,
        }

    distances: Dict[str, float] = {
        node: float("inf") for node in graph.get_locations()
    }
    parents: Dict[str, Optional[str]] = {start: None}

    distances[start] = 0.0

    # The counter prevents Python from comparing node names when
    # two heap entries have equal distances.
    tie_breaker = count()
    priority_queue = [(0.0, next(tie_breaker), start)]

    explored: List[str] = []
    settled = set()

    while priority_queue:
        current_distance, _, current = heapq.heappop(priority_queue)

        # Ignore outdated heap entries.
        if current_distance != distances[current]:
            continue

        # Each node is finalized at most once.
        if current in settled:
            continue

        settled.add(current)
        explored.append(current)

        events.append({
            "type": "explore",
            "node": current,
            "distance": current_distance,
            "message": f"Finalized {current} at cost {current_distance:g}",
        })

        if current == destination:
            events.append({
                "type": "destination_found",
                "node": destination,
                "distance": current_distance,
                "message": f"Destination {destination} reached.",
            })
            break

        for neighbor, weight in graph.get_neighbors(current):
            if neighbor in settled:
                continue

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                old_distance = distances[neighbor]
                distances[neighbor] = new_distance
                parents[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, next(tie_breaker), neighbor),
                )

                events.append({
                    "type": "relax",
                    "node": neighbor,
                    "parent": current,
                    "old_distance": old_distance,
                    "new_distance": new_distance,
                    "weight": weight,
                    "message": (
                        f"Updated distance to {neighbor}: "
                        f"{old_distance:g} → {new_distance:g}"
                    ),
                })

    if distances[destination] == float("inf"):
        events.append({
            "type": "unreachable",
            "node": destination,
            "message": f"No route exists from {start} to {destination}.",
        })
        return {
            "algorithm": "Dijkstra",
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
        current = parents[current]

    path.reverse()

    events.append({
        "type": "path_found",
        "path": path.copy(),
        "path_cost": distances[destination],
        "message": f"Minimum-cost route found: {distances[destination]:g}",
    })

    return {
        "algorithm": "Dijkstra",
        "found": True,
        "path": path,
        "explored": explored,
        "path_cost": distances[destination],
        "events": events,
    }
