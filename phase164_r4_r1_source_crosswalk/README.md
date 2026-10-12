# Phase 164 R4-R1 — Two-leaf source crosswalk audit

This package performs a **read-only** audit of the two literature-derived input `ProofStep` objects for the existing `E: pi_4^2 -> pi_5^3` reconstruction. It looks up source-locator candidates in the actual Phase 163 R94 archive and reports their source Statement IDs. This is not a proof of mathematical equivalence, citation eligibility, or original-edition publication order.

Run from the repository root after extracting the archive:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase164_r4_r1_source_crosswalk\run.ps1
```

The script installs only two new audit files and runs explicitly named focused tests, then creates `phase164_r4_r1_output/report.json` and `report.md`. The full test suite is not run. Existing production modules, source archives, and documentation are not altered.

The archive's `proof_eligible_count` must remain zero. A unique locator match does not authorize a statement, and the unverified source TeX publication position is not a usable proof-completion position.
