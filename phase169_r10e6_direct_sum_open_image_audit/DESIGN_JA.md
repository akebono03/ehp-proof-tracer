# Phase 169 R10E6 — 直和群の未解決生成元像監査設計

## 監査対象

- $\pi_{23}^{15}$（8-stem）。安定基点は $\pi_{18}^{10}$、懸垂回数は5。
- $\pi_{24}^{15}$（9-stem）。安定基点は $\pi_{20}^{11}$、懸垂回数は4。

## 新規ファイル・関数

本番コード・既存テストに変更なし。監査モジュール `audit.py` を追加する。新規関数は `_element_name`, `_component_generators`, `_observed_inferred`, `_cited_families`, `_candidate_profile`, `_expected_component_audit`, `_unresolved`, `audit_case`, `render_markdown`, `main`。追加テストは `tests/test_r10e6_audit.py` に含む。

## 証拠の境界

`exact_prior_database_result` が返す群構造は、`admitted_db_step` で先行前提かを確認する。証明目標は `registered_group_goal_candidates` から取得し、`search_group_from_registered_goal` で実際の探索結果を得る。

`generator_images_for_group_transport` により、各直和成分に必要な一回ずつの `GeneratorImage` を生成する。ただしこれは目標の列挙であり、事実の追加ではない。各像が探索結果の `INFERENCE` に含まれるか、Open Goal にあるかを別々に記録する。

系列定義は引用審査を通った `CitedStableFamilyDefinition` のみを区別する。`HyoujiGen.csv` における型と命名の対応があっても、文献に根拠のない等式は採用しない。`expand_cited_stable_family` と `expand_composite_generator_image` はあくまで候補を返す。

`Relation` の未解決は `GeneratorImage` と分離して記録する。監査出力は証明完了を宣言せず、Narrative や Renderer を変更しない。

## 完了条件

1. 両対象について、安定基点、直和成分、各回の懸垂像の状況を取得。
2. 一件ずつ未解決 `GeneratorImage`、未解決 `Relation` の型を保存。
3. 追加 pytest は監査専用の限定テストのみ。
4. 既存追跡ファイルの差分を監査前後で保持。
5. 全体 pytest は実施しない。

## 次段階との境界

R10E6 は原因調査だけを行い、原典根拠が検証されるまでは $\bar\nu$、$\varepsilon$、$\mu$ の新規系列定義や既存推論規則の変更を行わない。
