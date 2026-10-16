# Phase 165 R6-2 R4：統一規則適用監査

- status: `APPLICABILITY_AUDITED`
- 検査 Goal: 201
- 台帳規則: 55
- 接続 Provider: 8
- 証明成立の検証: 0

| Provider ID | 適用 Goal | 候補 | エラー |
|---|---:|---:|---|
| phase165_r14_r6_generic_iso.expand_generic_iso_goal | 0 | 0 | {} |
| phase165_r14_r9_ehp_exactness.expand_generic_ehp_hopf_goal | 0 | 0 | {} |
| phase165_r14_r11_delta_zero.expand_delta_zero_from_suspension_iso | 0 | 0 | {} |
| phase165_r14_r14_diagonal_and_prop42.expand_diagonal_suspension | 0 | 0 | {} |
| phase165_r57_r7_stable_expansion.expand_registered_toda45_finite_cyclic_goal | 0 | 0 | {} |
| phase165_r57_r8_eta_specialization.expand_registered_eta_specialization | 0 | 0 | {} |
| phase165_r57_r19_delta_image_backward.expand_registered_delta_image_goal | 0 | 0 | {} |
| phase165_r57_r20_general_specialization.expand_cited_general_specialization | 0 | 0 | {} |
| generic_r26 | 7 | 7 | {} |
| shared_provider | 7 | 22 | {} |

## 制約

- Emitted GoalExpansion is not a verified proof.
- Provider results are not additive: paths can overlap.
- Runtime checks are limited to registered assertion-content Goals.
- Witness and seeded paths are included in shared aggregate, not individually attributed.
- R8 argument-required factories are not automatically instantiated.
