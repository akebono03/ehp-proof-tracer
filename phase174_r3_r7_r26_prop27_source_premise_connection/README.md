# Phase 174 R3-R7-R26R1: Pytest Import-Mode Fix

This package fixes a test-collection name collision between the R24 and R26 `test_audit.py` modules.
It retains the original source guard and focused test selection, adding `--import-mode=importlib` and a dedicated regression test.

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r26_prop27_source_premise_connection\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r26_prop27_source_premise_connection\run.ps1'
```

No mathematical inference, production rule, registry, or other existing source file is changed. Only focused pytest is run; the full suite remains deferred.
