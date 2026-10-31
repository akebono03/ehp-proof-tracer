# Phase 171 R20R12R2 — Unindexed nu-prime display repair

This package repairs one display fallback in the existing Phase 171 R20R12 projection. The corrected function uses the repository's established Toda expression renderer for a proved generator without an index. It neither changes the public proof search, the Proof Tree, nor the Web renderer.

Extract the archive at the repository root. First run `run.ps1 -DryRun`, then `run.ps1` to run focused regression tests and the real canonical proof/narrative audit. The original Phase 171 R20R12 package and its already-installed renderer patch must be present. The installer guards both against unforeseen edits and does not commit any files.

Results and full replacement code are saved within `phase171_r20r12r2_unindexed_nu_projection_fix/output`. Full-suite pytest is deliberately excluded.
