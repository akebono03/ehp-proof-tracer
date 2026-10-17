# Phase 165 R2 — 共通規則パイプライン監査

## 変更対象

本番ファイル・クラス・関数の変更はありません。
新規 `audit.py`: `main()` を追加。
新規 `test_audit.py`: `test_generic_pipeline_report_is_consistent()`, `test_only_real_source_leaves_are_counted()` を追加。

命題台帳と規則台帳の変更はありません。

## 対象 pytest

`python -m pytest -q .\phase165_rule_pipeline_r2\test_audit.py`

## 完了条件

群別 Adapter が存在しないことを確認し、規則発見数・結論照合成功数・前提生成成功数・共通 root 候補数を JSON に出力すること。

## 次の Phase との境界

今回の作業は診断のみで、一般規則や逆向き適用の変更は次の R に限定します。全体 pytest は Phase 165 の終了時だけに実行します。
