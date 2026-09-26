Phase 143-75AL read-only audit

Target:
Toda514FirstShortExactStatement

Current inventory:
- total fallback occurrences: 79
- target: 10 occurrences / 10 groups
- rule: Toda (5.14) first short exact sequence

GitHub Phase 75 canonical instance stores:
- source_group = pi_12^5
- middle_group = pi_13^6
- target_group = pi_13^11
- suspension_map E
- hopf_map H

The audit checks all Narrative runtime instances and whether any explicit
zero-endpoint / short-exactness field exists before choosing rendering.

Read-only.
No source/test/docs changes.
No pytest.
