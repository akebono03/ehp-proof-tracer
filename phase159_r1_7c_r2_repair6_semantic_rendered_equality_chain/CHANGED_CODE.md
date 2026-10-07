# Phase 159-R1-7c R2 repair6

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - 新規:
    - `_phase159_r1_7c_rendered_equality_parts`
  - 変更:
    - `_phase159_r1_7c_equality_transitivity_chain_latex`
    - `_phase159_r1_7c_collapse_equality_transitivity_chains`

### Test
- 新規:
  - `tests/test_phase159_r1_7c_r2_repair6_semantic_rendered_equality_chain.py`

## import

import の変更はありません。

## 新規 helper 全文

```python
def _phase159_r1_7c_rendered_equality_parts(
  proof_step: ProofStep,
) -> tuple[
  str,
  str,
] | None:
  content = (
    _phase159_r1_7c_rendered_step_math_content(
      proof_step
    )
  )

  if (
    content is None
    or content.count(
      " = "
    )
    != 1
  ):
    return None

  left, right = content.split(
    " = ",
    1,
  )

  if (
    not left
    or not right
  ):
    return None

  return (
    left,
    right,
  )
```

## 変更関数全文

```python
def _phase159_r1_7c_equality_transitivity_chain_latex(
  proof_step: ProofStep,
) -> str | None:
  conclusion = proof_step.conclusion
  inference_rule = proof_step.inference_rule

  if (
    inference_rule is None
    or inference_rule.name
    != "equality transitivity"
    or not isinstance(
      conclusion,
      Relation,
    )
    or conclusion.relation_type
    is not RelationType.EQUALITY
    or len(
      proof_step.premises
    )
    != 2
  ):
    return None

  first_step, second_step = (
    proof_step.premises
  )
  first = first_step.conclusion
  second = second_step.conclusion

  if (
    not isinstance(
      first,
      Relation,
    )
    or first.relation_type
    is not RelationType.EQUALITY
    or not isinstance(
      second,
      Relation,
    )
    or second.relation_type
    is not RelationType.EQUALITY
  ):
    return None

  first_parts = (
    _phase159_r1_7c_rendered_equality_parts(
      first_step
    )
  )
  second_parts = (
    _phase159_r1_7c_rendered_equality_parts(
      second_step
    )
  )
  conclusion_parts = (
    _phase159_r1_7c_rendered_equality_parts(
      proof_step
    )
  )

  if (
    first_parts is None
    or second_parts is None
    or conclusion_parts is None
  ):
    return None

  first_left, first_right = (
    first_parts
  )
  second_left, second_right = (
    second_parts
  )
  conclusion_left, conclusion_right = (
    conclusion_parts
  )

  if (
    first_left == conclusion_left
    and first_right == second_left
    and second_right == conclusion_right
  ):
    middle = first_right
  elif (
    second_left == conclusion_left
    and second_right == first_left
    and first_right == conclusion_right
  ):
    middle = second_right
  else:
    return None

  if middle == conclusion_right:
    return None

  return (
    conclusion_left
    + " = "
    + middle
    + " = "
    + conclusion_right
  )
```

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

    first_parts = (
      _phase159_r1_7c_rendered_equality_parts(
        first_step
      )
    )
    second_parts = (
      _phase159_r1_7c_rendered_equality_parts(
        second_step
      )
    )
    conclusion_parts = (
      _phase159_r1_7c_rendered_equality_parts(
        proof_step
      )
    )

    if (
      first_parts is None
      or second_parts is None
      or conclusion_parts is None
    ):
      continue

    first_left, first_right = (
      first_parts
    )
    second_left, second_right = (
      second_parts
    )
    conclusion_left, conclusion_right = (
      conclusion_parts
    )

    if (
      first_left == conclusion_left
      and first_right == second_left
      and second_right == conclusion_right
    ):
      ordered_steps = (
        first_step,
        second_step,
      )
      middle = first_right
    elif (
      second_left == conclusion_left
      and second_right == first_left
      and first_right == conclusion_right
    ):
      ordered_steps = (
        second_step,
        first_step,
      )
      middle = second_right
    else:
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
          conclusion_left
          + " = "
        )
        and content.endswith(
          " = "
          + middle
        )
      ):
        projected_indices.append(
          index
        )
        continue

      if content == (
        conclusion_left
        + " = "
        + middle
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
import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_collapse_equality_transitivity_chains,
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


def test_phase159_r1_7c_r2_repair6_pi6_3_uses_public_semantic_chain():
  rendered = _render(
    3,
    3,
  )

  expected = (
    r"[R2] より, "
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5} "
    r"= \eta_{3}^{3}$."
  )

  assert expected in rendered
  assert (
    r"\eta_{3}E\eta_{3}\eta_{5}"
    not in rendered
  )
  assert "(1) と (2) より," not in rendered


def test_phase159_r1_7c_r2_repair6_identity_transitivity_stays_compact():
  rendered = _render(
    3,
    3,
  )

  assert (
    r"$H\left(\nu'\right) = \eta_{5}$."
    in rendered
  )
  assert (
    r"$H\left(\nu'\right) = \eta_{5} = \eta_{5}$."
    not in rendered
  )


def test_phase159_r1_7c_r2_repair6_preserves_pi6_map_property_contract():
  rendered = _render(
    3,
    3,
  )

  assert (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ は単射."
    in rendered
  )
  assert (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ は全射."
    in rendered
  )


def test_phase159_r1_7c_r2_repair6_preserves_pi11_exactness_contract():
  rendered = _render(
    4,
    7,
  )

  assert (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
    in rendered
  )
  assert (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ は全射."
    in rendered
  )


def test_phase159_r1_7c_r2_repair6_has_no_group_or_theorem_special_case():
  source = inspect.getsource(
    _phase159_r1_7c_collapse_equality_transitivity_chains
  )

  forbidden = (
    "pi6",
    "(6, 3)",
    "nu_prime",
    "ν'",
    "Proposition 5.6",
    "Proposition 5.15",
  )

  for fragment in forbidden:
    assert fragment not in source
```

## 監査結果

full provenance では対象 step の raw expression は

- `2nu' = eta3 E eta3 eta5`
- `eta3 E eta3 eta5 = eta3 eta4 eta5`
- conclusion `2nu' = eta3 eta4 eta5`

である。

一方 generic renderer は同じ3 step を public semantics として

- `2nu' = eta3 eta4 eta5`
- `eta3 eta4 eta5 = eta3^3`
- conclusion `2nu' = eta3^3`

と表示している。

R1-7c は public Narrative の整理なので、
raw expression を書き換えず、generic renderer が確定した public equality を
`a=b`, `b=c`, `a=c` として検証して `a=b=c` に統合する。

## 実行する pytest

focused tests のみ。
full pytest は Phase 159 最後まで実行しない。

## 完了条件

- pi6_3:
  `[R2] より, $2\nu' = \eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}$.`
- raw 中間表示 `eta3 E eta3 eta5` は public body に残らない。
- identity transitivity は重複等式にしない。
- pi6 map-property contract を維持。
- pi11 exactness contract を維持。
- focused tests PASS。

## 次 R3 との境界

R2 は equality-transitivity の public semantic composition まで。
pi11_4 direct-premise specialization と known-result ancestry suppression は R3。
