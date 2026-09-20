# Phase 103 — Applicable theorem / lemma discovery and relevance classification

Phase 103 は Phase 102 の recursive proof-scope exploration を、既存 inference-rule catalog に対する applicable theorem / lemma candidate discovery へ接続した。

---

# 1. 目的

```text
generator
→ actual proof ancestry
→ source statement
→ compatible inference-rule premise pattern
→ applicable theorem / lemma candidate
```

candidate discovery と proof execution は分離する。

---

# 2. Applicability candidate

```text
catalog_entry
premise_index
premise_pattern
source_step
bindings
```

```text
one matched premise != all premises satisfied
candidate != proof result
```

---

# 3. Production integration

```text
explore_standard_repository_generator_applicability_input(
  generator_input,
)
```

CLI:

```text
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

---

# 4. Relevance metadata

```text
THEOREM_SPECIFIC
MAP_PROPERTY
STRUCTURAL
GENERIC_RELATION
BRIDGE
UNCLASSIFIED
```

presentation order:

```text
THEOREM_SPECIFIC
→ MAP_PROPERTY
→ STRUCTURAL
→ BRIDGE
→ GENERIC_RELATION
→ UNCLASSIFIED
```

これは proof ranking ではない。

---

# 5. Production classification closure

```text
catalog entries = 1188
families = 267
classified families = 158
unclassified families = 109

STRUCTURAL = 201
MAP_PROPERTY = 60
THEOREM_SPECIFIC = 424
GENERIC_RELATION = 63
BRIDGE = 140
UNCLASSIFIED = 300
```

---

# 6. Strict ν′ closure

```text
MAP_PROPERTY
toda_57_nu_prime_eta6_hopf_inference_rule
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_prop59_nu_prime_eta6_squared_hopf_inference_rule

THEOREM_SPECIFIC
toda_prop56_e2_nu_prime_order_four_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
toda_prop511_pi8_2_eta2_nu_prime_eta6_squared_inference_rule

BRIDGE
toda_lemma57_nu_prime_hypothesis_inference_rule
toda_prop58_e_nu_prime_eta6_bridge_inference_rule
```

```text
strict nu-prime target residual UNCLASSIFIED entries = 0
```

---

# 7. Residual closure review

Phase 103-6D109:

```text
residual factories = 109
strict one-factory/one-family factories = 109
non-strict multi-family factories = 0
```

残る109 families / 300 entries は intentional closure-deferred residual とした。

---

# 8. Final closure audit

```text
mixed-category families = 0
unique catalog keys = OK
fixed_point_safe remains False for all entries = OK
presentation ordering = OK
strict nu-prime residual UNCLASSIFIED entries = 0
residual factories = 109
all residual factories map to exactly one residual family = OK
```

```text
PHASE103_7_CLOSURE_AUDIT = PASS
```

---

# 9. Regression

```text
Phase 103 test files = 54
409 passed in 186.07s

git diff --check:
clean
```

---

# 10. Phase boundary

未実装:

```text
automatic rule execution from candidates
automatic theorem ranking
best theorem recommendation
general theorem solver
classification of every residual family
```

Phase 103 は COMPLETE。
