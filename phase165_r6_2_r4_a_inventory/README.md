# Phase 165 R6-2 R4-A: Read-only Rule Inventory

This package performs an AST-only inspection of top-level Python modules, production search connections, and tests under `tests/`. It does not import project production modules, modify existing source files, or certify mathematical soundness.

## Run on Windows PowerShell

From the `ehp_proof` repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase165_r6_2_r4_a_inventory.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_2_r4_a_inventory\run.ps1"
```

Outputs are created at `phase165_r6_2_r4_a_inventory/reports/rule_inventory.json` and `.md`. Only five targeted tests are run. The full test suite is not run. No project production files are changed.

## Scope and limitations

Factory eligibility is inferred statically and must not be interpreted as successful runtime discovery. A syntactically visible provider call is not proof that a particular rule is usable for a goal. Dynamic or nested factory registration may require additional review. Archived patch copies are excluded from the live inventory.
