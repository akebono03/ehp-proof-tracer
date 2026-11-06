# Phase 174 R3-R7-R7 — Composite Zero Generator Source Audit

This package examines a generic inference: if a homotopy generator has a separately proved image represented by `a ∘ b`, and `a = 0` has been independently proved, then the generator image is zero. The mathematical rule is isolated and **not** wired into production proof search, the public web route, the renderer, or the statement registry.

The source is the project's adopted transcription of Toda Proposition 5.9 and Equation (5.9), not an independently verified printed-edition scan. A transcription is not a proof leaf. The source-screened provider is used only to count available backward options.

Run on the `develop` branch in the EHP Proof Tracer repository. The previous R3-R7-R6 full audit report in `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r6\cyclic_generator_zero_image.json` is required.

```powershell
Expand-Archive -Path "$HOME\Downloads\R7.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r7_composite_zero_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r7_composite_zero_audit\run.ps1"
```

The script runs limited test groups in separate pytest processes to prevent collection conflicts. It validates the exact reviewed Git HEAD, pinned source files, the previous audit report, and the relative source and conclusion locations. The report is written outside the repository to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r7\composite_zero_audit.json`.

No full pytest suite is run. No production source file is modified.
