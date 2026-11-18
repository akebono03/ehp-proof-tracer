# Phase 175 R4R10 — Cited Toda (5.8) and Proposition 2.5

This phase makes two existing Toda literature statements available to the shared, source-first proof-search engine. It does **not** re-prove equation (5.8), register a direct result for pi_9^5, assert an arbitrary sign, or replace the mathematical conclusion of Proposition 5.8.

The adopted Japanese transcription (`sources/toda/Toda_02_2.tex` and `Toda_05_2.tex`) is checked against pinned Git blobs and precise proposition/equation anchors. The original printed edition has not been independently verified. A cited, typed fixed statement (GIVEN) is registered for (5.8) and another for Proposition 2.5. The existing R4R7 dimension guard and signed-inference semantics are reused. The identity `iota_9 o E^2 eta_7 = eta_9` is an inference from the existing cited eta-family definition, not a new GIVEN.

The installer makes only two complete-function replacements in `phase165_r52_r9_shared_math.py`: `build_shared_typed_bridge()` and `shared_expansion_provider()`. No module imports, other functions, or shared search policy are changed. It validates committed Git content, local changes, source order, the previous R4R8 audit, and source-dependent inference replay. It exports the full resulting functions and full resulting module to the audit output directory, even in dry-run mode.

## Running on Windows

Expand the ZIP into the EHP Proof Tracer root and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r4r10_cited_58_prop25_public\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r4r10_cited_58_prop25_public\run.ps1"
```

The optional `-R4R8Report` parameter selects a specific successful R4R8 `report.json`. Without it, the audit finds the most recent report satisfying the R4R8 gate and evidence contract.

Only focused tests are run. Do not execute the full test suite until the end of Phase 175. The target pi_9^5 remains incomplete until its separate quotient and generator arguments are certified by ordinary proof search.
