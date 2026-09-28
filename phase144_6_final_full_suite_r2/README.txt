Phase 144-6 Final Full Suite R2
================================

目的
----
Phase 144-6 の最終 full suite を、repository root に蓄積された
phase143_* / phase144_* 配布・監査ディレクトリ内の duplicate tests を
誤って収集せず、正規 tests/ suite のみに対して実行する。

今回判明したこと
----------------
前回 runner の `pytest -q` は repository root 全体を再帰探索したため、
過去の Phase ZIP を展開して残っているディレクトリ内の同名 test module と、
正規 tests/ 内の test module が衝突した。

ログでは `import file mismatch` が多数発生し、
テスト本体の実行前の collection 段階で 213 errors となった。

これは Phase 144-6 production implementation の regression failure ではない。

変更対象
--------
Production files: none
Persistent test files: none
Documentation files: none

実行時だけ行うこと
------------------
1. tests/__init__.py が存在しない場合だけ、一時的に空ファイルを作成する。
2. PYTHONPATH を repository root に設定する。
3. `pytest -q tests` を実行する。
4. runner が作成した tests/__init__.py は finally で必ず削除する。
5. 既存 tests/__init__.py があった場合は変更・削除しない。

tests/__init__.py の一時作成理由
--------------------------------
正規 tests には `from tests.test_... import ...` 形式の相互 import がある。
ローカル Python 環境で別の `tests` package に解決されることを防ぎ、
repository の tests/ を明示的な package として解決させる。

実行
----
repository root で:

Expand-Archive `
  -Path "$HOME\Downloads\phase144_6_final_full_suite_r2.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_final_full_suite_r2\run_phase144_6_final_full_suite_r2.ps1"

完了条件
--------
`pytest -q tests` が全件 PASS すること。

PASS 後
-------
Phase 144-6 の implementation/test boundary を完了と判定し、
completion documentation 更新へ進む。
