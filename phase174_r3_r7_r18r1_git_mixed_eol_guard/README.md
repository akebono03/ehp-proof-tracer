# Phase 174 R3-R7-R18R1 — Reviewed Git Mixed-EOL Source Guard Fix

This package corrects an audit-only false rejection of a Git-tracked source file with mixed CRLF and LF line endings. It leaves EHP inference rules, proof search, production renderers, literature premises, and the database unchanged.

It also permits the exactly reviewed R18 merge commit and a clean R17 local checkout with that R18 remote commit. Unknown commits or unrelated tracked edits fail closed.

Extract the archive into the EHP Proof Tracer repository root, alongside the existing `phase174_r3_r7_r18_delta_image_surjectivity` package.

Run `phase174_r3_r7_r18r1_git_mixed_eol_guard/run.ps1 -DryRun`, then run the same script without `-DryRun`. The script performs focused tests and runs the original R18 audit. It never runs the full pytest suite.

The reviewed replacement source for `phase174_r3_r7_r18_delta_image_surjectivity/audit.py` is supplied as `replacement_audit.py.txt`. The patcher requires its exact SHA-256 and the exact original audit SHA-256 before updating. Backups are stored outside the repository. The runner restores the original audit on failure.

Do not edit `map_facts.py` or reset the repository to address this issue.
