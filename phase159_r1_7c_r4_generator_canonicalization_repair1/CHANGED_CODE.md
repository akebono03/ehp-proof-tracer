# Phase 159 R1-7c R4 generator canonicalization repair1

## 変更対象

### `toda_group_proof_generic_narrative_renderer.py`

import の変更はありません。

新規関数の追加位置:
`_try_render_generic_narrative_expression_latex()` の直後。

```python
def _try_render_generic_narrative_group_structure_latex(
  group,
) -> str | None:
  try:
    return render_toda_raw_group_structure_latex(
      group
    )
  except (
    TypeError,
    ValueError,
  ):
    return None
```

変更関数全体:

```python
def _normalize_generic_narrative_statement_latex(
  statement,
  latex: str,
) -> str:
  if not isinstance(
    latex,
    str,
  ):
    raise TypeError(
      "latex must be a str"
    )

  if not hasattr(
    statement,
    "lhs",
  ):
    return (
      _normalize_generic_eta_family_latex(
        latex
      )
    )

  if not hasattr(
    statement,
    "rhs",
  ):
    return (
      _normalize_generic_eta_family_latex(
        latex
      )
    )

  replacements = []
  search_start = 0

  for expression in (
    statement.lhs,
    statement.rhs,
  ):
    rendered_expression = (
      _try_render_generic_narrative_expression_latex(
        expression
      )
    )
    normalized_expression = None

    if rendered_expression is not None:
      normalized_expression = (
        _render_generic_narrative_expression_latex(
          expression
        )
      )
    else:
      rendered_expression = (
        _try_render_generic_narrative_group_structure_latex(
          expression
        )
      )

      if rendered_expression is not None:
        normalized_expression = (
          _normalize_generic_eta_family_latex(
            rendered_expression
          )
        )

    if (
      rendered_expression is None
      or normalized_expression is None
    ):
      continue

    expression_start = latex.find(
      rendered_expression,
      search_start,
    )

    if expression_start < 0:
      continue

    expression_end = (
      expression_start
      + len(
        rendered_expression
      )
    )
    search_start = expression_end

    if (
      normalized_expression
      == rendered_expression
    ):
      continue

    replacements.append(
      (
        expression_start,
        expression_end,
        normalized_expression,
      )
    )

  normalized = latex

  for (
    expression_start,
    expression_end,
    normalized_expression,
  ) in reversed(
    replacements
  ):
    normalized = (
      normalized[
        :expression_start
      ]
      + normalized_expression
      + normalized[
        expression_end:
      ]
    )

  return normalized
```

### `tests/test_phase143_3_generic_eta_normalization.py`

import の変更はありません。

変更テスト関数全体:

```python
def test_phase143_3_pi6_3_generic_step_uses_eta_cube():
  rendered_steps = tuple(
    _render_generic_narrative_step(step)
    for step in _pi6_3_steps()
  )

  assert any(
    r"\eta_{3}^{3}"
    in rendered
    for rendered in rendered_steps
  )
  assert any(
    (
      r"\eta_{3}\eta_{4}\eta_{5}"
      in rendered
    )
    and (
      r"\eta_{3}^{3}"
      in rendered
    )
    for rendered in rendered_steps
  )
```

### `tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py`

新規ファイルです。import を含む全文を ZIP に収録しています。
