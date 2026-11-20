# Phase 176 R3R12 — 証拠の詳細抽出

## 対象

R3R10 および R3R11 の監査報告書を読み、実際の `observed` 以下のネストした証拠を出力する。共有 Provider の条件を現行コードで静的に確認する。型付きの実行時 Goal と出典付き零関係の完全照合を行わない限り、候補0件の原因は未確定とする。

## 変更するファイル・関数

既存コード・既存テストの変更なし。新規ディレクトリ `phase176_r3r12_bridge_evidence_detail/` に `audit.py` を追加し、関数 `read_json`、`flatten`、`selected`、`evaluate_static_guards`、`audit`、`main` を定義する。`tests/test_audit.py` に4テストを追加する。`run.ps1`、README、監査計画およびコード一覧も新規追加する。

## 境界

GIVEN追加0、一般数学規則追加0、共有 Provider 登録変更0、結論の直接注入0。公開 proof の完成判定を変更しない。

## テスト・完了条件

`python -m pytest -q -p no:cacheprovider phase176_r3r12_bridge_evidence_detail/tests/test_audit.py phase175_r4r14r5_public_zero_transport/tests/test_provider.py` を限定実行する。DryRun と本実行 PASS、報告書の生成、証拠の実際の値の出力を完了条件とする。全体 pytest は Phase 終了時だけ。

## 次段階

R3R12 の抽出した実際の typed Step / Goal が十分であれば、R3R13 で共有 Provider のガード条件の動的照合を検討する。原因未確定のまま実装しない。
