# Phase 169 R4A1 — import 経路修正

## 原因

R4A は限定 pytest 11件が PASS したが、`run.ps1` が `python (Join-Path $PSScriptRoot 'audit.py')` を呼び出したため、実行時の `sys.path` にリポジトリルートが入らず、`ModuleNotFoundError: No module named 'homotopy_groups'` となった。

## 変更対象

- `phase169_r4a1_prop44_audit_import_fix/run.ps1` — 新しい独立 ZIP の実行スクリプト。R4A の元のスクリプトと同じ処理を保ち、監査の起動だけを `python -m phase169_r4a1_prop44_audit_import_fix.audit` に変更する。
- `phase169_r4a1_prop44_audit_import_fix/__init__.py` — Python package の識別用に追加。
- `phase169_r4a1_prop44_audit_import_fix/tests/test_r4a1_runner.py` — 新規のランチャー回帰テスト1件。
- `phase169_r4a1_prop44_audit_import_fix/README.md` — この ZIP に対応した英語の使用説明。
- `phase169_r4a1_prop44_audit_import_fix/R4A1_CHANGELOG_JA.md` — この変更記録。

以下は **内容不変のコピー**：`audit.py`、`tests/test_r4a.py`、`AUDIT_JA.md`。

本番コード・既存のレポジトリの追跡ファイル、既存テスト、プロジェクト全体のドキュメントは変更しない。

## 検証

構文：`audit.py` と追加した回帰テストを Python でコンパイルする。Python module discovery はテスト用の独立したディレクトリで確認する。本来の既存依存モジュールを使う動作確認は Windows のリポジトリで実行する。

限定 pytest は R4A 4件 + R4A1 1件 + 既存 R3O 7件、合計12件。全体 pytest は実行しない。

## 完了条件

1. `R4A1_GIT_BRANCH=develop` が表示される。
2. 12件の限定 pytest が PASS する。
3. `R4A_PI64_STATUS`、`R4A_PROP44_SCREENED` などの R4A 監査結果が表示され、`output/audit.json` と `output/audit.md` が出力される。
4. `R4A1_TRACKED_STATUS_UNCHANGED=True`、`R4A1_AUDIT_ONLY=True` が表示される。

## 次 Phase との境界

R4A1 は実行経路だけ修正する。Proposition 4.4 の単射性規則、EHP の新規規則、生成元の証明・表示は追加しない。R4A の監査結果に基づいて後続の実装を判断する。
