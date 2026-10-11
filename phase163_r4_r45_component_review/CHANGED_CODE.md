# Phase 163 R4-R45 変更一覧

## 対象ファイル・クラス・関数

- 新規 `phase163_r4_r45_component_review.py`：`check_inputs`、`make_review`、`write_output`、`main`。
- 新規 `tests/test_phase163_r4_r45_component_review.py`：テスト5件。
- 新規 `run.ps1`：対象テストと監査だけを実行。
- 新規 `README.md`、`CHANGED_CODE.md`。
- 既存ファイル・既存クラス・既存関数・既存テストは変更しない。

各新規コードは import から末尾まで ZIP 内に全文収録し、`...` による省略を行わない。

## 完了条件

- 第1〜5章の TeX SHA-256 が R4-R42/R4-R43/R4-R44 間で一致する。
- 優先5 Reference の原文と全 Assertion を校閲資料へ収録する。
- その他の Assertion も件数・ID を維持する。
- 意味的一致と命題内順序を推測で確定しない。

## 次工程との境界

R4-R46 以降で原文に照らして明示的に各主張の span と順序を確定する。命題台帳への書き込み・新規 ID 発行・証明探索接続は本 Phase では行わない。全体 pytest は Phase 163 終了時のみ実行する。
