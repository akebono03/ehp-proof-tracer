Phase 161-R4-R5 repair13
Reference selection source binding

Design correction
=================
Reference selection is already performed near the beginning of the public
Narrative pipeline. The defect is that only the rendered statement lines are
kept; the proof step representing the selected displayed statement is not
bound back into the Reference entry.

This leaves later filtering and body linkage free to use an aggregate proof
step that no longer matches the displayed Reference statement.

Repair
======
Add:

  _select_toda_group_proof_narrative_reference_entries_and_statement_lines()

immediately before:

  _toda_group_proof_narrative_reference_statement_lines_by_number()

The new helper performs the existing Reference statement selection and returns:

1. normalized Reference entries
2. statement_lines_by_reference_number

When the selected aggregate statement is rendered through one fixed component,
and exactly one FIXED_STATEMENT step in the presentation represents that same
component and locator, the corresponding entry.proof_steps item is replaced by
that fixed component step.

The existing statement-lines function becomes a compatibility wrapper.

The main Narrative renderer now uses the normalized entries immediately after
fixed-statement-boundary filtering, before:
- root exclusion
- body generation
- body-usage filtering
- restoration
- Reference/body linkage

This binds Reference display semantics and linkage source semantics at the same
selection stage.

No Proposition 5.1 or pi_4^2 specific production condition is added.
No dataclass/API field is added.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py
  - new helper:
    _select_toda_group_proof_narrative_reference_entries_and_statement_lines()
  - changed:
    _toda_group_proof_narrative_reference_statement_lines_by_number()
  - changed:
    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

New:
- tests/test_phase161_r4_r5_repair13_reference_selection_source_binding.py

Imports
=======
No production import changes.

Expected pi_4^2 public output
=============================
Reference:
- R1 (5.2), general form
- R2 Proposition 5.1, general higher-eta form

Body:
- [R2]より, pi_4^3 = Z/2{eta_3}.
- [R1] applied at i=4.
- eta_3 -> eta_2 eta_3.
- pi_4^2 = Z/2{eta_2^2}.
- QED

Full pytest is not run until Phase161 ends.
