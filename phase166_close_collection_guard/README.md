# Phase 166 closure: pytest collection guard

Runs the repository-wide pytest suite while excluding exactly one known installer `phase165_r6_8_eta_name_fix/install_and_test.py` from collection. The script is not a test: its module body rewrites production files and can raise `SystemExit`. No tests or production files are modified by this package. Pytest may still identify other problems; closure is granted only for exit code 0.
