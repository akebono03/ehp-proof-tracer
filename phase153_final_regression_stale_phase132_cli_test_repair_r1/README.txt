Phase 153 Final Regression — Stale Phase 132 CLI Test Repair R1
====================================================================

Production changes
------------------
None.

Updated file
------------
tests/test_phase132_7_group_proof_cli_modes.py

Updated tests
-------------
test_phase132_7_group_proof_default_mode_is_narrative
test_phase132_7_group_proof_narrative_mode_uses_narrative_renderer

Reason
------
The current CLI contract is that group-proof defaults to Narrative mode at
depth 2. The Phase 132 tests still identified Narrative by old public Markdown
headings such as "# Group proof narrative" and also required the old root
Reference "[R1] Proposition 5.15."

Current generic Narrative output no longer guarantees those presentation
details. Phase 153 Reference filtering also excludes root self-references.

The repaired tests verify the current CLI contract instead:
- mode defaults to narrative;
- depth defaults to 2;
- CLI execution succeeds without stderr;
- generic Narrative content is present;
- the final pi_16^9 result is present;
- trace output "# Group result" is absent.

No production code and no Phase 154 prose behavior are changed.

After focused verification passes, run:

python -m pytest .\tests -x

to locate the next final-regression failure, if any.
