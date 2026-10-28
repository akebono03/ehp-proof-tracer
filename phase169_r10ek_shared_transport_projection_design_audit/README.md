# Phase 169 R10EK — Shared generator transport projection design audit

This package is read-only. It compares the actual, separately implemented cyclic and direct-sum narrative projections on four already proven group queries. It never installs a shared renderer, creates an inference, changes a database source, or rewrites an existing test.

Run from the repository root after extracting the ZIP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase169_r10ek_shared_transport_projection_design_audit\run.ps1
```

The runner checks the reviewed R10EJ source hash and the reviewed R10EC and renderer blobs. It leaves existing tracked changes untouched, disables pytest cache writes, runs only six focused tests, replays the trust boundary for four complete proof trees, and writes a timestamped `output/run_*/audit.json` and proof narratives.

Included files: `contract.py`, `audit.py`, `tests/test_r10ek_contract.py`, `run.ps1`, `DESIGN_JA.md`, and `__init__.py`.

Scope is strictly architectural evidence, not unification implementation. For the final answer, avoid claiming coverage of free cyclic groups, zero groups, incomplete targets, or the separate one-stem eta-notation path.
