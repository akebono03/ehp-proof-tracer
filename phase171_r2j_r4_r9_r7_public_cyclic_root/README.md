# EHP Proof Tracer — Phase 171 R2J-R4-R9-R7

## Scope

Introduce exactly one source-anchored, generic root backward proposal for finite order-four cyclic goals. A screened typed double relation identifies a possible generator, but the proposed `FiniteGroupCardinality` and `FiniteElementOrder` remain **unproved subgoals**. They must be reconstructed by the existing canonical engine and cannot be supplied as completed `ProofStep`s. No proof result, `GIVEN` leaf, or purported citation is added.

This phase modifies only the existing function `shared_expansion_provider()` in `phase165_r52_r9_shared_math.py` and introduces `phase171_r2j_r4_r9_r7_public_cyclic_root/` containing the proposer, guarded installer, audit and tests. The existing root rule and all existing Hopf, EHP, proof trust, renderer and Web APIs are unchanged.

## Before applying

The reference repository was reviewed on GitHub `akebono03/ehp-proof-tracer` `develop` at `54a372a9370404d65d42a5b8d8693c8f64de2b03`. An installer checks the branch, unchanged tracked files, a unique existing hook anchor, parses the entire resulting module, and refuses a partial prior installation. It preserves the original line-ending convention. Dry-run does not mutate files.

## Run (Windows PowerShell)

Unzip the package at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r7_public_cyclic_root\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r7_public_cyclic_root\run.ps1"
git status -sb
git diff --stat
```

The installer writes the **complete** post-change `shared_expansion_provider` function to `output/shared_expansion_provider_FULL.py` and the full amended source file to `output/phase165_r52_r9_shared_math.FULL.py`; it also saves a complete pre-change backup. Focused tests only; full pytest is deferred until Phase closeout.

## Completion criteria and phase boundary

The newly registered public root proposal must match R4-R8's inferred root, must be backed by a screened typed double relation, and must not contain a precompleted proof step. The real public search status and unresolved subgoals are reported, without claiming complete Web output. Later phases must connect missing subgoal expansions (if any), the two source-bound Hopf obligations, and independently verify public Web provenance before a public-complete claim.
