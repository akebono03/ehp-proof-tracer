# Phase 169 R10E6 — Read-only direct-sum generator-image audit

This package diagnoses unresolved suspension-image obligations in the typed proof search for `pi_23^15` and `pi_24^15`. It changes **no production file, existing test, theorem registry, proof rule, or database**. All outputs are audit reports, not proofs.

## Requirements

- The project checkout on Windows with Python and pytest installed.
- Branch `develop` and either commit `c61bfaa72b75121c256518fbe37c7e8e27e5f815` or the earlier `d6c4bd745b2537ffe4da72a7a77865d3c00f6e18` containing a local R10E5 installation whose critical file blobs match the reviewed GitHub state.
- The R10E4 and R10E5 modules and related tests already present.

## Execute from the repository root

```powershell
Expand-Archive -Path "$HOME\Downloads\phase169_r10e6_direct_sum_open_image_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e6_direct_sum_open_image_audit\run.ps1"
```

The runner checks the branch, HEAD and reviewed source blobs, then executes **only focused pytest**, followed by the audit. No full-suite pytest is run. It restores or deletes any new audit output files on failure, preserving production files unchanged.

Read `phase169_r10e6_direct_sum_open_image_audit/output/audit.md` for component-level summaries or `output/audit.json` for individual suspension-image obligations and provider classifications.

## Interpretation

- A proposal is never a proved generator image.
- A generator-image inference observed in the search's `proven_steps` is not itself an independent trust-boundary replay.
- The database provides an authorized earlier premise; it does not provide generator-image equations.
- Missing rules for bar-nu, epsilon and mu should be investigated in cited source material, not invented or inferred from matching DB names.
- A `partial` result stays `partial` until the proof engine has discharged every obligation.
