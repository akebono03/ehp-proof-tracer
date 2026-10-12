# Phase 163 R4-R49 — Read-only TeX candidate triage

This package lexically groups the R4-R48 review candidates. It does not decide whether a formula is an independent mathematical statement, and it does not register or allocate any statement IDs.

## Prerequisites

Run from the EHP Proof Tracer project root after R4-R42, R4-R47 and R4-R48. Python and pytest must be installed.

## Execute

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r49_candidate_triage\run.ps1"
```

The runner executes nine focused pytest tests and creates `phase163_r4_r49_output/triage.json`, `review_queue.csv`, and `report.md`. The complete original queue of 316 candidates is maintained, with source context and a lexical category attached to each.

## Boundaries

This package leaves the existing 108 TeX catalog source units, 23 references, 67 assertions, production registries, and TeX files unmodified. All review decisions remain `UNREVIEWED`. Only lexical duplicate and delimiter detection is automatic. A human mathematical review is necessary before registering additional assertions or definitions. The full pytest suite is not executed.
