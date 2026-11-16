# Annotated replay and recording

Generate the default replay with `python -m openyield --output outputs/default --seed 7`
using the development environment described in [getting started](getting-started.md).
Open `outputs/default/replay.html` in a modern browser. It contains all assets and
trace data and needs no server, network or Node installation to play.

## Controls and explanations

- Starts paused at frame zero, without displaying the final outcome early.
- **Play/Pause** advances by elapsed viewing time through discrete recorded frames.
- **Restart** returns to frame zero and pauses. Play again at the end restarts.
- **Recorded frame** scrubs the trace and pauses. Simulation time labels use that frame.
- **Playback speed** offers 0.5×, 1× and 2×. This affects viewing time only; the
  simulation's time step, speeds, trace and summary do not change.
- Hiding the page pauses it; returning does not jump ahead.

Captions explain recorded waiting/passing, B clearing A, scripted sideways movement,
and proceeding to destinations. They use actions and positions, not fixed default
timestamps. Unknown action combinations display the recorded actions. The final
accepted frame shows the actual success/violation/timeout outcome and reason.
For violations, the rejected proposal is not drawn as an accepted movement.

The road and all footprints preserve the configured geometry. Hatching identifies
parked-vehicle obstacles; a dashed green area marks the bay. These are abstract
rectangles, not realistic parked-car models. Arrows identify the fixed headings.
Sideways translation is explicitly labeled: steering is not simulated. On narrow
screens, leader callouts label vehicles outside their unchanged footprints; the
legend and captions also use the configured vehicle IDs.

## Preparing a short recording

Select **Recording view** for a stable 16:9 composition. Record only the bordered
composition above the controls with an existing screen recorder. The title, stage,
simulation clock, legend and persistent caveat are included in that region:

**Scripted simulation · No negotiation or realistic steering.**

At 1×, the default trace covers 18.25 simulated seconds. Restart, select 1×, begin
your recorder, then press Play. Recording view changes layout only. No built-in
encoder, video export or automatic publication is supplied. This work does not
establish a recorded video exists or authorize publishing one.

Normal mobile layout stacks the controls and explanatory text for reading. The
complete road remains visible. Recording view keeps 16:9 even on a narrow screen;
use a desktop or landscape recording for legible public video. No interpolation,
cinematic camera, steering animation or synthetic trajectory is introduced.

## Developer checks

Python tests cover output integrity, markup escaping and package resources. Node
24 is a development checker only: `node --test tests/replay.test.cjs` uses its
built-in runner to check timing, controls and captions without extra packages.
CI runs it on Windows and Ubuntu alongside Python tests and strict MkDocs build.
Visual checks should cover initial/passing/lateral/terminal frames, keyboard and
touch-sized controls, mobile layout and the entire recording composition. Record
any preview security limitation instead of bypassing a browser block.

See [the upgrade verification record](replay-verification.md) for observed results
and the outstanding owner-operated visual checks.
