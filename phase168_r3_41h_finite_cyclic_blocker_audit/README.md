# Phase 168 R3-41H — Finite Cyclic Premise Audit

This is a read-only diagnostic package. It repeats two existing typed backward searches and inspects the exact finite cyclic structure goals that have no backward expansion. It compares these goals with the screened `GIVEN` proof links and fixed assertions, and separately lists registered backward rule templates.

It does not certify a source, add a rule, change the proof model, or alter rendering. A registered template is a *candidate*, not a completed proof.

## Run

From the repository root in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File '.\phase168_r3_41h_finite_cyclic_blocker_audit\run.ps1'
```

The script runs focused pytest cases and then exports `output/audit.json`, `output/audit.md`, and `output/review_bundle.zip`. The previous `phase168_r3_41g_zero_step_search_trace` audit package must be present in the repository working directory. The complete test suite is not run.
