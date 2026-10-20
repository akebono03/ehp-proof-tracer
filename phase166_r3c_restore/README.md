# Phase 166 R3-C temporary rollback

Run `run.ps1` from the extracted folder in the repository root. Restores the exact pre-R3-C backup of `phase165_r3_recursive_search.py`, after checking the current R3-C marker and saving the current source. It runs only `tests/test_phase165_r3_recursive_search.py`. It does not alter the R3-B order binder, public proof data, SQLite, or the renderer. Verify the pi_3^2 narrative manually after execution. No full pytest runs.
