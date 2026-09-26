Phase 143-75AP R10D read-only audit

Purpose:
Print the complete current-local definitions of:
- render_toda_group_proof_narrative_argument_body_markdown
- extract_toda_group_proof_narrative_argument_local_body_blocks
- _insert_toda_group_proof_narrative_transition_connector

R10C established that the multi-argument renderer inserts the DERIVATION
connector immediately before argument.conclusion_block. R10D determines
whether the aggregate semantic source is removed by local-body selection
or by body rendering.

No production files are modified.
No tests are run.
