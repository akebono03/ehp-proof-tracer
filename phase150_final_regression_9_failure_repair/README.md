# Phase 150 Final Regression 9-Failure Repair

Production code is unchanged.

Changed tests:
- tests/test_phase148_rc2_4_repair_r5.py
- tests/test_phase148_rc2_4_repair_r5_r2.py
- tests/test_phase150_rc4_5_visible_reasons.py

Phase 148 keeps semantic exactness evidence as the required contract while no
longer requiring a literal exactness phrase in generic Narrative output.

Phase 150 RC4-5 counts distinct rendered reason sentences. Multiple typed
reasons may legitimately render to the same sentence, so the rendered sentence
must be counted once rather than once per duplicate typed reason.

The package runs only focused tests. It does not run the full regression.
