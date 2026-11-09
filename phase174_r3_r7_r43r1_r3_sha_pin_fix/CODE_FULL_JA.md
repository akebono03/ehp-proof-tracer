# R43R1 変更コード全文

- 変更対象: `phase174_r3_r7_r43_public_ehp_map_property_wiring/source_guard.py` の `PINS` の1件だけ。
- このファイルの **変更後全文** は `replacement/source_guard.py` に収録（同じ ZIP 内）。
- **変更前全文** は `baseline/source_guard.py` に収録。
- 旧 `source_guard.py` の import 全文も含め、他のコードはすべて同一。
- 新規 `install.py` は `install.py` に全文を収録。追加位置は新規ディレクトリ直下。
- 新規テスト関数は `tests/test_fix.py` に全文を収録。import 全文も同梱。
- PowerShell 実行ファイル全文は `run.ps1` を参照。

## 修正箇所

```python
PINS = {
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
}
```

上の辞書は説明用の変更対象1行だけの抜粋であり、**そのまま置換するための完全な辞書は `replacement/source_guard.py`** に収録している。既存の他の `PINS` は一切除去しない。
