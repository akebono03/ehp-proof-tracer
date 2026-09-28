# Phase 144-6 R25-11-R4 Closure-Origin Boundary Audit

## Purpose

Separate two potentially different regressions:

1. the depth=2 semantic-closure path used to recover the nu-prime definition;
2. the full-depth six-group contribution population regression from 190 to 192.

No production repair is made in this package.

## Files, classes, functions, and methods changed

Production files changed: none.

Existing tests changed: none.

Audit-only files added:

- `audit_r25_11_r4.py`
- `test_phase144_6_r25_11_r4_closure_origin_boundary.py`
- `run_phase144_6_r25_11_r4.ps1`
- `README.md`

Production functions inspected before this audit:

- `build_toda_group_proof_narrative_semantic_closure_presentation`
- `build_toda_group_proof_narrative_semantic_sidecar`
- `build_toda_group_proof_narrative_ordered_contributions`
- `_build_visibility_occurrences`
- `_toda_group_proof_narrative_argument_frontier_hidden_step_ids`

Related tests inspected:

- `test_phase144_6_r5_18_production_generic_proof_chain_foundation.py`
- `test_phase144_6_r5_43_11c_r2_argument_participation_guard.py`

## What the audit establishes

### A. Closure origin

For depth=2 pi_6^3, compare the original presentation and semantic-closure
presentation by `ProofStep` identity.

The current closure implementation reuses provenance `ProofStep` objects, so
the identity difference precisely identifies closure-added steps.

### B. Ownership before and after closure

Build blocks, semantic sidecar, arguments, proof chains, visibility
occurrences and ordered contributions for both presentations.

Every selected contribution is marked as either:

- `original`
- `closure_added`

### C. Full-depth boundary

Rebuild the six representative full-depth contexts without semantic closure
and report their selected contribution counts.

This determines whether 192 vs 190 is actually caused by semantic closure or
is an independent ownership regression.

## Focused pytest

```powershell
pytest -q `
  ".\phase144_6_r25_11_r4_closure_origin_boundary_audit\test_phase144_6_r25_11_r4_closure_origin_boundary.py"
```

## Completion conditions

R25-11-R4 is complete when:

- original step identity is preserved through semantic closure;
- closure-added steps are explicitly identified;
- depth=2 ownership before/after closure is classified by origin;
- full-depth six-group selected population is measured without semantic
  closure;
- we can state whether closure-origin and 192-vs-190 are the same regression
  or two independent regressions.

## Next Phase boundary

R25-11-R4 does not change production ownership rules.

Only after this audit identifies the boundary should R25-11-R5 introduce a
minimal general production repair.

No full pytest is run in R25-11-R4.
