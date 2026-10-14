# R52-R13-R3 変更一覧

- 変更ファイル: `phase165_typed_component_lookup.py`
- 変更関数: `index_typed_components()`（関数全体の変更後コードは `index_typed_components.after.py`）
- 新規テストファイル: `test_phase165_r52_r13_r3_compat_fix.py`（全文同梱）
- import は既存のまま。変更は `index_typed_components()` の旧4フィールド形式の互換判定のみ。
- 既存の `search_typed_components()` および `expand_cited_given_components()` は変更しない。
- 新規一般形の特殊化、出典資格の追加承認、証明規則追加は行わない。
