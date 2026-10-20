
import pytest

from src.dijkstra import solve_dijkstra
from src.graph import Graph


@pytest.fixture
def sample_graph():
    graph = Graph()

    for name in ["A", "B", "C", "D", "E"]:
        graph.add_location(name)

    graph.add_road("A", "B", 2)
    graph.add_road("A", "C", 1)
    graph.add_road("B", "D", 2)
    graph.add_road("C", "D", 10)
    # E is intentionally disconnected.

    return graph


def test_dijkstra_finds_minimum_cost_path(sample_graph):
    result = solve_dijkstra(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "B", "D"]
    assert result["path_cost"] == 4


def test_dijkstra_can_choose_more_edges_for_lower_cost():
    graph = Graph()

    for node in ["A", "B", "C", "D"]:
        graph.add_location(node)

    graph.add_road("A", "D", 10)
    graph.add_road("A", "B", 2)
    graph.add_road("B", "C", 2)
    graph.add_road("C", "D", 2)

    result = solve_dijkstra(graph, "A", "D")

    assert result["path"] == ["A", "B", "C", "D"]
    assert result["path_cost"] == 6


def test_dijkstra_respects_blocked_roads(sample_graph):
    sample_graph.block_road("B", "D")

    result = solve_dijkstra(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "C", "D"]
    assert result["path_cost"] == 11


def test_dijkstra_reports_unreachable_destination(sample_graph):
    result = solve_dijkstra(sample_graph, "A", "E")

    assert result["found"] is False
    assert result["path"] == []
    assert result["path_cost"] is None


def test_dijkstra_start_equals_destination(sample_graph):
    result = solve_dijkstra(sample_graph, "A", "A")

    assert result["found"] is True
    assert result["path"] == ["A"]
    assert result["path_cost"] == 0


def test_dijkstra_rejects_unknown_locations(sample_graph):
    with pytest.raises(ValueError):
        solve_dijkstra(sample_graph, "Unknown", "D")

    with pytest.raises(ValueError):
        solve_dijkstra(sample_graph, "A", "Unknown")


def test_dijkstra_records_animation_events(sample_graph):
    result = solve_dijkstra(sample_graph, "A", "D")

    event_types = [event["type"] for event in result["events"]]

    assert "start" in event_types
    assert "explore" in event_types
    assert "relax" in event_types
    assert "destination_found" in event_types
    assert "path_found" in event_types
