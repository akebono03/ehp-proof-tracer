Phase 154-R2 Fix2 — Semantic sentence composition

前提
----
Phase 154-R2 初版および Fixed1 が適用済みであること。

変更対象
--------
1. toda_group_proof_generic_narrative_renderer.py
   - import
   - _render_generic_narrative_statement_prose()
2. toda_group_proof_narrative_renderer.py
   - _append_narrative_for_step()
   - render_toda_group_proof_narrative_markdown()
3. tests/test_phase154_r2_fix2_semantic_sentence_composition.py
   - 新規追加

今回の変更
----------
1. Toda56Nu4DecompositionIsomorphismStatement に semantic prose を追加する。
2. 末尾が "." または "。" の semantic prose は完成文として扱い、
   "を用いる。" や "を得る。" を二重付加しない。
3. legacy public Narrative の先頭に source_entry.theorem を直接表示しない。
4. Reference section と proof body はそのまま維持する。

今回触れないもの
----------------
- semantic duplication
- transition repetition
- Reference の役割接続
- punctuation normalization
- Test Suite Consolidation

変更後 import 全文
------------------
from expression import (
  Composition,
  HomotopyElement,
)
from homotopy_groups import (
  DirectSumGroup,
  TodaDeltaMap,
  TodaHopfInvariantMap,
  TodaIteratedSuspensionMap,
  TodaPrimaryGroup,
  TodaSuspensionMap,
)
from proof import (
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from repository_element_presentation import (
  render_repository_conclusion_latex,
)
from toda_group_proof_aggregate_statement_renderer import (
  render_toda_group_proof_aggregate_statement_prose,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
  TodaGroupProofNarrativeMathematicalBlockRole,
)
from toda_group_proof_narrative_provenance_catalog import (
  is_toda_group_proof_narrative_provenance_only_statement,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeSemanticSidecar,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
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
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  Toda56Nu4DecompositionStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaNuFamilyDefinitionStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp42ExactnessStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionSurjectiveStatement,
)


変更後 _render_generic_narrative_statement_prose() 全文
-----------------------------------------------------
def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  reference_prose = (
    _render_phase153_r3_9_reference_statement_prose(
      statement
    )
  )

  if reference_prose is not None:
    return reference_prose

  reference_prose = (
    _render_phase153_r3_6_reference_statement_prose(
      statement
    )
  )

  if reference_prose is not None:
    return reference_prose

  aggregate_prose = (
    render_toda_group_proof_aggregate_statement_prose(
      statement
    )
  )

  if aggregate_prose is not None:
    return aggregate_prose

  if isinstance(
    statement,
    Toda56Nu4DecompositionStatement,
  ):
    return (
      r"$\nu_{4}$ の分解を用いる."
    )

  if isinstance(
    statement,
    Toda56Nu4DecompositionIsomorphismStatement,
  ):
    return (
      r"$\nu_{4}$ の分解写像は同型写像である."
    )

  if isinstance(
    statement,
    TodaProp42ExactnessStatement,
  ):
    window = statement.window
    return (
      "$"
      + render_toda_primary_group_latex(
        window.source_term
      )
      + r" \xrightarrow{"
      + window.first_map.name
      + r"} "
      + render_toda_primary_group_latex(
        window.middle_term
      )
      + r" \xrightarrow{"
      + window.second_map.name
      + r"} "
      + render_toda_primary_group_latex(
        window.target_term
      )
      + "$ は完全である."
    )

  if isinstance(
    statement,
    _GENERIC_INJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は単射である."
    )

  if isinstance(
    statement,
    _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は全射である."
    )

  if isinstance(
    statement,
    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は同型写像である."
    )

  if isinstance(
    statement,
    _GENERIC_ZERO_MAP_STATEMENT_TYPES,
  ):
    map_latex = (
      _render_generic_narrative_group_map_latex(
        statement.map
      )
    )

    if map_latex is None:
      return None

    return (
      "$"
      + map_latex
      + "$ は零写像である."
    )

  if isinstance(
    statement,
    TodaNuFamilyDefinitionStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.element
      )
      + r"$ を \(\nu\)-family の元として定める."
    )

  if isinstance(
    statement,
    TodaSigmaFamilyDefinitionStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.element
      )
      + r"$ を \(\sigma\)-family の元として定める."
    )

  return None


