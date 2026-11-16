# Contributing and verification

Follow [getting started](getting-started.md). Use a feature branch; do not merge,
deploy, publish packages/articles or tag releases without owner approval. There
is no contribution license agreement or selected project license yet.

Simulation/model code is under `src/openyield/`; geometry, monitoring, script,
outputs and CLI have separate responsibilities. Tests live in `tests/`.

Before proposing a change, run:

```powershell
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m openyield --output outputs/default --seed 7
.\.venv\Scripts\python -m mkdocs build --strict
git diff --check
```

Open `outputs/default/replay.html` and inspect initial waiting, B passing, A's
lateral movement and the terminal frame. The trace contains source configuration;
keep outputs private if a custom configuration includes identifying information.
Use independently calculated geometry fixtures, including contact, exact margin,
thin obstacles and relative crossings. Check fail-stop and timeout, not just success.

CI installs the package with dev dependencies, runs tests and the default demo,
then builds documentation strictly on Windows and Ubuntu/Python 3.12. It does not
deploy anything or replace a human visual review. CI status must be checked on
the actual PR; a workflow file alone is not evidence that checks passed.

For a portable package check, build with `python -m pip wheel . --no-deps -w dist`,
install that wheel in a new environment, then run `python -m openyield` outside
the repository. This ensures the installed default scenario is packaged.

Use [the milestone handoff template](handoff-template.md). Describe observed
behavior, verification environment and limitations, and avoid comparative claims
without experiments. No comprehensive literature review is claimed.
