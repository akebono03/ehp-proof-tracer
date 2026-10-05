# Phase 159-R1-3 repair2

## 変更対象

`toda_group_proof_narrative_renderer.py`

### `_phase159_unique_preimage_definition_line()` 全体

```python
def _phase159_unique_preimage_definition_line(
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion
  group_map = getattr(
    statement,
    "map",
    None,
  )
  element = getattr(
    statement,
    "element",
    None,
  )
  image = getattr(
    statement,
    "image",
    None,
  )

  if (
    group_map is None
    or element is None
    or image is None
  ):
    return None

  isomorphism_premise = next(
    (
      premise_step
      for premise_step in proof_step.premises
      if (
        isinstance(
          premise_step,
          ProofStep,
        )
        and isinstance(
          premise_step.conclusion,
          _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
        )
        and getattr(
          premise_step.conclusion,
          "map",
          None,
        )
        == group_map
      )
    ),
    None,
  )

  if isomorphism_premise is None:
    return None

  map_name = getattr(
    group_map,
    "name",
    None,
  )

  if not isinstance(
    map_name,
    str,
  ):
    return None

  return (
    "この同型写像により, $"
    + map_name
    + "("
    + render_toda_expression_latex(
      element
    )
    + ") = "
    + render_toda_expression_latex(
      image
    )
    + "$ となる $"
    + render_toda_expression_latex(
      element
    )
    + r" \in "
    + render_toda_primary_group_latex(
      group_map.source_group
    )
    + "$ が一意に存在する."
  )
```

### 呼び出し側

```python
    replacement = _phase159_unique_preimage_definition_line(
      proof_step,
    )
```

## import

変更なし。

## test

変更なし。

## 実行 pytest

- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
- `tests/test_phase159_r1_2_hopf_injective_dependency_role.py`
- `tests/test_phase159_r1_2_hopf_isomorphism_dependency_role.py`
- `tests/test_phase49_generator_transport.py`
- `tests/test_phase143_71a_eta_definition_visibility.py`

## 完了条件

focused tests が全て PASS し、public Narrative に

`この同型写像により, $H(\eta_{2}) = \iota_{3}$ となる $\eta_{2} \in \pi_{3}^{2}$ が一意に存在する.`

が表示されること。

## 次 Phase との境界

Reference attribution、exactness、numbering、theorem/rule、stable range は変更しない。
