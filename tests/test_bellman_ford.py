
import pytest

from src.bellman_ford import solve_bellman_ford
from src.graph import Graph


@pytest.fixture
def sample_graph():
    graph = Graph()

    for node in ["A", "B", "C", "D", "E"]:
        graph.add_location(node)

    graph.add_road("A", "B", 2)
    graph.add_road("A", "C", 1)
    graph.add_road("B", "D", 2)
    graph.add_road("C", "D", 10)

    return graph


def test_bellman_ford_finds_minimum_cost_path(sample_graph):
    result = solve_bellman_ford(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "B", "D"]
    assert result["path_cost"] == 4
    assert result["negative_cycle"] is False


def test_bellman_ford_respects_blocked_roads(sample_graph):
    sample_graph.block_road("B", "D")

    result = solve_bellman_ford(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "C", "D"]
    assert result["path_cost"] == 11


def test_bellman_ford_reports_unreachable_destination(sample_graph):
    result = solve_bellman_ford(sample_graph, "A", "E")

    assert result["found"] is False
    assert result["path"] == []
    assert result["path_cost"] is None
    assert result["negative_cycle"] is False


def test_bellman_ford_start_equals_destination(sample_graph):
    result = solve_bellman_ford(sample_graph, "A", "A")

    assert result["found"] is True
    assert result["path"] == ["A"]
    assert result["path_cost"] == 0


def test_bellman_ford_rejects_unknown_locations(sample_graph):
    with pytest.raises(ValueError):
        solve_bellman_ford(sample_graph, "Unknown", "D")

    with pytest.raises(ValueError):
        solve_bellman_ford(sample_graph, "A", "Unknown")


def test_bellman_ford_records_animation_events(sample_graph):
    result = solve_bellman_ford(sample_graph, "A", "D")

    event_types = [event["type"] for event in result["events"]]

    assert "start" in event_types
    assert "iteration" in event_types
    assert "relax" in event_types
    assert "path_found" in event_types
    assert result["negative_cycle"] is False
