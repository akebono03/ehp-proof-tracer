# Phase 159-R1-7b — changed code

## 変更対象
- `toda_group_proof_narrative_renderer.py`
- `tests/test_phase157_r20_repair37_short_exact_after_map_support.py`
- `tests/test_phase159_r1_7b_exact_sequence_display_order.py`（新規）

## import
import の変更はありません。

## 新規関数
追加位置: `_phase158_normalize_public_narrative_contract` の直前。

```python
def _phase159_r1_7b_exactness_step_latex(
  proof_step: ProofStep,
) -> str | None:
  if not isinstance(
    proof_step.conclusion,
    TodaProp42ExactnessStatement,
  ):
    return None

  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if (
    not rendered.startswith(
      "$"
    )
    or not rendered.endswith(
      "$"
    )
  ):
    return None

  latex = rendered[
    1:-1
  ]
  english_suffix = (
    r" \text{ is exact}"
  )

  if latex.endswith(
    english_suffix
  ):
    latex = latex[
      :-len(
        english_suffix
      )
    ]

  return latex


def _phase159_r1_7b_inline_exactness_latex(
  line: str,
) -> str | None:
  stripped = line.strip()
  suffix = "$ は完全である."

  if (
    not stripped.startswith(
      "$"
    )
    or not stripped.endswith(
      suffix
    )
  ):
    return None

  latex = stripped[
    1:-len(
      suffix
    )
  ]

  if (
    r"\xrightarrow{" not in latex
    and r"\longrightarrow" not in latex
  ):
    return None

  return latex


def _phase159_r1_7b_inline_short_exact_latex(
  line: str,
) -> str | None:
  stripped = line.strip()

  if not stripped.startswith(
    r"$0\longrightarrow "
  ):
    return None

  if stripped.endswith(
    "$."
  ):
    latex = stripped[
      1:-2
    ]
  elif stripped.endswith(
    "$"
  ):
    latex = stripped[
      1:-1
    ]
  else:
    return None

  if not latex.endswith(
    r"\longrightarrow 0"
  ):
    return None

  return latex


def _phase159_r1_7b_display_math_lines(
  latex: str,
) -> tuple[
  str,
  ...,
]:
  return (
    r"\[",
    latex.rstrip(
      "."
    )
    + ".",
    r"\]",
    "",
  )


def _phase159_r1_7b_map_property_signature(
  line: str,
) -> tuple[
  str,
  str,
  str,
] | None:
  stripped = line.strip()

  if not stripped.startswith(
    "$"
  ):
    return None

  math_end = stripped.find(
    "$",
    1,
  )

  if math_end < 0:
    return None

  suffix = stripped[
    math_end + 1:
  ].strip()

  if not (
    suffix.startswith(
      "は単射"
    )
    or suffix.startswith(
      "は全射"
    )
    or suffix.startswith(
      "は零写像"
    )
    or suffix.startswith(
      "は同型"
    )
  ):
    return None

  math = stripped[
    1:math_end
  ]

  if ": " not in math:
    return None

  map_name, map_expression = math.split(
    ": ",
    1,
  )

  arrow = r" \to "

  if arrow not in map_expression:
    return None

  source, target = map_expression.split(
    arrow,
    1,
  )

  if (
    not source.startswith(
      r"\pi_{"
    )
    or not target.startswith(
      r"\pi_{"
    )
  ):
    return None

  return (
    map_name,
    source,
    target,
  )


def _phase159_r1_7b_exactness_matches_map_property(
  exactness_latex: str,
  signature: tuple[
    str,
    str,
    str,
  ],
) -> bool:
  map_name, source, target = signature
  map_segment = (
    source
    + r" \xrightarrow{"
    + map_name
    + "} "
    + target
  )

  return (
    map_segment
    in exactness_latex
  )


def _phase159_r1_7b_find_display_math_span(
  lines: list[
    str
  ],
  latex: str,
) -> tuple[
  int,
  int,
] | None:
  normalized_target = latex.rstrip(
    "."
  )
  index = 0

  while index < len(
    lines
  ):
    if lines[
      index
    ].strip() != r"\[":
      index += 1
      continue

    end_index = index + 1
    inner_lines = []

    while (
      end_index < len(
        lines
      )
      and lines[
        end_index
      ].strip() != r"\]"
    ):
      if lines[
        end_index
      ].strip():
        inner_lines.append(
          lines[
            end_index
          ].strip()
        )
      end_index += 1

    if end_index >= len(
      lines
    ):
      return None

    normalized_inner = " ".join(
      inner_lines
    ).rstrip(
      "."
    )

    if (
      normalized_inner
      == normalized_target
    ):
      span_end = end_index + 1

      if (
        span_end < len(
          lines
        )
        and not lines[
          span_end
        ].strip()
      ):
        span_end += 1

      return (
        index,
        span_end,
      )

    index = end_index + 1

  return None


def _phase159_r1_7b_next_nonblank_index(
  lines: list[
    str
  ],
  start: int,
) -> int | None:
  return next(
    (
      index
      for index in range(
        start,
        len(
          lines
        ),
      )
      if lines[
        index
      ].strip()
    ),
    None,
  )


def _phase159_r1_7b_normalize_public_exact_sequences(
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

  exactness_latex = tuple(
    latex
    for latex in (
      _phase159_r1_7b_exactness_step_latex(
        node.proof_step
      )
      for node in presentation.nodes
    )
    if latex is not None
  )

  lines = []

  for line in proof_body:
    inline_exactness = (
      _phase159_r1_7b_inline_exactness_latex(
        line
      )
    )

    if inline_exactness is not None:
      lines.extend(
        _phase159_r1_7b_display_math_lines(
          inline_exactness
        )
      )
      continue

    inline_short_exact = (
      _phase159_r1_7b_inline_short_exact_latex(
        line
      )
    )

    if inline_short_exact is not None:
      lines.extend(
        _phase159_r1_7b_display_math_lines(
          inline_short_exact
        )
      )
      continue

    lines.append(
      line
    )

  connector_index = 0

  while connector_index < len(
    lines
  ):
    if lines[
      connector_index
    ].strip() != "完全性より,":
      connector_index += 1
      continue

    property_index = (
      _phase159_r1_7b_next_nonblank_index(
        lines,
        connector_index + 1,
      )
    )

    if property_index is None:
      break

    signature = (
      _phase159_r1_7b_map_property_signature(
        lines[
          property_index
        ]
      )
    )

    if signature is None:
      connector_index += 1
      continue

    matching_latex = next(
      (
        latex
        for latex in exactness_latex
        if (
          _phase159_r1_7b_exactness_matches_map_property(
            latex,
            signature,
          )
        )
      ),
      None,
    )

    if matching_latex is None:
      connector_index += 1
      continue

    existing_span = (
      _phase159_r1_7b_find_display_math_span(
        lines,
        matching_latex,
      )
    )

    if (
      existing_span is not None
      and existing_span[
        0
      ] < connector_index
    ):
      connector_index += 1
      continue

    if existing_span is not None:
      span_start, span_end = existing_span
      del lines[
        span_start:span_end
      ]

      if span_start < connector_index:
        connector_index -= (
          span_end
          - span_start
        )

    display_lines = list(
      _phase159_r1_7b_display_math_lines(
        matching_latex
      )
    )
    lines[
      connector_index:connector_index
    ] = display_lines

    connector_index += len(
      display_lines
    ) + 1

  return lines


```

