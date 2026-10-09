Phase 162 R7-B: Delta premise reuse, focused repair.

Changes:
- toda_group_proof_narrative_contribution_renderer.py
- insert_toda_group_proof_narrative_map_property_dependencies() only
- no import changes or inference changes

The matching helper in this function previously treated >1 matching paragraphs
as missing. It now reuses the earliest existing matching paragraph so that
map-property dependency insertion does not duplicate visible facts.

The apply script writes the ENTIRE modified function to modified_function.py.
This file is generated from your actual local file for exact replacement.
Backups are created before modification.

Tests: 3 newly added tests and 3 preexisting R7-B final tests.
No full suite.

Completion: test suite passes, duplicated Delta phrase occurs fewer than
8 times and root math statement is preserved.
Next: identify and resolve original duplicated premise ownership, and separately
audit stable tail and eta-square expression. No other changes anticipated here.
