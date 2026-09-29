Phase 143-75AI read-only audit

Target:
TodaProp59DeltaKernelStatement

Current inventory:
- total fallback occurrences: 116
- target: 15 occurrences / 15 groups
- rule: Toda Proposition 5.9 Delta nu_5 kernel

GitHub inspection confirms a Phase 70 canonical statement with:
- map = TodaDeltaMap(pi_8^5 -> pi_6^2)
- kernel_group = FiniteCyclicGroup(order=2, generator=4 nu_5)

This audit checks all Narrative runtime instances before any renderer is
implemented. The candidate semantic form is:

Ker(Delta: source -> target) = kernel_group

The audit verifies field names, map/group types, and whether all occurrences
share a safe first-class structure.

Read-only.
No production/test/docs changes.
No pytest.
