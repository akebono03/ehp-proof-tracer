# Phase 174 R3-R7-R48R2 監査計画

## 原因
R48 は出典付き候補を検出するが、`typed_reference` の先行直接 `GIVEN` が自由巡回群の `Relation` を採用し、R35 の三前提のうち始域だけが必須の `INFERENCE` にならない。核の `INFERENCE=0` は数学的証明の完成を意味しない。

## 変更ファイル
- `phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/audit.py`：`inspect_integrated_lower_kernel_frontier()` 全体。関数内の import を追加し、既存 R35 `GoalExpansion.rule` のまま、始域の子 Goal を `SourceBoundGoal` に束縛する。既存 source-first 審査済み GIVEN に結び付いた候補だけ使う。
- `phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_static.py`：`test_r35_kernel_domain_is_explicitly_bound_to_a_cited_inference()` を末尾に追加。
- `phase174_r3_r7_r48r2_source_bound_kernel_dfs_fix/`：修正手順、完全な置換ファイル、限定テストを新規追加。

## 契約
R35 の数学的推論規則、共有 Provider、一般探索エンジン、共通 Renderer を一切変更しない。登録する新規 GIVEN=0、直接証明の注入=0。標準探索は First Successful Proof Search を維持。最終群 `π_12^7=0` は未完成。

## 判定
R48 Source Guard、14から増加した検証済み ProofStep、`KernelMultipleStatement` の `INFERENCE`、始域の `INFERENCE`、Toda Prop.5.8 と (5.10) の親、次の Prop.2.7 Goal 到達、限定 pytest PASS。全体 pytest は Phase 174 完了時のみ。
