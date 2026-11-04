# Phase 173 R15R17-R3R4: Historical Test Contract Correction

This package updates historical test expectations after the verified abstract proof tree was connected to the one canonical `ProofNarrativeModel` and rendered by the shared Narrative renderer.

**Scope:** Ten reviewed test files only. No production implementation, proof search, type, bibliography, Web adapter, or documentation outside this package is modified. All changes replace complete test functions or selected assertions within those functions. Tests are never skipped, deleted, or marked as expected failures.

The current public model route displays a single Reference list, actual verified `ProofStep` records, an abstract-group isomorphism only when certified, and unchanged named-generator open goals. It does not append separate abstract certificate or verified-tree progress sections. Existing dedicated helper APIs and explicitly selected legacy routes still have their former interfaces; their direct tests remain intact.

## Installation

Extract `EHP_Phase173_R15R17_R3R4_TEST_CONTRACT_CORRECTION.zip` at the root of `akebono03/ehp-proof-tracer` (`develop`). Run `run.ps1 -DryRun` before running `run.ps1` without flags. The runner fetches `origin/develop` and checks that both local and remote refs descend from reviewed commit `a4e01bcafcd2afd295c61843bbaa597a6262f75a`. Each of the ten tracked test files must have its reviewed Git blob unchanged and no preexisting staged or unstaged edits. Unrelated Git index entries are preserved.

DryRun generates `FULL_CHANGED_UNITS.md`, containing the entire revised test functions, unchanged import blocks, and the complete new tests. Normal installation saves byte-for-byte backups and a hash manifest, runs focused regression tests, and restores only its ten files if tests fail. Run `run.ps1 -Restore` to restore after a successful install, provided their content and the Git index have not changed.

## Completion criteria

`R15R17R3R4_DRY_RUN=PASS`, `R15R17R3R4_INSTALL=PASS`, `R15R17R3R4_FOCUSED_PYTEST=PASS`, `R15R17R3R4_GIT_INDEX_PRESERVED=PASS`, and `R15R17R3R4_APPLY=PASS`.

Only targeted pytest runs are performed; the full suite is reserved for the Phase 173 closeout.
