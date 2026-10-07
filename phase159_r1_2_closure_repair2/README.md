# Phase 159-R1-2 closure repair2

## Purpose

Repair the second Phase 159-R1-2 closure issue without changing proof depth or
reference policy.

The previous repair inspected only the selected presentation nodes. For
`pi_3^2`, the suspension isomorphism and the derived injectivity are farther
upstream than `max_depth=2`, although the retained `ProofStep` premises still
preserve that recursive ancestry.

This repair changes the dependency-visibility helper to traverse recursive
`ProofStep.premises` from the root step.

## Files changed

- `toda_group_proof_narrative_renderer.py`
  - replace the whole function
    `_phase159_restore_isomorphism_to_injective_dependency_visibility`
- `tests/test_phase159_r1_2_pi3_2_closure.py`
  - replace the whole test file
  - add a test proving the dependency exists in recursive ancestry

No imports are changed in production code.

## Run

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_2_closure_repair2" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_2_closure_repair2.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_2_closure_repair2\run_phase159_r1_2_closure_repair2.ps1"
```

The full pytest suite is intentionally not run.
