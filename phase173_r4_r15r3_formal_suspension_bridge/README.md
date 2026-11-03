# EHP Proof Tracer — Phase 173 R4-R15R3

This package isolates a dimension-independent **formal suspension** construction for typed generators, including arbitrary well-typed compositions. It does **not** install the new rule in public search, identify any independently named database generator, or claim to complete a homotopy-group proof.

## Reviewed basis

- Repository: `akebono03/ehp-proof-tracer`, `develop`.
- Reviewed ancestor: `c44519a123fdbf2c5ec57fe9c89e2fb1027f41a5` (R15R1 committed).
- The subsequent HEAD may differ only by a prior R15R2 audit-package commit or the test-cache node list. All mathematical dependencies must match the exact reviewed Git blobs and working-tree content. A required R15R2 `audit.py` is independently SHA-256 checked.
- The existing R15R1 abstract-prior gate, R15R2 factor audit, source-first proof rules, CSV records, and public routes remain untouched.

## What the package adds

- `bridge.py`: `canonical_formal_suspension`, `formal_image_goal`, `is_canonical_formal_image`, and `expand_canonical_formal_image`. One E distributes over any supported typed composition, without renaming atoms. The inference proposal has no premises and is checked against an exact canonical formal target; it is not inserted into the production expansion provider.
- `audit.py`: diagnostics for k=4,7,8,31 and cautious residual-target indexing by order, without guessing a permutation among equal-order named generators.
- `preflight.py`: strict reviewed source, R15R2 audit, and commit-lineage gates.
- `tests/`: isolated executable checks, standalone static checks, and real repository-focused tests.

## Running on Windows PowerShell

Extract the ZIP into the repository root, then:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r3_formal_suspension_bridge\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase173_r4_r15r3_formal_suspension_bridge\run.ps1"
```

DryRun runs source checks and isolated tests without modifying any production file. The normal run performs focused pytest and creates `formal_image_report.json` in the extracted package directory.

## Limitations and next step

For k=31, the R15R2 right-side matching and four formal left E-images do **not** establish equality with the four remaining independently named generators. All four residual terms have order two; order alone cannot determine a matching permutation. R15R4 must seek verified source equations or independent inference for named-generator identifications before connecting a full public group proof. Run the full pytest suite only at the Phase 173 closeout.
