# Phase 166 R3-AQ: Stable Generator Notation

This minimal patch uses the canonical `latex` field from `data/HyoujiGen.csv` to index all `kinds=0` generator families, rather than treating non-eta/nu/sigma/iota families as exceptional suspensions.

## Target

- `phase166_r3aj_structured_generator.py`: replace the complete `_base_element()` function.
- No import changes, no API changes, no proof-search changes.
- `test_r3aq.py`: four targeted checks.

## Run

Extract the ZIP into the repository root and execute `phase166_r3aq_stable_generator_names/run.ps1` from PowerShell. It backs up the production file and runs targeted pytest only.

## Completion

`pi_20^12` displays indexed barred nu and epsilon; exceptional `nu'` still uses suspension. Full pytest is reserved for the end of Phase 166.
