# Provisional roadmap

These are planning stages, not release promises or established research results.

| Milestone | Intended scope | Evidence/status |
| --- | --- | --- |
| v0.1 | Geometry, deterministic script, monitors, replay, tests, local docs | Implemented on the feature branch; see development update for verification. Pending review, no release tag. |
| v0.2 | Define and implement independent and fixed-priority controllers with common local constraint enforcement | Proposed; not implemented or validated. |
| v0.3 | Minimal decentralized geometry-aware negotiation, with explicit state and disagreement handling | Proposed; protocol and evaluation design undecided. |
| v0.4 | Scenario suite and controlled comparative experiments | Proposed; metrics, baselines and statistical analysis not yet established. |
| v0.5 | Robustness investigation and research synthesis | Proposed; uncertainty and communication conditions need a separate approved design. |

For v0.2, first define progress, deadlock, failure, completion time and fairness
metrics; make destination semantics controller-independent; add more bottleneck
geometries; verify equivalent information and constraints across policies. Review
literature before choosing mechanisms or making novelty claims. Keep communication
and optimization outside v0.1. More realistic motion requires its own validation.
