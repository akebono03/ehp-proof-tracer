# Phase 150 Performance Diagnostic R2 Repair

This repairs only the standalone diagnostic environment from R2.

The Phase 144-6 audit modules import helper modules located under `tests/`.
pytest makes that layout importable during normal test execution, while the
original standalone R2 script added only the repository root to `PYTHONPATH`.

This repair adds both the repository root and `tests/` to the import path.

No production code, existing tests, or project documentation are changed.
The full regression suite is not run.
