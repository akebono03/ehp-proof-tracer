Phase 161 Reference range whitespace repair

Target:
  toda_group_proof_narrative_references.py
  render_toda_group_proof_narrative_reference_entries_markdown()

Replace the two replacements in the already-installed Phase 161 renderer:
  component.range_text.replace(">=", r"\ge ")
  .replace("<=", r"\le ")
with:
  component.range_text.replace(">=", r"\ge")
  .replace("<=", r"\le")

This retains original trailing whitespace after >= and <= in range_text.
The apply script is idempotent and fails closed on unknown renderer versions.
The existing two focused tests and a new whitespace/duplication test run.
No full suite is invoked.
