# Phase 176 R3R38 — Isolated Right-Hopf Equality Transport

This package audits a **source-screened local replay** of right-Hopf equality transport, using existing generic inference rules. It does **not** install a shared proof-search provider, register new mathematical theorems, or complete the root group proof.

## Scope

The construction uses an independently inferred composite suspension equality and an independently inferred specialization of Toda Proposition 2.2. Six ordinary inference steps apply equality under left composition, equality preservation by EHP H, symmetry, and transitivity.

The output corresponds to a concrete Hopf relation involving the right-associated composite of two suspended eta generators. It does not prove a relation to Toda (5.5), nor a group structure.

## Files

- `source.py`: typed input validation and existing-rule replay, with no new inference rule.
- `audit.py`: source-screened, read-only public-candidate replay and JSON report.
- `tests/test_source.py`: focused validation of the general replay and fail-closed guards.
- `run.ps1`: PowerShell DryRun, audited replay and focused tests.
- `AUDIT_PLAN_JA.md`: Japanese audit plan and proof boundaries.
- `CODE_FULL_JA.md`: complete added code and test file contents.

## Execution

From the project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r38_equality_transport_isolated\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r38_equality_transport_isolated\run.ps1
```

The report is saved under `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r38_equality_transport_isolated\report.json` (or the platform's temporary directory if `LOCALAPPDATA` is unset).

No full test suite is executed.
