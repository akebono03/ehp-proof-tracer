# Phase 168 R3-41P7 — 既存証明済み情報と表示再判定の責務境界監査

## 監査範囲

- audit-only。アプリケーションコード、既存テスト、DB を変更しない。
- 対象: `_stable_eta_renaming_shape()`、`prop42_exactness_indices()`。
- 検証済み ProofStep の出典を利用した表示と、不正入力に対する拒否を区別する。
- 人工 Probe は表示境界の性質を調べるだけで、数学的証明として使用しない。

## 既存コードの責務配置

| 関数 | 証明側の使用 | 表示側の使用 |
|---|---|---|
| `_stable_eta_renaming_shape` | `stable_eta_notation_rule` の guard 等 | `project_stable_eta_notation_transition` |
| `prop42_exactness_indices` | Proposition 4.2 の特殊化と EHP 像＝核規則 | `typed_sentence` |

いずれも単なる LaTeX 整形ではなく、数学的形状・添字を検査する。
表示側での再検査を削除するには、型付き ProofStep の妥当性を信頼する境界と不正入力時の挙動を明示する必要がある。

## 3群の比較

| 群 | ProofStep | Reference | R3-41P6全文 | Citation | 固定基準 |
|---|---:|---:|---|---|---|
| pi3_2 | 18 | 4 | PASS | PASS | PASS |
| pi4_3 | 25 | 4 | PASS | PASS | PASS |
| pi5_4 | 10 | 3 | PASS | PASS | PASS |

## 動的な検査関数の呼び出し

- `public_cases`: `{}`
- `probes`: `{'_stable_eta_renaming_shape / phase166_r3ac_stable_notation.py / guard': 1, '_stable_eta_renaming_shape / phase168_r3_27_typed_statement_projection.py / project_stable_eta_notation_transition': 3, 'prop42_exactness_indices / phase168_r3_27_typed_statement_projection.py / typed_sentence': 2}`
- `details`: `[{'validator': '_stable_eta_renaming_shape', 'caller_file': 'phase166_r3ac_stable_notation.py', 'caller_function': 'guard', 'from_projection': False, 'accepted': True}, {'validator': '_stable_eta_renaming_shape', 'caller_file': 'phase168_r3_27_typed_statement_projection.py', 'caller_function': 'project_stable_eta_notation_transition', 'from_projection': True, 'accepted': True}, {'validator': '_stable_eta_renaming_shape', 'caller_file': 'phase168_r3_27_typed_statement_projection.py', 'caller_function': 'project_stable_eta_notation_transition', 'from_projection': True, 'accepted': False}, {'validator': '_stable_eta_renaming_shape', 'caller_file': 'phase168_r3_27_typed_statement_projection.py', 'caller_function': 'project_stable_eta_notation_transition', 'from_projection': True, 'accepted': True}, {'validator': 'prop42_exactness_indices', 'caller_file': 'phase168_r3_27_typed_statement_projection.py', 'caller_function': 'typed_sentence', 'from_projection': True, 'accepted': True}, {'validator': 'prop42_exactness_indices', 'caller_file': 'phase168_r3_27_typed_statement_projection.py', 'caller_function': 'typed_sentence', 'from_projection': True, 'accepted': False}]`

## 明示的な形状 Probe

### stable_eta

- `source`: `synthetic r=2, based on phase166_r3ac_stable_notation/tests/test_r3ac.py`
- `rule_guard_has_valid_match`: `True`
- `valid_projection`: `[R1]の $\eta$ 系列の定義より, $E^{2}\eta_{3}=\eta_{5}$.`
- `valid_projection_has_citation`: `True`
- `invalid_order_projection`: `None`
- `invalid_order_rejected`: `True`
- `uncited_projection`: `None`
- `uncited_rejected`: `True`

### ehp

- `source`: `observed EHPImageEqualsKernelStatement from public search`
- `valid_window`: `TodaEHPExactnessWindow(source_term=TodaPrimaryGroup(group_dimension=5, sphere_dimension=5), middle_term=TodaPrimaryGroup(group_dimension=3, sphere_dimension=2), target_term=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3), first_map=MapSymbol(name='Δ'), second_map=MapSymbol(name='E'))`
- `valid_math_indices`: `(2, 4, 'delta_e')`
- `valid_projection`: `完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ.`
- `invalid_math_indices`: `None`
- `invalid_projection`: `None`
- `valid_projection_present`: `True`
- `invalid_window_rejected`: `True`

## 判定上の注意

- 3群で動的再検証が0回でも、その関数が将来群の表示に不要とは断言できない。
- 不正な人工 ProofStep が拒否された場合、検証関数の即時削除は不正表示を発生させる危険がある。
- `ProofNarrativeModel` は引用 provenance を持つが、全 ProofStep を数学的に再検証したことを示す専用証明書ではない。
- R3-41P7 では実装の移動・削除を行わず、結果を踏まえて最小修正を別工程で判断する。
- 全体 pytest は Phase 168 の終了時まで実行しない。
