Phase 143-75AP R12 read-only trace audit

Purpose:
Trace Toda515Sigma8TransportedDecompositionStatement through the actual
pi_15^8 multi-argument Narrative runtime.

This audit does not modify production code and does not run pytest.

It reports:
- local_body_blocks containing sigma8 / 5.15 statements;
- body-renderer calls and preserved block IDs;
- generic renderer calls for target-related blocks;
- whether the target block is rendered;
- final Narrative;
- source files containing the target statement class name.
