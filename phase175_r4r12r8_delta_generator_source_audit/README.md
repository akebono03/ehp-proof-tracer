# Phase 175 R4R12R8 — Source-first Delta Generator Image Audit

This package performs a read-only audit of the adopted Toda Chapter V source for the generator image `Delta(eta_9) = E(nu') o eta_7`. It explicitly does **not** prove the identity in the application's typed proof engine.

## Files

- `audit.py`: repository/source/rule inspection and JSON report.
- `tests/test_audit.py`: four isolated focused contract tests.
- `run.ps1`: PowerShell execution, with optional `-DryRun`.
- `AUDIT_PLAN_JA.md`: Japanese mathematical and engineering audit plan.
- `CODE_FULL_JA.md`: full source of all added executable code.

## Usage

Extract at the root of `akebono03/ehp-proof-tracer` on branch `develop`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r8_delta_generator_source_audit\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r8_delta_generator_source_audit\run.ps1
```

Reports are written under `phase175_r4r12r8_delta_generator_source_audit/output/` (untracked). The package neither modifies production code nor executes the full pytest suite.

The expected success gate is `PASS_R4R12R8_ADOPTED_SOURCE_FOUND_TYPED_PROOF_PENDING`. This gate does not imply the completion of the target group proof. The source examined is the repository's adopted TeX transcription, not a separately authenticated scan of the original printed book.
