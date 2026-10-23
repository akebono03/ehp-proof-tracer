# Phase 168 R3-31a — Import Path Fix

Audit-only correction for R3-31. When `audit.py` is launched as a file from a nested folder, Python does not automatically include the repository root in `sys.path`. This package adds the repository root before importing project modules. No repository application files are changed.

Files: `audit.py` (complete file), `run.ps1`, `tests/test_phase168_r3_31_audit.py`. The existing audit logic and tests are retained.

Extract in the repository root and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase168_r3_31a_import_path_fix\run.ps1
```

Reports are written under `phase168_r3_31a_import_path_fix/output/`. Only the two audit tests and three runtime probes are run. The complete suite remains deferred.
