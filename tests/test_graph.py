
import pytest

from src.graph import Graph


@pytest.fixture
def sample_graph():
    graph = Graph()

    for name, position in [
        ("Entrance", (0, 0)),
        ("Hall", (1, 0)),
        ("Library", (2, 1)),
        ("Exit", (3, 0)),
    ]:
        graph.add_location(name, position)

    graph.add_road("Entrance", "Hall", 4)
    graph.add_road("Hall", "Library", 3)
    graph.add_road("Library", "Exit", 2)
    graph.add_road("Entrance", "Exit", 15)

    return graph


def test_locations_and_positions(sample_graph):
    assert len(sample_graph) == 4
    assert sample_graph.has_location("Entrance")
    assert sample_graph.positions["Hall"] == (1.0, 0.0)


def test_roads_are_bidirectional(sample_graph):
    assert sample_graph.get_weight("Entrance", "Hall") == 4
    assert sample_graph.get_weight("Hall", "Entrance") == 4


def test_blocking_road_preserves_original_data(sample_graph):
    sample_graph.block_road("Entrance", "Hall")

    assert sample_graph.is_road_blocked("Hall", "Entrance")
    assert ("Hall", 4.0) not in sample_graph.get_neighbors("Entrance")
    assert sample_graph.get_weight("Entrance", "Hall") == 4
    assert len(sample_graph.get_roads()) == 4
    assert len(sample_graph.get_roads(include_blocked=False)) == 3


def test_unblock_road(sample_graph):
    sample_graph.block_road("Entrance", "Hall")
    sample_graph.unblock_road("Hall", "Entrance")

    assert not sample_graph.is_road_blocked("Entrance", "Hall")
    assert ("Hall", 4.0) in sample_graph.get_neighbors("Entrance")


def test_invalid_road_and_weight(sample_graph):
    with pytest.raises(ValueError):
        sample_graph.add_road("Entrance", "Unknown", 3)

    with pytest.raises(ValueError):
        sample_graph.add_road("Entrance", "Hall", 0)

    with pytest.raises(ValueError):
        sample_graph.block_road("Entrance", "Library")


def test_invalid_location(sample_graph):
    with pytest.raises(ValueError):
        sample_graph.add_location("   ")

    with pytest.raises(ValueError):
        sample_graph.get_neighbors("Unknown")
