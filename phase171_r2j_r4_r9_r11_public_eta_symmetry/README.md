# EHP Proof Tracer — Phase 171 R2J-R4-R9-R11

This narrowly scoped integration exposes **backward equality-symmetry obligations** for source-screened η–Hopf calculation chains. It reuses the existing mathematical equality-symmetry rule; no new theorem or proof leaf is introduced.

## Scope

- Modify only `shared_expansion_provider()` in `phase165_r52_r9_shared_math.py` by one six-line in-function hook.
- Add the `phase171_r2j_r4_r9_r11_public_eta_symmetry/` module with a guarded installer, generic source-anchored expander, public-search audit, focused tests, and this documentation.
- Only the seven exact, source-derivable forward equalities of a cited η–Hopf chain qualify. No arbitrary symmetry search or graph replay is enabled.
- The uniquely source-anchored reverse route takes precedence over generic inverse searches to prevent redundant cyclic alternatives. The shared recursive search must independently prove every forward equality. Neither a previously complete R2I proof tree nor a new `GIVEN` is imported into the public provider.
- The existing Web and trust boundary remain unchanged. `public_complete` is observed and not promised.

## Prerequisites

The `develop` checkout of `akebono03/ehp-proof-tracer`, including the R7–R10 integrations and the verified R2I source and tests. The reference HEAD before this phase is `6dbd6ac2bcb29fe742991376adacd037fb4ff141`. R10 can be committed or a precisely reviewed local patch. Unknown modifications to the provider are refused.

## Run from repository root — PowerShell

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2J_R4_R9_R11_PUBLIC_ETA_SYMMETRY.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r11_public_eta_symmetry\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r9_r11_public_eta_symmetry\run.ps1"
git status -sb
git diff --stat
```

Run only the focused pytest set. The installer writes the full revised provider function and file to `output/`. The audit writes `output/audit.json` and prints the first remaining public open goal. Any partial public search is a valid observation and **not a completed Web proof**.
