Phase 156-R5 repair4 — bridge Reference inference

Production:
- toda_group_proof_narrative_references.py
- _infer_toda_group_proof_literature_reference_from_rule_name()

Rule:
If an inference rule has no explicit LiteratureReference and its rule name
contains "bridge", do not infer a literature reference from the rule name.

Explicit LiteratureReference is still honored before fallback inference.

Why:
E^2 eta_3 = eta_5 is derived from eta-family definition statements.
It is an internal structural bridge, not a direct statement of Toda (5.3).

Tests:
- new focused repair4 tests
- Phase58 / Phase144 / Phase153 / Phase156-R5 repair regression
- 112 groups at depth 2 and depth 3

No import changes.
No proof-body ordering changes.
Repository-wide pytest remains reserved for Phase 156 closure.
