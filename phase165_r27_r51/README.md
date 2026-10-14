# Phase 165 R27-R51

This installer migrates the Web Group Query entry away from the legacy `build_standard_toda_report()` call and into the canonical typed registry-backed group search. Only complete, renderable group-structure conclusions are reported as FOUND; partial and unresolved results are NOT_FOUND in the existing public view contract.

It replaces the complete `build_standard_web_group_query_view()` function in `web_group_query.py` and removes two now-obsolete imports. Other files and the legacy calculation APIs remain unchanged. A backup is stored in `phase165_r27_r51_backup`, and an audit JSON is written to the repository root. The operation is safe to repeat and fails closed for unexpected source structures.

Execute `run.ps1` from PowerShell after extracting the ZIP in the repository root. Only package-local targeted tests are run, not the full suite.
