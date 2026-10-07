# 変更対象

## production

`toda_group_proof_narrative_renderer.py`

新規関数:
- `_phase159_recursive_map_property_triples()`
- 追加位置:
  `_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()`
  の直前

変更関数:
- `_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()`

import の変更:
- なし

## tests

変更:
- `tests/test_phase159_r1_2_pi3_2_narrative_repair.py`
  - `test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically()`
- `tests/test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py`
  - synthetic prose-only test を semantic presentation 必須契約へ更新

新規:
- `tests/test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py`

削除:
- repair24 の一時 focused test
  `tests/test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair24.py`

# 新規関数全体

```python
def _phase159_recursive_map_property_triples(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  tuple[
    ProofStep,
    ProofStep,
    ProofStep,
  ],
  ...,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  steps = (
    _phase159_r1_6c_recursive_proof_steps(
      presentation.root_step
    )
  )
  injective_by_map = {}
  surjective_by_map = {}
  isomorphism_steps = []

  for proof_step in steps:
    statement = proof_step.conclusion
    group_map = getattr(
      statement,
      "map",
      None,
    )

    if group_map is None:
      continue

    if isinstance(
      statement,
      _GENERIC_INJECTIVE_STATEMENT_TYPES,
    ):
      injective_by_map.setdefault(
        group_map,
        proof_step,
      )
      continue

    if isinstance(
      statement,
      _GENERIC_SURJECTIVE_STATEMENT_TYPES,
    ):
      surjective_by_map.setdefault(
        group_map,
        proof_step,
      )
      continue

    if isinstance(
      statement,
      _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
    ):
      isomorphism_steps.append(
        proof_step
      )

  triples = []

  for isomorphism_step in isomorphism_steps:
    group_map = getattr(
      isomorphism_step.conclusion,
      "map",
      None,
    )

    if group_map is None:
      continue

    injective_step = (
      injective_by_map.get(
        group_map
      )
    )
    surjective_step = (
      surjective_by_map.get(
        group_map
      )
    )

    if (
      injective_step is None
      or surjective_step is None
    ):
      continue

    triples.append(
      (
        injective_step,
        surjective_step,
        isomorphism_step,
      )
    )

  return tuple(
    triples
  )

```

# 変更関数全体

