# EHP Proof Tracer — Phase 174 R57R1

This repair changes only R57's installer source guard. R57 originally rejected every Git HEAD except `0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9`, even though R56 was subsequently committed onto `develop`.

R57R1 permits descendant commits of the reviewed base **only if** R57's existing checks still pass: `develop` branch, no staged changes, three exact tracked Git blob pins, exact R56 local rule/test SHA-256 hashes, and unambiguous patch anchors.

It does not waive the source guard, edit the mathematical rules, change a narrative renderer, or add any source GIVEN. The normal run then executes the existing R57 DryRun, focused pytest, and public proof audit.

Extract into the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r57r1_head_lineage_fix\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r57r1_head_lineage_fix\run.ps1"
```

Never continue to the non-DryRun command if the DryRun fails. The entire source of the changed R57 installer and its changed `review()` function are included in `R57_INSTALL_FULL_AFTER.py.txt` and `CODE_FULL_JA.md`.
