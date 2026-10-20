
import pytest

from src.dfs import solve_dfs
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



def test_dfs_finds_a_valid_path(sample_graph):
    result = solve_dfs(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "B", "D"]
    assert result["path_cost"] == 4



def test_dfs_respects_blocked_roads(sample_graph):
    sample_graph.block_road("A", "C")

    result = solve_dfs(sample_graph, "A", "D")

    assert result["found"] is True
    assert result["path"] == ["A", "B", "D"]
    assert result["path_cost"] == 4


def test_dfs_reports_unreachable_destination(sample_graph):
    result = solve_dfs(sample_graph, "A", "E")

    assert result["found"] is False
    assert result["path"] == []
    assert result["path_cost"] is None


def test_dfs_start_equals_destination(sample_graph):
    result = solve_dfs(sample_graph, "A", "A")

    assert result["found"] is True
    assert result["path"] == ["A"]
    assert result["path_cost"] == 0


def test_dfs_rejects_unknown_locations(sample_graph):
    with pytest.raises(ValueError):
        solve_dfs(sample_graph, "Unknown", "D")

    with pytest.raises(ValueError):
        solve_dfs(sample_graph, "A", "Unknown")


def test_dfs_records_animation_events(sample_graph):
    result = solve_dfs(sample_graph, "A", "D")

    event_types = [event["type"] for event in result["events"]]

    assert "start" in event_types
    assert "explore" in event_types
    assert "destination_found" in event_types
    assert "path_found" in event_types
