# Phase 165 R12-R34-R4: Scope Gate

This is a read-only, limited scope audit, **not the R4 renderer repair**.
It checks that existing shared renderer functions still expose reference-internal suppression and short-exact support ordering. It confirms the previously identified foundational GIVEN reference. It deliberately does not claim to inspect the active pi43 proof tree or to modify narrative presentation.

## Run

Extract the archive at the project root, then run:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase165_r12_r34_r4_scope_gate\run.ps1"
```

Focused tests only; full-suite pytest is reserved for Phase closure.
