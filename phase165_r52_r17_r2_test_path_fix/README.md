# Phase 165 R52-R17-R2: Targeted test path correction

Run `run.ps1` from the repository root after R17-R1 installation. This package changes no production code. It finds targeted test files in their actual locations, reports missing optional regressions explicitly, and requires the R17 test file. It does not run full pytest.
