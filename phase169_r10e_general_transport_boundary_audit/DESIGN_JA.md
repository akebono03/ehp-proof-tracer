# Phase 169 R10E0 — 輸送規則の適用境界監査

## 目的

R10D2 の成果（`π_11^8` の完成など）を維持したまま、零群、単一有限巡回群、直和群、および安定範囲の開始点を同じ型付き基準で切り分ける。

## 読み取り対象

`phase165_r55_nk_only_goal.py` の DB Goal、`phase169_r3m_prior_result_catalog/prior_results.py` の掲載順ゲート、`phase169_r7_general_stable_transport/rule.py` の finite-cyclic 輸送条件、`phase165_r52_r9_shared_math.py` の共通 Provider。

## 数学的な境界

Toda (4.5) は `n >= k+2` の範囲で安定な懸垂同型を与える。最初の安定次元 `n=k+2` には、これより低い安定範囲の輸送元はない。また現在の R7 は根の構造として `FiniteCyclicGroup` を必要とするため、零群・直和の一般輸送を提供しない。

## 信頼境界

* DB 群構造は目標または先行候補。文献出典・掲載順序を通った命題のみが引用可能。
* 各 `GeneratorImage` は独立に証明される必要がある。
* 本監査から `GIVEN`、`INFERENCE`、`ProofStep` は追加しない。
* 探索の失敗を `complete` と読み替えない。

## 完了条件

限定 pytest が PASS し、5つの群それぞれについて Goal の型、安定範囲、先行候補の引用可否、Provider の拡張候補が JSON と Markdown に出力され、本番3ファイルが byte-for-byte 不変であること。

## 次の Phase 169 作業との境界

R10E0 は監査のみ。結果に応じて「零群の輸送」「直和群の輸送」「単一巡回群の引用条件」を別々の共通機能として計画できるが、本監査では実装しない。全体 pytest は Phase 169 終了時まで実行しない。
