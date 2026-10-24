# Phase 168 R3-41P11 — Screened GIVEN Provenance Audit

This audit-only package compares each GIVEN step in the public three-group proof path to the exact ProofStepLink entries in the screened registry bridge passed to the Narrative Model. It preserves the R3-41P10 fulltext baselines, and tests that a fabricated GIVEN is not mistaken for a screened source.

It does not modify EHP Proof Tracer application modules or existing tests. It does not certify publication order, statement truth, source-edition verification, or arbitrary ProofSteps. Those are separate trust boundaries.

Run from the repository root with PowerShell:

```powershell
Expand-Archive -Path "$HOME\Downloads\phase168_r3_41p11_given_provenance_audit.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41p11_given_provenance_audit\run.ps1"
```

For an audit without focused tests, pass `-SkipTests` to `run.ps1`. The full pytest suite is deliberately not run.

Output includes `output/audit.json`, `output/audit.md`, per-group markdown, focused pytest logs, and `output/review_bundle.zip`. Missing links or missing fixed-source citations are recorded as findings rather than silently treated as certified evidence.
