# Annotated replay implementation plan

Approved design: owner-approved proposal 72409, presentation only.

Goal: readable offline replay with elapsed-time playback, explanatory stages,
mobile controls and a stable recording composition. No dynamics, scenario,
monitoring, trace-schema or metric changes; no new runtime dependencies.

1. Add failing Node built-in tests for paused start, elapsed time, speed changes,
   scrub/restart/end/hidden-page pause and action-derived stage fallback. Add a
   Python regression comparing exact pre-change trace and summary bytes.
2. Implement a small renderer asset bundle (HTML/CSS/JavaScript) embedded by the
   existing exporter. Keep deterministic data exports unchanged. Use discrete
   recorded frames, faithful geometry, accessible controls and persistent caveat.
3. Document recording/mobile behavior and developer checks. Run Node and Python
   tests, default demo, byte comparisons and strict docs build. Inspect the replay
   only through permitted preview tooling; record any visual-inspection blocker.
4. Review the branch, correct findings, push and open a PR. Do not merge/publish.

Files: `src/openyield/replay/` owns presentation and pure playback logic;
`output.py` embeds assets; `pyproject.toml` packages them; `tests/replay.test.cjs`
checks playback with Node's built-in runner; Python output tests verify data.
CI uses Node only as a development checker, never a replay runtime dependency.

Checkpoints: `[before-replay]` outputs are ignored local fixtures. Existing
controller and monitor files must have no diff. Acceptance-status docs PR and
other checkouts remain separate. Recording means a clean layout for an existing
screen recorder; no built-in video encoder or new recording tools.
