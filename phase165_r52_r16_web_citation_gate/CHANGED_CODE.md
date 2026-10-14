# 変更コード

- `phase165_r52_r9_shared_math.py` の import は変更なし。
- `build_shared_typed_bridge()` の `records.extend(source.records)` を以下の行に変更する。

```python
        records.extend(replace(record, assertion_id=prefix + record.assertion_id) for record in source.records)
```

- `search_shared_group_goal()` は `search_shared_group_goal.txt` の全文で置換。
- 新規ファイル `phase165_r52_r16_web_citation_gate.py` に import と `screen_shared_proof_context()` 全文を収録。
- 新規ファイル `test_phase165_r52_r16_web_citation_gate.py` に import と全テスト関数を収録。
- `install.py` は元ファイル検査・バックアップ・書換え。変更の範囲外のコードは保持。
