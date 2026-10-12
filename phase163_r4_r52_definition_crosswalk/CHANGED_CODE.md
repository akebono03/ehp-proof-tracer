# Phase 163 R4-R52 変更一覧

既存ファイル・クラス・関数・import は変更しない。新規追加のみ。

- `phase163_r4_r52_definition_crosswalk.py`：新規。`SOURCE_NAMES`、監査用 `LABELS` の後に `catalog_digest()`、`audit()`、`write_results()`、`main()` を追加。すべて全文を本ファイルに収録。
- `tests/test_phase163_r4_r52_definition_crosswalk.py`：新規。必要な import と9つのテスト関数の全文を収録。
- `run.ps1`：新規。R4-R51 / R4-R47 / R4-R42 の実在パスを参照し、限定 pytest と監査を順に実行。
- `README.md`：新規。英語で全内容を記載。
- `CHANGED_CODE.md`：新規。日本語で全内容を記載。

完了条件：19候補すべてを R4-R48 ID で追跡し、ソースと R4-R47 スナップショットの改ざんを検出する。既存 Definition への直接一致がないことを確認する一方、数学的な同値性および新規登録の要否は未確定とする。限定 pytest 9件が通過する。本番 Registry や Statement ID は変更しない。

次の R4-R53 との境界：既存 Assertion と候補の数学的な重複・包含については R4-R52 で決めず、後続の原文・形式的主張の照合へ委ねる。全体 pytest は Phase 163 の最後のみ。
