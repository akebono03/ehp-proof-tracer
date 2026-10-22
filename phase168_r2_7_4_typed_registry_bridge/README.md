# Phase 168 R2-7④ — Typed Literature Registration

This package connects previously authored explicit mathematical statements for Toda Proposition 5.3 (four components) and Proposition 5.6 (five components) to the default shared bridge. It uses existing registration validators, without importing old proof outputs. The registration carries mathematical conclusions as indexed source statements, not completed derivations or pre-created `ProofStepLink` objects.

Only `build_shared_typed_bridge` in `phase165_r52_r9_shared_math.py` is patched. The original file is backed up under `backup/`. The complete resulting function is saved in `build_shared_typed_bridge_full.py`.

Run `run.ps1` from PowerShell. Only focused tests are run; full-suite pytest belongs at the end of Phase 168. The original registration input module still calls its records source-unverified. This is provenance metadata, not a new search gate. Source text was independently compared for the main group statements, but proof completeness and specialization are outside this step.
