# Phase 159-R1-7c R2 repair3

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - `_phase159_r1_7c_collapse_equality_transitivity_chains`

### Test
- 新規:
  - `tests/test_phase159_r1_7c_r2_repair3_projected_chain_match.py`

## import

import の変更はありません。

## 変更後関数全文

```python
def _phase159_r1_7c_collapse_equality_transitivity_chains(
  presentation: TodaGroupProofPresentation,
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    proof_body,
    list,
  ):
    raise TypeError(
      "proof_body must be a list"
    )

  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  result = list(
    proof_body
  )

  for node in semantic_presentation.nodes:
    proof_step = node.proof_step
    chain_latex = (
      _phase159_r1_7c_equality_transitivity_chain_latex(
        proof_step
      )
    )

    if chain_latex is None:
      continue

    first_step, second_step = (
      proof_step.premises
    )
    first = first_step.conclusion
    second = second_step.conclusion
    conclusion = proof_step.conclusion

    if (
      first.lhs == conclusion.lhs
      and first.rhs == second.lhs
      and second.rhs == conclusion.rhs
    ):
      ordered_steps = (
        first_step,
        second_step,
      )
      middle = first.rhs
    elif (
      second.lhs == conclusion.lhs
      and second.rhs == first.lhs
      and first.rhs == conclusion.rhs
    ):
      ordered_steps = (
        second_step,
        first_step,
      )
      middle = second.rhs
    else:
      continue

    if middle == conclusion.rhs:
      continue

    first_indices = (
      _phase159_r1_7c_exact_step_line_indices(
        result,
        ordered_steps[
          0
        ],
      )
    )
    second_indices = (
      _phase159_r1_7c_exact_step_line_indices(
        result,
        ordered_steps[
          1
        ],
      )
    )
    conclusion_indices = (
      _phase159_r1_7c_exact_step_line_indices(
        result,
        proof_step,
      )
    )

    if (
      len(
        first_indices
      )
      == 1
      and len(
        second_indices
      )
      == 1
      and len(
        conclusion_indices
      )
      == 1
    ):
      first_index = first_indices[
        0
      ]
      second_index = second_indices[
        0
      ]
      conclusion_index = (
        conclusion_indices[
          0
        ]
      )

      if not (
        first_index
        < second_index
        < conclusion_index
      ):
        continue

      first_number = (
        _phase158_public_equation_tag_number(
          result[
            first_index
          ]
        )
      )
      second_number = (
        _phase158_public_equation_tag_number(
          result[
            second_index
          ]
        )
      )

      if (
        first_number is None
        or second_number is None
      ):
        continue

      connector_indices = tuple(
        index
        for index in range(
          second_index + 1,
          conclusion_index,
        )
        if (
          _phase158_public_equation_connector_numbers(
            result[
              index
            ]
          )
          == (
            first_number,
            second_number,
          )
        )
      )

      if len(
        connector_indices
      ) != 1:
        continue

      connector_index = (
        connector_indices[
          0
        ]
      )
      local_indices = frozenset(
        (
          first_index,
          second_index,
          connector_index,
          conclusion_index,
        )
      )

      if (
        _phase159_r1_7c_equation_number_reused(
          result,
          first_number,
          local_indices,
        )
        or _phase159_r1_7c_equation_number_reused(
          result,
          second_number,
          local_indices,
        )
      ):
        continue

      allowed_nonblank_indices = {
        first_index,
        second_index,
        connector_index,
        conclusion_index,
      }

      if any(
        result[
          index
        ].strip()
        and index
        not in allowed_nonblank_indices
        for index in range(
          first_index,
          conclusion_index + 1,
        )
      ):
        continue

      prefix = (
        _phase159_r1_7c_reference_prefix(
          result[
            first_index
          ]
        )
      )
      replacement = (
        prefix
        + "$"
        + chain_latex
        + "$."
      )

      result[
        first_index:
        conclusion_index + 1
      ] = [
        replacement,
      ]
      continue

    try:
      lhs_latex = (
        render_toda_expression_latex(
          conclusion.lhs
        )
      )
      middle_latex = (
        render_toda_expression_latex(
          middle
        )
      )
    except (
      TypeError,
      ValueError,
    ):
      continue

    projected_indices = []

    for index, line in enumerate(
      result
    ):
      content = (
        _phase159_r1_7c_inline_math_content(
          line
        )
      )

      if content is None:
        continue

      if (
        content.startswith(
          lhs_latex
          + " = "
        )
        and content.endswith(
          " = "
          + middle_latex
        )
      ):
        projected_indices.append(
          index
        )
        continue

      if content == (
        lhs_latex
        + " = "
        + middle_latex
      ):
        projected_indices.append(
          index
        )

    if len(
      projected_indices
    ) != 1:
      continue

    projected_index = (
      projected_indices[
        0
      ]
    )
    line = result[
      projected_index
    ]
    math_start = line.find(
      "$"
    )
    math_end = line.find(
      "$",
      math_start + 1,
    )

    if (
      math_start < 0
      or math_end < 0
    ):
      continue

    result[
      projected_index
    ] = (
      line[
        :math_start + 1
      ]
      + chain_latex
      + line[
        math_end:
      ]
    )

  return (
    _phase158_normalize_public_equation_numbers(
      result
    )
  )
```

## 新規テスト全文

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate
    .group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )

  return render_toda_group_proof_narrative_markdown(
    presentation
  )


def test_phase159_r1_7c_r2_repair3_uses_canonical_transitivity_chain():
  rendered = _render(
    3,
    3,
  )

  assert (
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}$."
    in rendered
  )
  assert (
    r"$2\nu' = \eta_{3}E\eta_{3}\eta_{5} "
    r"= \eta_{3}\eta_{4}\eta_{5}$."
    not in rendered
  )
  assert "(1) と (2) より," not in rendered


def test_phase159_r1_7c_r2_repair3_does_not_duplicate_identity_transitivity():
  rendered = _render(
    3,
    3,
  )

  assert (
    r"$H\left(\nu'\right) = \eta_{5} = \eta_{5}$"
    not in rendered
  )


def test_phase159_r1_7c_r2_repair3_preserves_pi11_delta_surjectivity():
  rendered = _render(
    4,
    7,
  )

  assert (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は全射."
    in rendered
  )
```

## 修正理由

repair2 focused test は 23/24 PASS。
既存 R1-7b / Phase157 regression はすべて復旧した。

残る失敗は equality-transitivity chain だけ。

runtime diagnosis では semantic projection 後の pi6_3 が

`$2\nu' = \eta_{3}E\eta_{3}\eta_{5} = \eta_{3}\eta_{4}\eta_{5}$.`

となり、元の前提式そのものは public body に残っていなかった。

repair3 では pipeline を動かさず、
proof graph の `a=b`, `b=c`, `a=c` と
projected public math `$a=...=b$` を照合し、
canonical `$a=b=c$` に置換する。

`b=c` が identity (`b=c` で b==c) の場合は変換しない。

group / theorem / generator 固有分岐は追加しない。

## 実行する pytest

focused tests のみ。
full pytest は Phase 159 最後まで実行しない。

## 完了条件

- pi6_3 が
  `$2\nu' = \eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}$.`
  になる。
- semantic projection の余分な中間式
  `$\eta_{3}E\eta_{3}\eta_{5}$`
  を残さない。
- identity transitivity を重複等式にしない。
- pi11_4 Delta 全射と R1-7b exactness contract を維持。
- focused tests PASS。

## 次 R3 との境界

R2 は equality-transitivity 表示統合のみ。
pi11_4 の direct-premise specialization / known-result ancestry suppression は R3。
