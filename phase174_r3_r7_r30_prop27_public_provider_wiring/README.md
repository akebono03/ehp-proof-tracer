# Phase 174 R3-R7-R30R1 — Complete Provider and Pre-install Guard

R30 was distributed with an empty `provider.py`. This package supplies the three
complete provider functions required by `audit.py`, `install.py`, and existing
regression tests. It first checks the provider contract using focused pytest,
before installing the reviewed two-function patch to the shared provider.

Unzip at the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r30_prop27_public_provider_wiring\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r30_prop27_public_provider_wiring\run.ps1'
```

The ordinary source guard and source-first publication-order checks remain
mandatory. No concrete `n=6` GIVEN, unrelated renderer change, or complete
zero-group proof is introduced. The full test suite is deferred.
