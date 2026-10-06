
Phase 159 pi_4^3 repair2g fix8 audit

Purpose
-------
Locate the exact stage where the pi_4^3 public Reference entries disappear.

Known facts before this audit
-----------------------------
- Fixed-boundary filter keeps:
  R1 (5.1)
  R2 Proposition 5.1

- no-marker step-usage filter also keeps both entries.

- All four fixed source steps have used_flags=True.

- Yet final public "使用する結果" is empty.

This audit instruments:
1. _toda_group_proof_narrative_reference_statement_lines_by_number
2. filter_toda_group_proof_narrative_reference_entries_by_step_usage
3. filter_toda_group_proof_narrative_reference_entries_by_body_usage
4. render_toda_group_proof_narrative_reference_entries_markdown

It prints entry numbers and statement-line keys at every stage.

Scope
-----
Production code changes: none.
Existing test changes: none.
Repository-wide pytest: not run.
