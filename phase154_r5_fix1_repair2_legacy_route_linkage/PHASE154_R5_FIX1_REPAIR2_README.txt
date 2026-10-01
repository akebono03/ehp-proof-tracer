Phase 154-R5 Fix1 Repair2 — Legacy public route linkage

原因
----
pi11_4 は generic multi-Argument route を通っていない。

Fix1 / Repair1 では
toda_group_proof_narrative_contribution_renderer.py 内の
render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
で linkage helper を呼んでいたため、pi11_4 では一度も実行されなかった。

診断結果では Proposition 4.4 の graph relation 自体は一意:

  Proposition 4.4
    -> Toda56Nu4DecompositionIsomorphismStatement
    -> pi11_4 = 0

また、legacy route では marker は _append_narrative_for_step() 後に生成される。

Repair2
-------
legacy public route の

  suppress reference-body duplicates
    ↓
  filter references by body usage

の間に

  link_toda_group_proof_narrative_reference_body_consumers()

を追加する。

これにより pre-filter の [R3] Proposition 4.4 が consumer と結合され、
その後の body-usage filtering で public [R2] に再番号付けされる。

変更対象
--------
toda_group_proof_narrative_renderer.py

import 変更
-------------
変更後 import 全文:

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
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
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


変更関数全文
------------
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  phase134_24_pi15_8 = (
    _phase134_24_render_pi15_8_narrative(
      presentation
    )
  )

  if phase134_24_pi15_8 is not None:
    return (
      _phase153_r3_10_connect_public_reference_section(
        presentation,
        phase134_24_pi15_8,
      )
    )

  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
    or _is_phase150_rc4_generic_route_target(
      presentation
    )
  ):
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=semantic_sidecar,
      )
    )

    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

    if _is_phase150_rc4_generic_route_target(
      presentation
    ):
      return _wrap_phase150_rc4_generic_public_narrative(
        presentation,
        rendered,
      )

    return rendered

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    rendered = (
      _render_phase134_9_pi8_5_narrative_markdown(
        presentation
      )
    )

    return (
      _phase153_r3_10_connect_public_reference_section(
        presentation,
        rendered,
      )
    )

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
    if presentation.max_depth >= 2
    else ()
  )
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
    if reference_entries
    else {}
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }
  reference_reuse_marker_by_step_id = (
    build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
      presentation,
      reference_entries,
    )
  )

  lines = [
    "# Group proof narrative",
    "",
  ]

  if reference_section:
    lines.extend(
      (
        "## 使用する結果",
        "",
        reference_section,
        "",
        "## 証明",
        "",
      )
    )

  root_edges = (
    _narrative_edges_for_parent(
      presentation,
      presentation.root_step,
    )
  )

  if root_edges:
    target = (
      presentation
      .source_replay
      .group_result
      .target
    )

    if (
      target.group_dimension == 16
      and target.sphere_dimension == 9
    ):
      lines.extend(
        (
          (
            "$\\sigma_{9}$ の位数を確認し、"
            "これが $\\pi_{16}^{9}$ を生成することを示す。"
          ),
          "",
        )
      )

    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
      reference_marker_by_step_id,
      reference_reuse_marker_by_step_id,
    )

    lines.extend(
      (
        "",
        (
          "したがって、"
          + _render_group_proof_narrative_fact(
            presentation.root_step
          )
          + "を得る。"
        ),
      )
    )
  else:
    lines.append(
      (
        "したがって、"
        + _render_group_proof_narrative_fact(
          presentation.root_step
        )
        + "である。"
      )
    )

  rendered = (
    "\n".join(
      lines
    )
    + "\n"
  )

  if reference_section:
    proof_section_marker = "## 証明\n\n"
    proof_section_index = rendered.find(
      proof_section_marker
    )

    if proof_section_index >= 0:
      body_start = (
        proof_section_index
        + len(
          proof_section_marker
        )
      )
      body = rendered[
        body_start:
      ]
      suppressed_body = (
        suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
          presentation,
          body,
          reference_entries,
        )
      )
      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          suppressed_body,
          statement_lines_by_reference_number,
        )
      )
      suppressed_body = (
        link_toda_group_proof_narrative_reference_body_consumers(
          presentation,
          suppressed_body,
          reference_entries,
        )
      )
      (
        filtered_reference_entries,
        filtered_statement_lines,
        suppressed_body,
      ) = (
        filter_toda_group_proof_narrative_reference_entries_by_body_usage(
          reference_entries,
          statement_lines_by_reference_number,
          suppressed_body,
        )
      )
      filtered_reference_section = (
        render_toda_group_proof_narrative_reference_entries_markdown(
          filtered_reference_entries,
          filtered_statement_lines,
        )
      )
      prefix_lines = [
        "# Group proof narrative",
        "",
      ]

      if filtered_reference_section:
        prefix_lines.extend(
          (
            "## 使用する結果",
            "",
            filtered_reference_section,
            "",
            "## 証明",
            "",
          )
        )

      rendered = (
        "\n".join(
          prefix_lines
        )
        + "\n"
        + suppressed_body
        + "\n"
      )

  return rendered


新規テスト
----------
tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py

テスト全文
----------
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


def _render_group(
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


def test_phase154_r5_fix1_repair2_pi11_4_links_reference_after_marker_generation():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    r"[R2]より、$\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert "まず、[R2]を用いる。" not in rendered
  assert (
    r"このことから、$\nu_{4}$ の分解写像は同型写像である."
    not in rendered
  )


def test_phase154_r5_fix1_repair2_reference_filtering_renumbers_linked_marker():
  rendered = _render_group(
    4,
    7,
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "**[R2] Proposition 4.4.**" in rendered
  assert "**[R3]" not in rendered
  assert "[R3]より、" not in rendered


def test_phase154_r5_fix1_repair2_keeps_root_only_reference_neutral():
  rendered = _render_group(
    4,
    7,
  )

  assert "[R1]を用いる。" in rendered
  assert r"[R1]より、$\pi_{11}^{4} = 0" not in rendered


def test_phase154_r5_fix1_repair2_keeps_consumer_once_and_final_conclusion():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    rendered.count(
      r"$\nu_{4}$ の分解写像は同型写像である."
    )
    == 1
  )
  assert r"\pi_{11}^{4} = 0" in rendered


完了条件
--------
1. pi11_4 で `[R2]より、$\nu_{4}$ の分解写像は同型写像である.` が出る。
2. `まず、[R2]を用いる。` が消える。
3. Proposition 4.4 は public [R2] のまま。
4. [R3] は public output に残らない。
5. consumer fact は1回のみ。
6. [R1] root-only linkage は中立のまま。
7. final conclusion を維持。
8. focused tests PASS。

全体テスト
----------
実行しない。Phase 154 最後まで保留。

次の境界
--------
Repair2 が PASS したら R5 の代表群再監査を行い、
Reference linkage の残存がなければ R5 完了、R6 punctuation normalization へ進む。
