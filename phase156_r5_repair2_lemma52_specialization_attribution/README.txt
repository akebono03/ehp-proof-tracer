Phase 156-R5 repair2 — Lemma 5.2 specialization attribution

Production change:
- toda_rules.py
  - toda_53_nu_prime_lemma52_hopf_inference_rule()
  - toda_53_nu_prime_lemma52_double_inference_rule()
  - toda_53_nu_prime_lemma52_membership_inference_rule()

Each rule receives:
  label   = Toda Lemma 5.2
  locator = Lemma 5.2

(5.3) remains the source attribution for:
  nu' in {eta_3, 2 iota_4, eta_4}_1

Updated legacy test:
- tests/test_phase144_6_r3_production_references.py

New focused test:
- tests/test_phase156_r5_repair2_lemma52_specialization_attribution.py

Import changes:
- none

Completion:
- 3/3 Lemma 5.2 rules have explicit attribution
- no composite (5.3) / Lemma 5.2 header
- pi_6^3 has exactly one (5.3) header
- pi_6^3 has exactly one Lemma 5.2 header
- 112 groups, exceptions 0

Boundary:
This repair changes Reference attribution only.
Proof-body ordering is not changed.
Repository-wide pytest is reserved for Phase 156 closure.
