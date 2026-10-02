# GitHub baseline — Phase 155 Closure-R2B-R2

Repository: `akebono03/ehp-proof-tracer`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Inspected before R2B-R2:
- tests/test_phase144_6_r5_43_6.py
- tests/test_phase144_6_r5_43_8.py
- tests/test_phase144_6_r5_43_9.py
- tests/test_phase144_6_r5_43_10_transport_chain_compression_production.py
- tests/test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py
- tests/test_phase144_6_r5_43_11a_insertion_failure_classification_audit.py
- tests/test_phase144_6_r5_43_11c_non_detached_fallback_placement_repair.py
- tests/test_phase144_6_r5_43_11d_final_completion_audit.py
- audit_phase144_6_r5_43_8.py
- audit_phase144_6_r5_43_9.py
- audit_phase144_6_r5_43_11.py
- audit_phase144_6_r5_43_11a.py
- audit_phase144_6_r5_43_11d.py

Critical verified boundary:
`completion_invariants_pass()` checks six groups, selected>0,
participating_selected == participating_insertable,
detached_insertable <= detached_selected, transport_connectors == 16, and
missing_inserted_lines == 0.

It does NOT check duplicate violations, contribution order violations, or
conclusion-placement violations.
