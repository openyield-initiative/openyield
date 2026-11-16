# Roadmap

The later milestone scopes below are the agreed research direction. They are
planning stages, not release promises or established research results. v0.1 is
accepted as the scripted simulation foundation; later milestones have not started.

| Milestone | Intended scope | Evidence/status |
| --- | --- | --- |
| v0.1 | Geometry, deterministic script, monitors, replay, tests, local docs | Accepted and merged via [PR #2](https://github.com/openyield-initiative/openyield/pull/2) on 16 November 2026; see [development update](updates/v0.1.md) for evidence and limitations. No release tag. |
| v0.2 | Baseline Algorithms and Reproducible Scenarios: independent and fixed-priority strategies and reproducible encounter scenarios | Agreed scope; not implemented or validated. |
| v0.3 | Cooperative Negotiation | Agreed scope; not implemented. Protocol and evaluation design remain undecided. |
| v0.4 | Robustness and Experiments: communication failures, sensor uncertainty, sensitivity analysis and statistical comparisons | Agreed scope; not implemented or evaluated. |
| v0.5 | Scientific Publication: literature synthesis, mathematical formulation, results/discussion and manuscript | Agreed scope; not started. No publication or submission is authorized by this roadmap. |

## Implementation proposals for later review

The following suggestions are proposals within the agreed direction, not approved
changes to milestone scope or authorization to start later work:

- For v0.2, define progress, deadlock, failure, completion time and fairness metrics;
  make destination semantics controller-independent; add more bottleneck geometries;
  and verify equivalent information and local constraint enforcement across policies.
- For v0.3, consider a minimal decentralized, geometry-aware protocol with explicit
  state and disagreement handling.
- For v0.4, develop a scenario suite and controlled comparative experiments under
  the agreed robustness topics, with an explicit statistical analysis plan.

Review literature before choosing mechanisms or making novelty claims. Keep
communication and optimization outside v0.1. More realistic motion requires its
own validation. Detailed designs and experiments remain subject to review.
