# Phase 171 R2J-R4-R3: Typed Double-Relation / Suspension-Image Bridge

## Scope

This package adds one **read-only, audit-scoped inference rule**. It connects a publication-screened, citation-linked Toda (5.3) equality `2 nu' = eta_3 eta_4 eta_5` with the already replayable, typed R4-R2 proof `E(eta_2^3) = eta_3 eta_4 eta_5`, to derive a new inferred proof node for `2 nu' = E(eta_2^3)`.

It never assumes the desired cyclic presentation of `pi_6(S^3)` and never inserts a new GIVEN. The existing R4-R2 replay and its locally selected provider are imported at run time; they are **not overwritten** by this archive. New inference requires an exact structural match, verified map endpoints, a trusted earlier reference link, an actual previously inferred image root, and two distinct proof ancestors.

This step does **not** prove the surjectivity of `H: pi_6^3 -> pi_6^5`, the short exact sequence, order four, or the cyclic group structure. Those obligations remain for later R4 phases. In particular, a short exact sequence with outer terms of order two does not, by itself, distinguish a cyclic group from an elementary abelian group.

The Toda (5.3) source follows the repository's adopted-transcription/source-hash verification policy; this work does not independently verify the original edition.

## Newly added files

- `source.py`: complete generic typed equality/substitution rule and its validation.
- `audit.py`: read-only, publication-screened proof replay and report writer.
- `tests/test_audit.py`: focused positive, negative, and live integration tests.
- `run.ps1`: dry-run, focused pytest, and execution entry point.
- `CODE_FULL_JA.md`: full source, tests, imports, and PowerShell code.
- `監査仕様.md`: Japanese audit specification.

No files outside this new package are changed. No repository-wide documents or existing APIs are modified.

## Run (Windows PowerShell at the repository root)

```powershell
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2J_R4_R3_TYPED_DOUBLE_IMAGE.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r3_double_image_bridge\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r3_double_image_bridge\run.ps1"
git status -sb
git diff --stat
```

The focused test command also reruns the seven R4-R2 tests. The report is written to `phase171_r2j_r4_r3_double_image_bridge/output/audit.json`. Full pytest is reserved for Phase 171 closeout. A local run is required to establish a real inferred proof in the user's worktree; this archive was statically checked, but could not execute the repository's complete dependencies in the packaging environment.
