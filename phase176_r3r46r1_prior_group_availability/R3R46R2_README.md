# Phase 176 R3R46R2 — Focused pytest import isolation

Overlay this ZIP on the already extracted R3R46R1 package at the repository root. It replaces only its `run.ps1` and adds a focused test runner and this documentation. The prior guarded production patch and actual Web audit are unchanged. No rollback, reset, commit, or push is performed.

The reviewed develop HEAD is `d91cb175ea361e0b4433092bc0a004e78a787f15`. `tests/conftest.py` inserts the `tests` directory first in `sys.path`, where `tests/hopf_rules.py` defines a different `HopfInvariantStatement` without `source` and `note`. The root `hopf_rules.py` has both fields. Combining historical `tests/` and phase-specific suites in the same pytest invocation exposes the collision. Importlib collection mode alone cannot undo explicit `sys.path` edits.

Each original focused test file is now run in its own interpreter. The runner checks and loads the root Hopf modules before pytest collection, then verifies the signature and identity of the actual production fact. It does not replace test stubs or change `tests/conftest.py`, and it does not alter mathematical inference. The original public audit runs in another fresh interpreter only after all focused groups pass. No full suite is run.

Run the original package's `run.ps1 -DryRun`, then `run.ps1`. The idempotent R3R46R1 installer handles the already applied production patch. If canonical import checks or tests fail, the process stops with the precise failing group. R3R46R1 completion requires the actual public audit PASS, not just a successful import or collection.
