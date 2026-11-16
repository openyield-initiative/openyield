# v0.1 implementation plan

Spec: the supplied OpenYield milestone handoff, 16 November 2026.

Architecture: Python 3.12+, standard-library simulation; JSON configuration;
fixed-heading rectangles translated linearly per step. A separate monitor checks
continuous relative motion against axis-aligned forbidden rectangles. Rendering
consumes traces only. MkDocs and pytest are development dependencies.

1. Write analytical geometry and scenario validation tests, observe missing
   implementation, then add model and monitoring modules.
2. Test scripted success, timeout, fail-stop and determinism before implementing
   the simulation. Reject an unsafe proposed step and retain the last safe state.
3. Test output serialization, then add JSON trace/summary and portable HTML replay.
4. Document setup, exact semantics, limitations, research leads, provisional roadmap,
   decisions and draft article. Add Windows/Linux CI and strict MkDocs build.
5. Run fresh installation, full tests, default demo and strict docs build; inspect
   replay visually; review the complete diff and open a PR without merging.

Design decisions: no runtime dependencies or randomness; seed is recorded but
unused. Use conservative L-infinity clearance (a square margin), with exact
clearance allowed and physical contact prohibited. Road boundary is rectangular;
passing space is a labeled usable subregion, not proof of steering feasibility.
The demonstration starts one vehicle inside that space, waits while the opposing
vehicle passes, then translates laterally and proceeds. No planner or negotiation.

Review focus: nonfinite/bool values; unknown configuration keys; moving vehicles
crossing each other; exact margin equality; installed default scenario availability.
License and ownership remain owner decisions. No deployment or publication.
