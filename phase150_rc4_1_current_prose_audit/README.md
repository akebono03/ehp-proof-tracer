# Phase 150 / RC4-1 — Current prose audit

This package performs an audit only. It does not modify production code or existing tests.

## Purpose

Compare the current generic `pi_6^3` Narrative with the established Phase 136-2 historical baseline at the level relevant to RC4:

- facts/equations already present,
- missing explanatory dependency prose,
- provenance/reason relations that can potentially be generated generically.

The audit deliberately does not redesign RC3 ordering, add RC5 EHP semantic naming, or change RC6 equation numbering.

## Files

- `audit_phase150_rc4_1.py` — audit program.
- `run_phase150_rc4_1.ps1` — Windows PowerShell runner.
- `audit_output/` — created when the audit runs.

## Run

From the repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase150_rc4_1_current_prose_audit.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase150_rc4_1_current_prose_audit\run_phase150_rc4_1.ps1"
```

## Focused tests

The runner executes only the related focused tests:

```powershell
python -m pytest -q `
  ".\tests\test_phase134_9_pi6_3_snapshot.py" `
  ".\tests\test_phase142_3_generic_proof_text.py" `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py"
```

Repository-wide tests are intentionally deferred until the end of Phase 150.

## Completion condition

RC4-1 is complete when the audit:

1. renders the current `pi_6^3` generic Narrative;
2. identifies reason/provenance prose gaps without changing production behavior;
3. separates RC4 gaps from RC3 ordering, RC5 naming, and RC6 formatting;
4. provides a stable input classification for RC4-2.
