
import streamlit as st
import plotly.graph_objects as go

from src.graph import Graph
from src.bfs import solve_bfs
from src.dfs import solve_dfs
from src.dijkstra import solve_dijkstra
from src.bellman_ford import solve_bellman_ford
from src.benchmark import benchmark_algorithms
from src.visualization import create_graph_figure


st.set_page_config(
    page_title="Emergency Route Planner",
    page_icon="🚨",
    layout="wide",
)

st.title("🚨 Emergency Evacuation & Route Planner")
st.caption(
    "Explore graph algorithms, find evacuation routes, "
    "and simulate road closures on a sample campus network."
)


# ---------------------------------------------------------
# 1. Create the predefined campus graph
# ---------------------------------------------------------
@st.cache_resource
def build_campus_graph():
    graph = Graph()

    locations = {
        "Main Gate": (0, 3),
        "Admin Block": (2, 4),
        "Library": (4, 4),
        "Academic Block": (2, 2),
        "Cafeteria": (4, 1),
        "Hostel": (6, 3),
        "Medical Center": (6, 5),
        "Assembly Ground": (8, 3),
    }

    for name, position in locations.items():
        graph.add_location(name, position)

    roads = [
        ("Main Gate", "Admin Block", 4),
        ("Main Gate", "Academic Block", 3),
        ("Admin Block", "Library", 2),
        ("Admin Block", "Academic Block", 2),
        ("Library", "Medical Center", 3),
        ("Library", "Hostel", 5),
        ("Academic Block", "Cafeteria", 3),
        ("Cafeteria", "Hostel", 2),
        ("Cafeteria", "Assembly Ground", 5),
        ("Hostel", "Medical Center", 2),
        ("Hostel", "Assembly Ground", 3),
        ("Medical Center", "Assembly Ground", 4),
    ]

    for u, v, weight in roads:
        graph.add_road(u, v, weight)

    return graph


graph = build_campus_graph()
locations = graph.get_locations()


# ---------------------------------------------------------
# 2. Sidebar controls
# ---------------------------------------------------------
st.sidebar.header("Route Configuration")

start = st.sidebar.selectbox(
    "Start location",
    locations,
    index=0,
)

destination_options = [
    node for node in locations if node != start
]

destination = st.sidebar.selectbox(
    "Destination",
    destination_options,
    index=len(destination_options) - 1,
)

algorithm = st.sidebar.selectbox(
    "Pathfinding algorithm",
    ["BFS", "DFS", "Dijkstra", "Bellman-Ford"],
)

st.sidebar.caption(
    "BFS minimizes the number of edges. "
    "DFS finds a path without optimizing cost. "
    "Dijkstra and Bellman–Ford minimize total path cost."
)


# ---------------------------------------------------------
# 3. Road closure controls
# ---------------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("Road Closures")

all_roads = graph.get_roads(include_blocked=True)


def road_label(road):
    u, v, weight = road
    status = " [BLOCKED]" if graph.is_road_blocked(u, v) else ""
    return f"{u} ↔ {v} (cost {weight:g}){status}"


road_lookup = {
    road_label(road): (road[0], road[1])
    for road in all_roads
}

selected_road_labels = st.sidebar.multiselect(
    "Select roads to block",
    options=list(road_lookup.keys()),
    default=[
        label
        for label, (u, v) in road_lookup.items()
        if graph.is_road_blocked(u, v)
    ],
    help="Selected roads will be closed. Clear the selection to reopen them.",
)

desired_blocked = {
    frozenset(road_lookup[label])
    for label in selected_road_labels
}

# Synchronize the graph with the current selection.
for u, v, _ in all_roads:
    edge = frozenset((u, v))

    if edge in desired_blocked:
        graph.block_road(u, v)
    else:
        graph.unblock_road(u, v)


# ---------------------------------------------------------
# 4. Run the selected algorithm
# ---------------------------------------------------------
SOLVERS = {
    "BFS": solve_bfs,
    "DFS": solve_dfs,
    "Dijkstra": solve_dijkstra,
    "Bellman-Ford": solve_bellman_ford,
}

