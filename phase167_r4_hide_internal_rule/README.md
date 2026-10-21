# Phase 167 R4-1: Hide One Internal Rule Label

Scope: only suppress the exact public display of `infinite cyclic quotient structure`. No inference, registry, ProofStep, routing or other prose changes.

## Modified production function

- File: `toda_group_proof_narrative_shared_components.py`
- Function: `_render_generic_narrative_step()` (complete post-patch function exported at runtime to `modified_function_full.py.txt`)
- Imports: unchanged.

The patch checks that the current fallback is exactly the known implementation before editing; otherwise it aborts. `run.ps1` backs up the original file, compares five 1-stem groups before/after and runs focused pytest. A failed comparison or test restores the backup. This ZIP does not test the full suite.

Run from the repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase167_r4_hide_internal_rule.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase167_r4_hide_internal_rule\run.ps1"
```

Next phase boundary: no equation deduplication, theorem terminology or LaTeX normalization is included.
