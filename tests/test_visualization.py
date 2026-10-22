
import pytest

from src.graph import Graph
from src.visualization import create_graph_figure


@pytest.fixture
def sample_graph():
    graph = Graph()

    graph.add_location("Entrance", (0, 0))
    graph.add_location("Hall", (1, 1))
    graph.add_location("Exit", (2, 0))

    graph.add_road("Entrance", "Hall", 3)
    graph.add_road("Hall", "Exit", 4)
    graph.add_road("Entrance", "Exit", 10)

    return graph


def test_visualization_creates_figure(sample_graph):
    figure = create_graph_figure(sample_graph)

    assert len(figure.data) > 0
    assert figure.layout.title.text == "Emergency Evacuation Road Network"


def test_visualization_accepts_path_and_exploration(sample_graph):
    figure = create_graph_figure(
        sample_graph,
        start="Entrance",
        destination="Exit",
        path=["Entrance", "Hall", "Exit"],
        explored=["Entrance", "Hall"],
        current_node="Hall",
    )

    assert len(figure.data) > 0


def test_visualization_displays_blocked_roads(sample_graph):
    sample_graph.block_road("Entrance", "Hall")

    figure = create_graph_figure(sample_graph)

    road_trace = figure.data[0]
    assert road_trace.line.dash == "dash"
    assert road_trace.line.color == "#DC2626"


def test_visualization_rejects_missing_positions():
    graph = Graph()
    graph.add_location("Entrance")

    with pytest.raises(ValueError, match="Missing visualization positions"):
        create_graph_figure(graph)


def test_visualization_rejects_unknown_path_nodes(sample_graph):
    with pytest.raises(ValueError, match="Unknown node in path"):
        create_graph_figure(sample_graph, path=["Entrance", "Unknown"])


def test_visualization_rejects_unknown_start(sample_graph):
    with pytest.raises(ValueError, match="Unknown start location"):
        create_graph_figure(sample_graph, start="Unknown")
