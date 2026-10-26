# R3S1 コードの置換単位

## 対象

`phase168_r3_37c_reference_projection.py` の
`project_reference_bodies()` を、以下のファイル全文で示す関数へ置き換えます。

- `full_functions/project_reference_bodies_FULL.py`：変更後の関数全文
- `tests/test_r3s1_composite_scope.py`：新規テスト4関数と必要 import の全文
- 実行後の `output/phase168_r3_37c_reference_projection.py`：対象ファイル全文

既存クラス、その他の関数、トップレベル import の変更はありません。
旧 R3S と同じ操作を重複適用せず、正常な親複合命題も今まで通り展開します。
