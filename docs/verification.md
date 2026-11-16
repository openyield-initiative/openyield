# v0.1 verification record

Observed locally on 16 November 2026: Windows, Python 3.12.10, pytest 9.2.0,
MkDocs 1.6.1. Commands below are PowerShell from the repository root unless noted.

| Command | Observed result |
| --- | --- |
| `python -m venv .venv` | Created project environment. |
| `.\.venv\Scripts\python -m pip install -e ".[dev]"` | Installed editable package and development tools. |
| `.\.venv\Scripts\python -m pytest -q` | 27 passed. |
| `.\.venv\Scripts\python -m openyield --output outputs/default --seed 7` | Success, 73 accepted steps, 18.25 simulated seconds. |
| `.\.venv\Scripts\python -m mkdocs build --strict` | Build succeeded; output `site/`. |
| `git diff --check` | Exit 0, no whitespace errors (Git emitted Windows line-ending notices). |
| `.\.venv\Scripts\python -m pip wheel . --no-deps -w dist` | Built local wheel; not published. |
| `python -m venv .venv-wheel` | Created clean environment. |
| `.\.venv-wheel\Scripts\python -m pip install --no-index --force-reinstall dist/openyield-0.1.0-py3-none-any.whl` | Installed built wheel with no runtime dependencies. |

From the **parent directory**, ran:

```powershell
& '.\openyield\.venv-wheel\Scripts\python' -m openyield --output wheel-smoke-output --seed 7
```

Observed success outside the source checkout, confirming that the installed
default scenario is available. The wheel smoke test outputs are in the parent's
`wheel-smoke-output/` folder, outside the Git repository.

Tests cover analytical contact/clearance fixtures, relative crossings and a thin
obstacle swept across between clear endpoints, strict scenario validation, initial
clearance failure, boundary contact, script success, timeout, deterministic trace
equality, fail-stop rejection, nonfinite rejected-state export and JSON/HTML outputs.

Visually inspected the generated HTML replay in the browser: initial frame 0,
B passing while A waited, frame 42 (10.50 s) during A's scripted lateral movement,
and final frame 73 (18.25 s), with A at (26, 2.5) and B at (4, 2.5). Road,
obstacles, passing space, both vehicles, labels and scrub/play controls rendered.
The first preview server was inaccessible due to process socket restrictions;
the accessible local preview used port 8766. The offline HTML needs no server.

Review caught two corrected issues: an initially over-wide corridor and rejected
nonfinite proposals breaking JSON export. Regression tests cover both. A Windows
test read also required explicit UTF-8 for the HTML file. No unresolved local
test/build failures remain in this record. Earlier implementation tests initially
failed because pytest/package files were not yet installed or implemented.

Acceptance: package installation/run, default reproducibility, output inspection,
monitoring tests, strict docs build and visual replay inspection passed locally.
Documentation distinguishes implemented behavior from proposed research; article
is a draft. PR/review and hosted CI status are reported separately in the handoff.
No merge, deployment, publication or release tagging was performed.
