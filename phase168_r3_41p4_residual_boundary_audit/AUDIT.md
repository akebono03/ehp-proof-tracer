# Phase 168 R3-41P4 — GitHub 事前確認と監査設計

## 現状と目標

R3-41P3：限定 pytest 33件 PASS、3群の証明本文と Reference の全文比較 PASS。

R3-41P4 は次の3種類を対象とする監査専用パッケージとする。

1. `_stable_eta_renaming_shape()`：`phase168_r3_27_typed_statement_projection.py` の `project_stable_eta_notation_transition()` 内で安定 η 表記の成立形状を再評価している。
2. `prop42_exactness_indices()`：同ファイル `typed_sentence()` 内で完全性の文章を描画する前に EHP 窓の添字を再検査している。
3. `inference_rule.name`：`phase168_r3_5_model_renderer.py` の重複表示省略条件、および `typed_sentence()` で完全性に由来する説明を選ぶ処理で参照される。

## GitHub `develop` で確認した主なファイル

- `phase168_r3_5_model_renderer.py`（R3-41P3 の関数が適用されていることを確認）
- `phase168_r3_27_typed_statement_projection.py`（R3-41P3 の関数が適用されていることを確認）
- `phase168_r3_3_proof_narrative_model.py`
- `phase168_r3_12_body_binding.py`
- `phase168_r3_29_order_projection.py`
- `phase168_r3_41o_renderer_closure/tests/test_phase168_r3_41o_renderer_closure.py`
- `phase168_r3_41n1_import_scope_fix/tests/test_phase168_r3_41n_composed_proof_display.py`
- `phase168_r3_29_order_projection/tests/test_phase168_r3_29_order_projection.py`
- `phase168_r3_39f_frozen_comparison/audit.py`

実際の監査結果には、ユーザーの Windows 作業ツリーにある対象ファイルの SHA-256 を収録する。GitHub とローカルが異なる可能性を前提としている。

## R3-41P4 の変更対象

- **アプリ本体の変更対象ファイル・関数：なし**。
- **新規監査ファイル：** `phase168_r3_41p4_residual_boundary_audit/audit.py` の全関数。
- **新規テスト：** `tests/test_audit_r341p4.py` の4関数。
- **Windows 実行ファイル：** `run.ps1`。
- R3-41P3 の証明本文・Reference 3群を比較用 fixture として使用する。

## 判定方針

- Proof Tree の型・前提関係を参照すること自体は再推論とはみなさない。
- 結果の正しさを数学的ルール関数で再判定する処理と、表示できる構造があるか確かめる処理を分離する。
- 既存の Model にある出典と ProofStep の関係を保持する。
- 動的に実行されない分岐は「未検証」として明記し、安易に削除しない。
- 全体 pytest は Phase 168 終了時にのみ実行する。

## 次工程への境界

R3-41P4 の監査結果で、実際に動いている数学的再検証や文字列依存の範囲を確定してから、最小修正の必要性を判定する。今回は修正を行わない。
