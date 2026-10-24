# Phase 168 R3-41L — 実装内容

## 変更するファイル

- `phase168_r3_5_model_renderer.py`
  - `render_model_backed_narrative_markdown()`：全体を置換。モジュール先頭の import は変更しない。関数内部の新規 import は関数全文に記載。
- 新規 `phase168_r3_41l_reasoned_prose/tests/test_phase168_r3_41l_reasoned_prose.py`：限定テスト全文。
- 既存テスト・固定基準・証明探索・Reference 台帳は変更しない。

## 最小限の変更

1. 一般の対角群関係・円周零群・球面の次元未満の零群に対して、**直接の GIVEN 前提**と既存の特殊化判定・整数境界が一致する場合に限って、`model.step_citation_numbers` の番号を表示する。
2. `TodaSuspensionIsomorphismStatement` が、同じ写像の `GeneratorSuspension` を実際の前提に含む場合に限って、文頭に「これより」を付ける。
3. 該当しない推論、未完成証明、他の型付き文は変更しない。

## テスト

- 新規限定テスト：3群の完全証明、(5.1) の具体的な出典、懸垂同型の接続、未変更群での表示、Reference 番号、根拠不明の推論の保守性。
- 既存限定テスト：R3-41J2, R3-41I, R3-26a, R3-19。
- 差分監査：従来どおり `BASELINE_REVIEW_REQUIRED` を欠陥件数と混同しない。

## 完了条件と境界

限定テストの成功、3群の Reference 本文欠落0・引用番号欠落0・基準論証不足0、固定基準と ProofStep の順序維持を確認する。Phase 168 の全体 pytest は終了時のみ実行する。

次の区切りでは終了条件、Web 表示と既存互換 API、ドキュメントを確認する。
