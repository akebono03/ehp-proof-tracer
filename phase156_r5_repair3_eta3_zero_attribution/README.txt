Phase 156-R5 repair3 — eta_3 twice-zero attribution

Current diagnosis
=================
After repair2, pi_6^3 has two "(5.3)" Reference entries.

ENTRY 1:
  rule: Toda 5.3 nu-prime Lemma 5.2 bracket specialization
  statement:
    nu' in {eta_3, 2 iota_4, eta_4}_1
  correct source:
    Toda (5.3)

ENTRY 2:
  rule: Toda 5.3 eta_3 twice zero
  statement:
    2 eta_3 = 0
  current source:
    inferred from internal rule name as Toda (5.3)
  correct source:
    Toda Proposition 5.1, via pi_4^3 = Z/2{eta_3}

Production change
=================
toda_rules.py

Function:
  toda_53_eta3_twice_zero_inference_rule()

Add explicit:
  label   = Toda Proposition 5.1
  locator = Proposition 5.1

No import changes.

Tests
=====
New:
  tests/test_phase156_r5_repair3_eta3_zero_attribution.py

Existing repair2 and Phase144/58/153 tests are rerun.

Completion
==========
- eta_3 twice-zero attribution -> Proposition 5.1
- Lemma 5.2 explicit attribution 3/3
- pi_6^3 has exactly one (5.3)
- pi_6^3 has exactly one Lemma 5.2
- pi_6^3 has exactly one Proposition 5.1
- no composite (5.3) / Lemma 5.2
- 112 groups, exceptions 0

Boundary
========
No proof-body ordering changes.
No repository-wide pytest until Phase 156 closure.
