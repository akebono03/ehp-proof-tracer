# Phase 169 R10E5 — Typed Composition Suspension

This package adds a source-neutral, typed inference for suspension of a composition of homotopy elements. It does **not** add an unsupported generator identity, a database result as an axiom, or a new family-specific relation. The pre-existing eta composition path takes priority, avoiding duplicate derivations.

## Scope

- Existing production module: `phase165_r52_r9_shared_math.py`.
- Existing function: `shared_expansion_provider` (complete modified function and module exported to `output/` during execution).
- New module: `phase169_r10e5_composite_generator_image/rule.py`.
- New focused tests: `phase169_r10e5_composite_generator_image/tests/test_r10e5_composite_generator_image.py`.
- New targeted search audit: `phase169_r10e5_composite_generator_image/audit.py`.

The inference can only conclude `GeneratorImage(E, f ∘ g, Ef ∘ Eg)` after **two independent INFERENCE premises** establish the images of both `f` and `g`. The parent and child dimensions must match, and the maps must be composable. Higher nested compositions are handled recursively without any extra case-specific theorem.

## Installation and execution

Extract `phase169_r10e5_composite_generator_image.zip` at the repository root, then run:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r10e5_composite_generator_image.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r10e5_composite_generator_image\run.ps1"
```

The runner verifies the pinned `develop` revision, preserves pre-existing tracked edits, saves a byte-for-byte backup of the one changed production file, runs only focused pytest modules, and audits the remaining composite and direct-sum targets. On failure, it restores the original production file. It never runs the complete pytest suite or `git reset`.

## Interpreting results

`R10E5_pi_20^14_STATUS` identifies the key composite-nu target. `COMPOSITE_IMAGES` counts inferred composition image steps. The three remaining direct-sum targets may stay incomplete if they require source definitions for other families or additive images. An incomplete search is never presented as a completed proof.
