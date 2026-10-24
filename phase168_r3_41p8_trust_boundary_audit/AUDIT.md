# Phase 168 R3-41P8 — ProofStep の信頼境界監査

## 対象

- `phase168_r3_3_proof_narrative_model.py`: `ProofNarrativeModel`、`build_proof_narrative_model()`
- `phase168_r3_27_typed_statement_projection.py`: `project_stable_eta_notation_transition()`、`typed_sentence()`
- `phase166_r3ac_stable_notation.py`: `_stable_eta_renaming_shape()`、`stable_eta_notation_rule()`
- `phase165_r12_r11_prop42_unified.py`: `prop42_exactness_indices()`
- `phase165_r12_r12_ehp_consequences.py`: `ehp_image_equals_kernel_inference_rule()`

GitHub `akebono03/ehp-proof-tracer` の `develop` と関連テストを、実装・監査前に確認した。今回の変更対象は新規監査パッケージのみであり、既存アプリケーションの import、クラス、関数、テストは変更しない。

## 目的

R3-41P7 では表示の数学的形状検査が偽の Step を拒否していることを確認した。今回はより厳しい入力（推論規則・関連型・Citation を備えた偽の Step）でも、任意の Model 自体を証明書と扱えるかどうかを確認する。

比較用の 3 群全文は R3-41P7 の保存版。Reference、Citation、ProofStep の現状を変更しない。

## 完了条件

- 3 群の証明本文と Reference が R3-41P7 全文と一致する。
- 公開3群の Citation 対応と固定基準が全て通過する。
- 偽の η / EHP Step の数学的 guard が拒否することを確認する。
- 形状検査を監査内でだけ無効化した場合に偽表示の危険があるか記録する。
- 既存コードへの変更 0、限定 pytest のみ、全体 pytest は実行しない。

## 次工程との境界

この監査は Renderer の実装変更を行わない。Proof Tree の妥当性をどこで保証するかを明確にしてから、表示処理の数学的再検証を削除するか判定する。
