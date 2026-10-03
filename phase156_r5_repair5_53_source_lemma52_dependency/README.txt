Phase 156-R5 repair5 — (5.3) source / Lemma 5.2 proof dependency

変更対象
========
Production:
- toda_rules.py
  - toda_53_nu_prime_lemma52_hopf_inference_rule()
  - toda_53_nu_prime_lemma52_double_inference_rule()
  - toda_53_nu_prime_lemma52_membership_inference_rule()
- toda_group_proof_narrative_reason_renderer.py
  - render_toda_group_proof_narrative_reason_sentence()
  - _toda_group_proof_narrative_reason_insertion_index()

Tests:
- tests/test_phase150_rc4_5b_3_reference_binding.py
- tests/test_phase156_r5_repair5_53_source_lemma52_dependency.py

import変更
==========
なし。

意味
====
Reference source:
  Toda (5.3)

Internal proof dependency:
  Lemma 5.2

本文順:
  nu' bracket membership
  -> 2 eta_3 = 0
  -> Lemma 5.2 を beta = nu' として適用

群計算・InferenceRule の conclusion 自体は変更しない。
repository-wide pytest は Phase 156 closure 最後のみ。
