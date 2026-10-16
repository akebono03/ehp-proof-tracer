# Phase 165 R6-2: Retire the pi4^3-only adapter

Run `run.ps1` from the repository root after extracting this package. It runs six focused tests, removes the explicit pi4^3 adapter import and tuple entry from the shared expansion provider, and quarantines the retired Python module with `.r6_2_removed.bak` suffix. Backups are retained at the repository root. It does not introduce a generic replacement or assert the pi4^3 proof will complete. No full test suite is run.

The installer refuses unexpected source shapes and repeat installations. It prints the changed production path and backup name. Existing historical archives and tests are not removed.
