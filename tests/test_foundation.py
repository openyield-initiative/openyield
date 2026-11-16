import copy
import json
import subprocess
import sys
from importlib.resources import files

import pytest

from openyield.geometry import Rect, pair_violation, swept_pair
from openyield.model import load_scenario, parse_scenario
from openyield.simulation import run
from openyield.output import export


def config():
    return json.loads(files("openyield").joinpath("scenarios/default.json").read_text())


def test_contact_and_clearance():
    a = Rect(0, 0, 2, 2)
    assert pair_violation(a, Rect(2, 0, 2, 2), 0) == "collision"
    assert pair_violation(a, Rect(2.25, 0, 2, 2), .25) is None
    assert pair_violation(a, Rect(2.125, 0, 2, 2), .25) == "clearance"
    assert pair_violation(a, Rect(1.9, 0, 2, 2), .25) == "collision"


def test_sweep_detects_thin_obstacle_and_relative_crossing():
    assert swept_pair(Rect(0, 0, 1, 1), Rect(10, 0, 1, 1),
                      Rect(5, 0, .1, 1), Rect(5, 0, .1, 1), 0)
    assert swept_pair(Rect(0, 0, 1, 1), Rect(10, 0, 1, 1),
                      Rect(10, 0, 1, 1), Rect(0, 0, 1, 1), 0)
    assert swept_pair(Rect(0, 0, 1, 1), Rect(10, 0, 1, 1),
                      Rect(5, 1.25, 1, 1), Rect(5, 1.25, 1, 1), .25) is None


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -1, 0, True, "2"])
def test_invalid_dimension(value):
    c = config()
    c["vehicles"][0]["length"] = value
    with pytest.raises(ValueError):
        parse_scenario(c)


@pytest.mark.parametrize("change", ["overlap", "outside", "heading", "unknown", "passing", "time"])
def test_invalid_scenario(change):
    c = config()
    if change == "overlap":
        c["vehicles"][1].update(x=12, y=6)
    elif change == "outside":
        c["obstacles"][0]["x"] = 100
    elif change == "heading":
        c["vehicles"][0]["heading"] = 90
    elif change == "unknown":
        c["typo"] = 1
    elif change == "passing":
        c["passing_space"]["width"] = -1
    else:
        c["dt"] = float("nan")
    with pytest.raises(ValueError):
        parse_scenario(c)


def test_success_determinism_and_wait():
    s = parse_scenario(config())
    a = run(s, seed=7)
    assert a == run(s, seed=7)
    assert a["summary"]["outcome"] == "success"
    assert any(f["actions"][0] == "wait in passing space" for f in a["frames"])
    assert a["frames"][-1]["vehicles"][0]["x"] == 26
    assert a["frames"][-1]["vehicles"][1]["x"] == 4


def test_timeout():
    c = config()
    c["max_duration"] = .5
    result = run(parse_scenario(c))
    assert result["summary"]["outcome"] == "timeout"
    assert result["frames"][-1]["time"] == .5


def test_fail_stop_rejects_unsafe_step():
    s = parse_scenario(config())
    def bad_controller(scenario, states, step):
        proposed = copy.deepcopy(states)
        proposed[0]["x"] = 100
        return proposed, ["unsafe", "wait"]
    result = run(s, controller=bad_controller)
    assert result["summary"]["outcome"] == "violation"
    assert result["frames"][-1]["vehicles"][0]["x"] == 12
    assert result["summary"]["rejected_step"][0]["x"] == 100


def test_export(tmp_path):
    s = parse_scenario(config())
    result = run(s)
    export(s, result, tmp_path)
    assert json.loads((tmp_path / "trace.json").read_text()) == result
    assert json.loads((tmp_path / "summary.json").read_text()) == result["summary"]
    html = (tmp_path / "replay.html").read_text(encoding="utf-8")
    assert "<canvas" in html and "requestAnimationFrame" in html
    assert "https://" not in html


def test_malformed_json(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{bad")
    with pytest.raises(ValueError):
        load_scenario(p)


def test_oversized_integer_is_configuration_error(tmp_path):
    c = config()
    c["dt"] = 10**400
    with pytest.raises(ValueError, match="finite numeric"):
        parse_scenario(c)
    path = tmp_path / "oversized.json"
    path.write_text(json.dumps(c), encoding="utf-8")
    with pytest.raises(ValueError, match="finite numeric"):
        load_scenario(path)
    result = subprocess.run(
        [sys.executable, "-m", "openyield", "--scenario", str(path)],
        capture_output=True, text=True,
    )
    assert result.returncode == 2
    assert "invalid dt" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("margin,offset,expected", [(0, 0, "road boundary"), (.25, .125, "boundary clearance")])
def test_boundary_contact_semantics(margin, offset, expected):
    from openyield.monitor import monitor
    s = parse_scenario(config())
    s.clearance = margin
    states = copy.deepcopy(s.vehicles)
    states[1]["y"] = 1 + states[1]["width"] / 2 + offset
    assert any(expected in e for e in monitor(s, s.vehicles, states))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), 10**400])
def test_monitor_rejects_nonfinite_proposal(value):
    from openyield.monitor import monitor
    s = parse_scenario(config())
    states = copy.deepcopy(s.vehicles)
    states[0]["x"] = value
    assert any("invalid state" in e for e in monitor(s, s.vehicles, states))


def test_monitor_rejects_changed_dimensions():
    from openyield.monitor import monitor
    s = parse_scenario(config())
    states = copy.deepcopy(s.vehicles)
    states[0]["length"] = .1
    assert any("invalid state" in e for e in monitor(s, s.vehicles, states))


def test_default_bottleneck_cannot_fit_two_vehicle_widths():
    c = config()
    road_bottom = c["road"]["y"] - c["road"]["width"] / 2
    obstacle_bottom = min(o["y"] - o["width"] / 2 for o in c["obstacles"])
    assert obstacle_bottom - road_bottom < sum(v["width"] for v in c["vehicles"])


def test_nonfinite_rejection_remains_exportable(tmp_path):
    s = parse_scenario(config())
    def invalid(scenario, states, step):
        states[0]["x"] = float("nan")
        return states, ["invalid", "wait"]
    result = run(s, controller=invalid)
    assert result["summary"]["outcome"] == "violation"
    export(s, result, tmp_path)
    assert json.loads((tmp_path / "summary.json").read_text())["rejected_step"][0]["x"] is None


def test_initial_clearance_violation_is_rejected():
    c = config()
    c["vehicles"][1]["y"] = 2.625  # top=3.375, obstacle bottom=3.5: only 0.125 m
    with pytest.raises(ValueError, match="clearance"):
        parse_scenario(c)


def test_swept_obstacle_violation_stops_simulation(tmp_path):
    c = config()
    c["obstacles"].append(dict(x=20, y=2.5, length=.1, width=1))
    s = parse_scenario(c)
    def jump(scenario, states, step):
        states[1]["x"] = 16  # both endpoints clear; obstacle at x=20 lies between
        return states, ["wait", "jump"]
    result = run(s, controller=jump)
    assert result["summary"]["outcome"] == "violation"
    assert "collision" in result["summary"]["reason"]
    assert result["summary"]["accepted_steps"] == 0
    assert result["frames"][-1]["vehicles"][1]["x"] == 26
    export(s, result, tmp_path)
    assert json.loads((tmp_path / "summary.json").read_text())["outcome"] == "violation"
