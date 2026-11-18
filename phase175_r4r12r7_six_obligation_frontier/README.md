# Phase 175 R4R12R7R1 — Reviewed Commit Lineage Fix

Read-only replacement of the Phase 175 R4R12R7 audit package. The previous
commit guard rejected an already-reviewed commit containing R4R12R5 and R4R12R6.
This revision pins the exact reviewed descendant HEAD and its exact list of
changed paths. It rejects any unreviewed future commit, modified tracked
production code other than the previously permitted R4R3 rule, or divergence
from the reviewed lineage. The six proof obligations are unchanged.

Extract into the repository root and run
`powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r7_six_obligation_frontier\run.ps1 -DryRun`,
then run the same command without `-DryRun`.

Only focused tests; no project-wide pytest, production modifications, or new
mathematical rules.
