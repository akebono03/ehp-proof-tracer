# Phase 165-R57-R23-R1 変更対象

- `phase165_r57_r23_conclusion_unification.py`: `_instantiate_nested()` 全体のみ修正。import は変更なし。
- `phase165_r57_r23_conclusion_unification_r1_fix/test_phase165_r57_r23_conclusion_unification.py`: 回帰テスト1件追加。

## `_instantiate_nested()` 置換用全文

```python
def _instantiate_nested(pattern: object, bindings: tuple[VariableBinding, ...]) -> object:
    if isinstance(pattern, PatternVariable):
        return substitute_pattern_value(pattern, bindings)
    if isinstance(pattern, tuple):
        return tuple(_instantiate_nested(value, bindings) for value in pattern)
    if is_dataclass(pattern) and not isinstance(pattern, type):
        return type(pattern)(**{
            field.name: _instantiate_nested(getattr(pattern, field.name), bindings)
            for field in fields(pattern)
        })
    return substitute_pattern_value(pattern, bindings)

```

## 追加テスト全文

```python
def test_r23_pattern_variable_is_instantiated_before_dataclass_rebuild():
    variable = PatternVariable("item")
    rule = InferenceRule(name="bare variable", conclusion_pattern=variable)
    result = unify_inference_conclusion(rule, "actual")
    assert result is not None
    assert result.bindings == (VariableBinding(variable, "actual"),)
```

必要な import は既存テストに揃っています。
