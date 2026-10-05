Phase157-R20 repair21 runtime audit

Purpose
-------
Locate the source of the base Narrative paragraph:

  eta_3^3 = eta_3^3

repair20 proved that this paragraph is already present before contribution
insertion.

This audit wraps only the base multi-argument renderer inputs:
- render_toda_group_proof_narrative_argument_body_markdown()
- number_toda_group_proof_narrative_equations()

When the target appears in an argument body, the audit prints:
- the local body blocks;
- every proof step in those blocks;
- statement type;
- inference rule;
- generic rendered form;
- full conclusion repr.

It also records the paragraph before and after equation numbering.

Production code changes: none.
Tests: none.
pytest: not run.
