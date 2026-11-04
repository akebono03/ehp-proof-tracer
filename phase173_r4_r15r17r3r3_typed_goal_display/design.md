# Phase 173 R15R17-R3R3 設計

## 背景

R15R17-R3R2 では, `open_goals` の各要素の実際の型を検査した. `CyclicStructureStatement`, 正方向の `Relation`, 逆方向の `Relation` は同一数式として表示される場合があるが, 内部では異なる検証待ち条件である. `R15R17R3_RUNTIME_AUDIT=PASS` と限定 pytest 14 PASS を確認した.

## 修正対象

本体は `phase168_r3_5_model_renderer.py` のみ. 新規 `project_typed_open_goal_displays()` を `render_model_backed_narrative_markdown()` の直前に追加し, 後者の未解決 Goal 出力部分だけを変更する. `import` の変更, クラスの変更は行わない. `FULL_CHANGED_UNITS.md` は DryRun に実コードから全文生成する.

## GitHub 照合

GitHub develop は `a4e01bcafcd2afd295c61843bbaa597a6262f75a`. `aa25a993` からの差分は R3R2 監査ファイルに限り, Renderer の Git Blob `53a542ee5903def81a87ecb11a35be31d7143341` は不変. ローカル HEAD は両コミットを許容し, remote HEAD と Renderer Blob は固定検証する.

## 安全性と表示契約

- 証明探索結果, `model.open_goals`, `result.open_goals`, 結論, 証明木, Reference を一切変更しない.
- 同値判定は Python の型付き群構造 `(TodaPrimaryGroup, FiniteCyclicGroup|FreeCyclicGroup|DirectSumGroup)` による. 表示 LaTeX や文字列を比較して同一視しない.
- `RelationType.EQUALITY` 以外の `Relation` は集約しない.
- `CyclicStructureStatement` の `order` が正確な具体整数 (2以上) または `None` の場合だけ対象とする.
- 見た目を1件にまとめても, `未解決 Goal N 件` の表示を残す. いずれも未証明である.
- 群・次元・生成元・定理名に依存する専用分岐を新設しない.
- 検証済み抽象群の結論を記名生成元の完成証明に昇格させない.

## 既存テストと Phase 境界

本工程の対象 pytest は新規型付きGoal表示, R15R17-R1/R2 の共通 Narrative, 既存完成群の限定回帰. 古い抽象群の別 Section を要求するテストの更新は **R3R4** に限定する. レガシー補助 API の仕様変更や探索規則の一般化も実施しない. 全体 pytest は Phase 173 終了時に実施する.
