Phase 145 Final Regression Repair R6

Purpose
-------
Fix canonical test-to-test imports after Phase 145 archive cleanup.

Diagnosis
---------
R5 established that the three representative modules reported as missing by
pytest all physically exist under tests/, are tracked in the Git index, and
exist in HEAD. Therefore the failure is not missing archived content.

The canonical tests use imports such as:

    from tests.test_phase143_19_method_evidence import ...

The current repository has no tests/__init__.py. R6 adds an empty package
marker so the tests namespace resolves deterministically as the repository's
own Python package.

Files changed
-------------
New file:
- tests/__init__.py

Production files changed:
- none

Existing test files changed:
- none

Archive files changed:
- none

Verification
------------
1. Import the three representative canonical helper modules directly.
2. Run pytest collection only for tests/.
3. Run the Phase 145 focused regression set.

The repository-wide test bodies are intentionally not run by this package.
After R6 passes, the final Phase 145 gate is:

    python -m pytest tests -q
