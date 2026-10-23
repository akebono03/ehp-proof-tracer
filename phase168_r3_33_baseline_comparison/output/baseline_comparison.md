# Phase 168 R3-33 — 固定基準比較

判定: AUDIT_ONLY

| 群 | 順序一致 | 欠落・表記差 | 順序差・重複 | Reference一致 |
|---|---:|---:|---:|---|
| pi_3^2 | 13 | 0 | 0 | True |

## pi_3^2

- complete_ehp_sequence: IN_ORDER
- pi21_zero: IN_ORDER
- hopf_injective: IN_ORDER
- pi11_free: IN_ORDER
- pi22_free: IN_ORDER
- suspension_generator: IN_ORDER
- suspension_iso: IN_ORDER
- delta_zero: IN_ORDER
- hopf_surjective: IN_ORDER
- hopf_iso: IN_ORDER
- pi33_free: IN_ORDER
- hopf_generator: IN_ORDER
- final_group: IN_ORDER
| pi_4^3 | 12 | 0 | 0 | True |

## pi_4^3

- complete_ehp_sequence: IN_ORDER
- suspension_generator: IN_ORDER
- diagonal_general: IN_ORDER
- pi55_free: IN_ORDER
- delta_generator: IN_ORDER
- delta_image: IN_ORDER
- kernel: IN_ORDER
- pi45_zero: IN_ORDER
- suspension_surjective: IN_ORDER
- source_group: IN_ORDER
- quotient: IN_ORDER
- final_group: IN_ORDER
| pi_5^4 | 2 | 4 | 0 | True |

## pi_5^4

- source_group: IN_ORDER
- toda45_specialization: MISSING_OR_DIFFERENT_EXPRESSION
- transport_map: MISSING_OR_DIFFERENT_EXPRESSION
- transport_isomorphism: MISSING_OR_DIFFERENT_EXPRESSION
- generator_transport: MISSING_OR_DIFFERENT_EXPRESSION
- final_group: IN_ORDER

## 注意

- Expression checks are conservative literal tokens, not semantic theorem equivalence.
- Out-of-order status may reflect repeated phrases such as 'は同型'.
- Reference numbers from the historical baseline are intentionally ignored.
- Frozen baseline files are preserved byte-for-byte.
- No production code is modified and full pytest is not run.
