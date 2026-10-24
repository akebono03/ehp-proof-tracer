# Phase 168 R3-41P8 — ProofStep trust boundary audit

監査のみ。本体コード、既存テスト、データベースを変更しない。

## 3群の公開表示

| 群 | ProofStep | Reference | R3-41P7全文一致 | Citation | 固定基準 |
|---|---:|---:|---|---|---|
| pi3_2 | 18 | 4 | True | True | True |
| pi4_3 | 25 | 4 | True | True | True |
| pi5_4 | 10 | 3 | True | True | True |

## 偽の型付き ProofStep を利用した境界テスト

ProofNarrativeModel は引用と Step を格納するデータモデルであり、推論規則を適用した証明書ではない。
以下の人工 Step は監査入力に限り、文献や群構造の新しい事実とは扱わない。

### stable_eta

- `model_accepts_counterfeit_step`: `True`
- `same_typed_group_and_order`: `True`
- `counterfeit_inference_rule_has_matching_conclusion_pattern`: `True`
- `counterfeit_has_definition_citation`: `True`
- `genuine_projection`: `[R1]の $\eta$ 系列の定義より, $E^{2}\eta_{3}=\eta_{5}$.`
- `unverified_rule_guard_accepts_counterfeit`: `False`
- `original_shape_validator_accepts_counterfeit`: `False`
- `current_projection_rejects_counterfeit`: `True`
- `forced_validator_bypass_output`: `[R1]の $\eta$ 系列の定義より, $E^{2}\eta_{3}=\eta_{4}$.`
- `forced_bypass_would_emit_false_equation`: `True`

### ehp

- `model_accepts_counterfeit_step`: `True`
- `exactness_premise_window_matches_conclusion`: `True`
- `original_indices_are_invalid`: `True`
- `unverified_rule_guard_accepts_counterfeit`: `False`
- `real_proof_projection`: `完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ.`
- `current_projection_rejects_counterfeit`: `True`
- `forced_validator_bypass_output`: `完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ.`
- `forced_bypass_would_emit_false_exactness`: `True`

## 結論

- 公開された3群の証明は維持されている。
- 有効な出典付き Step の存在と、数学的に正しい推論済みであることは別の性質である。
- もし推論規則の guard と同等の検証なしに任意の Model を受理するなら、偽の数学的本文を表示し得る。
- 数学的再検証を完全に追放するには、検証済み Proof Tree からのみ表示へ渡す trust boundary を確定する必要がある。
- この監査は本体の実装変更を行わない。全体 pytest は Phase 終了まで実行しない。

監査状態: **PASS**
