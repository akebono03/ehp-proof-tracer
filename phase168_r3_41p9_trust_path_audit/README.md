# Phase 168 R3-41P9 — Proof trust-path audit

This package is **audit-only**. It does not modify application source, existing tests, or databases.

It observes the public Web proof path and records calls made by the shared backward search to the checked inference matcher and derivation factory. It compares the three complete narratives against the full-text files collected in R3-41P8. It also demonstrates that a manually assembled, rejected inference step can enter a `PartialProofResult` and `ProofNarrativeModel` without a derivation certificate.

**Caution:** Observing a factory call does not certify a whole result. A step not observed in this one capture could come from a registered GIVEN or an earlier reusable derivation. The audit does not replay the full proof nor claim overall completeness or soundness.

## Run

Extract the ZIP into the repository root, then run in Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41p9_trust_path_audit\run.ps1"
```

Use `-SkipTests` to run only the audit. The default executes the audit and **focused pytest only**. It does not execute the full test suite.

Output: `output/audit.json`, `output/audit.md`, current complete texts, console logs, and `output/review_bundle.zip`.

All source files are read-only and the only generated files are inside this package's `output/` folder.
