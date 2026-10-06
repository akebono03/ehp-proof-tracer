# Phase 159-R1-7c R2 repair2

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - R2 適用前 backup から既存 public renderer を復元
  - 新規 helper:
    - `_phase159_r1_7c_inline_math_content`
    - `_phase159_r1_7c_rendered_step_math_content`
    - `_phase159_r1_7c_exact_step_line_indices`
    - `_phase159_r1_7c_equality_transitivity_chain_latex`
    - `_phase159_r1_7c_reference_prefix`
    - `_phase159_r1_7c_equation_number_reused`
    - `_phase159_r1_7c_collapse_equality_transitivity_chains`
    - `_phase159_r1_7c_normalize_public_equality_chains`
  - 既存 render 関数を
    `_phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown`
    として保持
  - `render_toda_group_proof_narrative_markdown` を wrapper 化

### Test
- 新規:
  - `tests/test_phase159_r1_7c_r2_repair2_restore_pipeline.py`

## import

import の変更はありません。

## 新規 helper 全文

```python
def _phase159_r1_7c_inline_math_content(
  line: str,
) -> str | None:
  if line.count(
    "$"
  ) != 2:
    return None

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
    return None

  content = line[
    math_start + 1:
    math_end
  ]

  tag_number = (
    _phase158_public_equation_tag_number(
      content
    )
  )

  if tag_number is not None:
    content = content.replace(
      (
        r"\tag{"
        + str(
          tag_number
        )
        + "}"
      ),
      "",
      1,
    )

  return content.strip()


def _phase159_r1_7c_rendered_step_math_content(
  proof_step: ProofStep,
) -> str | None:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if (
    not rendered
    or rendered.count(
      "$"
    )
    != 2
  ):
    return None

  math_start = rendered.find(
    "$"
  )
  math_end = rendered.find(
    "$",
    math_start + 1,
  )

  if (
    math_start < 0
    or math_end < 0
  ):
    return None

  return rendered[
    math_start + 1:
    math_end
  ].strip()


def _phase159_r1_7c_exact_step_line_indices(
  proof_body: list[
    str
  ],
  proof_step: ProofStep,
) -> tuple[
  int,
  ...,
]:
  expected = (
    _phase159_r1_7c_rendered_step_math_content(
      proof_step
    )
  )

  if expected is None:
    return ()

  return tuple(
    index
    for index, line in enumerate(
      proof_body
    )
    if (
      _phase159_r1_7c_inline_math_content(
        line
      )
      == expected
    )
  )


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

  if (
    first.lhs == conclusion.lhs
    and first.rhs == second.lhs
    and second.rhs == conclusion.rhs
  ):
    middle = first.rhs
  elif (
    second.lhs == conclusion.lhs
    and second.rhs == first.lhs
    and first.rhs == conclusion.rhs
  ):
    middle = second.rhs
  else:
    return None

  try:
    return (
      render_toda_expression_latex(
        conclusion.lhs
      )
      + " = "
      + render_toda_expression_latex(
        middle
      )
      + " = "
      + render_toda_expression_latex(
        conclusion.rhs
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    return None


def _phase159_r1_7c_reference_prefix(
  line: str,
) -> str:
  math_start = line.find(
    "$"
  )

  if math_start < 0:
    return ""

  prefix = line[
    :math_start
  ]

  if (
    prefix.endswith(
      "より, "
    )
    or prefix.endswith(
      "より,"
    )
  ):
    return prefix

  return ""


def _phase159_r1_7c_equation_number_reused(
  proof_body: list[
    str
  ],
  number: int,
  ignored_indices: frozenset[
    int
  ],
) -> bool:
  marker = (
    "("
    + str(
      number
    )
    + ")"
  )

  return any(
    marker in line
    for index, line in enumerate(
      proof_body
    )
    if index not in ignored_indices
  )


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
    elif (
      second.lhs == conclusion.lhs
      and second.rhs == first.lhs
      and first.rhs == conclusion.rhs
    ):
      ordered_steps = (
        second_step,
        first_step,
      )
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
      != 1
      or len(
        second_indices
      )
      != 1
      or len(
        conclusion_indices
      )
      != 1
    ):
      continue

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

  return (
    _phase158_normalize_public_equation_numbers(
      result
    )
  )


def _phase159_r1_7c_normalize_public_equality_chains(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  proof_marker = "\n## 証明\n"

  if proof_marker not in rendered:
    return rendered

  prefix, proof = rendered.split(
    proof_marker,
    1,
  )
  proof_lines = proof.rstrip().splitlines()

  normalized_lines = (
    _phase159_r1_7c_collapse_equality_transitivity_chains(
      presentation,
      proof_lines,
    )
  )

  return (
    prefix
    + proof_marker
    + "\n".join(
      normalized_lines
    ).rstrip()
    + "\n"
  )
```

## 変更後 public wrapper 全文

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase159_r1_7c_preexisting_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  return (
    _phase159_r1_7c_normalize_public_equality_chains(
      presentation,
      rendered,
    )
  )
```

## 修正理由

R2 repair1 診断で以下を確認した。

1. R2 は preexisting public renderer の最終処理を置換してしまい、
   map-property prose の既存契約を回帰させた。
2. equality transitivity conclusion の検索が substring matching だったため、
   後続文章内の同じ数式まで候補になり、line index が一意にならなかった。
3. pre-R2 出力では局所 transitivity chain は残っていたため、
   既存 pipeline を完全維持した後の最終 wrapper で畳むのが最小変更。

repair2 は R2 適用直前 backup の public renderer をそのまま復元し、
その出力にだけ equality-chain normalization を追加する。

## 実行する pytest

focused tests のみ。
full pytest は Phase 159 最後まで実行しない。

## 完了条件

- pi6_3 の局所 transitivity が1本の連続等式になる。
- tag(1), tag(2), connector が消える。
- pi6_3 E/H map-property の既存簡潔表現を維持。
- pi11_4 Delta 全射の既存簡潔表現と exactness 順序を維持。
- R1-7b / Phase157 focused regression が PASS。

## 次 R3 との境界

R2 は equality-transitivity 表示統合だけ。
pi11_4 の direct-premise specialization / known-result ancestry suppression は R3。
