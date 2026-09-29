Phase 145 Final Regression Diagnosis R7

目的
----
R6 で tests/__init__.py を追加した後に判明した canonical test 間 import の
混在状態を全件監査する。

背景
----
canonical tests には次の2形式が混在している可能性がある。

1. package import
   from tests.test_xxx import ...

2. bare top-level import
   from test_xxx import ...

tests/__init__.py により前者は安定して解決できる一方、後者は repository root
だけが PYTHONPATH にある通常の Python import では解決されない。

R7 で確認するもの
-----------------
- tests.test_* package import の総数
- bare test_* import の総数
- bare import の unique module 数
- 各 bare import の参照元
- 各 bare import の canonical tests/<module>.py が存在するか
- relative import の件数
- tests/__init__.py の現在状態

変更
----
なし。

この診断では production code、既存 tests、archive、tests/__init__.py を変更しない。
repository-wide pytest も実行しない。
