# Phase 159-R1-7c R2

## 変更対象

### Production
- `toda_group_proof_narrative_renderer.py`
  - 新規:
    - `_phase159_r1_7c_equality_transitivity_chain_latex`
    - `_phase159_r1_7c_line_without_equation_tag`
    - `_phase159_r1_7c_step_line_indices`
    - `_phase159_r1_7c_reference_prefix`
    - `_phase159_r1_7c_equation_number_reused`
    - `_phase159_r1_7c_collapse_equality_transitivity_chains`
    - `_phase159_r1_7c_normalize_public_equality_chains`
  - 変更:
    - `render_toda_group_proof_narrative_markdown`

### Test
- 新規:
  - `tests/test_phase159_r1_7c_r2_equality_transitivity_collapse.py`

## import

import の変更はありません。

既存 import:
- `ProofStep`
- `Relation`
- `RelationType`
- `render_toda_expression_latex`
- `build_toda_group_proof_narrative_semantic_closure_presentation`

を再利用する。

## 新規 helper 全文

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
    return None

  try:
    latex = (
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

  return latex


def _phase159_r1_7c_line_without_equation_tag(
  line: str,
) -> str:
  tag_number = (
    _phase158_public_equation_tag_number(
      line
    )
  )

  if tag_number is None:
    return line

  return line.replace(
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


def _phase159_r1_7c_step_line_indices(
  proof_body: list[
    str
  ],
  proof_step: ProofStep,
) -> tuple[
  int,
  ...,
]:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if not rendered:
    return ()

  return tuple(
    index
    for index, line in enumerate(
      proof_body
    )
    if rendered in (
      _phase159_r1_7c_line_without_equation_tag(
        line
      )
    )
  )


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

  if not prefix.endswith(
    "より, "
  ):
    return ""

  return prefix


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
      _phase159_r1_7c_step_line_indices(
        result,
        ordered_steps[
          0
        ],
      )
    )
    second_indices = (
      _phase159_r1_7c_step_line_indices(
        result,
        ordered_steps[
          1
        ],
      )
    )
    conclusion_indices = (
      _phase159_r1_7c_step_line_indices(
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

## 変更後関数全文

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  normalized = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )

  return (
    _phase159_r1_7c_normalize_public_equality_chains(
      presentation,
      normalized,
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


def test_phase159_r1_7c_r2_pi6_3_collapses_local_transitivity_chain():
  rendered = _render(
    3,
    3,
  )
  expected = (
    "[R2] より, "
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5} "
    r"= \eta_{3}^{3}$."
  )

  assert expected in rendered
  assert (
    r"$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$."
    not in rendered
  )
  assert (
    r"$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$."
    not in rendered
  )
  assert "(1) と (2) より," not in rendered


def test_phase159_r1_7c_r2_pi11_4_exactness_contract_is_preserved():
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
    "\\[\n"
    r"\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}."
    "\n\\]"
    in rendered
  )


def test_phase159_r1_7c_r2_helper_has_no_group_or_theorem_special_case():
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

## 一般規則

`equality transitivity` の2前提

`a=b`, `b=c`

と結論 `a=c` が public body に局所的に並び、
前提の式番号がその局所 connector 以外では再利用されていない場合のみ、

`a=b=c`

へ統合する。

Reference marker が最初の前提に付いていれば維持する。

後続で再利用される equation number は削除しない。

## 実行する pytest

focused tests のみ。
repository-wide pytest は Phase 159 最後まで実行しない。

## 完了条件

- pi6_3 が
  `[R2] より, $2\nu' = \eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}$.`
  になる。
- `tag(1)`, `tag(2)`, `(1) と (2) より` が消える。
- pi11_4 の R1-7b exactness contract を壊さない。
- focused tests PASS。

## 次 R3 との境界

R2 は equality transitivity の局所表示統合だけ。
pi11_4 の root direct-premise specialization と ancestry suppression は R3 で扱う。
Reference aggregate の一般的な component selection は R3 の必要範囲だけを監査し、
将来 Phase の全面的な Reference redesign は行わない。
