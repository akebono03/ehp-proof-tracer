# Phase 175 R4R12R13R8 — Citation Audit (read-only)

This R13R8R1 revision corrects the PowerShell 5.1 `Join-Path` argument error in the focused pytest invocation. It changes no Python source or production code.

This is a **diagnostic-only package**, not a fix or completion claim. It inspects the current `develop` checkout for the actual citation pipeline and local line endings. It makes no changes to production files, mathematical facts, the proof tree, or the Web renderer. It intentionally does not attempt to reconstruct R3 or R7 statements from printed locator labels.

From the repository root, extract the ZIP, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r13r8_reference_audit\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r13r8_reference_audit\run.ps1
```

The normal run executes only three audit-focused pytest cases. The report is written to `$env:TEMP\EHP_Phase175_R13R8_report.json`. Provide that report and the exact Web proof output to identify the smallest safe citation patch. No full pytest suite is run.

Completion remains pending until R3 and R7 have verified source bodies, the matching ProofSteps cite their original reference numbers, and the public complete proof remains unchanged mathematically.
