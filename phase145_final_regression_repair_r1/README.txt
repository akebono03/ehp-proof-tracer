Phase 145 Final Regression Repair R1

Purpose
-------
Repair the Phase 145-2 archival regression exposed by the final repository-wide
pytest collection.

Scope
-----
Only canonical test dependencies that are still imported directly by files
under tests/ and were moved under archive/phases/ are restored to their former
canonical import locations.

This repair does not:
- change production behavior;
- change Narrative rendering;
- change group-proof defaults;
- rewrite canonical test imports to depend on archive/phases;
- implement Phase 146 functionality;
- run the repository-wide test bodies.

Verification
------------
1. Restore direct missing canonical dependencies with git mv.
2. Syntax-check restored Python modules one file at a time.
3. Run pytest collection only for tests/.
4. Re-run the Phase 145 focused regression set.

If this gate passes, run the repository-wide pytest exactly once as the final
Phase 145 gate:
    python -m pytest tests -q
