Phase 144-6-R5-43-9-R2 PowerShell Copy-Item repair

Repair only:
- run_phase144_6_r5_43_9.ps1
- Replace invalid Copy-Item parameter -DestinationPath with -Destination.

Unchanged:
- audit_phase144_6_r5_43_9.py
- test_phase144_6_r5_43_9.py
- all production code

The original R5-43-9 run stopped before copying files or running pytest because
PowerShell rejected the first Copy-Item command.

No full test suite is run.
