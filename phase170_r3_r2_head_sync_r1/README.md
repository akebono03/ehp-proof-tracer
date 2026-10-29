# Phase 170 R3-R2 — Root Expansion Audit (Reviewed HEAD Sync)

This package corrects a fail-closed preflight incompatibility in the previous
`phase170_r3_r2_root_expansion_audit` package. The previous package reused
the reviewed R3-R1 preflight, which admitted the 13 R2 files committed after
`f9e9a9d...` but did not admit the six R3-R1 audit files committed subsequently.
No production code was changed by those commits. The original R3-R1 module is
loaded unchanged and is checked against its original SHA-256.

## Exact reviewed revisions

- R2 source baseline: `f9e9a9d59970943d967e2cbcb0a98f13b2471407`.
- HEAD of the successful saved R3-R1 report: `56347c34c36dd458d23af2851b7a1af531d00a6d`.
- Current reviewed repository HEAD: `d63e644ea4c5353cffcdd31cf183111e43e5de17`.

The current HEAD must match exactly. The preflight checks the complete set
of 19 added R2 and R3-R1 audit files, the reviewed source blobs, the absence
of staged and unstaged changes, and the committed state of the four relevant
database files. A different branch/HEAD or any other diff is rejected. This
is not a blanket exception for audit-directory changes.

## Purpose and limits

For each of the five recorded `SEARCH_FAILED` targets, this read-only audit
reconstructs the current typed root Goal and invokes only the existing
root backward-expansion provider after production's source screening. It
reports inference proposals, their subgoals, and exact matches to screened
GIVEN facts. It does not recursively search, prove a theorem, modify a source
or database, or treat a proposal as a completed proof.

Input: previously successful R1, R2, and R3-R1 `audit.json` reports. They
remain unchanged. Output: a fresh directory under
`%LOCALAPPDATA%\EHPProofTracerRecovery`, containing `audit.json` and `audit.md`.

## Execute on Windows PowerShell

Extract the ZIP from the repository's root directory and run:

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase170_r3_r2_head_sync_r1.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -NoProfile `
  -ExecutionPolicy Bypass `
  -File ".\phase170_r3_r2_head_sync_r1\run.ps1"

git status -sb
```

By default, `run.ps1` selects the latest saved R3-R1 report. It can also
accept `-R3Report 'C:\path\to\audit.json'`. The package runs only its own
focused contract tests and never launches the full pytest suite. A nonzero
exit code means the audit was refused or requires review; do not reset Git
to work around the refusal.
