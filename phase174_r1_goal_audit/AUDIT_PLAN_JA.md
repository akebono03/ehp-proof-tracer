# Phase 174 R1 — 未解決 Goal 読み取り専用監査

## 目的
- `develop` の最新 HEAD・保護対象ソースの一致を検査する。
- $\pi_8^5$、$\pi_{12}^4$、$\pi_{13}^4$ の公開探索結果を比較する。
- 未解決 Goal、実際に導出された ProofStep、Reference、診断を原形で保存する。
- 抽象群構造の独立した証明書と記名証明の完了状態を分けて扱う。

## 対象
- 既存コードへの変更なし。
- 新規監査用ファイル `phase174_r1_goal_audit/audit.py` および `run.ps1`。
- 新規テスト `phase174_r1_goal_audit/tests/test_audit.py`。
- 既存関連テストは読み取り・限定 pytest の対象とし、改変しない。

## 完了条件
- remote/local HEAD と Source Guard が PASS。
- 各群の公開探索について全 Open Goal と証明ステップが JSON に記録される。
- 関連限定 pytest が PASS。
- Git index と作業ツリーの状態が実行前後で同一。
- 文献未確認の命題を GIVEN に昇格させていない。

## 次段階との境界
R1 では新規の数学命題や Inference Rule を実装しない。
R2 で必要な文献関係と型付き前提を精査する。
R3 の実装は R2 で根拠が確認された場合に限る。
