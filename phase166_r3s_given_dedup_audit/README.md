# Phase 166 R3-S — Read-only GIVEN Deduplication Audit

This bundle checks the existing Hopf-image duplicate `GIVEN` exclusion, without patching production code. The registry assertions must remain registered, while two specific redundant `Relation` proof links must not be supplied as independent `GIVEN` steps.

## Scope

- New files only: `audit.py` (`inspect_bridge`, `run_audit`, `main`), `test_audit.py` (three full unit tests), `run.ps1`, and this README.
- No production classes, functions, imports, renderers, or documentation files are modified.
- Executes the shared `pi_3^2` proof search and checks its source-anchored `GeneratorImage → Relation` ancestry using the preceding R3-R audit.
- Checks the narrative section markers for `pi_3^2` and `pi_4^3`. This is **not** a certification of every mathematical step in the `pi_4^3` proof.
- Lists unrelated `Relation` `GIVEN` links for later review; it does not delete them.

## Prerequisite

The previously installed directory `phase166_r3r_proof_tree_audit` must be present at project root, with `audit.py` inside it. The Phase 166 R3-Q module must also be installed.

## Run

From the EHP Proof Tracer project root in PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3s_given_dedup_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase166_r3s_given_dedup_audit\run.ps1"
```

Targeted tests: `python -m pytest -q phase166_r3s_given_dedup_audit/test_audit.py`.

Completion: all three tests pass, audit `pass=true`, `pi32_search_status=COMPLETE`, `pi32_image_relation_chain_verified=true`, no duplicate Hopf relation `GIVEN` links, and both web narrative section checks pass. Full pytest is reserved for Phase completion.

Next phase boundary: `pi_5^4` complete-proof restoration is excluded.
