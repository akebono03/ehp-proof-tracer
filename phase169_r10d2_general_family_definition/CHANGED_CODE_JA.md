# R10D2 コード変更一覧と置換単位

1. `phase165_r52_r9_shared_math.py`：既存の `build_shared_typed_bridge()` と `shared_expansion_provider()`。両関数の完全な変更後コードは、実行時に `output/build_shared_typed_bridge_FULL.py` と `output/shared_expansion_provider_FULL.py` に保存する。変更後のモジュール全文は `output/phase165_r52_r9_shared_math.py.FULL`。
2. `phase168_r3_37c_reference_projection.py`：既存の `project_reference_bodies()`。変更後の完全な関数は `output/project_reference_bodies_FULL.py`、変更後のモジュール全文は `output/phase168_r3_37c_reference_projection.py.FULL`。
3. **新規** `phase169_r10d2_general_family_definition/family_citation.py`：`FamilySourceRecord`、`CitedStableFamilyDefinition`、`StableFamilyMemberDefinition` をファイル先頭から追加、`verified_source_positions()`、`build_cited_stable_family_definitions()`、`canonical_member()`、`expand_cited_stable_family()` ほかを順次追加。import も含めた全文が ZIP 内にある。
4. **新規** `tests/test_r10d2_general_family.py`：全 import・テスト関数の全文を ZIP 内に収録。
5. **新規** `patch.py`、`audit.py`、`run.ps1`、`README.md`、`DESIGN_JA.md`：全文を ZIP 内に収録。

既存の import はモジュール先頭では変更せず、既存関数内部の import を追加する。コードの省略はなく、対象関数を完全な置換単位で書き出す。R10D2 の ZIP は、先行する R10D の部分的な専用アダプタ ZIP と併用しない。
