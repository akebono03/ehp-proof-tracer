Phase 144-6 Final Full Suite R4
================================

目的
----
Phase 144-6 の Phase-end full suite を、正規 tests/ のみに限定しつつ、
repository 内に混在している二種類の test-to-test import を同時に解決する。

GitHub develop で確認した現状
----------------------------
現行 repository には次の二形式が実在する。

1. package style

   from tests.test_phase143_19_method_evidence import (
     _method_evidence_data,
   )

2. top-level style

   from test_phase105_14_qualified_execution_family_grouping import (
     _build_phase105_14_fixture,
   )

また、tests/test_phase143_19_method_evidence.py 自体も現行 develop に存在する。

R2/R3 が失敗した理由
--------------------
R2:
- tests/__init__.py を一時作成
- PYTHONPATH は repository root のみ
- package style は成立するが top-level style が成立しない

R3相当:
- repository root と tests/ を検索対象にしても tests/ が package でない
- 環境内の別 tests package に解決される可能性があり package style が成立しない

R4
--
次の二条件を同時に満たす。

- 一時 tests/__init__.py
  -> `tests.test_phase...` を repository の tests package として解決する。

- PYTHONPATH=<repository root>;<repository root>\tests
  -> repository root から package style を解決する。
  -> tests/ から top-level `test_phase...` style を解決する。

さらに pytest 前に両形式の import preflight を実行する。

変更対象
--------
Production files: none
Persistent test files: none
Documentation files: none

一時的な実行環境変更
--------------------
- tests/__init__.py が存在しない場合のみ一時作成
- PYTHONPATH を実行中だけ変更
- 終了時に runner が作った tests/__init__.py を削除
- 元の PYTHONPATH を復元
- 既存 tests/__init__.py がある場合は保存

実行対象
--------
pytest -q tests

repository root の phase143_* / phase144_* 展開フォルダは収集しない。

完了条件
--------
1. Dual import preflight が PASS
2. pytest -q tests が全件 PASS

両方 PASS した場合、Phase 144-6 implementation/test boundary は完了。
次は completion documentation 更新へ進む。
