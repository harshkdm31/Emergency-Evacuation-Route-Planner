
import pytest

from src.bfs import solve_bfs
from src.graph import Graph


@pytest.fixture
def sample_graph():
    graph = Graph()

    for name in ["A", "B", "C", "D", "E"]:
        graph.add_location(name)

    graph.add_road("A", "B", 5)
    graph.add_road("A", "C", 1)
    graph.add_road("B", "D", 2)
    graph.add_road("C", "D", 10)
    # E is intentionally disconnected.

    return graph


def test_bfs_finds_fewest_edges_path(sample_graph):
    result = solve_bfs(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "B", "D"]
    assert result["path_cost"] == 7
    assert result["explored"][0] == "A"


def test_bfs_respects_blocked_roads(sample_graph):
    sample_graph.block_road("A", "B")

    result = solve_bfs(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "C", "D"]
    assert result["path_cost"] == 11


def test_bfs_reports_unreachable_destination(sample_graph):
    result = solve_bfs(sample_graph, "A", "E")

    assert result["found"] is False
    assert result["path"] == []
    assert result["path_cost"] is None
    assert result["explored"] == ["A", "B", "C", "D"]


def test_bfs_start_equals_destination(sample_graph):
    result = solve_bfs(sample_graph, "A", "A")

    assert result["found"] is True
    assert result["path"] == ["A"]
    assert result["path_cost"] == 0


def test_bfs_rejects_unknown_locations(sample_graph):
    with pytest.raises(ValueError):
        solve_bfs(sample_graph, "Unknown", "D")

    with pytest.raises(ValueError):
        solve_bfs(sample_graph, "A", "Unknown")


def test_bfs_records_animation_events(sample_graph):
    result = solve_bfs(sample_graph, "A", "D")

    event_types = [event["type"] for event in result["events"]]

    assert "start" in event_types
    assert "explore" in event_types
    assert "discover" in event_types
    assert "destination_found" in event_types
    assert "path_found" in event_types
