"""Continuous translation monitors, independent of controller decisions."""
from .geometry import contained, swept_pair
from .model import footprint, number


def monitor(scenario, before, after):
    errors = []
    if len(after) != len(before):
        return ["invalid state: vehicle count changed"]
    for old, new in zip(before, after):
        if (not isinstance(new, dict) or set(new) != set(old)
                or any(new[k] != old[k] for k in ("id", "length", "width", "heading"))):
            return ["invalid state: finite positions and unchanged footprints/headings required"]
        try:
            for key in ("x", "y", "speed"):
                number(new[key], key)
        except ValueError:
            return ["invalid state: finite positions and unchanged footprints/headings required"]
    for i, (old, new) in enumerate(zip(before, after, strict=True)):
        a, end = footprint(old), footprint(new)
        # The road's inset is convex: endpoint containment covers the whole segment.
        road = scenario.road
        touches = (abs(end.x - road.x) + end.length / 2 >= road.length / 2
                   or abs(end.y - road.y) + end.width / 2 >= road.width / 2)
        if touches:
            errors.append(f"{old['id']}: road boundary")
        elif not contained(end, scenario.road, scenario.clearance):
            errors.append(f"{old['id']}: boundary clearance")
        for j, obstacle in enumerate(scenario.obstacles):
            violation = swept_pair(a, end, obstacle, obstacle, scenario.clearance)
            if violation:
                errors.append(f"{old['id']}: obstacle {j} {violation}")
        for k in range(i):
            violation = swept_pair(a, end, footprint(before[k]), footprint(after[k]),
                                   scenario.clearance)
            if violation:
                errors.append(f"{old['id']}/{before[k]['id']}: {violation}")
    return errors
