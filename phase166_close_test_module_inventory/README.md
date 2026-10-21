# Phase 166 Closure: Explicit Test Module Inventory

This package avoids importing installation/migration scripts during pytest collection. It parses candidate Python filenames (`test_*.py` and `*_test.py`) and supplies only files defining top-level `test_` functions or `Test` classes as explicit pytest arguments. It does not alter existing tests or production code. All omitted and unreadable candidates are listed in `test_inventory.json`. This is a guarded broad suite, not a claim that every possible dynamically declared test is covered.
