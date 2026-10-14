# Phase 165 R27-R21

Removes the legacy Toda calculation lookup from the *modern* automatic typed proof search. This prevents the new search from treating an old repository result as a typed goal candidate and removes its runtime dependency on `toda_calculation_facade`.

The old `toda_calculation_facade.py` is intentionally kept unchanged in this phase: its legacy report types cannot represent PARTIAL or SEARCH_FAILED, and its existing group-query consumers still depend on it. A follow-up must migrate those consumers before removing the old bootstrap.

Extract at the repository root, then run `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r21\run.ps1`.

Targeted tests only. No full test suite.
