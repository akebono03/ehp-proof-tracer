# Phase 165 R27-R28

This package removes two orphaned legacy proof-construction bootstrap modules:
`toda_prop58_zero_bootstrap.py` and `toda_prop511_zero_bootstrap.py`.

It deliberately retains `toda_prop56_zero_bootstrap.py`, shared proof-step factories, rules, and the unified statement registry. A root-level production Python import audit blocks deletion if an active dependency remains. Deleted modules are backed up under `phase165_r27_r28_removed_backup/`. Historical tests and nested phase archives are not rewritten in this phase.

Run `run.ps1` from the extracted package folder. Only focused tests run. Full pytest is deferred to the end of Phase 165.
