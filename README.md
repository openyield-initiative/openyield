# OpenYield

Research into decentralized cooperation between autonomous vehicles on narrow
roads. **v0.1 is a scripted simulation foundation**, not a negotiation algorithm,
validated driving baseline, comparative result, or real-world safety system.

Research question: Does decentralized, geometry-aware negotiation improve
efficiency and reliability in narrow-road encounters compared with independent
decision-making and fixed-priority strategies?

## Quick start (Windows PowerShell, Python 3.12+)

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m openyield --output outputs/default
.\.venv\Scripts\python -m mkdocs build --strict
Start-Process outputs/default/replay.html
```

No activation or PowerShell execution-policy change is required. On Linux/macOS,
use `python3` to create the environment and `.venv/bin/python` thereafter.
Simulation has no runtime dependencies. Development tools require package-index
access on first installation. Python 3.12 is the documented CI environment.

See [getting started](docs/getting-started.md), [model semantics](docs/model.md),
[research context](docs/research.md), and [roadmap](docs/roadmap.md).
Run `.\.venv\Scripts\python -m mkdocs serve` for the local documentation website.
The introductory article is a draft; no site is deployed.

License and copyright ownership await the owner's decision. No license has been
selected; public visibility alone does not grant an open-source license.
