# Phase 175 R4R12R9 — Typed Delta Equality to Generator Image Bridge

This package adds one **general**, type-checked backward inference: an independently proved equality `Delta(g) = h` implies the corresponding `GeneratorImage(Delta, g, h)`. It never adds Equation (5.11) as a GIVEN, does not register the target group as a proof leaf, and does not complete the group proof. Its purpose is to let the existing R4R10/R4R11 source-first equation route feed the R4R12 EHP quotient obligations.

## Boundaries

The only pre-existing production file modified is `phase165_r52_r9_shared_math.py`, limited to the **whole-function replacement** of `shared_expansion_provider()`. The installer writes the complete replacement function to `output/SHARED_PROVIDER_FULL_AFTER.py`, including in DryRun. The new `rule.py` is reusable for any correctly typed Toda Delta source/target dimensions. It never removes a sign from an unproved equality and requires an INFERENCE proof step, not a direct GIVEN.

The code accepts exactly the reviewed R7 commit `b7bbb1032ef6c0568cb0cbf1c0116c2b183716e4` or its verified one-commit merge descendant `3ec001a59044aeb056ec7190c43c6066eaf5abae`. The merge must have no changed files relative to R7 and must satisfy local commit-count and ancestry checks. Any other HEAD is rejected. The prior R8 package is required.

## Running

Unzip at the repository root on `develop` and run:

```powershell
$script = '.\phase175_r4r12r9_delta_generator_image_bridge\run.ps1'
powershell -NoProfile -ExecutionPolicy Bypass -File $script -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File $script
```

Both runs execute ten focused pytest tests (four existing bridge tests and six merge-lineage regression tests). The full test suite must wait for the Phase 175 closeout. Audit output is written to the package `output` directory.

The success gate `PASS_R4R12R9_GENERIC_BRIDGE_CONNECTED_PROOF_PENDING` means the **bridge candidate** is visible in shared search. It does **not** mean the separate Equation (5.11) equality proof has succeeded or that the group is complete. Inspect `shared.delta_equality_candidates` in the report before selecting a subsequent step.
