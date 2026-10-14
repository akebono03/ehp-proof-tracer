# Phase 165 R27-R49: Remove legacy group-result seeding

This installer modifies only `phase165_r52_r5_auto_search.py` (function `search_group_structure_automatically`). Its default discovery path now starts from the unified statement registry, rather than first obtaining an assumed group structure from legacy `TodaCalculation` results. It preserves the caller-supplied `discovery` behavior, guards against unrecognized function structures, and creates a backup.

Run `run.ps1` from Windows PowerShell after extracting the ZIP in the project root. Only the targeted installer tests are run. The legacy `toda_calculation.py` public API and four remaining `repository_*` modules are retained for subsequent migration; no completed group calculation is claimed.
