
from src.animation import build_animation_frames


def test_empty_events_return_no_frames():
    assert build_animation_frames({"events": []}) == []


def test_frames_preserve_cumulative_explored_nodes():
    result = {
        "events": [
            {"type": "start", "node": "A"},
            {"type": "explore", "node": "A"},
            {"type": "discover", "node": "B", "parent": "A"},
            {"type": "explore", "node": "B"},
        ]
    }

    frames = build_animation_frames(result)

    assert len(frames) == 4
    assert frames[1]["explored"] == ["A"]
    assert frames[2]["discovered"] == ["A", "B"]
    assert frames[2]["discovered_edges"] == [("A", "B")]
    assert frames[3]["explored"] == ["A", "B"]


def test_final_path_and_cost_are_preserved():
    result = {
        "path": ["A", "B", "C"],
        "path_cost": 7,
        "events": [
            {"type": "start", "node": "A"},
            {"type": "path_found", "path": ["A", "B", "C"], "path_cost": 7},
        ],
    }

    frames = build_animation_frames(result)

    assert frames[-1]["path"] == ["A", "B", "C"]
    assert frames[-1]["path_cost"] == 7
    assert frames[-1]["status_message"] == "Final route found."


def test_unreachable_event_has_status_message():
    result = {
        "events": [
            {"type": "start", "node": "A"},
            {"type": "unreachable"},
        ]
    }

    frames = build_animation_frames(result)

    assert frames[-1]["status_message"] == "The destination is unreachable."


def test_relax_event_records_edge():
    result = {
        "events": [
            {
                "type": "relax",
                "node": "B",
                "parent": "A",
                "new_distance": 4,
            }
        ]
    }

    frames = build_animation_frames(result)

    assert frames[0]["discovered_edges"] == [("A", "B")]
    assert frames[0]["current_node"] == "B"

def test_edge_check_sets_current_edge_and_status():
    result = {
        "events": [
            {
                "type": "edge_check",
                "node": "B",
                "parent": "A",
                "weight": 3,
                "already_visited": True,
            }
        ]
    }

    frames = build_animation_frames(result)

    assert frames[0]["current_edge"] == ("A", "B")
    assert frames[0]["current_node"] == "A"
    assert "already visited" in frames[0]["status_message"]