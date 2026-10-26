# R3O 置換可能なコード

`new_files/phase169_r3o_stable_composite_rule.py` は **新規モジュール全文**。全 import、新規2関数の全文を含む。追加位置はリポジトリ直下。

既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` は、実行時に元ファイルを AST で抽出し、以下の provider 呼び出しを `expand_finite_cyclic_relation(goal)` の直後に加える。実行後の置換可能な **関数全文** は `output/shared_expansion_provider_FULL.py` に書き出される。トップレベル import は変更しない。

```python
        from phase169_r3o_stable_composite_rule import (
            expand_cited_toda45_composite_transport,
        )
        options.extend(expand_cited_toda45_composite_transport(
            goal, tuple(available),
        ))
```

新規テスト関数7件と全 import は `tests/test_r3o_toda45_composite_transport.py` の全文を参照。既存テストは変更しない。
