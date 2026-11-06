# Phase 174 R3-R7-R5: Isolated zero-image/Hopf-injectivity audit

This package introduces one **isolated, generally valid EHP inference proposal**:
if the suspension map has zero image and the corresponding E-H sequence is exact, then the Hopf map is injective. It never assumes that the preceding group is zero.

The rule is **not installed** in the public proof-search provider or Web UI. It does not register any new GIVEN theorem or group result. Its image-zero premise remains a separate obligation requiring an independently certified proof. A candidate root is not a completed proof.

## Files

- `rule.py`: generic typed rule and backward proposal, with no proof leaves.
- `audit.py`: read-only Source Guard, previous audit evidence validation, source screening, and live frontier inspection.
- `tests/test_rule.py`: generic inference and negative tests.
- `tests/test_audit.py`: previous audit, source, and trust-boundary tests.
- `run.ps1`: scoped pytest in separate processes, DryRun, and normal read-only audit.
- `AUDIT_PLAN_JA.md`: Japanese audit scope.
- `CODE_FULL_JA.md`: complete replacement-ready code and tests.

## Run

Expand the ZIP in the repository root and run from PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r5_zero_image_hopf_injective\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r5_zero_image_hopf_injective\run.ps1"
```

Requires a checked-out `develop` branch at the reviewed commit, with the R3-R7-R4 normal audit JSON under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r4\delta_surjectivity_audit.json`.

The read-only report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r5\zero_image_hopf_injective.json`. The two previous audits' results remain unchanged.

This package does not run the full pytest suite. The full suite belongs only at the end of Phase 174.
