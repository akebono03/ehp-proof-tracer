# Phase 166 R3-AC Regression Diagnostic

Read-only investigation of the missing R3-V `r=1` candidate after installing the stable eta-notation extension. Run `run.ps1` from the repository root. Compare `old_expected_generated` and `old_expected_survives` in `report.json` to identify whether candidate construction or filtering is responsible. No production code is modified and no full test suite is executed.
