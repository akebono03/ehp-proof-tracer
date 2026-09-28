Phase 144-6-R5-43-R3 current_markdown plumbing repair

Changed target:
- toda_group_proof_narrative_contribution_ordering.py
  - _build_visibility_occurrences
  - build_toda_group_proof_narrative_ordered_contributions
- tests/test_phase144_6_r5_43_r3_current_markdown_plumbing_repair.py

Minimal repair:
- current_markdown is optional at both API layers.
- public builder passes it to the internal visibility builder.
- five-argument R5-42 callers keep the previous behavior.
- R2's unrelated _group_key experiment is reverted to R5-42 behavior.

No public renderer route switch.
No pi_6^3-specific branch.
No full suite.
