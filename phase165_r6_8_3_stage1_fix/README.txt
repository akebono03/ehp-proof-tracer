Phase 165 R6-8(3) Stage1 correction
Changes only probes/probe_phase53_capabilities.py:
- remove obsolete toda_45_pi4_3_finite_cyclic_transport_inference_rule import/call
- import and use toda_45_generic_finite_cyclic_transport_inference_rule from toda_stable_group_transport
No adapters, no new inference rules, no Phase55 migration.
Runs three targeted tests; no full pytest.
