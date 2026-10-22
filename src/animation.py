
def build_animation_frames(result):
    """
    Convert an algorithm result's recorded events into animation frames.

    Each frame contains the cumulative search state up to that event.
    The algorithm is not rerun when moving between frames.
    """
    events = result.get("events", [])

    frames = []
    explored = []
    discovered = []
    discovered_edges = []
    final_path = []
    current_node = None
    current_edge = None
    status_message = "Ready to begin."
    path_cost = None

    for index, event in enumerate(events):
        event_type = event.get("type", "")

        # Identify the node involved in this event.
        node = event.get("node")

        # Reset the transient edge on every frame.
        current_edge = None

        if event_type == "start":
            node = event.get("node", event.get("start"))
            current_node = node
            status_message = f"Starting search at {node}."

            if node is not None and node not in discovered:
                discovered.append(node)

        elif event_type == "explore":
            if node is not None:
                current_node = node

                if node not in explored:
                    explored.append(node)

            status_message = (
                f"Exploring {node}."
                if node is not None
                else "Exploring the next state."
            )

        
        elif event_type == "edge_check":
            parent = event.get("parent")
            neighbor = event.get("node")
            current_node = parent

            if parent is not None and neighbor is not None:
                current_edge = (parent, neighbor)

            if event.get("candidate_distance") is not None:
                candidate = event["candidate_distance"]
                existing = event.get("existing_distance")

                if existing is None:
                    status_message = (
                        f"Checking {parent} → {neighbor}: "
                        f"candidate distance {candidate:g}."
                    )
                elif existing == float("inf"):
                    status_message = (
                        f"Checking {parent} → {neighbor}: "
                        f"candidate distance {candidate:g}; "
                        "no route to this neighbor is known yet."
                    )
                elif event.get("current_distance") is None:
                    status_message = event.get(
                        "message",
                        f"Cannot evaluate {parent} → {neighbor}: "
                        "the source distance is unknown.",
                    )
                elif event.get("already_visited"):
                    status_message = (
                        f"Checking {parent} → {neighbor}: "
                        "neighbor already visited."
                    )
                else:
                    status_message = (
                        f"Checking {parent} → {neighbor}: "
                        "neighbor not yet visited."
                    )

            elif event.get("already_visited"):
                status_message = (
                    f"Checking {parent} → {neighbor}: "
                    "neighbor already visited."
                )
            else:
                status_message = (
                    f"Checking {parent} → {neighbor}: "
                    "neighbor not yet visited."
                )


        elif event_type in ("discover", "relax"):
            parent = event.get("parent")

            if node is not None and node not in discovered:
                discovered.append(node)

            if parent is not None and node is not None:
                current_edge = (parent, node)

                edge = (parent, node)
                reverse_edge = (node, parent)

                if (
                    edge not in discovered_edges
                    and reverse_edge not in discovered_edges
                ):
                    discovered_edges.append(edge)

            current_node = node

            if event_type == "discover":
                status_message = f"Discovering {parent} → {node}."
            else:
                old_distance = event.get("old_distance")
                new_distance = event.get("new_distance")

                if new_distance is not None:
                    status_message = (
                        f"Relaxing {parent} → {node}: "
                        f"new distance {new_distance}."
                    )
                else:
                    status_message = f"Checking edge {parent} → {node}."

                
        elif event_type == "no_update":
            parent = event.get("parent")
            node = event.get("node")

            if parent is not None and node is not None:
                current_edge = (parent, node)
                current_node = parent

            candidate = event.get("candidate_distance")
            existing = event.get("old_distance")
            iteration = event.get("iteration")

            prefix = (
                f"Iteration {iteration}: "
                if iteration is not None
                else ""
            )

            if candidate is None:
                status_message = event.get(
                    "message",
                    f"{prefix}No update for {node}.",
                )
            elif existing is not None:
                status_message = (
                    f"{prefix}No update for {node}: candidate "
                    f"distance {candidate:g} is not less than "
                    f"the existing distance {existing:g}."
                )
            else:
                status_message = event.get(
                    "message",
                    f"{prefix}No update for {node}.",
                )


        elif event_type == "iteration":
            status_message = (
                f"Bellman–Ford iteration "
                f"{event.get('iteration', index + 1)}."
            )

        elif event_type == "early_stop":
            status_message = "No further distance updates were needed."

        elif event_type == "destination_found":
            current_node = event.get("node", current_node)
            status_message = "Destination reached."

        elif event_type == "negative_cycle":
            status_message = "A reachable negative-weight cycle was detected."

        elif event_type == "path_found":
            final_path = list(event.get("path", result.get("path", [])))
            path_cost = event.get("path_cost", result.get("path_cost"))
            current_node = final_path[-1] if final_path else current_node
            status_message = "Final route found."

        elif event_type == "unreachable":
            status_message = "The destination is unreachable."

        # Save a snapshot so playback never needs to rerun the algorithm.
        frames.append({
            "frame_index": index,
            "event_type": event_type,
            "event": dict(event),
            "current_node": current_node,
            "explored": list(explored),
            "discovered": list(discovered),
            "discovered_edges": list(discovered_edges),
            "path": list(final_path),
            "path_cost": path_cost,
            "status_message": status_message,
            "total_frames": len(events),
            "current_edge": current_edge,
        })

    return frames
