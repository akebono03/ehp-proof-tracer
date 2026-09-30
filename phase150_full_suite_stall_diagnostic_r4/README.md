# Phase 150 Full-Suite Stall Diagnostic R4

Diagnosis only. No production, existing-test, or documentation changes.

Runs the complete suite in one pytest process. From 30% onward an external
pytest plugin immediately flushes each test START/END, elapsed time, exact node
ID, and RSS memory when psutil is available.

If the console stalls, use a second PowerShell window:

```powershell
Get-Content .\phase150_full_suite_stall_diagnostic_r4_trace.txt -Tail 20
```

If one START remains without END for several minutes, interrupt the main run.
The trace already written remains usable.
