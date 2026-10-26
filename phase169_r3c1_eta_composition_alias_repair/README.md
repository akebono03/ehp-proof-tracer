# Phase 169 R3C1 — Eta Composition Name-Identity Repair

This repair addresses a failed live proof audit after the first R3C patch was automatically restored. The R3C fixture used canonical eta elements, whereas the structured database uses Unicode-subscript names. These are equivalent only when the existing `_matching_eta_name` contract confirms exact family, index, dimension, source and target. The repaired composite-image inverse generates two **canonical**, provable `GeneratorSuspension` subgoals while checking all four factors of the actual database goal.

## Scope

- **One production module only:** `phase165_r12_r21_eta_generator_chain.py`.
- **Compared with the restored GitHub baseline:** add `_composition_eta_suspensions()` and `composition_eta_suspension_image_rule()` immediately after `suspension_to_generator_image_rule()`, and replace the entire `expand_cited_eta_generator()` function.
- **Compared with the failed R3C proposal:** only `_composition_eta_suspensions()` has been corrected. Complete replaceable definitions for all three functions are in `full_functions/`, and the complete module is in `full_files/`.
- Import change relative to the restored baseline: `from expression import Composition, HomotopyElement`. The full resulting import section is in `imports_full.py` and the full module.
- Five new regression tests exercise Unicode-subscript aliases, the **actual ID-database goals**, rejection of incorrect family/dimension/name, and canonical premise generation. The previous seven R3C tests are included unchanged.
- `audit.py` runs the actual screened typed proof search. It writes `output/composite_image.json` even when the image cannot be proved, and the command exits nonzero and restores on such failure.
- The patch only applies to the GitHub 5f340986-reviewed baseline after R3C's automatic restoration. Unknown local changes are rejected.
- This does **not** prove the EHP isomorphism or finish the pi5^3 group proof. No statement or isomorphism is added as GIVEN.

## Execute on Windows PowerShell

Run `run.ps1` inside the extracted package in the EHP repository root. It will back up the only changed module, run focused pytest, audit the live composite-image derivation, and restore on failure. The full pytest suite must be reserved for the end of Phase 169.
