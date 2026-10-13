# Phase 165 R50 Delta Reason Preservation Repair

This package replaces only `phase165_r49_display_order.py` after R49 and R50 have already been applied. It keeps existing literature references intact and restores a typed EHP exactness explanation for Delta=0 when reference-aware body suppression has removed the original explanation. The reason is restored only when the existing typed ReasonSidecar identifies an `EXACTNESS_TO_DELTA_ZERO` inference. The correction is idempotent and preserves existing reference labels.

Run `run.ps1` from PowerShell after extraction to the repository root. The script saves a backup before editing the helper, then runs the existing focused R49/R50 tests. It does not run the full test suite. No root project documentation is changed.
