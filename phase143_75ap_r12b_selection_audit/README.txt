Phase 143-75AP R12B read-only body-selection audit

R12 established:
- Toda515Sigma8TransportedDecompositionStatement is in local_body_blocks.
- Its block ID is included in preserve_provenance_block_ids.
- It never reaches _render_generic_narrative_proof_block.

Therefore this audit prints the current body-renderer functions responsible
for selecting/filtering render blocks before generic rendering.

No production files are modified.
No pytest is run.
