# Phase 169 R4B — Source-bound Proposition 4.4 injectivity

## Scope

This package installs **one** narrowly scoped production integration: the
cited Toda Proposition 4.4 rule proving suspension injectivity for maps
`E: π_{i-1}^3 -> π_i^4` in the Hopf dimension-four setting.

The preceding paragraph of Toda's adopted source describes the dimension-four
Hopf fibration; Proposition 4.4 then makes the suspension map injective.
The claim must be available in the screened earlier-citation context. The
rule does not assume a map isomorphism, surjectivity, a group structure, or
any extension of Toda (4.5)'s stable range.

The production file is changed only inside the existing function
`shared_expansion_provider`, using one local import plus one call to the new
source-bound expansion. Its full new function and whole new production file
are written to the package's `output/` directory when `run.ps1` is executed.

## Usage

Extract this archive in your repository root on Windows; run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase169_r4b_prop44_injectivity\run.ps1
```

The patch checks the Git-tracked source blob and requires a clean provider file.
It preserves a backup and rolls back on failed focused tests or proof audit.
Only narrowly selected pytest files are run. The full test suite is reserved
for the end of Phase 169.

## File changes

- Existing: `phase165_r52_r9_shared_math.py` — only the body of
  `shared_expansion_provider` changes; no module-level imports change.
- New: `phase169_r4b_prop44_injectivity/rule.py` — source-bound inference.
- New: package patch, audit, documentation and scoped tests.
- Existing tests and the shared Renderer are unchanged.

## Remaining boundary

The cyclic presentation of `π_6^4` remains subject to an independently
verified surjectivity proof, map isomorphism, cited generator image, and
complete Backward Search. R4B certifies only the injection.
