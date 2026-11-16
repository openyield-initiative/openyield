# Getting started

Use Python 3.12 or newer. The verified local environment is Windows with Python
3.12.10; the CI configuration targets Python 3.12 on Windows and Ubuntu.

From a fresh checkout, in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m openyield --output outputs/default --seed 7
.\.venv\Scripts\python -m mkdocs build --strict
Start-Process outputs/default/replay.html
```

On Linux/macOS use `python3 -m venv .venv` and `.venv/bin/python` in the remaining
commands. The replay runs offline in a modern browser: Play/Pause and a frame slider
allow inspection. It needs no server, external fonts or network resources.

Outputs (ignored by Git): `outputs/default/trace.json`, `summary.json` and
`replay.html`. Trace schema version 1 includes the complete scenario, each accepted
frame's time, positions, headings, actual translational speeds and actions, plus
the terminal summary. Units are metres, seconds, metres/second and degrees.
Summary contains outcome, reason, accepted time/step count, seed and randomness
flag. A violation records the rejected proposed state and its attempted time;
the accepted trace stays at the last safe state.
Nonfinite values in rejected proposals are represented as JSON `null`; the
violation reason identifies the invalid-state condition.

There is no randomness. Seeds are recorded for future compatibility but do not
affect movement. Identical inputs and seeds produce identical trace content;
there are no wall-clock timestamps or incidental run identifiers.

## Configure an encounter

Copy `src/openyield/scenarios/default.json` and run:

```powershell
.\.venv\Scripts\python -m openyield --scenario my-scenario.json --output outputs/custom
```

All keys are required and unknown keys are rejected. Rectangles specify centre
`x`, `y`, positive `length` along x and positive `width` along y. Vehicle objects
also require unique nonempty `id`, `heading` (0 east or 180 west), and positive
cruise `speed`. Exactly two vehicles are required in eastbound/westbound order.
`road`, `obstacles`, `passing_space`, `vehicles`, nonnegative `clearance`, positive
`dt` and `max_duration` are the top-level keys. `dt` cannot exceed duration;
at most 100,000 steps are permitted. No NaN, infinity, booleans or numeric strings.

The script requires A initially wholly inside the passing space and B east of A.
It uses B's initial y as the shared lane, B's initial x as A's destination and a
west destination two metres beyond B's half-length from the road's left edge.
Other valid geometries may timeout or fail monitoring: configuration support
does not imply general encounter-solving ability.

The default road is 30 × 7 m (y from 1 to 8), with parked obstacles on the north side and a
6 × 3 m passing space centred at (12, 6). A starts there at (12, 6); B starts at
(26, 2.5). Both are 4 × 1.5 m, cruise at 2 m/s, with clearance 0.25 m,
time step 0.25 s and maximum duration 40 s.

The blocked sections leave a 2.5 m corridor (y = 1 to 3.5), narrower than two
1.5 m vehicle widths. Obstacles represent rectangular occupied regions, not
dimensionally realistic parked-car models.

Exit status is 0 for success, 1 for violation/timeout and 2 for configuration or
file errors. To browse documentation locally, run
`.\.venv\Scripts\python -m mkdocs serve`; strict build output is in `site/`.
