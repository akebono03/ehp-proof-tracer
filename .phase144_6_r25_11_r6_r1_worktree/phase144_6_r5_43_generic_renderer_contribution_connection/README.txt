Phase 144-6-R5-43 generic renderer contribution connection

Files:
- toda_group_proof_narrative_contribution_ordering.py
  Adds optional current_markdown input so a renderer can reuse R5-42 ordering
  without recursively invoking the base multi-Argument renderer.
- toda_group_proof_narrative_contribution_renderer.py
  New generic opt-in renderer connection. It renders the existing Narrative,
  builds ProofChains, obtains R5-42 ordered contributions, and inserts missing
  contribution prose before the owning Argument conclusion.
- tests/test_phase144_6_r5_43_generic_renderer_contribution_connection.py
  Verifies the pi_6^3 five-contribution baseline, order, opt-in behavior, and
  absence of pi_6^3-specific production branches.

Boundary:
- Existing render_toda_group_proof_narrative_multi_argument_markdown remains
  unchanged in R5-43.
- CLI/Web/public route is not switched yet.
- No six-group prose-quality rewrite is attempted.
- No full suite is run.