```python
def _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
  rendered: str,
  presentation: TodaGroupProofPresentation | None = None,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if (
    presentation is not None
    and not isinstance(
      presentation,
      TodaGroupProofPresentation,
    )
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation or None"
    )

  if presentation is None:
    return rendered

  proof_marker = "## 証明\n\n"
  marker_index = rendered.find(
    proof_marker
  )

  if marker_index < 0:
    return rendered

  proof_start = (
    marker_index
    + len(
      proof_marker
    )
  )
  prefix = rendered[
    :proof_start
  ]
  proof_body = rendered[
    proof_start:
  ]
  lines = proof_body.splitlines()

  (
    semantic_presentation,
    semantic_sidecar,
    _primary_component,
  ) = _phase159_public_semantic_projection_context(
    presentation
  )

  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      semantic_presentation,
      semantic_sidecar,
    )
  )
  exactness_conclusion_step_ids = {
    id(
      reason.conclusion_step
    )
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  }

  tag_pattern = re.compile(
    r"\\tag\{(\d+)\}"
  )

  existing_numbers = tuple(
    int(
      match.group(
        1
      )
    )
    for line in lines
    for match in tag_pattern.finditer(
      line
    )
  )
  next_number = (
    max(
      existing_numbers,
      default=0,
    )
    + 1
  )

  def semantic_map_latex(
    proof_step: ProofStep,
  ) -> str | None:
    group_map = getattr(
      proof_step.conclusion,
      "map",
      None,
    )

    if group_map is None:
      return None

    return (
      _render_generic_narrative_group_map_latex(
        group_map
      )
    )

  def find_property_line(
    proof_step: ProofStep,
    property_label: str,
  ) -> tuple[
    int,
    int | None,
  ] | None:
    map_latex = semantic_map_latex(
      proof_step
    )

    if map_latex is None:
      return None

    prose_marker = (
      "は"
      + property_label
    )
    display_marker = (
      r"\text{は"
      + property_label
      + "}"
    )

    matches = []

    for index, line in enumerate(
      lines
    ):
      if map_latex not in line:
        continue

      if (
        prose_marker not in line
        and display_marker not in line
      ):
        continue

      tag_match = tag_pattern.search(
        line
      )
      matches.append(
        (
          index,
          (
            int(
              tag_match.group(
                1
              )
            )
            if tag_match is not None
            else None
          ),
        )
      )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  def find_isomorphism_line(
    proof_step: ProofStep,
  ) -> int | None:
    map_latex = semantic_map_latex(
      proof_step
    )

    if map_latex is None:
      return None

    matches = [
      index
      for index, line in enumerate(
        lines
      )
      if (
        map_latex in line
        and (
          "は同型." in line
          or "は同型写像." in line
          or "は同型である." in line
          or "は同型写像である." in line
        )
      )
    ]

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  numbered_by_index = {}
  isomorphism_by_index = {}

  for (
    injective_step,
    surjective_step,
    isomorphism_step,
  ) in _phase159_recursive_map_property_triples(
    presentation
  ):
    injective_row = find_property_line(
      injective_step,
      "単射",
    )
    surjective_row = find_property_line(
      surjective_step,
      "全射",
    )
    isomorphism_index = (
      find_isomorphism_line(
        isomorphism_step
      )
    )

    if (
      injective_row is None
      or surjective_row is None
      or isomorphism_index is None
    ):
      continue

    (
      injective_index,
      injective_number,
    ) = injective_row
    (
      surjective_index,
      surjective_number,
    ) = surjective_row

    if injective_number is None:
      injective_number = next_number
      next_number += 1

    if surjective_number is None:
      surjective_number = next_number
      next_number += 1

    injective_map_latex = (
      semantic_map_latex(
        injective_step
      )
    )
    surjective_map_latex = (
      semantic_map_latex(
        surjective_step
      )
    )
    isomorphism_line = (
      _phase159_plain_map_property_line(
        isomorphism_step,
        "同型",
      )
    )

    if (
      injective_map_latex is None
      or surjective_map_latex is None
      or isomorphism_line is None
    ):
      continue

    numbered_by_index[
      injective_index
    ] = (
      injective_map_latex,
      "単射",
      injective_number,
      (
        id(
          injective_step
        )
        in exactness_conclusion_step_ids
      ),
    )
    numbered_by_index[
      surjective_index
    ] = (
      surjective_map_latex,
      "全射",
      surjective_number,
      (
        id(
          surjective_step
        )
        in exactness_conclusion_step_ids
      ),
    )
    isomorphism_by_index[
      isomorphism_index
    ] = (
      injective_number,
      surjective_number,
      isomorphism_line,
    )

  output_lines = []

  def append_exactness_connector() -> None:
    previous_nonblank = next(
      (
        line.strip()
        for line in reversed(
          output_lines
        )
        if line.strip()
      ),
      None,
    )

    if previous_nonblank == "完全性より,":
      return

    if (
      output_lines
      and output_lines[
        -1
      ].strip()
    ):
      output_lines.append(
        ""
      )

    output_lines.extend(
      (
        "完全性より,",
        "",
      )
    )

  for index, line in enumerate(
    lines
  ):
    numbered = numbered_by_index.get(
      index
    )

    if numbered is not None:
      (
        map_latex,
        property_label,
        number,
        uses_exactness,
      ) = numbered

      if uses_exactness:
        append_exactness_connector()

      output_lines.extend(
        (
          r"\[",
          (
            map_latex
            + r"\quad\text{は"
            + property_label
            + r"}. \qquad ("
            + str(
              number
            )
            + ")"
          ),
          r"\]",
        )
      )
      continue

    isomorphism = isomorphism_by_index.get(
      index
    )

    if isomorphism is not None:
      (
        injective_number,
        surjective_number,
        isomorphism_line,
      ) = isomorphism
      output_lines.append(
        (
          "("
          + str(
            injective_number
          )
          + "), ("
          + str(
            surjective_number
          )
          + ") より, "
          + isomorphism_line
        )
      )
      continue

    output_lines.append(
      line
    )

  compacted = []
  previous_blank = False

  for line in output_lines:
    is_blank = not line.strip()

    if (
      is_blank
      and previous_blank
    ):
      continue

    compacted.append(
      line
    )
    previous_blank = is_blank

  return (
    prefix
    + "\n".join(
      compacted
    )
    + (
      "\n"
      if rendered.endswith(
        "\n"
      )
      else ""
    )
  )

```

