Phase 154 punctuation closure audit Repair1

原因
----
初回 audit は package subdirectory から直接 Python script を実行したため、
repository root が Python の import search path に入っていなかった。

そのため:
`ModuleNotFoundError: No module named 'toda_calculation_facade'`

これは punctuation finding ではなく audit runner の import path 不具合。

変更対象
--------
phase154_punctuation_closure_audit_repair1_import_path/
  audit_phase154_punctuation_closure.py

変更内容
--------
project import より前に:

- `import sys`
- `REPO_ROOT = Path(__file__).resolve().parent.parent`
- `sys.path.insert(0, str(REPO_ROOT))`

を追加する。

production 変更
---------------
なし。

既存 test 変更
--------------
なし。

監査条件
--------
- n = 2..15
- k = 0..7
- 112 groups
- depth = 2
- public Narrative renderer
- prose comma = `, `
- prose period = `.`
- TeX / math は除外

完了条件
--------
- focused R6 tests PASS
- scanned groups = 112
- rendered groups = 112
- exceptions = 0
- japanese comma violations = 0
- japanese period violations = 0

全体 test
---------
実行しない。
Phase 154 最後にのみ実行する。
