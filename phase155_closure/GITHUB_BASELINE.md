# GitHub baseline — Phase 155 Closure

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before Closure:
- README.md
- docs/design.md
- docs/development_log.md
- docs/roadmap.md
- docs/proof_records.md
- tests/conftest.py
- historical Phase150 performance/final-regression tooling.

Relevant established practice:
- repository-wide regression is `python -m pytest tests -q`;
- previous phase-final runs used `--durations`;
- bounded performance diagnostics were kept distinct from full regressions;
- tests/conftest.py supports canonical test helper imports.

Local Phase155 evidence supplied by the user is authoritative for the current
post-cleanup state:
- R4 canonical source test IDs: 9069;
- R5 lanes: 9069 canonical, 65 historical, 293 audit, 31 heavy, 664 residual;
- R6 collection: 21/21 batches PASS;
- R6 bounded runtime probes: 12/12 PASS after stale-expectation repairs.

Closure intentionally performs the phase-final full repository pytest once,
with visible progress and a persistent log.
