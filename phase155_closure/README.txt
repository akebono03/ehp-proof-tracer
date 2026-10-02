Phase 155 Closure

WARNING
-------
This is the heavy, phase-final repository-wide regression.

The runner performs:

1. lightweight closure-tool tests;
2. one repository-wide `python -m pytest tests` run;
3. documentation update only if the full suite passes;
4. verification that the five updated documents were copied in full.

Progress
--------
The full pytest run prints progress every 100 completed tests.

It does not use `-x` or `--maxfail=1`, so ordinary test failures do not stop the
suite at the first failure.

Full output is continuously saved to:

    phase155_closure_output/phase155_full_pytest.log

If the full suite fails, documentation is not changed.

Documents
---------
On full-suite PASS, the following files are updated:

- README.md — English
- docs/design.md — Japanese
- docs/development_log.md — Japanese, append-oriented
- docs/roadmap.md — Japanese
- docs/proof_records.md — Japanese, append-oriented

Complete post-update copies are written under:

    phase155_closure_output/full_documents/

Phase boundary
--------------
Phase 155 closes test-suite consolidation only.

Phase 156 functionality is not implemented here.
The next phase is Reference statement relevance / minimal display.
