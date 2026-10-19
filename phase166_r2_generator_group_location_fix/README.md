# Phase 166 R2 Generator/Group Input Location Repair

Unzip at the repository root and run `phase166_r2_generator_group_location_fix/run.ps1` in PowerShell.

This read-only audit uses repository-root CSV files first, then `data/` and finally the two uploaded CSV inputs bundled under this package's `data/`. The input path is printed. No production files are modified and no proof authority is granted. Targeted pytest only.
