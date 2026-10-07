# 変更対象

## production

`toda_group_proof_narrative_renderer.py`

変更対象:

- import 部分
- `_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning()`
- `render_toda_group_proof_narrative_markdown()`

既存の次の semantic helper は変更せず再利用する:

- `_phase159_public_semantic_projection_context()`
- `_phase159_matching_map_property_step()`
- `_phase159_public_map_property_triples()`
- `_phase159_plain_map_property_line()`

## test

新規:

`tests/test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair24.py`

# 修正方針

semantic comparison（意味比較）を先に行う。

- injective / surjective / isomorphism の対応は statement type と同一 `group_map` object で決める。
- exactness（完全性）由来かどうかは `EXACTNESS_TO_MAP_PROPERTY` typed reason で決める。
- `" は単射."` や `" は全射."` を辞書キーにして map の意味を再推測しない。
- 文字列は semantic に決まった statement の表示位置を見つけるためだけに使う。
- `完全性より,` は prose の保存・復元ではなく typed provenance から生成する。

# import の変更

変更後の import 部分全文:

```python
import re
from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from homotopy_groups import (
  HomotopyEHPExactnessWindow,
  HomotopyGroup,
  TodaDeltaMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaPrimaryGroupMembershipStatement,
  TodaProp44DecompositionMap,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionMap,
)
from proof import (
  ProofStep,
  Relation,
  RelationType,
  FoundationalReferenceIdentity,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
  _GENERIC_INJECTIVE_STATEMENT_TYPES,
  _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  _render_generic_narrative_group_map_latex,
  _generic_group_map_name,
  _GENERIC_ZERO_MAP_STATEMENT_TYPES,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  build_toda_group_proof_narrative_reference_reuse_marker_by_step_id,
  link_toda_group_proof_narrative_reference_body_consumers,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
  suppress_toda_group_proof_narrative_reference_body_restatements,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_component_latex,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
  TodaGroupProofNarrativeReasonKind,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
  TodaGroupProofNarrativeDependencySemanticRole,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_helpers import (
  root_generator,
  root_target_group,
)
from toda_group_proof_narrative_classifier import (
  TodaGroupProofNarrativeBlockRole,
  TodaGroupProofNarrativeFactRole,
  classify_toda_group_proof_narrative_step,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
  render_toda_raw_group_structure_latex,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda45IsomorphismStatement,
  Toda48Pi16_9OrderAndE4InjectiveStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  Toda58WhiteheadSquareUpToSignStatement,
  TodaDeltaImageFreeCyclicStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaDeltaZeroStatement,
  TodaEtaFamilyDefinitionStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaPi32Eta2DefinitionStatement,
  TodaPi32WhiteheadSquareUpToSignStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp56Pi8_5QuotientStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionKernelFreeCyclicStatement,
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
  ) in _phase159_public_map_property_triples(
    semantic_presentation
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

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  rendered = (
    _phase158_baseline_render_toda_group_proof_narrative_markdown(
      presentation
    )
  )
  rendered = (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_map_property_prose(
      rendered
    )
  )
  rendered = (
    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(
      rendered,
      presentation=presentation,
    )
  )

  return (
    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(
      rendered
    )
  )

```

# 新規テストファイル全文

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning,
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


def test_phase159_repair24_pi3_2_numbered_hopf_properties_keep_exactness_provenance():
  presentation = _presentation(
    2,
    1,
  )
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


def test_phase159_repair24_pi3_2_exactness_connector_is_backed_by_typed_reason():
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

  exactness_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )

  hopf_reasons = tuple(
    reason
    for reason in exactness_reasons
    if getattr(
      getattr(
        reason.conclusion_step.conclusion,
        "map",
        None,
      ),
      "name",
      None,
    )
    == "H"
  )

  assert len(
    hopf_reasons
  ) >= 2


def test_phase159_repair24_text_only_helper_does_not_infer_semantics_from_prose():
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


def test_phase159_repair24_pi11_6_numbered_hopf_reasoning_still_uses_semantic_pairing():
  presentation = _presentation(
    6,
    5,
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は単射}. \qquad (1)"
    in rendered
  )
  assert (
    r"H: \pi_{7}^{3} \to \pi_{7}^{5}"
    r"\quad\text{は全射}. \qquad (2)"
    in rendered
  )
  assert (
    r"(1), (2) より, "
    r"$H: \pi_{7}^{3} \to \pi_{7}^{5}$ は同型."
    in rendered
  )

```

# 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair24.py" `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py"
```

全体 pytest は Phase 159 の最後まで実行しない。

# 完了条件

- pi_3^2 の H の単射・全射が semantic triple から番号付けされる。
- それぞれが `EXACTNESS_TO_MAP_PROPERTY` 由来なら `完全性より,` が表示される。
- `(1), (2) より, H ... は同型.` が維持される。
- arbitrary prose だけを helper に渡しても map-property reasoning を推測しない。
- focused tests が PASS する。

# 次 Phase との境界

今回扱うのは Phase 159 の final public numbered map-property reasoning のみ。

以下は行わない。

- reason model 自体の再設計
- `ProofStep` のデータ構造変更
- Reference selection の変更
- 他の prose normalizer の全面的 semantic 化
- repository-wide refactor
- Phase 160 以降の機能先取り
