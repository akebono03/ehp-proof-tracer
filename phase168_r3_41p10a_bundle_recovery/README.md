# Phase 168 R3-41P10A — Review Bundle Recovery

This is a packaging fix for the audit-only R3-41P10 script. It does not change EHP Proof Tracer application modules, ProofSteps, mathematical rules, or existing test files.

The R3-41P10 run already passed its audit and focused tests, but its last step could fail while deleting `review_bundle.tmp.zip` in a Dropbox-synced working directory. The revised runner creates the review ZIP directly from an explicit set of output files, excluding pre-existing review ZIPs. If the fixed-name ZIP is temporarily locked, it falls back to a unique output filename.

## Recovery

Extract the ZIP at the EHP Proof Tracer repository root, then execute:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r3_41p10a_bundle_recovery\run.ps1"
```

The launcher backs up the old audit runner, installs the complete replacement `run.ps1`, and calls it with `-BundleOnly`. Existing `audit.json`, fulltext captures, and pytest logs are packaged without rerunning the audit or any tests. The console prints the exact path in `REVIEW_BUNDLE`.

An unexpected SHA-256 of the old runner causes the installer to stop without changing it. If the runner is already updated, the operation is repeatable. The entire new runner is in `run_FIXED.ps1`; there are no abbreviated code excerpts.

To rerun the complete *focused* audit later, use the existing R3-41P10 `run.ps1` without `-BundleOnly`. The full pytest suite remains deferred until the end of Phase 168.
