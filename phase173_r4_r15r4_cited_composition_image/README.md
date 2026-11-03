# EHP Proof Tracer — Phase 173 R4-R15R4

This package adds a source-first, generic composition-image inference **outside the public proof provider**. It does not change any existing production source file and does not claim that the target group has a completed proof.

## Mathematical contract

For typed maps of spheres, the suspension functor satisfies `E(f ∘ g) = E(f) ∘ E(g)`. The new inference requires independently established `GeneratorImage` proof steps for **both** factors. The proof replay reuses the existing cited Toda Chapter V / Chapter VI family definitions and the existing R15R3 canonical formal suspension rule. Database generator labels alone are not sufficient evidence.

In the `k=31, n=4` case, the cited ν-family definition and a formal `Eφ′` image may establish a composite generator image for the `φ′ν²` component. Other components may still require separately cited definitions of δ and bar-κ. The audit reports the actual proven count without assuming it in advance.

## Changes

All additions are under `phase173_r4_r15r4_cited_composition_image/`:

- `bridge.py`: typed `GeneratorImage` construction and composition proof expansion.
- `replay.py`: proof-engine replay from source-checked Chapter V/VI fixed statements.
- `audit.py`: source-backed generator-image audit for selected `k` values, with no public proof promotion.
- `preflight.py`: reviewed commit ancestry, Git blob guards and prior-package hashes.
- `tests/`: independent unit tests and focused repository-backed tests.
- `run.ps1`: DryRun and limited pytest execution.
- `SOURCE_CODE.md`: full source files and tests without omitted code.
- `design.md`: Japanese design, proof boundaries and next steps.

## Windows execution

Extract the ZIP into the EHP Proof Tracer repository root, without changing the provided directory name. Run from PowerShell:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

$ErrorActionPreference = 'Stop'

Expand-Archive `
  -Path "$HOME\Downloads\EHP_Phase173_R4_R15R4_CITED_COMPOSITION_IMAGE.zip" `
  -DestinationPath "." -Force

powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase173_r4_r15r4_cited_composition_image\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw 'R15R4 DryRun failed' }

powershell -NoProfile -ExecutionPolicy Bypass `
  -File ".\phase173_r4_r15r4_cited_composition_image\run.ps1"
if ($LASTEXITCODE -ne 0) { throw 'R15R4 execution failed' }

git status -sb
git diff --stat
```

The script requires the previously installed R15R2 and R15R3 packages. The reviewed develop commit is `3901da80ac4af7226b41246353b700708a33c085`. Later commits containing only the exact prior R15R3 package and the harmless pytest cache are accepted, provided all reviewed dependencies remain unchanged.

## Verification and completion criteria

DryRun executes static and isolated tests. The full invocation runs only focused tests, then writes `source_cited_image_report.json`. Expected invariant diagnostics include `SOURCE_GUARD=PASS`, `FOCUSED_PYTEST=PASS`, `AUDIT=PASS`, `PRODUCTION_EDIT=NONE`, `PUBLIC_COMPLETION=False`. The number of certified named images is reported from the actual proof engine rather than hardcoded.

Run the entire pytest suite only when Phase 173 closes. No new source `GIVEN`, unproven target identity, group-proof `complete` status or public adapter change is permitted by this package.
