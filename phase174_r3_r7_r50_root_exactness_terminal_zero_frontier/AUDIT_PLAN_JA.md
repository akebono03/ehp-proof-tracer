# Phase 174 R3-R7-R50：根の完全性と終端零群の監査

## 目的

R49 の同一 Canonical Proof Search で上側の Δ 全射性まで検証された23件の ProofStep に、Toda Proposition 4.2 に基づく根の2つの EHP 完全性と、Toda (5.1) に基づく π_12^13=0 の証明を追加接続する。新規数学規則、専用 Narrative、結論の直接 GIVEN、保存済み ProofStep の注入は行わない。

## 変更対象

新規 `phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/` のみ。`audit.py` の `inspect_integrated_root_frontier()` と `main()`、`source_guard.py` の `verify_checkout()`、3つのテストファイルの各関数、`run.ps1`、ドキュメントを追加。既存コードとテストは変更しない。

## 監査条件

1. R49 の零像・Hopf単射・下側核・Prop 2.7・上側 Δ 全射性の検証済み ProofStep を保持する。
2. 根の Δ–E と E–H 完全性を、一般 Prop. 4.2 GIVEN の祖先を持つ INFERENCE として2件追加する。
3. 終端 π_12^13=0 を一般 Toda (5.1) の祖先を持つ INFERENCE として導出する。
4. 根 π_12^7=0 の4親が全て正しい型・順序の INFERENCE であることと、数学的に必要な出典6件（Toda (5.9)、Prop. 4.2、Prop. 2.7、Prop. 5.8、(5.10)、(5.1)）が証明木に現れることを検査する。
5. 実際の探索から返った `ProofSearchStatus.COMPLETE` と根の `ProofStep` に一致する場合に限り、scoped proof complete と判定する。Web公開・全体pytest・Phase完了は宣言しない。
6. R49 監査だけの GitHub マージを認めるが、本番数学の差分や追跡ファイルのローカル変更は拒否する。

## pytest と境界

R50 自身の static/guard/frontier、および R49、EHP零根、Toda(5.1)、Prop. 4.2 の限定回帰だけを実行する。Toda (5.1) の過去テスト群には、現在2件ある既存一般出典を1件と仮定する古いテストが含まれるため、その古い件数テストは対象外にし、数学的特殊化を検証する4テストを選択する。実環境結果に未解決があれば完了扱いにせず、次の R50R1 で原因を監査する。R51 以降で HTTP/Web 共通 Renderer の到達性を検査し、Phase 174 最後にのみ全体 pytest を行う。
