# R52-R13-R2 変更対象と範囲

- `phase165_r52_r13_reference_registration.py`: `register_adopted_composite_reference()` に成分名メタデータを追加。
- `phase165_typed_component_lookup.py`: `index_typed_components()` がメタデータで複合命題を識別。
- `phase165_r52_r7_registered_common_proof.py`: `build_registered_common_replay()` の標準検索経路で GIVEN の root も許可。
- `test_phase165_r52_r13_r2_generic_reference_fix.py`: 新規テスト3件。

`*.after.py` は最初の2ファイルについて、置き換え可能な変更後全文を含む確認用コピーです。install.py は現行ファイルの対象箇所のみを置換します。

第三の変更は `build_registered_common_replay()` 内の次の分岐だけです。関数の他の部分は保持します。

```python
        if root is None or root.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE):
            raise GoalSearchIncompleteError("completed proof is not a typed proof step")
```

全体 pytest は実行しません。一般形の条件付き特殊化は次 Phase の範囲です。
