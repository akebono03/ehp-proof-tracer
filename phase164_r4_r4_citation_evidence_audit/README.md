# Phase 164 R4-R4 — Citation Evidence Audit

This package performs a **read-only, fail-closed** audit for the two literature-derived leaves used in the existing proof of the suspension isomorphism `E: pi_4^2 -> pi_5^3`.

It checks the translated-source identities and hashes, reuses the existing R4-R3 typed-clause validation, and reports missing original-edition, scope, provenance, and availability evidence. It does **not** attest to the original Toda edition or mathematical truth, certify a citation, populate an eligibility allowlist, connect the production registry, or modify the existing backward search or renderer.

## Install and execute (Windows PowerShell)

Run from the repository root:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase164_r4_r4_citation_evidence_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase164_r4_r4_citation_evidence_audit\run.ps1"
```

The script copies only the new module and its new test into the repository. It runs targeted tests (R4-R4, R4-R3, R4-R1), not the repository-wide test suite. The output is written to `phase164_r4_r4_output/report.json` and `phase164_r4_r4_output/report.md`.

## Scope and boundaries

- Proposition 5.1: `toda:tex:ch5:0002`, four typed components, with the remaining stable clause and universal scope kept outside verification.
- Equation (5.3): `toda:tex:ch5:0005`, the Hopf relation only; the double-nu clause is separate.
- Publication positions 78 and 81 are positions in translated TeX, **not independently confirmed positions in the original edition**.
- An existing `ProofStep` is not independent evidence that the corresponding original reference is available at a particular stage.
- Citation authorization remains false regardless of externally supplied flags; an authenticated evidence workflow belongs to a later step.
