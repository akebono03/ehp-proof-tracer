# Phase 174 R64R1 — Windows tmp_path Test Repair

This minimal package corrects exactly one focused pytest function in R64. The fixture `tmp_path` already exists, so its parent must be opened with `exist_ok=True`.

Run `run.ps1 -DryRun` before `run.ps1`. The installer checks pinned R64 test/audit/runner blobs and accepts either the original or already-corrected test. It changes no proof-search logic, bibliography, mathematical source, or renderer. All original R64 and R63 focused tests are re-run; no full-suite pytest is performed.

Reviewed repository: `akebono03/ehp-proof-tracer` `develop`; user-reported local commit `e5e392ddd2177fc4db70da48b1c1e6418b33c519`. HEAD equality is not required when the checked files match exact reviewed blobs.
