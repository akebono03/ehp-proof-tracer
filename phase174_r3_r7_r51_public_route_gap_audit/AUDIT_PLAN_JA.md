# Phase 174 R3-R7-R51 監査計画

## 対象と境界

R50 は検証済み ProofStep 28 件で $\pi_{12}^{7}=0$ を限定探索で証明した。しかし公開の Group query は一般 `shared_expansion_provider` を使用しており、R50 の厳選した候補と `SourceBoundGoal` が自動接続されない。R51 は既存コードを変更せず、公開呼び出し経路を直接調べる。

## 変更対象

新規 `phase174_r3_r7_r51_public_route_gap_audit/` 配下のみ。
- `audit.py`: `inspect_public_route_gap`, `main`。
- `source_guard.py`: `git`, `git_blob`, `matches_blob`, `verify_checkout`。
- `run.ps1`: DryRun、本監査、限定 pytest。
- `tests/test_static.py`, `tests/test_guard.py`, `tests/test_public.py`: 関連テスト。

## 検査する事実

1. GitHub `develop` の固定 HEAD と対象12ファイルを Git blob SHA で照合する。
2. 公開 Group query と Web の model 経路を実際に呼び出す。
3. R50 の scoped proof が 28 ProofStep、complete、引用済みという境界を確認する。
4. 一般 R35 核の前提に直接 `GIVEN` を採用し得るか、`SourceBoundGoal` が存在するかを報告する。
5. 公開 complete を捏造せず、結果が partial の場合も Gate PASS（差異の確認）を報告する。

## 完了条件と次工程

Source Guard、監査、限定 pytest が PASS すること。Group query が依然未完成なら、次工程で R35 の既存一般数学規則を保ちつつ Source-first な一般探索経路のみを接続する。共通 Renderer と直接 GIVEN は変更しない。全体 pytest は Phase 174 の最後にだけ行う。
