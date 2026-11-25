# Phase 176 R3R51 — Verified DB prior acceptance for finite cyclic subgroup lift

This package modifies only the existing finite cyclic subgroup lift and its public context wiring. The codomain premise may be a freshly verified ordered DB prior; the other four premises remain INFERENCE. No new mathematical theorem, GIVEN registration, DB admission policy, or renderer behavior is introduced.

Reviewed develop HEAD: `d1130527b2a55d085f650c3982f923576a2ffbaf`.

Run `run.ps1 -DryRun` first. The first full run checks the actual public baseline (all five premises accepted but the original rule rejecting the codomain prior), applies the guarded patch, runs each focused test independently, and checks a complete root proof on the actual public Web path. An already-applied rerun skips the historical baseline only. The installer refuses unreviewed file contents or partial application, preserves line endings, and emits `CHANGED_FUNCTIONS_FULL_JA.md` containing complete changed function and import sections. No Git commit is made. Full pytest is not run.

R44's historical installer test uses the reviewed pre-R51 shared blob, while R48's installer recognizes only the exact R51 successor of its shared patch. These changes preserve old checks rather than relaxing their unknown-byte rejection. Reports are under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r51_verified_db_subgroup_lift/`.
