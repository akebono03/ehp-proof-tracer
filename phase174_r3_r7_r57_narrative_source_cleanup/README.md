# Phase 174 R57: Shared Proof Display and Minimal Generator Surjectivity

This patch corrects the Phase 174 R56 proof dependencies and shared rendering. It does not create new axioms, new mathematical rules, fixed-group narrative branches, or completed-proof caches.

The inferred presentation of pi_11^6 still requires four certified source-first inferences, including Toda Proposition 2.7. The subsequent surjectivity of Delta for pi_12^7 instead uses the already admissible prior group presentation as its single premise; the Hopf-Delta formula is not reproved. This is justified because the canonical typed Delta of the identity already generates the target group.

The common typed display now verbalizes an independently proved zero-image suspension map as a zero homomorphism, prints a cyclic kernel using the subgroup's generator, and attributes a typed derived statement to a unique verified source ancestor. Signed Delta images are displayed without a redundant sign when an independently proved order-two cyclic target is in the same verified proof tree. The registered earlier printed Toda (5.10) equation, checked against the adopted text, is transcribed without the artificial sign inserted by the conservative internal claim type.

## Installation

Extract this ZIP directly into the `ehp-proof` Git repository root on the reviewed `develop` HEAD. Execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r57_narrative_source_cleanup\run.ps1"
```

Preflight checks the exact committed blobs of the three shared rendering modules, and the checked original or already-revised R56 rule and associated tests. Any unexpected staged file, changed HEAD, or unmatched target content stops the installation. The installer is idempotent with the reviewed before/after contents and preserves CRLF/LF for each modified file.

The full revised versions of all changed functions are written to `output/CHANGED_FUNCTIONS_FULL_JA.md`; complete revised production files are also exported under `output/` for review. `run.ps1` invokes only focused pytest groups and a real source-first model-rendering audit; it does not run the entire test suite.

This package was constructed from reviewed GitHub `develop` sources and the previously delivered R56 ZIP. Actual Windows production proof-search and regression verification is performed by the included runner, not asserted from offline syntax tests alone.
