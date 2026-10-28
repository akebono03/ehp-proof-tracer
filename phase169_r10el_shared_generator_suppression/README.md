# Phase 169 R10EL — Shared Generator-Proof Suppression

R10EK established a common proof-preserving narrative contract for finite cyclic and direct-sum group transport. R10EL extracts **only the repeated suppression-safety algorithm** into a new shared helper. The existing cyclic and direct-sum projections retain their public entry points, output data classes, mathematical premises, source citations, and formula formatting.

## Reviewed baseline and changes

The reviewed GitHub repository is `akebono03/ehp-proof-tracer`, branch `develop`, base commit `01e20c4d7bb74b8680bd3311130358266c97e884`. The expected local R10EJ implementation is the subsequent local commit `7861cbff41a7015186f3d79001ac89b0c64d4283`, or a descendant with the **same exact target file bytes**. The runner stops if its reviewed ancestor or the two expected target hashes do not match. It never checks out or resets Git history.

- New: `phase169_r10el_shared_generator_suppression/core.py`, implementing `exclusive_generator_inference_indices`.
- Updated: `phase169_r10a_verified_stable_chain_projection/projection.py`, **only** `project_verified_stable_image_chain`.
- Updated: `phase169_r10ec_direct_sum_narrative_projection/projection.py`, **only** `project_verified_direct_sum_transport`.
- New: package-local patch, focused tests, audit, and rollback-capable runner.

The common helper checks the actual rooted `GeneratorImage` objects, proof-object identity, all prerequisite indices, individually linked citations, and all consumers. A cyclic projection may retain a shared ancestor's individual prose; a direct-sum projection still refuses compression unless the whole eligible image subgraph can be suppressed safely. In both cases, existing GIVEN steps and individual citations are never suppressed. The helper is **not** a proof verifier; the caller must first use the existing trust-boundary verifier.

## Windows execution

From the repository root:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r10el_shared_generator_suppression.zip" `
  -DestinationPath "." `
  -Force
powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase169_r10el_shared_generator_suppression\run.ps1"
git status -sb
```

The R10EJ tests are expected to exist at `phase169_r10ej_cyclic_verified_projection/tests/test_r10ej_live.py`. The runner executes the package's ten isolated/patch tests, focused existing proof/regression tests, and a four-group verified search-and-render audit. It disables pytest's cache provider, preserving any already-existing `.pytest_cache` state. No full test suite is executed.

If the live regressions, trust verification, narrative checks, or unrelated tracked-file checks fail, the runner restores the two original production files **byte for byte**. It preserves the user's other tracked/untracked work and emits timestamped artifacts under the package's `output/run_*` directory. Review the results before committing.

The four audited targets are `(n,k)=(22,6),(22,10),(15,8),(24,9)` with expected, unchanged hidden inference counts `31,40,10,110`. Negative tests check external consumers, citations, duplicate indices, and missing proof ancestors. The 11-stem and 14-stem open proof problems, FreeCyclicGroup support, and generalized inference rules are not implemented in this stage.
