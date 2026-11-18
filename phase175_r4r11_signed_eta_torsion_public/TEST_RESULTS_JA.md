# Phase 175 R4R11R1 — テスト fixture 修正と検証記録

## 原因と変更範囲

2026年11月18日に報告された R4R11 DryRun では、限定 pytest が **124 passed、4 failed** で終了した。本実行の監査部分はまだ実行されていない。

4件とも `tests/test_provider.py` の `cited_bridge()` が `ProofStepLink(aid, ProofStep(...))` を使い、第2位置引数 `repository_key` に `ProofStep` を渡したため `TypeError: repository_key must be a str` が発生した。

R4R11R1 では `ProofStepLink(aid, step=ProofStep(...))` とする一箇所の修正だけを行う。関連する本番コード、`rule.py`、`provider.py`、`audit.py`、`run.ps1`、既存 API、出典登録、GIVEN、数学規則を変更しない。

## 作成環境での再検証

- 修正した `test_provider.py`：**4 passed**。
- R4R11 の新規4テストファイルと R4R10 の関連4テストファイル：**94 passed**（互換スタブ環境）。
- Python 構文検査：PASS。
- 元 ZIP との比較：上記テスト1ファイルと修正記録用3文書（`CODE_FULL_JA.md`, `README.md`, `TEST_RESULTS_JA.md`）のみ変更。
- ZIP の CRC/整合性検査：PASS。

これらはユーザー実リポジトリの実行結果ではない。

## ユーザー実環境での残確認

- 修正後 DryRun：未実施。
- 修正後 本実行：未実施。
- 共有 Registry / Provider の監査：未確認。
- 全体 pytest：Phase 175 終了まで実施しない。

## 期待 Gate

- DryRun：`PASS_R4R11_SIGNED_ETA_TORSION_DRYRUN`
- 本実行：`PASS_R4R11_SIGNED_ETA_TORSION_SHARED_CONNECTED_PI95_PENDING`

この Gate は符号正規化の証明候補を共有探索で利用できることを確認するものであり、$\pi_9^5$ の完成証明を意味しない。


## R4R11R2：改行コード照合修正の回帰確認

実環境ログで R4R11R1 の限定 pytest は **128 passed**、監査は `R4R11_SOURCE_DRIFT: expression.py` により FAIL と判定された。R4R11R2 では CRLF 原本 Git blob と LF checkout の相互照合、LF 原本と CRLF checkout の相互照合、および式・本文を改変したデータの拒否を検証する専用テストを追加した。

新規 GIVEN 0件、新規数学規則0件（R4R11 全体では規則1件）、本番コード変更なし。次 Phase の機能は先取りしない。R4R11R2 のユーザー実環境 DryRun／本実行は未確認。全体 pytest は Phase 175 終了時のみ実施。


## R4R11R2 作成環境での限定 pytest 実測

- `tests/test_rule.py`, `tests/test_provider.py`, `tests/test_installer.py`, `tests/test_audit.py`：**52 passed**。
- 上記4ファイルと R4R10 の関連4ファイルを合わせた限定テスト：**95 passed**。
- いずれも作成環境の互換スタブを用いたテストであり、実リポジトリ全体の pytest ではない。
- 本番 Git HEAD・先行 R4R10 レポート・Source Guard・公開 Provider の実リポジトリでの検証はユーザー側で要確認。
