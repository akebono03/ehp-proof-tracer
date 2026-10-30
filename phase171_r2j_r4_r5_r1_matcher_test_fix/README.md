# Phase 171 R2J-R4-R5-R1 — Inference Matcher Test Correction

This guarded test-only fix corrects one invalid assumption in the Phase 171 R4-R5 audit test: the repository's `find_inference_matches_for_rule()` matches input proof steps against premise patterns **irrespective of the order in which the available steps were supplied**. The matched premises are returned in pattern order.

The previous test incorrectly expected the reversed input sequence to yield no inference match. Its replacement confirms that the reversed input is accepted and canonicalized; it also verifies that an incompatible injection endpoint is rejected. The mathematical rule and the actual proof replay are unchanged.

## Files changed in the existing R4-R5 package

- `phase171_r2j_r4_r5_short_exact_sequence/tests/test_audit.py`: replace the complete `test_unrelated_sequence_or_reordered_premises_are_rejected()` test function with `test_unrelated_sequence_is_rejected_and_reordered_premises_are_matched()`; no import changes.
- `phase171_r2j_r4_r5_short_exact_sequence/CODE_FULL_JA.md`: replace the full code-document with its corrected full-text version.

The self-contained patch package adds `install.py`, `run.ps1`, and accompanying documentation. The guarded installer checks SHA-256 hashes before writing, refuses unfamiliar local modifications, and is safe to rerun. It does not change any tracked production code, any other test, any citation or `GIVEN`, or any target group proof.

## Windows PowerShell

Extract into the existing repository root, retaining the previously installed R4-R5 and R4-R4 directories.

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\EHP_Phase171_R2J_R4_R5_R1_MATCHER_TEST_FIX.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r5_r1_matcher_test_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2j_r4_r5_r1_matcher_test_fix\run.ps1"
git status -sb
git diff --stat
```

The existing R4-R5 runner performs its original **27 focused tests** and then reconstructs the cited proof tree. The full pytest suite remains deferred until Phase 171 closeout. An unchanged production worktree and the `SHORT_EXACT=INFERRED`, `NEW_GIVEN=0`, and `PI63_PROVEN=False` audit fields are the success conditions. A successful test-only preflight does **not** itself certify the proof.
