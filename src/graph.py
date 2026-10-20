
from __future__ import annotations

from typing import Dict, List, Tuple, Set, Optional


class Graph:
    """Undirected weighted graph for an emergency route planner."""

    def __init__(self) -> None:
        # Each location maps to its neighboring locations and road weights.
        self.adjacency: Dict[str, Dict[str, float]] = {}

        # Human-readable positions for graph visualization.
        self.positions: Dict[str, Tuple[float, float]] = {}

        # Preserve all roads; blocking a road should not delete it.
        self.blocked_edges: Set[Tuple[str, str]] = set()

    @staticmethod
    def _edge_key(u: str, v: str) -> Tuple[str, str]:
        """Return a consistent key for an undirected road."""
        return tuple(sorted((u, v)))

    def add_location(
        self,
        name: str,
        position: Optional[Tuple[float, float]] = None,
    ) -> None:
        """Add a location, optionally with its visualization position."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Location name must be a non-empty string.")

        name = name.strip()
        self.adjacency.setdefault(name, {})

        if position is not None:
            if len(position) != 2:
                raise ValueError("Position must contain exactly two coordinates.")
            self.positions[name] = (float(position[0]), float(position[1]))

    def add_road(self, u: str, v: str, weight: float = 1.0) -> None:
        """Add or update a bidirectional road with a positive weight."""
        if u not in self.adjacency or v not in self.adjacency:
            raise ValueError("Both locations must exist before adding a road.")

        if u == v:
            raise ValueError("Self-loop roads are not supported.")

        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise TypeError("Road weight must be a number.")

        if weight <= 0 or weight == float("inf") or weight != weight:
            raise ValueError("Road weight must be finite and positive.")

        weight = float(weight)
        self.adjacency[u][v] = weight
        self.adjacency[v][u] = weight

        # A road updated while blocked remains blocked until unblocked.
        # Call unblock_road() explicitly to reopen it.

    def block_road(self, u: str, v: str) -> None:
        """Temporarily block an existing road."""
        if u not in self.adjacency or v not in self.adjacency[u]:
            raise ValueError(f"Road {u!r} - {v!r} does not exist.")

        self.blocked_edges.add(self._edge_key(u, v))

    def unblock_road(self, u: str, v: str) -> None:
        """Reopen a previously blocked road."""
        if u not in self.adjacency or v not in self.adjacency[u]:
            raise ValueError(f"Road {u!r} - {v!r} does not exist.")

        self.blocked_edges.discard(self._edge_key(u, v))

    def is_road_blocked(self, u: str, v: str) -> bool:
        """Check whether a road is blocked."""
        return self._edge_key(u, v) in self.blocked_edges

    def get_neighbors(self, u: str) -> List[Tuple[str, float]]:
        """Return accessible neighbors and road weights."""
        if u not in self.adjacency:
            raise ValueError(f"Unknown location: {u!r}")

        return [
            (v, weight)
            for v, weight in self.adjacency[u].items()
            if not self.is_road_blocked(u, v)
        ]

    def get_locations(self) -> List[str]:
        """Return all locations in insertion order."""
        return list(self.adjacency.keys())

    def get_roads(self, include_blocked: bool = True) -> List[Tuple[str, str, float]]:
        """Return each undirected road once."""
        roads = []

        for u, neighbors in self.adjacency.items():
            for v, weight in neighbors.items():
                if u < v:
                    if include_blocked or not self.is_road_blocked(u, v):
                        roads.append((u, v, weight))

        return roads

    def has_location(self, name: str) -> bool:
        """Check whether a location exists."""
        return name in self.adjacency

    def get_weight(self, u: str, v: str) -> float:
        """Return the weight of a road, even if it is blocked."""
        if u not in self.adjacency or v not in self.adjacency[u]:
            raise ValueError(f"Road {u!r} - {v!r} does not exist.")

        return self.adjacency[u][v]

    def __len__(self) -> int:
        """Return the number of locations."""
        return len(self.adjacency)
