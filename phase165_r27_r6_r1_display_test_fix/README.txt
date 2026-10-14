Phase 165 R27-R6-R1: Fix five stale HTML status assertions.

Actual common narrative renderer maps ProofSearchStatus.SEARCH_FAILED to
"証明未完成" and intentionally does not print the internal enum "search_failed".
This package changes ONLY test assertions to the public Japanese status.

Files modified:
- phase165_r27_r6/test_phase165_r27_r6_legacy_entry_cut.py (1 assertion)
- test_phase165_r52_r5_auto_search.py (2 assertions)
- test_phase165_r52_r4_flask_connection.py (2 assertions)

Run from repository root via run.ps1. This runs three focused test files.
No production source or historical proof-building files are changed.
Full pytest is intentionally NOT run.
