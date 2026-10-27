# EHP Proof Tracer — Phase 169 R7: General Stable Transport

This package adds an **arbitrary-fold, cited stable cyclic transport** inference rule. It does not introduce a group answer, an isomorphism, or a named generator image as a GIVEN proof step. The new rule is parameterized by the source and target groups, the stem, and the number of suspensions.

## Installation on Windows

Run from the root of an existing checkout on the `develop` branch:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase169_r7_general_stable_transport.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r7_general_stable_transport\run.ps1"
```

The runner first inspects the local repository and the related source/test paths without making changes. It then patches only `shared_expansion_provider()` inside `phase165_r52_r9_shared_math.py`, runs focused tests, and performs a focused canonical-search/Web audit for the second stem. It **does not run the full pytest suite**.

If the post-patch tests or audit fail, the runner restores the original provider file byte-for-byte from `output/phase165_r52_r9_shared_math.py.before`. It does not remove this package or modify existing test files.

## Backward compatibility and current boundary

The existing R5B and R6A provider routes are preserved and take precedence. For this Phase 169 installation, the new generic rule is connected as a fallback **only for 2-stem finite-cyclic group goals**; the rule itself has no fixed stem or suspension exponent. Other stems are checked in focused rule tests, but their public search integration belongs to a later Phase. Free cyclic groups, direct sums and unnamed generator normalization are not implemented here.

The new rule proposes one independent `GeneratorImage` subgoal for each unit suspension. For `r > 1`, intermediate generators are constructed from typed endpoint structure, not treated as evidence. If the cited eta-definition rules or another existing proof route do not prove the image goals, the result remains partial.

## Outputs

- `output/phase165_r52_r9_shared_math.py.before`: exact pre-patch backup.
- `output/shared_expansion_provider_FULL.py`: full replacement function, including local imports.
- `output/phase165_r52_r9_shared_math.py.FULL`: entire updated production file.
- `output/patch_manifest.json`: SHA-256 hashes and changed-file list.
- `output/audit.json` and `output/audit.md`: focused proof/Web report.

Existing root-level `README.md`, `design.md`, `development_log.md`, `roadmap.md`, and `proof_records.md` are not modified.

The ZIP was assembled with syntax and archive checks; its focused application tests must be run in the user's checkout, which is not available in the authoring container.
