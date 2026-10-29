# Phase 170 R2 — Reviewed R1 HEAD Transition Repair

This is an independent, new read-only R2 audit package. It leaves the original
`phase170_r2_database_utilization_audit` package and all saved audit reports untouched.

The original R2 runner refused Git HEAD `f9e9a9d59970943d967e2cbcb0a98f13b2471407`
because it was pinned to the earlier R1 HEAD. GitHub confirms that the transition
from `790db364a8531693572fc510f969da831f1f9ffb` contains exactly one commit,
`170-1`, adding the six files of `phase170_r1_current_capability_audit` and no
production or data files.

The repaired gate verifies the explicit old/new SHA pair, actual Git ancestry,
and the exact six added file paths. It separately checks all previously reviewed
production file blob hashes and the original twelve-case R1 audit flags. No
arbitrary future HEAD, added files, or changed production is accepted.

The R2 functionality is unchanged: inspect database utilization of the actual R1
sample without rerunning Backward Search or changing mathematics. Run in the
existing repository root:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase170_r2_head_sync_r1.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase170_r2_head_sync_r1\run.ps1"
git status -sb
```

Results are written to a new timestamped folder in
`%LOCALAPPDATA%\EHPProofTracerRecovery`. The runner executes only its
focused tests, never the full pytest suite. A successful audit means that
the diagnostic evidence was collected, not that every group has a proof.
