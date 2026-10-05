Phase157-R20 repair11 runtime audit

Purpose
-------
Locate the exact final pipeline stage that removes Proposition 5.3 from the
public Reference section in the cumulative local Phase157-R20 tree.

Method
------
No production file is modified.

At runtime only, wrappers are installed around:
- _toda_group_proof_narrative_reference_statement_lines_by_number
- filter_toda_group_proof_narrative_reference_entries_by_body_usage
- restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage
- render_toda_group_proof_narrative_reference_entries_markdown

For every call, the audit prints:
- Reference number;
- literature locator;
- selected statement lines;
- whether the current body contains that Reference marker.

It then prints the final public Narrative and call counts.

No production code changes.
No tests.
No documentation changes.
No pytest.
