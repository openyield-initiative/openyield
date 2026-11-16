"""Strict JSON scenario loading. Geometry uses rectangle centres."""
import json
import math
from dataclasses import dataclass
from pathlib import Path

from .geometry import Rect, contained, pair_violation


def number(value, name, positive=False, nonnegative=False):
    error = f"invalid {name}: expected finite numeric value"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(error)
    try:
        value = float(value)
    except OverflowError as exc:
        raise ValueError(error) from exc
    if (not math.isfinite(value) or (positive and value <= 0)
            or (nonnegative and value < 0)):
        raise ValueError(error)
    return value


def keys(obj, expected):
    if not isinstance(obj, dict) or set(obj) != set(expected.split()):
        raise ValueError(f"expected keys: {expected}")


def rectangle(obj):
    keys(obj, "x y length width")
    return Rect(number(obj["x"], "x"), number(obj["y"], "y"),
                number(obj["length"], "length", positive=True),
                number(obj["width"], "width", positive=True))


def footprint(vehicle):
    return Rect(*(vehicle[k] for k in ("x", "y", "length", "width")))


@dataclass
class Scenario:
    road: Rect
    obstacles: list
    passing_space: Rect
    vehicles: list
    clearance: float
    dt: float
    max_duration: float
    source: dict


def parse_scenario(data):
    keys(data, "road obstacles passing_space vehicles clearance dt max_duration")
    road, passing = rectangle(data["road"]), rectangle(data["passing_space"])
    if not isinstance(data["obstacles"], list) or not isinstance(data["vehicles"], list):
        raise ValueError("obstacles and vehicles must be lists")
    obstacles = [rectangle(o) for o in data["obstacles"]]
    clearance = number(data["clearance"], "clearance", nonnegative=True)
    dt = number(data["dt"], "dt", positive=True)
    duration = number(data["max_duration"], "max_duration", positive=True)
    if dt > duration or duration / dt > 100000:
        raise ValueError("require dt <= duration and at most 100000 steps")
    vehicles = []
    for v in data["vehicles"]:
        keys(v, "id x y length width heading speed")
        r = rectangle({k: v[k] for k in ("x", "y", "length", "width")})
        if not isinstance(v["id"], str) or not v["id"].strip():
            raise ValueError("vehicle id must be a nonempty string")
        heading = number(v["heading"], "heading")
        if heading not in (0, 180):
            raise ValueError("only opposing fixed headings 0 and 180 degrees supported")
        vehicles.append(dict(id=v["id"], x=r.x, y=r.y, length=r.length,
                             width=r.width, heading=heading,
                             speed=number(v["speed"], "speed", positive=True)))
    if len(vehicles) != 2 or len({v["id"] for v in vehicles}) != 2:
        raise ValueError("exactly two uniquely identified vehicles required")
    if [v["heading"] for v in vehicles] != [0, 180]:
        raise ValueError("vehicle order must be eastbound then westbound")
    if not contained(passing, road):
        raise ValueError("passing space outside road")
    for i, obstacle in enumerate(obstacles):
        if not contained(obstacle, road) or pair_violation(obstacle, passing, 0):
            raise ValueError("obstacle outside road or overlapping passing space")
        if any(pair_violation(obstacle, other, 0) for other in obstacles[:i]):
            raise ValueError("overlapping obstacles")
    from .monitor import monitor
    s = Scenario(road, obstacles, passing, vehicles, clearance, dt, duration, data)
    errors = monitor(s, vehicles, vehicles)
    if errors:
        raise ValueError(f"invalid initial geometry: {errors}")
    return s


def load_scenario(path):
    return parse_scenario(json.loads(Path(path).read_text(encoding="utf-8")))