try:
    result = SOLVERS[algorithm](graph, start, destination)
except ValueError as exc:
    st.error(f"Unable to calculate route: {exc}")
    st.stop()


# ---------------------------------------------------------
# 5. Main results
# ---------------------------------------------------------
st.subheader("Route Results")

if result["found"]:
    path_text = " → ".join(result["path"])
    st.success(f"Route found: {path_text}")
else:
    st.error(f"No available route from {start} to {destination}.")

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Algorithm",
    result["algorithm"],
)

metric2.metric(
    "Route cost",
    f'{result["path_cost"]:g}' if result["path_cost"] is not None else "N/A",
)

metric3.metric(
    "Vertices explored",
    len(result["explored"]),
)

metric4.metric(
    "Route status",
    "Available" if result["found"] else "Unreachable",
)


# ---------------------------------------------------------
# 6. Interactive graph visualization
# ---------------------------------------------------------
st.subheader("Campus Road Network")

try:
    figure = create_graph_figure(
        graph,
        start=start,
        destination=destination,
        path=result["path"],
        explored=result["explored"],
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        key="campus_graph",
    )
except ValueError as exc:
    st.error(f"Unable to display graph: {exc}")


# ---------------------------------------------------------
# 7. Route details
# ---------------------------------------------------------
with st.expander("View algorithm details", expanded=True):
    if result["found"]:
        st.write("**Selected path:**", " → ".join(result["path"]))
        st.write("**Number of roads in path:**", len(result["path"]) - 1)
        st.write("**Path cost:**", result["path_cost"])
    else:
        st.write("No valid path is available under the current road closures.")

    st.write("**Exploration order:**")
    st.write(" → ".join(result["explored"]) or "No vertices explored")

    st.write("**Algorithm events:**", len(result["events"]))


# ---------------------------------------------------------
# 8. Benchmark all algorithms on the same graph
# ---------------------------------------------------------
st.divider()
st.subheader("Algorithm Performance Comparison")

st.write(
    "Compare all four algorithms using the same graph, start, "
    "destination, and current road closures."
)

repetitions = st.slider(
    "Number of timing repetitions",
    min_value=1,
    max_value=20,
    value=5,
)

if st.button("Run Benchmark", type="primary"):
    try:
        benchmark_results = benchmark_algorithms(
            graph,
            start,
            destination,
            repetitions=repetitions,
        )

        st.session_state["benchmark_results"] = benchmark_results

    except ValueError as exc:
        st.error(f"Benchmark failed: {exc}")


if "benchmark_results" in st.session_state:
    benchmark_results = st.session_state["benchmark_results"]

    # Rebuild the table using the stored results.
    st.dataframe(
        [
            {
                "Algorithm": row["algorithm"],
                "Execution time (ms)": round(
                    row["execution_time_ms"], 5
                ),
                "Vertices explored": row["explored_vertices"],
                "Route found": row["found"],
                "Path cost": row["path_cost"],
                "Time complexity": row["theoretical_time_complexity"],
            }
            for row in benchmark_results
        ],
        use_container_width=True,
        hide_index=True,
    )

    chart = go.Figure(
        data=[
            go.Bar(
                x=[row["algorithm"] for row in benchmark_results],
                y=[row["execution_time_ms"] for row in benchmark_results],
                text=[
                    f'{row["execution_time_ms"]:.5f} ms'
                    for row in benchmark_results
                ],
                textposition="auto",
            )
        ]
    )

    chart.update_layout(
        title="Execution Time Comparison",
        xaxis_title="Algorithm",
        yaxis_title="Median execution time (ms)",
        template="plotly_white",
    )

    st.plotly_chart(
        chart,
        use_container_width=True,
        key="benchmark_chart",
    )


# ---------------------------------------------------------
# 9. Footer
# ---------------------------------------------------------
st.divider()
st.caption(
    "Academic simulation only. This application uses a predefined "
    "weighted campus graph, not live maps, GPS, or real-time traffic."
)
