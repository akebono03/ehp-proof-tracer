# Phase 166 R3-AI: Database-first typed group goals (limited step)

Run `run.ps1` from the repository root after extracting this directory there.

Files changed by the script: `phase166_r3af_goal_adapter.py` and `phase165_r55_nk_only_goal.py`.
Original files are backed up to `phase166_r3ai_db_goal_priority_backup/`.

The database now supplies typed goals first when it can parse them. Direct nonstable rows are eligible. When conversion is unsupported, the existing fixed-statement / generic-specialization route remains as a transitional fallback. CSV data are **not proof premises**.

Out of scope: zero-group goals, composite/decorated generator parsing, comprehensive 112-group conversion, publication-boundary redesign. This step does not claim those are complete. Run only targeted tests; do not run the full suite until the phase closes.
