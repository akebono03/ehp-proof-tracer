# Phase 158-R5-5b repair1h changed code

## 変更対象

`toda_group_proof_generic_narrative_renderer.py`

変更関数:
`_normalize_generic_narrative_statement_latex()`

import の変更はありません。

変更後の関数全文:

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

    if rendered_expression is None:
      continue

    normalized_expression = (
      _render_generic_narrative_expression_latex(
        expression
      )
    )

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

## Tests

新規・変更なし。

既存の以下を実行する:

- `tests/test_phase156_r6_repair2_independent_relation_side_normalization.py`
- `tests/test_phase157_r20_repair28_match_step_level_eta_normalization.py`
- `tests/test_phase149_rc3_3_minimal_ordering.py`
- `tests/test_phase158_r5_5b_public_generic_order_route.py`
- Phase 150 route-contract tests

## Phase boundary

- equation numbering algorithm は変更しない
- proof graph は変更しない
- semantic dependency は変更しない
- Argument ordering は変更しない
- pi_6^3 固有処理は追加しない
- repository-wide pytest は実行しない
