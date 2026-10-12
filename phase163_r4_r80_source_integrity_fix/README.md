# Phase 163 R4-R80: Source Integrity Fix

This is a focused replacement for the R80 registration preflight script and tests. It verifies complete TeX file SHA-256 digests against the earlier R76 result at `phase163_r4_r76_output/numbered_boundary_crosswalk.json`, in addition to checking the eight extracted claim spans. This detects modifications outside the extracted spans without hard-coding machine-specific file hashes.

Extract the ZIP in the project root and run `run.ps1`. Requires previous R76 and R79 outputs. It adds only the R80 repair runner, implementation, and focused tests. The existing registry, proof logic, TeX source files, and root documentation remain unchanged. The focused test suite is run; the full suite is not run.
