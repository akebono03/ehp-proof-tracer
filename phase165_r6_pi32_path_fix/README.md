# Phase 165 R6: pi32 path correction

Repairs two migrated Phase 49 tests that incorrectly look for `phase165_r14_r39_toda51.tex` inside `tests/`. The source file is located at the repository root. This patch only replaces those paths and runs the three targeted tests. No production code or unrelated tests are modified. A backup is created before modification.
