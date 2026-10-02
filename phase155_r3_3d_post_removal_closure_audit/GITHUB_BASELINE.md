# GitHub baseline — Phase 155-R3-3D

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Re-inspected before R3-3D:
- Phase 109 decorated-sigma test file,
- Phase 132 web group proof mode tests,
- Phase 143 conclusion ordering tests,
- Phase 153 reference tests,
- Phase 154 ASCII punctuation tests,
- `tests/conftest.py`.

The public GitHub baseline still contains historical states that the user's
current local tree has intentionally moved past during Phase 155, including:
- the duplicate Phase 109 same-name test definition,
- pre-R3-3C-r2 stale expectations in Phase 132 / Phase 143.

R3-3D therefore audits the user's CURRENT local tree against the verified
Phase 155 audit artifacts rather than restoring the public baseline.

Authoritative Phase 155 inputs:
- R3-2F-r1: 332 verified pairs, 164 removable, 125 retain-independent,
  43 historical-keep, 0 needs-review.
- R3-3A: 161 unique deletion candidates, 0 cycle components,
  0 manual-review components.
- R3-3B: all 161 candidate functions safe, 5 whole-file deletions,
  0 unresolved files.
- R3-3C-r1: 161 test IDs removed, 5 whole files removed.
- R3-3C-r2: three post-removal stale expectations repaired and focused
  3/3 passed.

Repository-wide pytest remains deferred until Phase 155 closure.
