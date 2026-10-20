
from tracemalloc import start
from typing import List, Optional, Sequence, Set, Tuple

import plotly.graph_objects as go

from src.graph import Graph


def create_graph_figure(
    graph,
    start=None,
    destination=None,
    path=None,
    explored=None,
    current_node=None,
    show_weights=True,
    discovered=None,
    discovered_edges=None,
    current_edge=None,
) -> go.Figure:
    """
    Create a Plotly visualization of a weighted road network.

    Visual layers:
        - Ordinary roads
        - Blocked roads
        - Selected route
        - Explored locations
        - Start and destination locations
        - Current animation location

    All locations must have positions, either supplied when added
    to the graph or assigned to graph.positions beforehand.
    """
    locations = graph.get_locations()
    path = list(path or [])
    explored_set: Set[str] = set(explored or [])
    discovered_set: Set[str] = set(discovered or [])
    discovered_edges_set = {
        frozenset(edge) for edge in (discovered_edges or [])
    }

    missing_positions = [
        node for node in locations if node not in graph.positions
    ]
    if missing_positions:
        raise ValueError(
            "Missing visualization positions for: "
            + ", ".join(missing_positions)
        )

    for label, node in [("start", start), ("destination", destination)]:
        if node is not None and not graph.has_location(node):
            raise ValueError(f"Unknown {label} location: {node!r}")

    for node in path:
        if not graph.has_location(node):
            raise ValueError(f"Unknown node in path: {node!r}")

    for node in explored_set:
        if not graph.has_location(node):
            raise ValueError(f"Unknown explored node: {node!r}")

    fig = go.Figure()

    # Draw ordinary roads first.
    for u, v, weight in graph.get_roads(include_blocked=True):
        x1, y1 = graph.positions[u]
        x2, y2 = graph.positions[v]

        blocked = graph.is_road_blocked(u, v)

        if blocked:
            color = "#DC2626"
            dash = "dash"
            width = 2
        elif (
            frozenset((u, v))
            in {frozenset(edge) for edge in zip(path, path[1:])}
        ):
            color = "#16A34A"
            dash = "solid"
            width = 5
        elif (
            current_edge is not None
            and frozenset((u, v)) == frozenset(current_edge)
        ):
            color = "#F59E0B"
            dash = "solid"
            width = 6
        elif frozenset((u, v)) in discovered_edges_set:
            color = "#9333EA"
            dash = "solid"
            width = 4
        else:
            color = "#94A3B8"
            dash = "solid"
            width = 2

        fig.add_trace(
            go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(color=color, width=width, dash=dash),
                hoverinfo="text",
                text=[
                    f"{u} ↔ {v}<br>Weight: {weight:g}"
                    + ("<br>BLOCKED" if blocked else ""),
                    f"{u} ↔ {v}<br>Weight: {weight:g}"
                    + ("<br>BLOCKED" if blocked else ""),
                ],
                showlegend=False,
            )
        )

        if show_weights:
            midpoint_x = (x1 + x2) / 2
            midpoint_y = (y1 + y2) / 2

            fig.add_annotation(
                x=midpoint_x,
                y=midpoint_y,
                text=f"{weight:g}",
                showarrow=False,
                font=dict(size=11, color="#334155"),
                bgcolor="white",
                bordercolor="#CBD5E1",
                borderwidth=1,
                borderpad=2,
            )

    # Overlay the selected route.
    for u, v in zip(path, path[1:]):
        x1, y1 = graph.positions[u]
        x2, y2 = graph.positions[v]

        fig.add_trace(
            go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(color="#16A34A", width=5),
                hoverinfo="text",
                text=[f"Selected route: {u} → {v}"] * 2,
                showlegend=False,
            )
        )

    # Classify nodes so important roles receive visual priority.
    node_colors: List[str] = []
    node_sizes: List[int] = []
    hover_text: List[str] = []

    for node in locations:
        if node == start:
            color, size, role = "#2563EB", 27, "START"
        elif node == destination:
            color, size, role = "#DC2626", 27, "DESTINATION"
        elif node == current_node:
            color, size, role = "#F59E0B", 29, "CURRENT"
        elif node in path:
            color, size, role = "#16A34A", 23, "ROUTE"
        elif node in explored_set:
            color, size, role = "#A78BFA", 20, "EXPLORED"
        elif node in discovered_set:
            color, size, role = "#C084FC", 18, "DISCOVERED"
        else:
            color, size, role = "#64748B", 16, "LOCATION"

        node_colors.append(color)
        node_sizes.append(size)
        hover_text.append(f"{node}<br>Status: {role}")

    fig.add_trace(
        go.Scatter(
            x=[graph.positions[node][0] for node in locations],
            y=[graph.positions[node][1] for node in locations],
            mode="markers+text",
            text=locations,
            textposition="top center",
            textfont=dict(size=12, color="#0F172A"),
            hovertext=hover_text,
            hoverinfo="text",
            marker=dict(
                size=node_sizes,
                color=node_colors,
                line=dict(color="white", width=2),
            ),
            showlegend=False,
        )
    )

    # Add a compact legend for node roles and road status.
    legend_items = [
        ("Start", "#2563EB", "circle"),
        ("Destination", "#DC2626", "circle"),
        ("Current node", "#F59E0B", "circle"),
        ("Selected route", "#16A34A", "line"),
        ("Explored", "#A78BFA", "circle"),
        ("Blocked road", "#DC2626", "line"),
        ("Discovered", "#C084FC", "circle"),
        ("Discovered road", "#9333EA", "line"),
        ("Current edge", "#F59E0B", "line"),
    ]

    for label, color, symbol in legend_items:
        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="lines" if symbol == "line" else "markers",
                line=dict(color=color, width=4, dash="dash" if label == "Blocked road" else "solid"),
                marker=dict(color=color, size=10),
                name=label,
                hoverinfo="skip",
                showlegend=True,
            )
        )

    fig.update_layout(
        title="Emergency Evacuation Road Network",
        template="plotly_white",
        height=600,
        margin=dict(l=20, r=20, t=70, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        hovermode="closest",
    )

    return fig
