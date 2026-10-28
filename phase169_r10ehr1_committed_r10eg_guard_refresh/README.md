# Phase 169 R10EH-R1 — Reviewed R10EG Git blob guard refresh

This package fixes only the R10EH audit runner precondition after R10EG was committed to `develop` as `1a132f382b4fe93b1ab3cb30f5d9178684e9c65a`. It does not change proof rules, search, the renderer, databases, existing tests, or the original R10EH `run.ps1`.

The old reviewed transport blob `d60770fff1b6e14791db6b952733f4062a64c8eb` was replaced by the committed R10EG blob `3865d1e57923a0d45f0240cc357110e51b20a3e1`. The new runner checks the R10EG commit ancestry, the committed Git blob, and the currently checked-out `transport.py` bytes. All other reviewed dependency fingerprints are retained.

Extract this ZIP alongside the existing `phase169_r10eh_stem6_10_11_14_audit` directory and run `powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase169_r10ehr1_committed_r10eg_guard_refresh\run.ps1"` from the repository root. This wrapper verifies the old runner SHA-256, runs three guard tests, temporarily stages the entire reviewed replacement runner in the R10EH folder, delegates its eight focused policy tests and four live audits, then removes only that temporary runner. The original runner is never overwritten.

Outputs from R10EH are saved in its timestamped `output/run_*` directory. No repository-wide pytest is run. The four audit outcomes have **not** been preverified in the user's Windows environment.
