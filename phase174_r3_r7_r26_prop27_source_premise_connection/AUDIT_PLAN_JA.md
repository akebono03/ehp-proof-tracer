# Phase 174 R3-R7-R26R1：pytest import mode 修正

## 監査対象

R26 の `run.ps1` と `tests/test_audit.py`、R24 の `tests/test_audit.py` を確認。
同名テストが pytest の通常 import mode で衝突することを実行ログで確認。

## 変更対象

- `run.ps1`：限定 pytest に `--import-mode=importlib` を追加し、新規回帰テストを対象に含める。スクリプト全体を置換。
- `tests/test_run_import_mode.py`：新規追加。R26 の `tests/test_audit.py` と同じディレクトリに置く。
- `README.md`、`CODE_FULL_JA.md`、`AUDIT_PLAN_JA.md`：修正内容を完全記載。

## 非変更対象

`audit.py`、`bridge.py`、既存のテスト関数、数学規則、GIVEN、公開探索、証明表示経路は変更しない。

## 実行と完了条件

DryRun の Source Guard が PASS、通常実行の限定 pytest が PASS。
全体 pytest は実施しない。R26 の監査 Gate は元のまま維持。
次の R27 では出典認証された前提を公開経路へ接続する工程を扱う。
