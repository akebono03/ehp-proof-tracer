# Phase 165 R4 変更範囲

対象となる6関数：
- `toda_pi4_3_delta_image_free_cyclic_inference_rule`
- `toda_pi4_3_finite_cyclic_inference_rule`
- `toda_pi4_3_zero_right_implies_suspension_surjective_inference_rule`
- `toda_pi4_3_exactness_delta_image_to_suspension_kernel_inference_rule`
- `toda_pi4_3_eta3_generator_inference_rule`
- `toda_45_pi4_3_finite_cyclic_transport_inference_rule`

変更先：上記関数の所在するルート Python モジュール、`standard_production_applicability_catalog.py`、その関数を直接呼ぶ `tests/test_*.py` のテスト関数・import のみ。新しい証明規則は実装しない。

実行：専用 pytest 3件。全体 pytest は Phase 165 終了まで行わない。

完了条件：対象関数定義・規則台帳登録が消え、ルート本番コードの生きた参照がない。次段階は一般規則の接続監査。
