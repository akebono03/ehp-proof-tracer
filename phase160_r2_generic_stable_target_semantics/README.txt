Phase 160-R2
Generic stable target / canonical base semantics

Changes:
- stable_rules.py
  - import TodaPrimaryGroup
  - add concrete Toda target validation
  - add toda_primary_group_stem(target)
  - add is_in_toda_stable_range(target)
  - add canonical_toda_stable_base(target)
  - add toda_stable_transport_exponent(target)
- tests/test_phase160_stable_target_semantics.py
  - focused tests for stems 1 and 7
  - unstable-target boundary test
  - concrete-dimension validation tests

Not included in this R2:
- construction of TodaIteratedSuspensionMap
- Toda (4.5) specialization proof step
- group-structure transport
- generator-family normalization
- public Narrative changes

Focused tests only:
python -m pytest -q tests/test_phase160_stable_target_semantics.py tests/test_stable_rules.py
