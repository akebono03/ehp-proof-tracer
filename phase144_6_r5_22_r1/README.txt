Phase 144-6-R5-22-R1 runner-only repair.

The Phase 22 targeted tests passed, but the standalone audit failed because
test_phase65_equation57_injectivity.py lives under tests/ and the standalone
Python process had only the repository root on PYTHONPATH.

This repair changes no production code, audit logic, or tests.
It adds both the repository root and repository tests directory to PYTHONPATH
before rerunning the existing Phase 21/22 targeted tests and Phase 22 audit.
