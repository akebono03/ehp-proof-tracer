Phase 148 RC2-4 Repair R4.2-R1
Web depth assertion repair

Failure classification
----------------------
The preceding R4.2 run produced:
44 passed, 1 failed.

The only failure was the R4 Web-response test assertion:
Selected depth: 2

GitHub develop inspection confirmed that templates/index.html renders:

Selected depth:
          {{ group_proof_view.max_depth }}

Existing Phase 118 tests already assert the same newline/indentation contract.

Repair
------
Test-only.

Replace:
b"Selected depth: 2"

with:
b"Selected depth:\n          2"

Production changes
------------------
None.

R4.2 production semantic-closure code is not modified.

Focused rerun
-------------
The runner re-runs:
- R4.2 calculation-premise closure tests
- R4 Web depth-parity tests
- R4.1 audits
- Phase 144 equation-numbering tests
- Phase 143 direct-premise tests
- RC2 exactness-exposure tests
- Phase 118 existing depth-browser usability tests

Then it runs the R4.2 post-repair audit that the previous runner did not reach.

Phase boundary
--------------
No production change.
No recursive calculation closure.
No exactness-policy change.
No Narrative ordering change.
No repository-wide pytest.
