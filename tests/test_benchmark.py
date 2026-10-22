
import pytest

from src.benchmark import SOLVERS, benchmark_algorithms
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


def test_all_four_algorithms_are_registered():
    assert list(SOLVERS.keys()) == [
        "BFS",
        "DFS",
        "Dijkstra",
        "Bellman-Ford",
    ]


def test_benchmark_returns_all_algorithm_results(sample_graph):
    results = benchmark_algorithms(sample_graph, "A", "D", repetitions=2)

    assert len(results) == 4
    assert {result["algorithm"] for result in results} == set(SOLVERS)


def test_dijkstra_and_bellman_ford_find_minimum_cost(sample_graph):
    results = benchmark_algorithms(sample_graph, "A", "D", repetitions=1)
    by_name = {result["algorithm"]: result for result in results}

    assert by_name["Dijkstra"]["path_cost"] == 4
    assert by_name["Bellman-Ford"]["path_cost"] == 4


def test_benchmark_reports_metrics(sample_graph):
    results = benchmark_algorithms(sample_graph, "A", "D", repetitions=1)

    for result in results:
        assert result["execution_time_ms"] >= 0
        assert result["explored_vertices"] >= 1
        assert result["found"] is True
        assert result["path"][0] == "A"
        assert result["path"][-1] == "D"
        assert result["theoretical_time_complexity"]


def test_benchmark_respects_blocked_roads(sample_graph):
    sample_graph.block_road("B", "D")

    results = benchmark_algorithms(sample_graph, "A", "D", repetitions=1)
    by_name = {result["algorithm"]: result for result in results}

    assert by_name["Dijkstra"]["path_cost"] == 11
    assert by_name["Bellman-Ford"]["path_cost"] == 11


def test_benchmark_rejects_invalid_repetitions(sample_graph):
    with pytest.raises(ValueError):
        benchmark_algorithms(sample_graph, "A", "D", repetitions=0)


def test_benchmark_rejects_unknown_locations(sample_graph):
    with pytest.raises(ValueError):
        benchmark_algorithms(sample_graph, "Unknown", "D")

    with pytest.raises(ValueError):
        benchmark_algorithms(sample_graph, "A", "Unknown")


def test_benchmark_handles_unreachable_destination(sample_graph):
    sample_graph.block_road("A", "B")
    sample_graph.block_road("A", "C")

    results = benchmark_algorithms(
        sample_graph, "A", "D", repetitions=1
    )

    for result in results:
        assert result["found"] is False
        assert result["path"] == []
        assert result["path_cost"] is None


def test_benchmark_handles_start_equal_to_destination(sample_graph):
    results = benchmark_algorithms(
        sample_graph, "A", "A", repetitions=1
    )

    for result in results:
        assert result["found"] is True
        assert result["path"] == ["A"]
        assert result["path_cost"] == 0


def test_benchmark_reports_operation_count_metrics(sample_graph):
    results = benchmark_algorithms(
        sample_graph, "A", "D", repetitions=1
    )

    for result in results:
        assert result["edges_examined"] >= 0
        assert result["successful_relaxations"] >= 0
        assert result["event_count"] >= 0
