# Phase 174 R2R1 — Reviewed HEAD Lineage Correction

The previous R2 DryRun stopped before any mathematical audit because
`develop` advanced from `cb85913905b2f7452bda2a2c4428e6fe5a3a793a` to `3558d713fd7939ded656f2458aacc62d71c7e0b3`.
GitHub comparison confirms exactly one intervening commit: Phase 174
R1/R1R1 files were committed and the legacy focused test was corrected.
Toda source files and proof-search production files were not changed.

This package changes only the untracked Phase 174 R2 audit runner and its
audit module. It preserves the original Phase 174 R1 report's historical
HEAD `cb85913905b2f7452bda2a2c4428e6fe5a3a793a` and separately records the current HEAD
`3558d713fd7939ded656f2458aacc62d71c7e0b3`. It checks ancestry and content hashes before proceeding.
The original R1 JSON is not rewritten or recreated.

## Replaced units

* `phase174_r2_source_math_audit/run.ps1` — complete script, only the
  reviewed HEAD and ancestry/source-guard checks are changed.
* `phase174_r2_source_math_audit/audit.py` — complete module, separates
  `REVIEWED_HEAD` from `R1_BASELINE_HEAD` while preserving all inference
  and output semantics. The complete `audit_prior_record()` is included.
* New `phase174_r2r1_head_lineage_fix/tests/test_head_lineage.py` — three
  focused tests of original R1 evidence and the new R2 review head.

No registered theorem, production code, Narrative renderer, main document,
or existing test is modified. Source evidence and open goals are unchanged.

From the repository root, after extracting this correction ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r2r1_head_lineage_fix\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r2r1_head_lineage_fix\run.ps1'
```

The normal runner executes the three lineage checks and then the original
R2 DryRun, R2 read-only audit, and limited pytest regressions. It never
performs `git pull`, `reset`, `clean`, `checkout`, `commit`, or `push`.