変更後 _append_narrative_for_step() 全文
---------------------------------------
def _append_narrative_for_step(
  lines: list[str],
  presentation: TodaGroupProofPresentation,
  parent_step: ProofStep,
  active_step_ids: set[int],
  expanded_step_ids: set[int],
  reference_marker_by_step_id: dict[int, str] | None = None,
  reference_reuse_marker_by_step_id: dict[int, str] | None = None,
) -> None:
  parent_id = id(
    parent_step
  )

  if parent_id in active_step_ids:
    return

  active_step_ids.add(
    parent_id
  )

  edges = (
    _narrative_edges_for_parent(
      presentation,
      parent_step,
    )
  )

  for index, edge in enumerate(
    edges
  ):
    premise_step = edge.premise_step
    premise_id = id(
      premise_step
    )
    premise_fact = (
      _render_group_proof_narrative_fact(
        premise_step
      )
    )
    premise_reference_marker = (
      None
      if (
        reference_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
    premise_reference_reuse_marker = (
      None
      if (
        reference_reuse_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_reuse_marker_by_step_id.get(
        premise_id
      )
    )
    lead = (
      _premise_lead(
        index,
        len(
          edges
        ),
      )
    )

    if premise_id in expanded_step_ids:
      if parent_step is presentation.root_step:
        lines.append(
          (
            lead
            + "、すでに得た"
            + premise_fact
            + "を用いる。"
          )
        )
      continue

    premise_edges = (
      _narrative_edges_for_parent(
        presentation,
        premise_step,
      )
    )

    if (
      premise_edges
      and premise_reference_reuse_marker is not None
    ):
      lines.append(
        (
          lead
          + "、"
          + premise_reference_reuse_marker
          + "を用いる。"
        )
      )
    elif premise_edges:
      _append_narrative_for_step(
        lines,
        presentation,
        premise_step,
        active_step_ids,
        expanded_step_ids,
        reference_marker_by_step_id,
        reference_reuse_marker_by_step_id,
      )

      generic_premise_fact = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      if (
        generic_premise_fact.endswith(".")
        or generic_premise_fact.endswith("。")
      ):
        lines.append(
          (
            _derivation_lead(
              len(
                premise_edges
              )
            )
            + "、"
            + generic_premise_fact
          )
        )
      else:
        lines.append(
          (
            _derivation_lead(
              len(
                premise_edges
              )
            )
            + "、"
            + premise_fact
            + "を得る。"
          )
        )
    else:
      generic_premise_fact = (
        _render_generic_narrative_step(
          premise_step
        )
      )
      inference_rule = (
        premise_step.inference_rule
      )
      generic_fact_is_fallback = (
        (
          inference_rule is not None
          and generic_premise_fact == inference_rule.name
        )
        or generic_premise_fact
        == (
          "`"
          + type(
            premise_step.conclusion
          ).__name__
          + "`"
        )
        or generic_premise_fact == repr(
          premise_step.conclusion
        )
        or generic_premise_fact == str(
          premise_step.conclusion
        )
      )
      reference_plus_semantic_fact = (
        premise_reference_marker is not None
        and not (
          is_toda_group_proof_narrative_provenance_only_statement(
            premise_step.conclusion
          )
        )
        and not generic_fact_is_fallback
      )

      if reference_plus_semantic_fact:
        if (
          generic_premise_fact.startswith("$")
          and generic_premise_fact.endswith("$")
        ):
          lines.append(
            (
              lead
              + "、"
              + premise_reference_marker
              + " により、"
              + generic_premise_fact
              + "を得る。"
            )
          )
        else:
          lines.append(
            (
              lead
              + "、"
              + premise_reference_marker
              + " により、"
              + generic_premise_fact
            )
          )
      elif (
        not generic_fact_is_fallback
        and (
          generic_premise_fact.endswith(".")
          or generic_premise_fact.endswith("。")
        )
      ):
        lines.append(
          (
            lead
            + "、"
            + generic_premise_fact
          )
        )
      else:
        lines.append(
          (
            lead
            + "、"
            + (
              premise_reference_marker
              if premise_reference_marker is not None
              else premise_fact
            )
            + "を用いる。"
          )
        )

    expanded_step_ids.add(
      premise_id
    )

  active_step_ids.remove(
    parent_id
  )


変更後 render_toda_group_proof_narrative_markdown() 全文
--------------------------------------------------------
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


新規テスト全文
--------------
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


def test_phase154_r2_fix2_pi11_4_semantic_sentences_are_not_double_wrapped():
  rendered = _render_group(
    4,
    7,
  )

  assert "である.を用いる。" not in rendered
  assert (
    r"まず、$H: \pi_{10}^{3} \to \pi_{10}^{5}$ "
    r"は単射である."
    in rendered
  )
  assert (
    r"また、$\Delta: \pi_{10}^{5} \to \pi_{8}^{2}$ "
    r"は単射である."
    in rendered
  )
  assert (
    r"さらに、$\pi_{10}^{3} \xrightarrow{H} "
    r"\pi_{10}^{5} \xrightarrow{Δ} \pi_{8}^{2}$ "
    r"は完全である."
    in rendered
  )


def test_phase154_r2_fix2_pi11_4_does_not_expose_root_source_metadata():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    "Toda Proposition 5.15を用いる。"
    not in rendered
  )
  assert "# Group proof narrative" in rendered
  assert "## 使用する結果" in rendered
  assert "## 証明" in rendered


def test_phase154_r2_fix2_pi11_4_renders_nu4_decomposition_isomorphism_semantically():
  rendered = _render_group(
    4,
    7,
  )

  assert (
    "Toda (5.6) の ν₄ 分解同型"
    not in rendered
  )
  assert (
    r"$\nu_{4}$ の分解写像は同型写像である."
    in rendered
  )
  assert r"\pi_{11}^{4} = 0" in rendered


def test_phase154_r2_fix2_keeps_pi10_4_fixed1_result():
  rendered = _render_group(
    4,
    6,
  )

  assert (
    "Toda (5.6) nu_4 decomposition integration"
    not in rendered
  )
  assert (
    r"$\nu_{4}$ の分解を用いる."
    in rendered
  )
  assert (
    r"\pi_{10}^{4} = \mathbb{Z}/8\{\nu_{4}\nu_{7}\}"
    in rendered
  )


実行する pytest
---------------
- tests/test_phase154_r2_internal_prose_fallback_leakage.py
- tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py
- tests/test_phase154_r2_fix2_semantic_sentence_composition.py
- tests/test_phase143_50_generic_statement_prose_renderer.py
- tests/test_phase143_51a_r_provenance_semantic_catalog.py
- tests/test_phase153_r8_reference_use_prose_normalization.py

全体テストは実行しない。

完了条件
--------
1. pi_11^4 から "Toda Proposition 5.15を用いる。" が消える。
2. pi_11^4 から "である.を用いる。" が消える。
3. pi_11^4 の injective / exactness は日本語 semantic prose の完成文として表示される。
4. "Toda (5.6) の ν₄ 分解同型" が semantic prose に置換される。
5. pi_10^4 Fixed1 の修正を維持する。
6. 最終群結論を維持する。
7. focused tests が PASS する。

次 Phase との境界
-----------------
Fix2 が通れば Phase 154-R2 を完了候補とし、R3 で代表群を同条件に再監査する。
