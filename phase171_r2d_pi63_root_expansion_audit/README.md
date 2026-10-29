# Phase 171 R2D: pi_6^3 screened backward-frontier audit

This read-only package inspects **the exact typed proof-search context** for the registered `(n=3,k=3)` goal. It reports eligible literature GIVEN steps and root-level backward inference candidates, not completed proofs.

The saved Phase 171 R2C `frontier.json` is required. The run neither installs changes nor edits the production source, registry, database, renderer, existing tests, or official documents. The reviewed Git preflight allows local commits ahead of `origin/develop` only when all changes since the frozen Phase 170 baseline are confined to known Phase 171 audit directories. It rejects divergent/behind remotes and tracked modifications and verifies the previously reviewed source blobs.

The R2C `(4.4)` literal-locator count was zero because the registered source is actually named `Proposition 4.2 (4.4)`. R2D checks both exact locators and counts the GIVEN steps **after** the same citation screening performed by production search.

## Windows PowerShell

Extract `EHP_Phase171_R2D.zip` into the repository root, then run:

```powershell
$Report = Join-Path $env:LOCALAPPDATA "EHPProofTracerRecovery\phase171_r2c_pi63_20261029_074152_618884\frontier.json"
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2d_pi63_root_expansion_audit\run.ps1" -ReportPath $Report -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2d_pi63_root_expansion_audit\run.ps1" -ReportPath $Report
git status -sb
```

The focused tests run first. The full pytest suite is deliberately excluded until the end of Phase 171. The diagnostic report is saved under `%LOCALAPPDATA%\EHPProofTracerRecovery\phase171_r2d_pi63_*`.

No root expansion is promoted into a verified proof, and unverified source statements remain unverified. R2E (or later) must establish the mathematical derivation separately.
