# Phase 171 R2J-R4-R5 — Cited EHP Short Exact Sequence

This read-only replay derives an EHP short exact sequence from **three actually reconstructed inference proofs**:

1. `MapInjective(E: pi_5^2 -> pi_6^3)` from Phase 171 R2J-R3;
2. the E-H window of Proposition 4.2 (4.4), specialized from its earlier cited universal statement;
3. `MapSurjective(H: pi_6^3 -> pi_6^5)` from Phase 171 R2J-R4-R4.

The new typed `EHPShortExactSequence` represents

`0 -> pi_5^2 --E--> pi_6^3 --H--> pi_6^5 -> 0`.

All three map and group coordinates must match a mathematically valid E-H window. The root is formed using the repository's inference matcher and proof-step factory, and the entire ancestry is checked against citation-screened earlier source assertions. The derived sequence **does not imply** that the middle group is cyclic or has order four: both the end-group orders and the nontrivial extension remain separate proof obligations.

## Changes

Only this new package is added. Production source files, previously created R4-R4 audit files, existing tests, repository-wide documents, Git history, and database records are left untouched. No `GIVEN` is added, and no result from Proposition 5.6 is admitted as proof evidence.

- `source.py`: typed statement and reusable, checked backward inference rule.
- `audit.py`: replay the three existing proofs, check original citations and derive one new inference root.
- `tests/test_audit.py`: nine focused positive, negative, and real-context regression tests.
- `run.ps1`: dry-run, focused regression tests (new R4-R5, earlier R2J-R3 and R4-R4), and read-only audit execution.
- `CODE_FULL_JA.md`, `監査仕様.md`: complete source/test listing and Japanese audit specification.

## Windows PowerShell

Extract the archive into the repository root. **Do not reset or restore the worktree.** The successful local R4-R4 package must remain available at `phase171_r2j_r4_r4_cited_hopf_surjectivity/`.

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2J_R4_R5_SHORT_EXACT.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r5_short_exact_sequence\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r5_short_exact_sequence\run.ps1"
git status -sb
git diff --stat
```

**Expected proof result (not yet tested in the user's worktree):**

```text
PHASE171_R2J_R4_R5_SHORT_EXACT=INFERRED
PHASE171_R2J_R4_R5_NEW_GIVEN=0
PHASE171_R2J_R4_R5_ORDER_FOUR_PROVEN=False
PHASE171_R2J_R4_R5_PI63_PROVEN=False
PHASE171_R2J_R4_R5_RUN=PASS
```

This package has been syntax-checked and ZIP integrity-checked. The actual proof-tree reconstruction and the focused pytest suite must be run in the project environment. Full pytest is reserved for Phase 171 closeout.
