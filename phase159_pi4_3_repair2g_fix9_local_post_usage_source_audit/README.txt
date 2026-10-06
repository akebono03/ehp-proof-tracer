
Phase 159 pi_4^3 repair2g fix9 audit

Purpose
-------
Inspect the actual cumulative local source between:

  filter_toda_group_proof_narrative_reference_entries_by_step_usage(...)

and

  render_toda_group_proof_narrative_reference_entries_markdown(...)

Known state
-----------
Before this segment:
- R1 (5.1) exists,
- R2 Proposition 5.1 exists,
- both entries have statement lines,
- both entries survive the no-marker step-usage filter.

At final Reference rendering:
- entries == (),
- statement_lines_by_reference_number == {}.

Therefore the disappearance occurs in the local code after the step-usage
filter and before final Reference rendering.

This audit prints:
- the exact local source segment,
- every assignment touching reference_entries or
  statement_lines_by_reference_number in the whole renderer function,
- calls appearing in the post-usage segment.

Scope
-----
Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.
