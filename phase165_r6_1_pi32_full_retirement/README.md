# Phase 165 R6-1: legacy π₃² search retirement

This package removes the root `phase165_r14_r34_backward_search.py`, deletes the historical π₃² leaf-search and proof-reconstruction functions from R35/R36/R38 while retaining typed source registration, and removes four historical test files where present. It also removes the obsolete R38 replay-only test from two copies of the R52 shared math test, leaving the common-search tests in place.

`apply.py` uses AST-based definition removal and preserves locally modified source registration from earlier R6-1 patches. It refuses to modify files if independent adopted-source registration is missing, if an active root module still imports a removed module, or if preexisting backups could be overwritten. All original files are copied to `phase165_r6_1_pi32_retirement_backup/` before changes.

`run.ps1` performs three focused tests only. This does not certify all historical installer duplicates or the complete test suite; all-Phase pytest is deferred to the end of Phase 165.

No π₄³ adapter is changed here. Phase R6-2 is responsible for replacing its group-specific backward expansion with common rules.
