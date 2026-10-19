Phase 165 R6-14: read-only final dependency and pytest collection audit.
Run via run.ps1 from an extracted folder at the repository root.
No source or test files are modified or retired.
Only `python -m pytest --collect-only -q tests` is run for the application.
A zero collection return code does not mean tests pass.
Static AST checks inspect root/*.py, tests/**/*.py, probes/**/*.py; dynamic imports, generated files, and historical folders are not exhaustively examined.
Status READY_FOR_FINAL_PYTEST is a prerequisite only, not Phase 165 completion.
