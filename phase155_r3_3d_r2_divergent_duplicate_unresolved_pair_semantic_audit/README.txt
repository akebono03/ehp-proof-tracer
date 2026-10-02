Phase 155-R3-3D-r2 — divergent duplicate / unresolved pair semantic audit

Purpose
-------
R3-3D-r1 found:
- 8 same-name duplicate test groups with divergent bodies,
- 2 unresolved removable pairs,
- no overlap between those two problem sets.

This subphase changes nothing.

For each duplicate-name group it records:
- every source definition and line range,
- normalized assertion expressions,
- call targets,
- the runtime definition actually bound after module import,
- assertions present only in shadowed earlier definitions.

For each unresolved pair it joins the two endpoints back to:
- R3-3A graph-node deletion-candidate state,
- R3-3B candidate-safety state.

This determines whether the next repair is:
- safe shadowed-definition cleanup,
- preservation/migration of unique hidden coverage,
- graph/safety mapping repair,
- or deletion-candidate execution repair.

No repository-wide pytest is run.
