# Phase 174 R3-R7-R9 — Typed Composition Associativity Preflight

This package audits a structural mismatch between a right-associated database generator and a left-associated Toda composition. The new, isolated inference rule transports **only a separately proved generator image** through reassociation of composition; it does not supply any new reference fact, group result, or proof tree leaf.

## Files

- `rule.py`: generic, source-independent reassociation rule with one certified child obligation.
- `audit.py`: source-first GitHub HEAD and pinned-blob checks, certified R8 evidence, and live provider diagnostics.
- `tests/test_rule.py`: algebraic and negative-case checks.
- `tests/test_audit.py`: source, prior-report, and fail-closed SHA checks.
- `run.ps1`: dry run and full read-only audit, each with focused tests in independent pytest processes.
- `AUDIT_PLAN_JA.md`: Japanese review plan.
- `CODE_FULL_JA.md`: complete code and test listings.

## Running

Extract `R9.zip` into the root of a checked-out `develop` branch of `akebono03/ehp-proof-tracer`. The exact audited HEAD is `15785b921c15a19810b2b067715832ee20c61280`. Previously generated R8 evidence must exist at `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r8\composite_image_gap.json`.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r9_composition_associativity\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r9_composition_associativity\run.ps1"
```

The report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r9\composition_associativity.json`. Production inference providers, the database, the web renderer and existing tests are not modified. A candidate is not a proof. Full pytest is deferred until the end of Phase 174.