## `_phase158_normalize_public_narrative_contract` の変更箇所
既存の equation-number normalization の直後に以下を追加します。

```python
  proof_body = (
    _phase159_r1_7b_normalize_public_exact_sequences(
      presentation,
      proof_body,
    )
  )
```

## 変更後テストファイル全文

### tests/test_phase157_r20_repair37_short_exact_after_map_support.py
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


def _body_pi6_3_repair37() -> str:
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report
    .candidates[0]
    .source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  return rendered.split(
    "\n## 証明\n",
    1,
  )[1]


def test_phase157_r20_repair37_short_exact_follows_surjectivity():
  body = _body_pi6_3_repair37()

  surjectivity = (
    r"$H: \pi_{6}^{3} \to \pi_{6}^{5}$ "
    "は全射である."
  )
  reason = (
    "この完全性と, 左の写像が単射, "
    "右の写像が全射であることより, "
    "次の短完全列を得る."
  )
  short_exact = (
    "\\[\n"
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    "\\longrightarrow 0.\n"
    "\\]"
  )

  assert surjectivity in body
  assert reason in body
  assert short_exact in body

  assert body.index(
    surjectivity
  ) < body.index(
    reason
  )
  assert body.index(
    reason
  ) < body.index(
    short_exact
  )


def test_phase157_r20_repair37_short_exact_follows_injectivity():
  body = _body_pi6_3_repair37()

  injectivity = (
    r"$E: \pi_{5}^{2} \to \pi_{6}^{3}$ "
    "は単射である."
  )
  short_exact = (
    "\\[\n"
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    "\\longrightarrow 0.\n"
    "\\]"
  )

  assert body.index(
    injectivity
  ) < body.index(
    short_exact
  )
