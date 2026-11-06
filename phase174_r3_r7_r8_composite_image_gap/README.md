# Phase 174 R3-R7-R8 — Composite Image Gap Audit

This package is a read-only, source-first audit of the unproved generator-suspension image in Toda Proposition 5.9. It does not add new GIVEN statements, alter the production proof search, modify a renderer, or claim a completed proof.

The previously certified R3-R7-R7 audit must exist at `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r7\composite_zero_audit.json`.

Run from the repository root in PowerShell after extracting the archive:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r8_composite_image_gap\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r8_composite_image_gap\run.ps1"
```

The focused pytest suites run in separate processes to avoid duplicate test module basenames, with `--import-mode=prepend` for legacy file-versus-directory imports. A full pytest suite is intentionally not run.

The report is written outside the Git working tree to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r8\composite_image_gap.json`. It includes the source-screened public candidate counts, the existing generic composite-image rule's typed child goals, and the existing left-factor-zero branch's immediate child goals. Candidate expansions are not certified proofs.

The source guard pins audited SHA blobs and accepts only the reviewed `develop` head or its reviewed R7-only predecessor. If HEAD or a pinned source changes, this script stops for a fresh review.
