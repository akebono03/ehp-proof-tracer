# Phase 171 R20R4R2 — Source-Guarded Public Proof Audit

This is a read-only reissue of the R20R4 audit package after a legitimate
HEAD update. It retains the Python module launch from R20R4R1 and changes only
the audit preflight guard. Instead of freezing commit identifiers, the audit
verifies the on-disk production search engine and shared expansion provider
against GitHub-reviewed blob hashes for commit
`788261264e63d202b9e9bfe819212f12e0d0134e`.

## Run on Windows PowerShell

Extract this archive at the repository root, then execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r4_first_success_public_audit\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r4_first_success_public_audit\run.ps1" -RightOnly
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r20r4_first_success_public_audit\run.ps1"
```

The audit does not change production code or prior tests. A source hash
mismatch halts the run without writing to tracked files. Only two focused
existing tests are run; the full test suite is not invoked.

Audit results are stored in the package `output/` directory. A successful
search result does not establish an actual Web UI display without separate
verification.