```

### tests/test_phase159_r1_7b_exact_sequence_display_order.py
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


def _phase159_r1_7b_render(
  n: int,
  k: int,
) -> str:
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report
    .candidates[
      0
    ].source_candidate.group_result
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


def test_phase159_r1_7b_pi6_3_short_exact_sequence_is_display_math():
  rendered = _phase159_r1_7b_render(
    3,
    3,
  )
  short_exact = (
    "\\[\n"
    r"0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    "\\longrightarrow 0.\n"
    "\\]"
  )

  assert short_exact in rendered
  assert (
    r"$0\longrightarrow \pi_{5}^{2}"
    r"\xrightarrow{E} \pi_{6}^{3}"
    r"\xrightarrow{H} \pi_{6}^{5}"
    r"\longrightarrow 0$"
    not in rendered
  )


def test_phase159_r1_7b_pi11_4_delta_surjectivity_has_matching_exactness_before_it():
  rendered = _phase159_r1_7b_render(
    4,
    7,
  )
  matching_exactness = (
    "\\[\n"
    r"\pi_{10}^{3} \xrightarrow{H} \pi_{10}^{5} "
    r"\xrightarrow{\Delta} \pi_{8}^{2}."
    "\n\\]"
  )
  surjectivity_reason = (
    "完全性より,"
  )
  surjectivity = (
    r"$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$"
    " は全射."
  )

  assert matching_exactness in rendered
  assert surjectivity_reason in rendered
  assert surjectivity in rendered
  assert rendered.index(
    matching_exactness
  ) < rendered.index(
    surjectivity_reason
  )
  assert rendered.index(
    surjectivity_reason
  ) < rendered.index(
    surjectivity
  )


def test_phase159_r1_7b_pi11_4_visible_exactness_windows_use_display_math():
  rendered = _phase159_r1_7b_render(
    4,
    7,
  )
  second_exactness = (
    "\\[\n"
    r"\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}."
    "\n\\]"
  )

  assert second_exactness in rendered
  assert (
    r"$\pi_{9}^{2} \xrightarrow{E} \pi_{10}^{3} "
    r"\xrightarrow{H} \pi_{10}^{5}$ は完全である."
    not in rendered
  )
```

## Phase 境界
R1-7b で行う:
- 完全列の display math 統一
- 短完全列の display math 統一
- `完全性より,` の前に対応 typed exactness を配置

R1-7b で行わない:
- `2ν' = η3η4η5 = η3^3` への統合
- equation numbering policy の整理
- Reference aggregate suppression
- map-property prose 全般の統一
- full pytest
