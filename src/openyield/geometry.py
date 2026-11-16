"""Axis-aligned geometry; units are metres. Contact counts as collision."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    length: float
    width: float


def pair_violation(a, b, margin):
    dx = abs(a.x - b.x) - (a.length + b.length) / 2
    dy = abs(a.y - b.y) - (a.width + b.width) / 2
    if dx <= 0 and dy <= 0:
        return "collision"
    if dx < margin and dy < margin:
        return "clearance"
    return None


def _intersects(a, end_a, b, end_b, margin, strict):
    """Slab intersection in relative-position space over normalized time [0,1]."""
    low, high = 0., 1.
    for start, finish, extent in (
        (a.x - b.x, end_a.x - end_b.x, (a.length + b.length) / 2 + margin),
        (a.y - b.y, end_a.y - end_b.y, (a.width + b.width) / 2 + margin),
    ):
        velocity = finish - start
        if velocity == 0:
            if abs(start) > extent or (strict and abs(start) == extent):
                return False
            continue
        t1, t2 = sorted(((-extent - start) / velocity, (extent - start) / velocity))
        low, high = max(low, t1), min(high, t2)
        if low > high or (strict and low == high):
            return False
    return low <= high if not strict else low < high


def swept_pair(a, end_a, b, end_b, margin):
    if _intersects(a, end_a, b, end_b, 0, False):
        return "collision"
    if margin > 0 and _intersects(a, end_a, b, end_b, margin, True):
        return "clearance"
    return None


def contained(inner, outer, margin=0):
    return (abs(inner.x - outer.x) + inner.length / 2 + margin <= outer.length / 2
            and abs(inner.y - outer.y) + inner.width / 2 + margin <= outer.width / 2)
