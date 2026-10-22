
import streamlit as st
import plotly.graph_objects as go

from src.graph import Graph
from src.bfs import solve_bfs
from src.dfs import solve_dfs
from src.dijkstra import solve_dijkstra
from src.bellman_ford import solve_bellman_ford
from src.benchmark import benchmark_algorithms
from src.visualization import create_graph_figure
from src.animation import build_animation_frames


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
# 4. Run the selected algorithm only when inputs change
# ---------------------------------------------------------
SOLVERS = {
    "BFS": solve_bfs,
    "DFS": solve_dfs,
    "Dijkstra": solve_dijkstra,
    "Bellman-Ford": solve_bellman_ford,
}

blocked_signature = tuple(
    sorted(tuple(sorted(edge)) for edge in desired_blocked)
)

run_signature = (
    algorithm,
    start,
    destination,
    blocked_signature,
)

if st.session_state.get("route_signature") != run_signature:
    try:
        st.session_state["route_result"] = SOLVERS[algorithm](
            graph, start, destination
        )
        st.session_state["route_signature"] = run_signature

        # Reset playback whenever route inputs change.
        st.session_state["animation_frame"] = 0
        st.session_state["animation_playing"] = False

    except ValueError as exc:
        st.error(f"Unable to calculate route: {exc}")
        st.stop()

result = st.session_state["route_result"]



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
# 6. Animated graph visualization
# ---------------------------------------------------------
st.subheader("Campus Road Network")
st.caption(
    "Step through the algorithm's recorded events to see "
    "how it explores the campus graph."
)

frames = build_animation_frames(result)

if frames:
    total_frames = len(frames)

    # Keep the current frame index valid.
    frame_index = st.session_state.get("animation_frame", 0)
    frame_index = max(0, min(frame_index, total_frames - 1))
    st.session_state["animation_frame"] = frame_index

    speed_options = {
        "Slow": 1.2,
        "Normal": 0.6,
        "Fast": 0.25,
    }

    control_col1, control_col2 = st.columns([2, 1])

    with control_col1:
        speed_label = st.selectbox(
            "Playback speed",
            options=list(speed_options),
            index=1,
            key="animation_speed",
        )

    with control_col2:
        st.metric(
            "Animation frame",
            f"{frame_index + 1} / {total_frames}",
        )

    # Manual playback controls.
    previous_col, play_col, next_col, restart_col = st.columns(4)

    with previous_col:
        if st.button(
            "⏮ Previous",
            disabled=frame_index == 0,
            use_container_width=True,
            key="animation_previous",
        ):
            st.session_state["animation_frame"] = frame_index - 1
            st.session_state["animation_playing"] = False
            st.rerun()

    with play_col:
        is_playing = st.session_state.get("animation_playing", False)

        if st.button(
            "⏸ Pause" if is_playing else "▶ Play",
            use_container_width=True,
            key="animation_toggle",
        ):
            st.session_state["animation_playing"] = not is_playing

            # Stop automatically at the last frame.
            if frame_index >= total_frames - 1:
                st.session_state["animation_frame"] = 0
                st.session_state["animation_playing"] = True

            st.rerun()

    with next_col:
        if st.button(
            "Next ⏭",
            disabled=frame_index >= total_frames - 1,
            use_container_width=True,
            key="animation_next",
        ):
            st.session_state["animation_frame"] = frame_index + 1
            st.session_state["animation_playing"] = False
            st.rerun()

    with restart_col:
        if st.button(
            "↻ Restart",
            use_container_width=True,
            key="animation_restart",
        ):
            st.session_state["animation_frame"] = 0
            st.session_state["animation_playing"] = False
            st.rerun()

    # Automatic playback.
    # The fragment advances the frame and redraws the graph
    # together on each timed rerun.
    @st.fragment(
        run_every=(
            speed_options[speed_label]
            if st.session_state.get("animation_playing", False)
            else None
        )
    )
    def animation_autoplay():
        current = st.session_state.get("animation_frame", 0)
        playing = st.session_state.get("animation_playing", False)

        if playing:
            if current >= total_frames - 1:
                st.session_state["animation_playing"] = False
            else:
                current += 1
                st.session_state["animation_frame"] = current

        frame_to_show = frames[
            st.session_state.get("animation_frame", 0)
        ]

        st.info(
            f"**Step {frame_to_show['frame_index'] + 1}:** "
            f"{frame_to_show['status_message']}"
        )

        if frame_to_show["path_cost"] is not None:
            st.caption(
                f"Final route cost: {frame_to_show['path_cost']}"
            )

        figure = create_graph_figure(
            graph,
            start=start,
            destination=destination,
            path=frame_to_show["path"],
            explored=frame_to_show["explored"],
            current_node=frame_to_show["current_node"],
            discovered=frame_to_show["discovered"],
            discovered_edges=frame_to_show["discovered_edges"],
            current_edge=frame_to_show["current_edge"],
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
            key=f"autoplay_graph_{frame_to_show['frame_index']}",
        )

    animation_autoplay()

else:
    st.warning("No animation events were recorded for this algorithm run.")



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
                "Edges examined": row["edges_examined"],
                "Successful relaxations": row["successful_relaxations"],
                "Algorithm events": row["event_count"],
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

    # Compare graph traversal activity across algorithms.
    operation_chart = go.Figure(
        data=[
            go.Bar(
                name="Vertices explored",
                x=[
                    row["algorithm"]
                    for row in benchmark_results
                ],
                y=[
                    row["explored_vertices"]
                    for row in benchmark_results
                ],
            ),
            go.Bar(
                name="Edges examined",
                x=[
                    row["algorithm"]
                    for row in benchmark_results
                ],
                y=[
                    row["edges_examined"]
                    for row in benchmark_results
                ],
            ),
        ]
    )

    operation_chart.update_layout(
        title="Algorithm Operation Count Comparison",
        xaxis_title="Algorithm",
        yaxis_title="Recorded operations",
        barmode="group",
        template="plotly_white",
        legend_title="Metric",
    )

    st.plotly_chart(
        operation_chart,
        use_container_width=True,
        key="operation_count_chart",
    )



# ---------------------------------------------------------
# 9. Footer
# ---------------------------------------------------------
st.divider()
st.caption(
    "Academic simulation only. This application uses a predefined "
    "weighted campus graph, not live maps, GPS, or real-time traffic."
)
