# Phase 143-1

This package replaces `toda_group_proof_generic_narrative_renderer.py`
and adds `tests/test_phase143_1_generic_proof_order.py`.

The generic proof renderer now derives a proof order from block dependencies.
Dependencies are visited before their parent block. TARGET blocks are used only
as a general tie-breaker and are visited after non-TARGET blocks; there is no
pi_6^3-specific branch.

Phase 142-2 diagnostic block rendering is unchanged.
Phase 142-3 generic proof rendering uses the new proof order.
