# R23 変更一覧とコード参照

新規ファイル `phase165_r52_r23_existing_rule_adapter.py`：`_eta`、`_iota5`、`_objects`、`expand_existing_pi43_rules` をファイル全体として追加。実装コードは同梱ファイル全文を参照。

新規ファイル `install.py`：`install` を追加。新規ファイル `test_phase165_r52_r23_existing_rule_adapter.py`：4件のテストを全文収録。

既存 `phase165_r52_r9_shared_math.py`：`shared_expansion_provider` 内に `expand_existing_pi43_rules` を provider として追加。import に次の一行を追加：

```python
from phase165_r52_r23_existing_rule_adapter import expand_existing_pi43_rules
```

その他のコードに変更なし。既存の import ブロック全文および変更後の `shared_expansion_provider` 全文は、実行する `install.py` のローカル版が唯一の正本（過去の累積パッチを維持するため）。

## 完了条件

* 既存規則による逆向き展開を生成する。
* Whitehead square の出典を捏造しない。
* π4³の証明完成を主張しない。
* 対象テストのみ実行する。

## R24との境界

Delta-image の型付き出典接続と他の群への一般化は R23 に含めない。
