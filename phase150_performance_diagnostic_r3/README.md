# Phase 150 Performance Diagnostic R3

No production, test, or documentation changes.

The diagnostic collects the current local pytest suite, recalculates the 32%
center, selects 20 tests before and after it, and runs each selected node ID
in a separate pytest process with a 60-second timeout.

Outputs are written under `phase150_performance_diagnostic_r3_output`.
