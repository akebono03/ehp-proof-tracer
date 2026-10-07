Phase 159 pi_4^3 repair2g fix4v1

Purpose
-------
Repair only the verification-script import path.

Observed failure
----------------
The previous verification package failed with:

ModuleNotFoundError:
  No module named 'toda_literature_statement_boundary'

Cause
-----
When Python runs a script inside the extracted verification package,
the script directory becomes sys.path[0]. The repository root is not
guaranteed to be importable merely because PowerShell changed the
working directory.

Fix
---
Before importing repository modules, add:

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

Scope
-----
Production code changes: none.
Existing test changes: none.
Only the verification script is changed.
Repository-wide pytest is not run.
