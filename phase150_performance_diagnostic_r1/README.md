# Phase 150 Performance Diagnostic R1

Purpose: identify the pytest tests around the interrupted 32% point and measure
only that bounded window.

This package does not modify production code, tests, or documentation.
It does not run the full regression suite.

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass `
  -File ".\phase150_performance_diagnostic_r1\run_phase150_performance_diagnostic_r1.ps1"
```

After completion, provide:

- `phase150_performance_diagnostic\REPORT.txt`
- `phase150_performance_diagnostic\window_timing.txt`
