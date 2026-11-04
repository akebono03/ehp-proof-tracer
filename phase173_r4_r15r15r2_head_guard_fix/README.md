# Phase 173 R4-R15R15R2 — Git HEAD Lineage Correction

This package corrects the R15R15 Web status-banner installer for the committed R15R14 baseline. It does **not** add mathematical proof steps or infer named generators. The earlier R15R15 installer rejected the newer `develop` HEAD, even though R15R14 had already been merged into the branch.

## Baseline and safety

- Reviewed baseline: `5563a67008d097d08745481ee299dbb94e12c2b9` (`173-4-15-14`).
- Accept this commit or a descendant only if **all four reviewed Git blobs remain identical**, and local `HEAD` equals `origin/develop`.
- Refuse staged changes, unexpected local tracked edits, unknown source contents, and dirty installed files.
- DryRun performs only Source Guard and standalone contract tests; it does not change production files.
- Installation changes only `web_group_proof_common.py`, `phase165_r52_r3_web_adapter.py`, and `templates/index.html`.
- Backups are byte-for-byte, with SHA-256 checks; rollback is available.
- Full pytest runs only at Phase completion, not here.

## Use

Extract the ZIP in the repository root and run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r15r15r2_head_guard_fix\run.ps1 -DryRun`, followed by the same command without `-DryRun`.

## Verification

Expected outcome: real typed proof search for `(n,k)=(4,8)` still returns a partial named-generator proof, but the Web banner explains that the abstract group structure is verified. `(4,3)` remains complete. A missing abstract certificate still produces the former not-found banner. The new package does not modify existing tests, source proofs, or registered mathematics.
