Phase 165 R52-R2 / Goal-only R9 compatibility repair

Scope: Only replace construct_registered_group_proof() in phase165_goal_only_search.py.
- Discover production bridge/provider on absent optional inputs.
- Preserve fail-closed unproved goals; do not fall back to legacy proofs.
- Match the established failure message expected by existing tests.
- Preserve current R52-R2 progress observer and adapter as installed.
No whole-suite pytest is run.
