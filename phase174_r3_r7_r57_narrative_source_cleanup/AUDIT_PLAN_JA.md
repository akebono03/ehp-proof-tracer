# Phase 174 R57 実装・監査計画

## 現行コードと関連テストの確認

GitHub `akebono03/ehp-proof-tracer` の `develop` HEAD `0a5be29a4458cdffaa8a7ad4ad31c2e91f6941f9` を確認。R56 実行ログは Phase 174 R56R1 `PASS_R56R1_REPORT_PATH_AND_R56_PUBLIC_AUDIT`、`π_11^6` の root 4前提・23 steps、`π_12^7` の全射性 root 2前提・11 steps。現在の局所検証対象は R56 rules and public tests、R37 isolated math test、共通 typed statement projection、ProofNarrative Renderer、typed Reference projection。

## 変更対象・変更する完全関数

- `phase174_r3_r7_r56_cyclic_generator_bridge/rule.py`: `delta_surjectivity_generator_inputs`, `delta_surjectivity_from_generator_rule`。生成元が canonical typed `Δ(ι)` であることを前提の構造照合で確認し、`π_12^7` のために Proposition 2.7 をもう一度要求しない。`cyclic_generator_rule` はそのまま維持。
- `phase174_r3_r7_r56_cyclic_generator_bridge/tests/test_rule.py`: 変更した3 test 関数。1前提の場合、DB先行前提を認める場合、誤った生成元の拒否を確認。
- `phase168_r3_27_typed_statement_projection.py`: `typed_sentence`。型付き ImageZeroStatement を零写像として表示し、核の巡回部分群を `\mathbb Z\{2\iota\}` の形で表示。
- `phase168_r3_5_model_renderer.py`: `render_model_backed_narrative_markdown`。GIVEN の出典が1つに確定する場合のみ汎用的に `[R#]より` を表示。対象群が証明済みの2-torsionである場合のみ、signed image の `±` を標準的に除去する。ProofStep自体は変更しない。
- `phase168_r3_37c_reference_projection.py`: `project_reference_bodies`。(5.10) の出典位置と採用原文を再検証し、原文にある等号を符号なしで表示。文献出典の正確性に限った訂正で、専用 Narrative ではない。

既存 import 節への変更なし。新規関数／クラスなし。追加位置を要するものはない。Installer・audit・test ファイルは新規ディレクトリ `phase174_r3_r7_r57_narrative_source_cleanup` に配置する。

## 完了条件

1. GitHub/local Source Guard PASS。Local HEAD と対象原本が監査対象に一致。
2. R56 数学規則の 1-premise surjectivity / 4-premise cyclic の focused pytest が PASS。
3. `π_11^6=Z{Δ(ι_13)}` は引き続き complete。H の単射性・下側 Delta の核・Prop 2.7 が証明木に保持される。
4. `π_12^7=0` は complete。先行 DB 結果 `π_11^6` を1回採用、独立証明は再実行しない。Proposition 2.7 は当該証明木と Reference から消える。
5. `π_11^6` では `E` が零写像と明記され、核は `\mathbb Z\{2\iota_{11}\}` 表記、R7 の明確な出典表示、(5.10) は印刷原文を忠実に表示する。
6. 新 GIVEN 0、新数学規則 0、全体 pytest 未実行。

R57は証明内容の新規拡張ではなく、既にあるR56数学的結論の論理依存修正と共通表示統一。将来 Phase の群や追加公式・追加ルールは実装しない。
