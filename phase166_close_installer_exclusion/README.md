# Phase 166: installer-safe full test run

Run `run.ps1` from PowerShell. It runs the repository-wide pytest command while excluding files named `install_and_test.py`, which are installer entrypoints that may modify source code on import. Ordinary test files remain eligible for collection. The excluded paths, git state, full output, and exit code are retained in a timestamped `results` directory. No production code or existing tests are changed by this package.

Pass condition: pytest exit code 0. Other collection failures or test failures must be reported without being hidden.
