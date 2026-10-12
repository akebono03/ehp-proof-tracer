# Phase 163 R4-R53: Definition Overlap Boundary Audit

This read-only audit compares the 19 definition candidates from Phase 163 R4-R52 against the 108 TeX units and 23 existing literature reference IDs in the Phase 163 R4-R47 snapshot.

**Limitation:** The snapshot does not include the typed mathematical content of all 67 Assertions; hence semantic equivalence or inclusion cannot be asserted. The audit establishes only exact TeX unit containment or direct introductory prose attachment.

## Requirements

Run from the repository root after R4-R42, R4-R47 and R4-R52 have generated their output folders. Python and pytest are required.

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r53_semantic_overlap_audit\run.ps1"
```

Output files under `phase163_r4_r53_output`: `overlap_audit.json`, `overlap_audit.csv`, `report.md`.

No production code, registry, IDs, original TeX, or catalog is modified. Only focused tests are executed.
