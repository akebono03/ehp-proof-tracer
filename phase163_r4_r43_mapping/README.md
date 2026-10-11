# Phase 163 R4-R43: TeX reference matching audit

This package classifies the 108 environments extracted by R4-R42 against the current Unified Statement Registry. It preserves the source order and does not modify TeX, the registry, Statement IDs, or proof search.

## Prerequisites

Run R4-R42 from the project root first. The following paths must exist:

- `phase163_r4_r42_output/extraction.json`
- `phase163_r4_r42_tex_extract/inputs/` containing the five original TeX files
- `phase163_r4_registry_bridge.py` and its dependencies

## Run

Extract this ZIP into the project root, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r43_mapping\run.ps1"
```

Focused tests: `python -m pytest -q phase163_r4_r43_mapping/tests/test_phase163_r4_r43_mapping.py`.

Output:

- `phase163_r4_r43_output/mapping.json`: machine-readable records
- `phase163_r4_r43_output/mapping.csv`: review spreadsheet with one row per environment
- `phase163_r4_r43_output/report.md`: unresolved items and existing reference gaps

Classification statuses: `EXISTING_REFERENCE`, `NEW_REFERENCE_CANDIDATE`, `UNRESOLVED_SYMBOLIC_LABEL`, `UNNUMBERED_ENVIRONMENT`, and `UNRESOLVED_TAG`. These are audit categories, not proof/registration statuses. All three `tex_registered`, `structured`, and `source_verified` flags remain `false` as no state is updated.

The source SHA-256 hashes are checked against the exact R4-R42 extraction before producing output. Symbolic labels are not converted to invented Toda numbering. Matching a reference does **not** equate to reusing or assigning an assertion/Statement ID. Subsequent bulk registration needs explicit component-level mapping, source boundary review, and an appropriate persistence mechanism. No full test suite is run in this step.
