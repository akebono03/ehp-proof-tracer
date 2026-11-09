# Phase 174 R3-R7-R48 監査計画

## 基準

- GitHub `develop` HEAD: `398ad86615ec8484e5a9fe04143e367c059d4c85`（R47 の監査のみが追加された merge）。
- R47 PASS: 同一 Canonical Proof Search 内に零像、Hopf 単射、下側の像＝核の14 ProofStep を確認。
- R35: 一般的な自由巡回群から位数2の有限巡回群への写像の核を導出するルール。
- R36: 出典付き `Proposition 5.8` と `(5.10)` を使う共有 Provider 接続。

## 変更対象

新規 `phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/` 以下のみ。
`audit.py:inspect_integrated_lower_kernel_frontier()` と `main()`、
`source_guard.py:verify_checkout()`、`run.ps1`、限定テストを追加する。
既存 Python コード・テスト・データ・Narrative は変更しない。

## 証明契約

`KernelMultipleStatement` の3前提は
1. 出典から推論された始域 `Relation`（自由巡回群）。
2. Toda Proposition 5.8 に基づく終域 `Relation`（位数2）。
3. Toda (5.10) に基づく生成元の像 `TodaDeltaImageUpToSignStatement`。

この3件を同一の正準探索が受理し、核を `INFERENCE` で導出するか検証する。
直接 `GIVEN`、既存 ProofStep の注入、専用 Narrative は禁止。

## 範囲外

`Prop27TypedHopfDeltaStatement` は接続せず、次の未解決 Goal として残す。
上側 Delta 全射と最終群の完成、Web HTTP、全体 pytest は対象外。
