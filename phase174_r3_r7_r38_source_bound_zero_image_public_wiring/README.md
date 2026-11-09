# Phase 174 R3-R7-R38 — Source-bound public zero-image chain

This package connects existing general rules for a suspension with zero image to the common proof-search context. It introduces no mathematical source assertions, root conclusions, stored proofs, or custom narrative rendering.

The R14 cited Toda (5.9) general annihilator is required to enable the provider. A group presentation loaded from `sphere.csv` is a **candidate subgoal only**; the ordinary proof engine remains responsible for checking whether a result is admissible and proving every other obligation. The package does not certify the resulting zero image or the root group.

Extract at the repository root, then run `run.ps1 -DryRun`, followed by `run.ps1`. Both commands run source guards; the regular execution changes one approved registry file and runs focused pytest groups. No git reset, checkout, or pull occurs. Full-suite pytest is intentionally omitted.

`CHANGED_FUNCTION_FULL.py`, `IMPORTS_FULL.txt`, and `CODE_FULL_JA.md` include complete replacement units and explanatory text. The review stops if the code, branch lineage, or tracked working tree differs from approved inputs.
