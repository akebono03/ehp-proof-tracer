Phase 145 Final Regression Repair R8

目的
----
Phase 145 archive cleanup 後の canonical test collection regression を、
既存 test 本体を書き換えずに修復する。

確認済み事実
------------
R7:
- canonical test files: 774
- tests.test_* package imports: 43
- bare test_* imports: 547
- unique bare test_* modules: 184
- bare modules without canonical target: 0

GitHub develop:
- pytest.ini: none
- pyproject.toml: none
- setup.cfg: none
- tox.ini: none
- root conftest.py: none
- tests/conftest.py: none

変更対象
--------
1. tests/__init__.py
   R6 で追加済みの空 package marker を維持する。

2. tests/conftest.py
   新規追加。
   tests/ directory を sys.path に追加し、既存の bare `test_*` imports を維持する。

変更しないもの
--------------
- production code
- 既存 test file 本体
- archive
- 547箇所の bare import
- 43箇所の tests.test_* import

tests/conftest.py 全文
----------------------
from __future__ import annotations

import sys
from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent

if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

検証
----
1. conftest syntax
2. package import / bare import が混在する代表3 test の collection
3. tests/ 全体の collection only
4. Phase145 focused regression

repository-wide pytest の test body 実行は R8 では行わない。
R8 PASS 後に Phase145 最終 gate として一度だけ実行する:

    python -m pytest tests -q
