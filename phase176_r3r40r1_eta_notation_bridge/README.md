# Phase 176 R3R40R1 — typed eta notation bridge audit

R3R40 failed because the Unicode eta names in the R3R39 intermediate goal differ from the underscore names in the canonical Toda (5.5) statement. The actual types and names are printed separately. No global expression equality or source registration is changed.

This read-only audit supplies scoped backward expansions built from existing cited eta suspension, equality symmetry, transitivity and composition congruence rules. Each suspension witness remains an independently inferred obligation under the ordinary shared provider. The final audit checks the complete proof tree, including the six R3R39 steps and the independently inferred Toda (5.5) relation. It does not modify the default provider or prove the group structure.

Requires R3R40 and the committed R3R39R3 baseline. From the repository root, execute `run.ps1 -DryRun` then `run.ps1` in this directory. Only focused pytest paths are selected. The old R3R40 audit probe is not rerun. The final expected gate is `PASS_R3R40R1_TYPED_ETA_NOTATION_FOCUSED_TESTS`. The full repository suite is not run.

The original edition of Toda has not been independently verified; source provenance is inherited from the reviewed repository transcription.
