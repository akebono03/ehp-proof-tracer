# Phase 150 Full-Suite Stall Diagnostic R4 Repair R1

## Repair

The original R4 passed a filesystem path to `pytest -p`. Pytest expects a
Python import name there.

Repair R1 therefore makes only these runner changes:

1. Add this package directory to `PYTHONPATH`.
2. Load the plugin with `-p phase150_stall_trace_plugin`.
3. Run an explicit plugin-import preflight before pytest.

No production code, existing tests, mathematical assertions, or diagnostic
behavior are changed.

## Run

Use the supplied PowerShell runner from the repository root.

If pytest later appears stalled, open another PowerShell window and run:

```powershell
Get-Content .\phase150_full_suite_stall_diagnostic_r4_trace.txt -Tail 20
```

The last `START` without a matching `END` identifies the currently executing
test. RSS memory is also recorded when `psutil` is installed.
