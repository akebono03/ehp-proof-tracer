# Phase 168 R3-41P5 — 変更範囲と判断

## 事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop` の現行コード・関連テストを確認した。
また、ユーザーの R3-41P4 `review_bundle.zip`（Git HEAD `9a2834bb381da4073360959206858ff1a68acc0c`）を実際に確認した。

R3-41P4：限定32件 PASS、3群全文一致、Citation 対応良好。

## 変更対象（1ファイル・1関数）

- `phase168_r3_5_model_renderer.py`
  - `render_model_backed_narrative_markdown()` の中間表示ステップ省略条件。
  - 関数内の `from expression import IteratedSuspension` を追加。
  - 正規化規則の固定名比較を廃止し、既存の `Relation`、`FiniteCyclicGroup`、`IteratedSuspension`、`GeneratorSuspension`、`TodaSuspensionMap`、各生成元の表示同値、前提依存、Citation 有無に基づく省略条件を採用する。

変更する関数の全文と、関数内 import を含む変更後ソースファイル全文は `output/` に保存する。

## 新規テスト（独立ファイル）

- `phase168_r3_41p5_rule_name_independent/tests/test_phase168_r3_41p5_rule_name_independent.py`
  - 3群の公開 Web 本文と R3-41P4 保存全文の厳密一致。
  - 根 ProofStep の `inference_rule.name` のみ変更しても表示が不変。
  - Renderer が規則名に依存せず、推論規則の `match_guard` を再実行しないこと。

## 変更しないもの

- Backward Search / 型付き推論規則 / Narrative Model / Citation provenance。
- 安定 η 表記と EHP 完全性の数学的関数再判定。R3-41P4 で3群の呼び出し0回を確認したが、将来対象の安全性は別途監査する。
- `phase168_r3_27_typed_statement_projection.py` にある完全性説明の規則名依存。R3-41P5 の対象には含めない。
- 既存テスト・文書・公開API。

## 完了条件

1. 限定 pytest PASS。
2. 3群の本文・Reference 全文一致。
3. 規則名だけ変更しても中間表示の省略条件が変化しない。
4. 引用の落ち・重複がない。
5. 全体 pytest は Phase 168 終了時まで実施しない。
