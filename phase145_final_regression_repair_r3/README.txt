Phase 145 Final Regression Repair R3

Purpose
-------
Complete the minimal repair of the Phase 145-2 archive regression.

R2 proved that restoring direct imports reduced collection errors from 85 to
43 and allowed 10012 tests to be discovered before collection stopped. The
remaining errors are transitive dependencies of restored canonical test
helpers.

Scope
-----
R3 repeatedly scans the current canonical tests/ tree and restores only
missing modules that:
- are directly imported by a current tests/test_*.py file;
- have a tracked source under archive/phases/; and
- belong to the existing tests.* helper or audit_phase* dependency families.

The scan/restoration repeats until no additional missing dependency is found.

R3 does not:
- change production code;
- edit canonical test bodies or imports;
- make tests import from archive/phases;
- restore the archive wholesale;
- implement Phase 146 work;
- run repository-wide test bodies.

Verification
------------
1. Restore transitive dependencies to a fixed point.
2. Syntax-check the canonical tests/ Python files one at a time.
3. Run pytest collection only.
4. Re-run the Phase 145 focused regression set.

Only after this gate passes should the final Phase 145 repository-wide pytest
be run once:
    python -m pytest tests -q
