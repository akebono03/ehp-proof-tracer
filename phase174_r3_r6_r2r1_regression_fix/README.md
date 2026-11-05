# EHP Proof Tracer — Phase 174 R3-R6-R2R1 Regression Guard Fix

This package corrects **two historical regression checks** that failed after the
mathematically successful Phase 174 R3-R6-R2 change. It **does not change** the
proof rules, Proposition 4.4, Lemma 5.4, the public renderer, or the cyclic-group
result.

1. The R3-R4 cumulative provider test now normalizes Git checkout CRLF/LF
   line endings before reconstructing a *pinned* historical patch chain. It
   retains the original Git-blob assertion and does not accept unrelated edits.
2. The historical R3-R4 Delta-zero audit now admits the *source-verified* Lemma
   5.4 before screening Proposition 5.6's target, in the same way as the R3-R6-R2
   root audit. The reconstructed injectivity step must have both the cited
   Proposition 4.4 and the independently inferred Lemma 5.4 in its proof ancestry.
   The EHP exactness step must retain the cited Proposition 4.2.

## Reviewed baseline

- Branch: `develop`
- Pinned HEAD and origin/develop: `e4a5b73962bb98acb62b5335ffecae4728d98378`
- Previous patch: `phase174_r3_r6_r2_prop44_lemma54`, fully installed.
- Existing modified working-tree files from the previous patch are verified
  against all nine pinned Git blobs and their exact approved transformation.
- Two additional targets only:
  - `phase174_r3_r4_public_delta_connection/audit.py`:
    `inspect_public_provider()`
  - `phase174_r3_r4_public_delta_connection/tests/test_connection.py`:
    `test_r3r4_real_production_file_has_only_reviewed_wiring()`

No production proof modules are modified by this package. The new package
contains a fail-closed patcher, a separate proof-ancestry audit, and focused
tests. Every complete changed function and new file is reproduced in
`CODE_FULL_JA.md`. The installed full files and changed functions are also
written into `output/` during installation.

## Run

Extract the ZIP to the project root. In Windows PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r6_r2r1_regression_fix\run.ps1" -DryRun
```

If the DryRun passes, run without `-DryRun`. The runner repeats the original
focused test selection with the two historical failures corrected, and adds
four focused patch tests. It deliberately does **not** run the full test suite.

The runner stops without overwriting unreviewed changes. Other uncommitted
work (including historical `.pytest_cache` changes) is left untouched.