# 変更テスト関数全体

```python
def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  injective = (
    "完全性より,\n\n"
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
  )
  surjective = (
    "完全性より,\n\n"
    "\\[\n"
    r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
  )
  isomorphism = (
    r"(1), (2) より, "
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
  )

  assert injective in rendered
  assert surjective in rendered
  assert isomorphism in rendered

  assert rendered.index(
    injective
  ) < rendered.index(
    surjective
  ) < rendered.index(
    isomorphism
  )

  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{1}$ は単射."
    not in rendered
  )
  assert (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}\tag{2}$ は全射."
    not in rendered
  )

```

```python
def test_phase159_r1_7c_r4_numbered_reasoning_requires_semantic_presentation():
  from toda_group_proof_narrative_renderer import (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
  )

  rendered = (
    "# Group proof narrative\n\n"
    "## 証明対象\n\n"
    "target\n\n"
    "## 使用する結果\n\n"
    "---\n\n"
    "## 証明\n\n"
    "完全性より, $F: A \\to B$ は単射.\n"
    "完全性より, $F: A \\to B$ は全射.\n"
    "$F: A \\to B$ は同型写像である.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  assert normalized == rendered

```

# 新規テストファイル全文

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_group_map_name,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
  _phase159_recursive_map_property_triples,
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
  TodaGroupProofNarrativeReasonKind,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _presentation(
  n: int,
  k: int,
):
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

  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_repair25_pi3_2_exactness_reason_uses_semantic_map_name():
  presentation = _presentation(
    2,
    1,
  )
  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      semantic_presentation
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      semantic_presentation,
      semantic_sidecar,
    )
  )

  hopf_exactness_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
      and _generic_group_map_name(
        getattr(
          reason.conclusion_step.conclusion,
          "map",
          None,
        )
      )
      == "H"
    )
  )

  assert len(
    hopf_exactness_reasons
  ) == 2


def test_phase159_repair25_pi11_6_recursive_semantic_triple_exists():
  presentation = _presentation(
    6,
    5,
  )
  triples = (
    _phase159_recursive_map_property_triples(
      presentation
    )
  )

  hopf_triples = tuple(
    triple
    for triple in triples
    if (
      _generic_group_map_name(
        getattr(
          triple[
            2
          ].conclusion,
          "map",
          None,
        )
      )
      == "H"
      and getattr(
        getattr(
          triple[
            2
          ].conclusion,
          "map",
          None,
        ),
        "source_group",
        None,
      )
      is not None
    )
  )

  assert hopf_triples


def test_phase159_repair25_pi11_6_keeps_numbered_reasoning_without_prose_matching():
  presentation = _presentation(
    6,
    5,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    "\\[\n"
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は単射}. \qquad (1)"
    "\n\\]"
    in rendered
  )
  assert (
    "\\[\n"
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は全射}. \qquad (2)"
    "\n\\]"
    in rendered
  )
  assert (
    r"(1), (2) より, "
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型."
    in rendered
  )


def test_phase159_repair25_text_only_helper_still_refuses_semantic_inference():
  rendered = (
    "# Group proof narrative\n\n"
    "## 証明\n\n"
    "$F: A \\to B$ は単射.\n"
    "$F: A \\to B$ は全射.\n"
    "$F: A \\to B$ は同型.\n\n"
    "□\n"
  )

  normalized = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered
    )
  )

  assert normalized == rendered

```

# 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py" `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
```

全体 pytest は実行しない。

# 完了条件

- pi_3^2 の H 単射・全射に `完全性より,` が typed reason 由来で付く。
- pi_3^2 の numbered display `(1),(2)` が維持される。
- pi_11^6 の深い ancestry にある H triple も typed statement + group_map で番号付けされる。
- presentation 無しの arbitrary prose から semantic reasoning を作らない。
- focused pytest が PASS する。
- runner が pytest failure を無視して先へ進まない。

# 次 Phase との境界

今回扱うのは Phase 159 final public numbered map-property reasoning の
recursive ancestry 対応まで。

以下は行わない。

- semantic closure builder 自体の一般的な depth policy 変更
- reason model の再設計
- Reference selection 変更
- 他 normalizer の全面的 semantic 化
- repository-wide refactor
