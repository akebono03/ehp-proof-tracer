# Phase 144-6 R25-8R1-R1 — Semantic Route Audit

## Production changes

None.

The runner restores `toda_upstream_bootstrap.py` from Git HEAD and removes the
temporary R25-8 test if present.

## Why R1 is needed

R25-8R1 stopped before its audit because the existing Phase 144-6 R4
suppression control currently fails even after `toda_upstream_bootstrap.py`
has been restored to HEAD.

That failure is now diagnostic evidence rather than a prerequisite for the
semantic selection-boundary audit.

## Audit

The runner:

1. verifies relevant production files individually against HEAD;
2. runs stable semantic controls;
3. records the known R4 suppression control result without stopping;
4. compares depth 1, 2 and 3 for:
   - nu-prime bracket membership;
   - `DEFINITION_INTRODUCTION`;
   - `PRECONDITION`;
   - `PRECONDITION_FOR_DEFINITION`;
   - Narrative Argument roles;
5. prints the current frontier-hidden-step helper so the second-level premise
   protection can be compared with the semantic selection boundary.

## Boundary

No production repair is made here. The full test suite is intentionally not
run. The audit stops before deciding the next minimal repair.
