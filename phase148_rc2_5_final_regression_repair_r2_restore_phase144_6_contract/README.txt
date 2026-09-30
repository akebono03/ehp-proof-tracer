Phase 148 RC2-5 Final Regression Repair R2

Purpose
-------
Restore tests/test_phase144_6_pi6_generic_production_route.py to the
current GitHub develop contract after earlier RC2-5 repair packages
accidentally rewrote three expectations.

Changed file
------------
tests/test_phase144_6_pi6_generic_production_route.py

Production changes
------------------
None.

Focused pytest
--------------
pytest -q tests/test_phase144_6_pi6_generic_production_route.py

Repository-wide pytest
----------------------
Not rerun. The canonical final run already executed 10401 tests:
10398 passed and only these three accidentally stale expectations failed.

Phase boundary
--------------
No RC3 ordering behavior is introduced.
