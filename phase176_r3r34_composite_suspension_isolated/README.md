# Phase 176 R3R34 — Isolated Composite Suspension Equality Bridge

This package adds an **isolated general backward inference** from a separately verified composite suspension `GeneratorImage` to the matching typed element equality. It does not modify the public proof search, change existing math rules, register a new source or GIVEN, or claim a proof of the target group.

The only inference obligation is the pre-existing type-checked `GeneratorImage` statement for the same composite and target. A bare source assertion or a matching visual name cannot satisfy it. The rule is intentionally limited to a binary composition of concrete typed sphere maps.

Run from the repository root after extraction:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r34_composite_suspension_isolated\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r34_composite_suspension_isolated\run.ps1
```

The report is stored at `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r34_composite_suspension_isolated\report.json`.

The isolated rule does **not** make the existing Proposition 2.2 recognizer accept a suspended composite. That distinct generalization and its source/typing verification remain a subsequent phase boundary. The complete pytest suite is not run.
