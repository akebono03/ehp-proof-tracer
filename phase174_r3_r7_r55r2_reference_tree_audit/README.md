# Phase 174 R55R2 — Reference and Verified Proof Tree Audit

This is a **read-only diagnostic package**. It does not install a patch, register a new theorem, change proof search, or run the full test suite.

The audit inspects the actual `(n,k)=(7,5)` public proof and the same screened reference bridge used by the Web route. It distinguishes two different EHP Delta maps, inspects the four certified premises of upper Delta surjectivity, checks Toda (5.9) and Proposition 2.7 source ancestry, and records whether the corresponding formulas actually appear in Reference and proof prose.

Extract the ZIP directly into the repository root on the `develop` branch. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r55r2_reference_tree_audit\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R55R2 preflight failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r55r2_reference_tree_audit\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R55R2 audit failed" }
```

The machine-readable output is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r55r2\reference_tree_audit.json`.

A `PASS_CERTIFIED_TREE_DISPLAY_AUDIT_ONLY` result certifies **only** that the observed source-backed proof ancestry is present. It does **not** certify Reference prose as complete; the separate boolean fields report that status. The Phase 174 R56 full pytest is intentionally not run.
