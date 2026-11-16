"""Bounded deterministic simulation; the default controller is only a script."""
import copy
import math

from .geometry import contained
from .model import footprint
from .monitor import monitor


def _toward(value, target, distance):
    return value + max(-distance, min(distance, target - value))


def _rejected_record(value):
    """Keep invalid numeric proposals inspectable without emitting invalid JSON."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, list):
        return [_rejected_record(item) for item in value]
    if isinstance(value, dict):
        return {key: _rejected_record(item) for key, item in value.items()}
    return value


def scripted_demo(scenario, states, step):
    """Wait in the bay, let B pass, translate sideways, then proceed east."""
    a, b = copy.deepcopy(states)
    initial_a, initial_b = scenario.vehicles
    target_b = scenario.road.x - scenario.road.length / 2 + b["length"] / 2 + 2
    b["x"] = _toward(b["x"], target_b, initial_b["speed"] * scenario.dt)
    actions = ["wait in passing space", "proceed west"]
    # Use the start-of-step B position: moving A cannot anticipate B's clearance.
    gap = (a["length"] + b["length"]) / 2 + scenario.clearance + .5
    if states[1]["x"] < initial_a["x"] - gap:
        if a["y"] != initial_b["y"]:
            a["y"] = _toward(a["y"], initial_b["y"], initial_a["speed"] * scenario.dt)
            actions[0] = "scripted lateral translation"
        else:
            a["x"] = _toward(a["x"], initial_b["x"], initial_a["speed"] * scenario.dt)
            actions[0] = "proceed east"
    if b["x"] == states[1]["x"]:
        actions[1] = "wait at destination"
    return [a, b], actions


def run(scenario, seed=0, controller=None):
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer (recorded, unused; no randomness)")
    if controller is None:
        if not contained(footprint(scenario.vehicles[0]), scenario.passing_space):
            raise ValueError("scripted demo requires A initially inside the passing space")
        if scenario.vehicles[1]["x"] <= scenario.vehicles[0]["x"]:
            raise ValueError("scripted demo requires B east of A")
        controller = scripted_demo
    states = copy.deepcopy(scenario.vehicles)
    for state in states:
        state["speed"] = 0.
    frames = [{"time": 0., "vehicles": copy.deepcopy(states), "actions": ["initial", "initial"]}]
    summary = {"outcome": "timeout", "reason": "maximum duration reached", "seed": seed,
               "randomness": False, "rejected_step": None}
    steps = math.floor(scenario.max_duration / scenario.dt)
    for step in range(1, steps + 1):
        proposed, actions = controller(scenario, copy.deepcopy(states), step)
        violations = monitor(scenario, states, proposed)
        if violations:
            summary.update(outcome="violation", reason="; ".join(violations),
                           rejected_step=_rejected_record(proposed), rejected_time=step * scenario.dt)
            break
        for old, new in zip(states, proposed, strict=True):
            new["speed"] = math.hypot(new["x"] - old["x"], new["y"] - old["y"]) / scenario.dt
        states = proposed
        frames.append({"time": step * scenario.dt, "vehicles": copy.deepcopy(states), "actions": actions})
        a, b = states
        target_b = scenario.road.x - scenario.road.length / 2 + b["length"] / 2 + 2
        if (a["x"] == scenario.vehicles[1]["x"] and a["y"] == scenario.vehicles[1]["y"]
                and b["x"] == target_b):
            summary.update(outcome="success", reason="both scripted destinations reached")
            break
    summary.update(time=frames[-1]["time"], accepted_steps=len(frames) - 1)
    return {"schema_version": 1, "scenario": scenario.source, "frames": frames, "summary": summary}
