# GitHub baseline — Phase 155-R5

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Before R5, current GitHub tests were re-inspected.

Examples supporting the boundary:
- `tests/test_phase72_probe.py` explicitly renders `Historical only:`.
- Phase 144 narrative completion tests import `audit_phase144_*` modules and
  perform inventory/completion audits.
- Cross-group/population tests iterate representative groups and are suitable
  for non-routine audit/heavy lanes rather than the normal feedback loop.
- Some files contain the word `snapshot` only for local immutable-object
  checks, so `snapshot` alone is not treated as historical or heavy evidence.

Therefore R5 uses conservative, strong evidence and leaves ambiguous residual
tests retained.

No production/test changes are made.
No test bodies or repository-wide regression are executed.
