# R4-R62 変更一覧

既存ファイルは変更しない。新規追加位置はプロジェクト直下の `phase163_r4_r62_remaining_definitions/`。

- `phase163_r4_r62_remaining_definitions.py`：`load_json`、`audit_remaining`、`write_reports`、`main` を新規追加。
- `tests/test_phase163_r4_r62_remaining_definitions.py`：限定テスト9関数と fixture `inputs` を新規追加。
- `run.ps1`：既存 Phase 出力ディレクトリを明示指定する実行スクリプト。
- `README.md`：実行説明（英語）。

Python の import と新規関数、および pytest 関数の全文は同梱の Python ファイルに記載。省略なし。

完了条件：候補16件の集合一致、R55〜R61 の3件の除外、出典の整合、未知の掲載順・意味・ID の未認定、限定 pytest 成功。
次の R4-R63 は出典範囲と定義対象を原文から個別に検証する段階。数学的同値性・原本照合・本番台帳登録は範囲外。
全体 pytest は Phase 163 の終了時まで実施しない。
