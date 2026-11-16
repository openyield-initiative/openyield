# Decision log

Decisions made for v0.1 on 16 November 2026; routine implementation choices.

| Decision | Reason and consequence |
| --- | --- |
| Python 3.12+, standard-library runtime | Small installable package; pytest/MkDocs only for development. Windows and Ubuntu CI use 3.12. |
| JSON scenarios, strict keys and numeric validation | Inspectable configuration without a runtime parser dependency; typos fail explicitly. |
| Centres, fixed headings, rectangular envelope | Analytical continuous checks are understandable; cannot represent steering or realistic bay entry. |
| Start A inside passing space | Shows waiting/passing without pretending to solve bay entry. Scripted lateral exit remains physically simplified. |
| Closed physical contact, square clearance, exact margin allowed | Conservative and testable semantics, with diagonal over-rejection relative to Euclidean clearance. |
| Relative-motion slab checks | Prevent tunneling under linear fixed-footprint motion; no sampled substep approximation. |
| Reject entire unsafe step | Fail-stop preserves accepted history and records attempted state; does not estimate impact time. |
| No randomness, seed recorded only | Exact deterministic trace comparison without incidental metadata. |
| Self-contained HTML canvas replay | Portable offline output with playback and scrub controls; rendering has no controller role. |
| No license selected | Owner must decide license and copyright ownership before open-source distribution claims. |

Considered alternatives: sampled collision checking can miss crossings; a general
motion planner would exceed the milestone; GIF export introduces extra tools and
lacks scrubbing. The chosen vertical slice prioritizes explicit assumptions.
