Phase 165 R12-R9 - EHP exactness connection audit

This is a read-only source-window inventory and does not yet derive a new
ProofStep. In particular, classified EHP windows are not equalities of
concrete subgroups unless established with existing inference rules.

Extract ZIP into the project root, then run:
  powershell -ExecutionPolicy Bypass -File .\phase165_r12_r9_ehp_connection\run.ps1

Files changed in production: none.
New files: __init__.py, audit.py,
 tests/test_phase165_r12_r9_ehp_connection.py, run.ps1, README.txt.
Run targeted pytest only. No full pytest.
