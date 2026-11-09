# Phase 174 R3-R7-R43: Conditional public EHP map-property providers

This patch connects the already tested R5 Hopf-injectivity rule and the R37 upper-Delta-surjectivity rule to the common backward expansion provider. It does not change the mathematical inference rules, the Web renderer, database admission, or the existing R41 zero-image adapter.

The patch changes only `phase165_r52_r9_shared_math.py` (one complete function: `shared_expansion_provider`). The guarded installer writes a full copy of the revised function to `CHANGED_FUNCTION_FULL.py` and the complete preceding import section to `IMPORTS_FULL.txt` after installation. New package modules are provided in full in `CODE_FULL_JA.md`.

## Running on Windows

Extract `R43.zip` at the repository root on `develop`, run `phase174_r3_r7_r43_public_ehp_map_property_wiring/run.ps1 -DryRun`, then run the same script without `-DryRun`. The script runs only focused pytest groups; the full suite is reserved for the phase closeout.

## Proof boundary

A returned `GoalExpansion` is an unproved candidate. R37 still requires four independent inferred premises; R5 still requires separately inferred zero image and EHP exactness. The adopted database prior remains a distinct `GIVEN`, never a fabricated literature citation. The bounded scoped probe does not claim a completed proof or an HTTP verification of the Web view.
