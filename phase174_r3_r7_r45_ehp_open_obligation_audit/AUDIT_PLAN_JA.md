# Phase 174 R3-R7-R45 監査計画

## 対象

R44 の `Eπ_{10}^{5}=0` と最終目標 `π_{12}^{7}=0` を混同しない。
特に、R44 の限定探索が意図的に選択しなかった EHP 完全性の既存 Provider を監査する。

## 変更対象

- 既存の本番ファイル・クラス・関数: **変更なし**。
- リポジトリ直下に `phase174_r3_r7_r45_ehp_open_obligation_audit/` を追加。
- 新規関数: `source_guard.git`, `git_blob_sha`, `matches_git_blob`, `verify_checkout`、`audit.inspect_open_ehp_obligations`, `audit.main`。
- 監査用テスト: `tests/test_frontier.py`, `tests/test_source_guard.py`, `tests/test_static.py`。

## 数学的な確認範囲

- 出典付き Proposition 4.2 の一般前提が Source-first フィルタを通過したか。
- 次の4つの別個の完全性窓について、既存の一般特殊化候補と実際の `INFERENCE` の成立を区別して記録する。
  - `(n,i,kind)=(6,12,delta_e)`。
  - `(6,12,e_h)`。
  - `(5,11,e_h)`。
  - `(5,11,h_delta)`。
- `im(H)=ker(Δ)` の既存導出と、Hopf 単射性および上側 Δ 全射性の未完成状態を区別する。
- R44 の零像連鎖は再実行しない。この制限により本監査では Hopf 単射性の完成を主張しない。

## 完了条件

現行 HEAD の照合、ソース SHA 検証、4窓の型検査、Provider 候補確認、限定 Canonical Search の ProofStep/未解決 Goal 記録、および限定 pytest が実行されること。全体 pytest と Web HTTP 検証は対象外。

## R46 との境界

R45 で証明済みになった窓を重複実装しない。R46 では R44 の零像連鎖と R45 の一般完全性連鎖を、同じ標準探索の中で無改変の Provider を介して接続できるかを検討する。なお Prop. 4.2 が未成立なら、先に出典の公開適格性を監査する。
