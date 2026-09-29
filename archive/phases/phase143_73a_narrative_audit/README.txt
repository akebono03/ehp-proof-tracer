Phase 143-73A actual Narrative re-audit

This package does not modify implementation, tests, or documentation.

Audited production path:
  build_standard_toda_report
  -> build_toda_group_result_proof_replay
  -> build_toda_group_proof_presentation
  -> render_toda_group_proof_narrative_markdown

Cases:
  pi_7^5
  pi_8^6
  pi_9^7
  pi_10^8
  pi_11^9
  pi_12^10

Checks:
- ScalarGreaterEqualStatement is absent from rendered Narrative.
- TodaEtaFamilyDefinitionStatement is absent from rendered Narrative.
- At least one human-readable scalar >= condition is present.
- "eta-family definition" human-readable label is present.

Run from repository root with PYTHONPATH set to the repository root.
