from pathlib import Path
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent

GENERIC_PATH = (
    REPO_ROOT
    / "toda_group_proof_generic_narrative_renderer.py"
)
NARRATIVE_PATH = (
    REPO_ROOT
    / "toda_group_proof_narrative_renderer.py"
)
BACKUP_DIR = (
    REPO_ROOT
    / "phase154_r2_internal_prose_fallback_leakage_fix2"
    / "backup_before_fix2"
)

GENERIC_IMPORTS = 'from expression import (\n  Composition,\n  HomotopyElement,\n)\nfrom homotopy_groups import (\n  DirectSumGroup,\n  TodaDeltaMap,\n  TodaHopfInvariantMap,\n  TodaIteratedSuspensionMap,\n  TodaPrimaryGroup,\n  TodaSuspensionMap,\n)\nfrom proof import (\n  ProofStep,\n)\nfrom scalar_rules import (\n  ScalarGreaterEqualStatement,\n)\nfrom repository_element_presentation import (\n  render_repository_conclusion_latex,\n)\nfrom toda_group_proof_aggregate_statement_renderer import (\n  render_toda_group_proof_aggregate_statement_prose,\n)\nfrom toda_group_proof_narrative_blocks import (\n  TodaGroupProofNarrativeBlock,\n  TodaGroupProofNarrativeMathematicalBlockRole,\n)\nfrom toda_group_proof_narrative_provenance_catalog import (\n  is_toda_group_proof_narrative_provenance_only_statement,\n)\nfrom toda_group_proof_narrative_semantics import (\n  TodaGroupProofNarrativeSemanticSidecar,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_presentation import (\n  TodaGroupProofPresentation,\n)\nfrom toda_human_readable_renderer import (\n  _render_scalar_latex,\n  render_toda_expression_latex,\n)\nfrom toda_proof_narrative_renderer import (\n  render_toda_primary_group_latex,\n  render_toda_proof_statement_latex,\n  render_toda_raw_group_structure_latex,\n)\nfrom toda_rules import (\n  Toda36Lemma514SigmaDoublePrimeBridgeStatement,\n  Toda45IsomorphismStatement,\n  Toda52CompositionIsomorphismStatement,\n  Toda53NuPrimeBracketSpecializationStatement,\n  Toda55NuFamilyFiniteDimensionalStatement,\n  Toda56Nu4DecompositionIsomorphismStatement,\n  Toda56Nu4DecompositionStatement,\n  TodaDeltaInjectiveStatement,\n  TodaDeltaKernelFreeCyclicStatement,\n  TodaDeltaSurjectiveStatement,\n  TodaDeltaZeroStatement,\n  TodaHopfInvariantInjectiveStatement,\n  TodaHopfInvariantIsomorphismStatement,\n  TodaHopfInvariantSurjectiveStatement,\n  TodaHopfInvariantZeroStatement,\n  TodaIteratedSuspensionInjectiveStatement,\n  TodaLemma513Statement,\n  TodaLemma514Sigma8Statement,\n  TodaLemma514SigmaPrimeStatement,\n  TodaLemma54Statement,\n  TodaNuFamilyDefinitionStatement,\n  TodaProp27HopfInvariantUpToSignStatement,\n  TodaProp42ExactnessStatement,\n  TodaProp44IsomorphismStatement,\n  TodaProp44SecondSummandRestrictionStatement,\n  TodaProp44SuspensionInjectiveStatement,\n  TodaProp51FiniteDimensionalStatement,\n  TodaProp53FiniteDimensionalStatement,\n  TodaProp58FiniteDimensionalStatement,\n  TodaProp59FiniteDimensionalStatement,\n  TodaProp511FiniteDimensionalStatement,\n  TodaProp511NuSquaredFiniteDimensionalStatement,\n  TodaProp515Pi12_5HopfIsomorphismStatement,\n  TodaProp56FiniteDimensionalStatement,\n  TodaSigmaFamilyDefinitionStatement,\n  TodaSuspensionInjectiveStatement,\n  TodaSuspensionIsomorphismStatement,\n  TodaSuspensionSurjectiveStatement,\n)\n'
GENERIC_FUNCTION = 'def _render_generic_narrative_statement_prose(\n  statement,\n) -> str | None:\n  reference_prose = (\n    _render_phase153_r3_9_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n\n  reference_prose = (\n    _render_phase153_r3_6_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n\n  aggregate_prose = (\n    render_toda_group_proof_aggregate_statement_prose(\n      statement\n    )\n  )\n\n  if aggregate_prose is not None:\n    return aggregate_prose\n\n  if isinstance(\n    statement,\n    Toda56Nu4DecompositionStatement,\n  ):\n    return (\n      r"$\\nu_{4}$ の分解を用いる."\n    )\n\n  if isinstance(\n    statement,\n    Toda56Nu4DecompositionIsomorphismStatement,\n  ):\n    return (\n      r"$\\nu_{4}$ の分解写像は同型写像である."\n    )\n\n  if isinstance(\n    statement,\n    TodaProp42ExactnessStatement,\n  ):\n    window = statement.window\n    return (\n      "$"\n      + render_toda_primary_group_latex(\n        window.source_term\n      )\n      + r" \\xrightarrow{"\n      + window.first_map.name\n      + r"} "\n      + render_toda_primary_group_latex(\n        window.middle_term\n      )\n      + r" \\xrightarrow{"\n      + window.second_map.name\n      + r"} "\n      + render_toda_primary_group_latex(\n        window.target_term\n      )\n      + "$ は完全である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_INJECTIVE_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は単射である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_SURJECTIVE_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は全射である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_ISOMORPHISM_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は同型写像である."\n    )\n\n  if isinstance(\n    statement,\n    _GENERIC_ZERO_MAP_STATEMENT_TYPES,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      "$"\n      + map_latex\n      + "$ は零写像である."\n    )\n\n  if isinstance(\n    statement,\n    TodaNuFamilyDefinitionStatement,\n  ):\n    return (\n      "$"\n      + render_toda_expression_latex(\n        statement.element\n      )\n      + r"$ を \\(\\nu\\)-family の元として定める."\n    )\n\n  if isinstance(\n    statement,\n    TodaSigmaFamilyDefinitionStatement,\n  ):\n    return (\n      "$"\n      + render_toda_expression_latex(\n        statement.element\n      )\n      + r"$ を \\(\\sigma\\)-family の元として定める."\n    )\n\n  return None\n'
APPEND_FUNCTION = 'def _append_narrative_for_step(\n  lines: list[str],\n  presentation: TodaGroupProofPresentation,\n  parent_step: ProofStep,\n  active_step_ids: set[int],\n  expanded_step_ids: set[int],\n  reference_marker_by_step_id: dict[int, str] | None = None,\n  reference_reuse_marker_by_step_id: dict[int, str] | None = None,\n) -> None:\n  parent_id = id(\n    parent_step\n  )\n\n  if parent_id in active_step_ids:\n    return\n\n  active_step_ids.add(\n    parent_id\n  )\n\n  edges = (\n    _narrative_edges_for_parent(\n      presentation,\n      parent_step,\n    )\n  )\n\n  for index, edge in enumerate(\n    edges\n  ):\n    premise_step = edge.premise_step\n    premise_id = id(\n      premise_step\n    )\n    premise_fact = (\n      _render_group_proof_narrative_fact(\n        premise_step\n      )\n    )\n    premise_reference_marker = (\n      None\n      if (\n        reference_marker_by_step_id is None\n        or isinstance(\n          premise_step.conclusion,\n          TodaProp42ExactnessStatement,\n        )\n      )\n      else reference_marker_by_step_id.get(\n        premise_id\n      )\n    )\n    premise_reference_reuse_marker = (\n      None\n      if (\n        reference_reuse_marker_by_step_id is None\n        or isinstance(\n          premise_step.conclusion,\n          TodaProp42ExactnessStatement,\n        )\n      )\n      else reference_reuse_marker_by_step_id.get(\n        premise_id\n      )\n    )\n    lead = (\n      _premise_lead(\n        index,\n        len(\n          edges\n        ),\n      )\n    )\n\n    if premise_id in expanded_step_ids:\n      if parent_step is presentation.root_step:\n        lines.append(\n          (\n            lead\n            + "、すでに得た"\n            + premise_fact\n            + "を用いる。"\n          )\n        )\n      continue\n\n    premise_edges = (\n      _narrative_edges_for_parent(\n        presentation,\n        premise_step,\n      )\n    )\n\n    if (\n      premise_edges\n      and premise_reference_reuse_marker is not None\n    ):\n      lines.append(\n        (\n          lead\n          + "、"\n          + premise_reference_reuse_marker\n          + "を用いる。"\n        )\n      )\n    elif premise_edges:\n      _append_narrative_for_step(\n        lines,\n        presentation,\n        premise_step,\n        active_step_ids,\n        expanded_step_ids,\n        reference_marker_by_step_id,\n        reference_reuse_marker_by_step_id,\n      )\n\n      generic_premise_fact = (\n        _render_generic_narrative_step(\n          premise_step\n        )\n      )\n      if (\n        generic_premise_fact.endswith(".")\n        or generic_premise_fact.endswith("。")\n      ):\n        lines.append(\n          (\n            _derivation_lead(\n              len(\n                premise_edges\n              )\n            )\n            + "、"\n            + generic_premise_fact\n          )\n        )\n      else:\n        lines.append(\n          (\n            _derivation_lead(\n              len(\n                premise_edges\n              )\n            )\n            + "、"\n            + premise_fact\n            + "を得る。"\n          )\n        )\n    else:\n      generic_premise_fact = (\n        _render_generic_narrative_step(\n          premise_step\n        )\n      )\n      inference_rule = (\n        premise_step.inference_rule\n      )\n      generic_fact_is_fallback = (\n        (\n          inference_rule is not None\n          and generic_premise_fact == inference_rule.name\n        )\n        or generic_premise_fact\n        == (\n          "`"\n          + type(\n            premise_step.conclusion\n          ).__name__\n          + "`"\n        )\n        or generic_premise_fact == repr(\n          premise_step.conclusion\n        )\n        or generic_premise_fact == str(\n          premise_step.conclusion\n        )\n      )\n      reference_plus_semantic_fact = (\n        premise_reference_marker is not None\n        and not (\n          is_toda_group_proof_narrative_provenance_only_statement(\n            premise_step.conclusion\n          )\n        )\n        and not generic_fact_is_fallback\n      )\n\n      if reference_plus_semantic_fact:\n        if (\n          generic_premise_fact.startswith("$")\n          and generic_premise_fact.endswith("$")\n        ):\n          lines.append(\n            (\n              lead\n              + "、"\n              + premise_reference_marker\n              + " により、"\n              + generic_premise_fact\n              + "を得る。"\n            )\n          )\n        else:\n          lines.append(\n            (\n              lead\n              + "、"\n              + premise_reference_marker\n              + " により、"\n              + generic_premise_fact\n            )\n          )\n      elif (\n        not generic_fact_is_fallback\n        and (\n          generic_premise_fact.endswith(".")\n          or generic_premise_fact.endswith("。")\n        )\n      ):\n        lines.append(\n          (\n            lead\n            + "、"\n            + generic_premise_fact\n          )\n        )\n      else:\n        lines.append(\n          (\n            lead\n            + "、"\n            + (\n              premise_reference_marker\n              if premise_reference_marker is not None\n              else premise_fact\n            )\n            + "を用いる。"\n          )\n        )\n\n    expanded_step_ids.add(\n      premise_id\n    )\n\n  active_step_ids.remove(\n    parent_id\n  )\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  phase134_24_pi15_8 = (\n    _phase134_24_render_pi15_8_narrative(\n      presentation\n    )\n  )\n\n  if phase134_24_pi15_8 is not None:\n    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        phase134_24_pi15_8,\n      )\n    )\n\n  if (\n    _is_phase134_3_pi6_3_presentation(\n      presentation\n    )\n    or _is_phase150_rc4_generic_route_target(\n      presentation\n    )\n  ):\n    semantic_sidecar = (\n      build_toda_group_proof_narrative_semantic_sidecar(\n        presentation\n      )\n    )\n    blocks = (\n      build_toda_group_proof_narrative_blocks(\n        presentation,\n        semantic_sidecar=semantic_sidecar,\n      )\n    )\n    arguments = (\n      build_toda_group_proof_narrative_arguments(\n        presentation,\n        blocks,\n        semantic_sidecar=semantic_sidecar,\n      )\n    )\n\n    rendered = (\n      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n        presentation,\n        blocks,\n        semantic_sidecar,\n        arguments,\n      )\n    )\n\n    if _is_phase150_rc4_generic_route_target(\n      presentation\n    ):\n      return _wrap_phase150_rc4_generic_public_narrative(\n        presentation,\n        rendered,\n      )\n\n    return rendered\n\n  if _is_phase134_9_pi8_5_presentation(\n    presentation\n  ):\n    rendered = (\n      _render_phase134_9_pi8_5_narrative_markdown(\n        presentation\n      )\n    )\n\n    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        rendered,\n      )\n    )\n\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n    if presentation.max_depth >= 2\n    else ()\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n    if reference_entries\n    else {}\n  )\n  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n  reference_marker_by_step_id = {\n    id(proof_step): f"[R{entry.number}]"\n    for entry in reference_entries\n    for proof_step in entry.proof_steps\n  }\n  reference_reuse_marker_by_step_id = (\n    build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  lines = [\n    "# Group proof narrative",\n    "",\n  ]\n\n  if reference_section:\n    lines.extend(\n      (\n        "## 使用する結果",\n        "",\n        reference_section,\n        "",\n        "## 証明",\n        "",\n      )\n    )\n\n  root_edges = (\n    _narrative_edges_for_parent(\n      presentation,\n      presentation.root_step,\n    )\n  )\n\n  if root_edges:\n    target = (\n      presentation\n      .source_replay\n      .group_result\n      .target\n    )\n\n    if (\n      target.group_dimension == 16\n      and target.sphere_dimension == 9\n    ):\n      lines.extend(\n        (\n          (\n            "$\\\\sigma_{9}$ の位数を確認し、"\n            "これが $\\\\pi_{16}^{9}$ を生成することを示す。"\n          ),\n          "",\n        )\n      )\n\n    _append_narrative_for_step(\n      lines,\n      presentation,\n      presentation.root_step,\n      set(),\n      set(),\n      reference_marker_by_step_id,\n      reference_reuse_marker_by_step_id,\n    )\n\n    lines.extend(\n      (\n        "",\n        (\n          "したがって、"\n          + _render_group_proof_narrative_fact(\n            presentation.root_step\n          )\n          + "を得る。"\n        ),\n      )\n    )\n  else:\n    lines.append(\n      (\n        "したがって、"\n        + _render_group_proof_narrative_fact(\n          presentation.root_step\n        )\n        + "である。"\n      )\n    )\n\n  rendered = (\n    "\\n".join(\n      lines\n    )\n    + "\\n"\n  )\n\n  if reference_section:\n    proof_section_marker = "## 証明\\n\\n"\n    proof_section_index = rendered.find(\n      proof_section_marker\n    )\n\n    if proof_section_index >= 0:\n      body_start = (\n        proof_section_index\n        + len(\n          proof_section_marker\n        )\n      )\n      body = rendered[\n        body_start:\n      ]\n      suppressed_body = (\n        suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(\n          presentation,\n          body,\n          reference_entries,\n        )\n      )\n      suppressed_body = (\n        suppress_toda_group_proof_narrative_reference_body_duplicates(\n          suppressed_body,\n          statement_lines_by_reference_number,\n        )\n      )\n      (\n        filtered_reference_entries,\n        filtered_statement_lines,\n        suppressed_body,\n      ) = (\n        filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n          reference_entries,\n          statement_lines_by_reference_number,\n          suppressed_body,\n        )\n      )\n      filtered_reference_section = (\n        render_toda_group_proof_narrative_reference_entries_markdown(\n          filtered_reference_entries,\n          filtered_statement_lines,\n        )\n      )\n      prefix_lines = [\n        "# Group proof narrative",\n        "",\n      ]\n\n      if filtered_reference_section:\n        prefix_lines.extend(\n          (\n            "## 使用する結果",\n            "",\n            filtered_reference_section,\n            "",\n            "## 証明",\n            "",\n          )\n        )\n\n      rendered = (\n        "\\n".join(\n          prefix_lines\n        )\n        + "\\n"\n        + suppressed_body\n        + "\\n"\n      )\n\n  return rendered\n'


