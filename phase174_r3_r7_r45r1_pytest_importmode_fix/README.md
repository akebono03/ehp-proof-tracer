# Phase 174 R3-R7-R45R1: Pytest Import Mode Repair

This small, source-guarded repair changes only the R45 audit runner and its
static regression test. Historic Proposition 4.2 regression test directories
share the names of their corresponding top-level Python modules. Pytest
`--import-mode=importlib` can import a directory namespace instead of the
actual module; for these two historical test groups, the runner now uses
`--import-mode=prepend`. All R45 audit tests keep `importlib` mode.

Unpack into the repository root and run `run.ps1 -DryRun` first, then
`run.ps1`. The patch is idempotent and refuses unreviewed source bytes or
tracked changes. It changes no production files, proof assumptions, inference
rules, or source references. No full pytest suite or HTTP check is performed.