def replace_imports(
  source: str,
  imports: str,
) -> str:
    marker = "_BLOCK_ROLE_LABELS = {"
    index = source.find(
        marker
    )

    if index < 0:
        raise RuntimeError(
            "generic import boundary marker not found"
        )

    return (
        imports.rstrip()
        + "\n\n\n"
        + source[
            index:
        ]
    )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
    marker = (
        "def "
        + name
        + "("
    )
    start = source.find(
        marker
    )

    if start < 0:
        raise RuntimeError(
            "function not found: "
            + name
        )

    next_def = source.find(
        "\ndef ",
        start + len(
            marker
        ),
    )

    if next_def < 0:
        suffix = ""
    else:
        suffix = source[
            next_def + 1:
        ]

    return (
        source[
            :start
        ]
        + replacement.rstrip()
        + "\n\n"
        + suffix
    )


def backup(
  path: Path,
) -> None:
    target = (
        BACKUP_DIR
        / path.name
    )
    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    shutil.copy2(
        path,
        target,
    )


def main() -> int:
    for path in (
        GENERIC_PATH,
        NARRATIVE_PATH,
    ):
        if not path.exists():
            raise RuntimeError(
                "missing production file: "
                + str(
                    path
                )
            )
        backup(
            path
        )

    generic_source = GENERIC_PATH.read_text(
        encoding="utf-8",
    )
    generic_source = replace_imports(
        generic_source,
        GENERIC_IMPORTS,
    )
    generic_source = replace_function(
        generic_source,
        "_render_generic_narrative_statement_prose",
        GENERIC_FUNCTION,
    )
    GENERIC_PATH.write_text(
        generic_source,
        encoding="utf-8",
    )

    narrative_source = NARRATIVE_PATH.read_text(
        encoding="utf-8",
    )
    narrative_source = replace_function(
        narrative_source,
        "_append_narrative_for_step",
        APPEND_FUNCTION,
    )
    narrative_source = replace_function(
        narrative_source,
        "render_toda_group_proof_narrative_markdown",
        RENDER_FUNCTION,
    )
    NARRATIVE_PATH.write_text(
        narrative_source,
        encoding="utf-8",
    )

    test_source = (
        Path(__file__).resolve().parent
        / "tests"
        / "test_phase154_r2_fix2_semantic_sentence_composition.py"
    )
    test_target = (
        REPO_ROOT
        / "tests"
        / "test_phase154_r2_fix2_semantic_sentence_composition.py"
    )
    shutil.copy2(
        test_source,
        test_target,
    )

    print(
        "updated:",
        GENERIC_PATH.name,
    )
    print(
        "updated:",
        NARRATIVE_PATH.name,
    )
    print(
        "added:",
        test_target.relative_to(
            REPO_ROOT
        ),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
