from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = (
  REPO_ROOT
  / "toda_group_proof_narrative_renderer.py"
)
BACKUP = (
  REPO_ROOT
  / "phase154_r5_fix1_repair2_legacy_route_linkage"
  / "backup_before_repair2"
  / TARGET.name
)

IMPORT_BLOCK = 'from barratt_hilton_rules import (\n  HomotopyGroupMembershipStatement,\n)\nfrom homotopy_groups import (\n  HomotopyEHPExactnessWindow,\n  HomotopyGroup,\n  TodaDeltaMap,\n  TodaIteratedSuspensionMap,\n  TodaPrimaryGroup,\n  TodaPrimaryGroupMembershipStatement,\n  TodaProp44DecompositionMap,\n  TodaSuspensionIsomorphismStatement,\n  TodaSuspensionMap,\n)\nfrom proof import (\n  ProofStep,\n  Relation,\n  RelationType,\n)\nfrom scalar_rules import (\n  ScalarGreaterEqualStatement,\n)\nfrom repository_element_presentation import (\n  render_repository_conclusion_latex,\n)\nfrom toda_group_proof_presentation import (\n  TodaGroupProofPresentation,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_arguments import (\n  build_toda_group_proof_narrative_arguments,\n)\nfrom toda_group_proof_narrative_argument_multi_renderer import (\n  render_toda_group_proof_narrative_multi_argument_markdown,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_statement_lines_by_number,\n  build_toda_group_proof_narrative_reference_reuse_marker_by_step_id,\n  link_toda_group_proof_narrative_reference_body_consumers,\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,\n  suppress_toda_group_proof_narrative_reference_body_duplicates,\n)\nfrom toda_group_proof_narrative_blocks import (\n  build_toda_group_proof_narrative_blocks,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n  build_toda_group_proof_narrative_semantic_sidecar,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n  exclude_toda_group_proof_narrative_root_reference,\n  filter_toda_group_proof_narrative_reference_entries_by_body_usage,\n  render_toda_group_proof_narrative_reference_entries_markdown,\n)\nfrom toda_group_proof_narrative_provenance_catalog import (\n  is_toda_group_proof_narrative_provenance_only_statement,\n)\nfrom toda_group_proof_narrative_helpers import (\n  root_generator,\n  root_target_group,\n)\nfrom toda_group_proof_narrative_classifier import (\n  TodaGroupProofNarrativeBlockRole,\n  TodaGroupProofNarrativeFactRole,\n  classify_toda_group_proof_narrative_step,\n)\nfrom toda_human_readable_renderer import (\n  _render_scalar_latex,\n  render_toda_expression_latex,\n)\nfrom toda_proof_narrative_renderer import (\n  render_toda_primary_group_latex,\n  render_toda_proof_statement_latex,\n  render_toda_raw_group_structure_latex,\n)\nfrom toda_rules import (\n  Toda36Lemma514SigmaDoublePrimeBridgeStatement,\n  Toda45IsomorphismStatement,\n  Toda48Pi16_9OrderAndE4InjectiveStatement,\n  Toda52CompositionIsomorphismStatement,\n  Toda53NuPrimeBracketSpecializationStatement,\n  Toda55NuFamilyFiniteDimensionalStatement,\n  Toda56Nu4DecompositionIsomorphismStatement,\n  Toda56Nu4DecompositionStatement,\n  Toda58WhiteheadSquareUpToSignStatement,\n  TodaDeltaImageFreeCyclicStatement,\n  TodaDeltaKernelFreeCyclicStatement,\n  TodaDeltaSurjectiveStatement,\n  TodaDeltaZeroStatement,\n  TodaEtaFamilyDefinitionStatement,\n  TodaHopfInvariantInjectiveStatement,\n  TodaHopfInvariantIsomorphismStatement,\n  TodaHopfInvariantSurjectiveStatement,\n  TodaIteratedSuspensionInjectiveStatement,\n  TodaLemma513Statement,\n  TodaLemma514Sigma8Statement,\n  TodaLemma514SigmaPrimeStatement,\n  TodaLemma54Statement,\n  TodaPi32Eta2DefinitionStatement,\n  TodaPi32WhiteheadSquareUpToSignStatement,\n  TodaProp27HopfInvariantUpToSignStatement,\n  TodaProp42ExactnessStatement,\n  TodaProp44IsomorphismStatement,\n  TodaProp44SecondSummandRestrictionStatement,\n  TodaProp51FiniteDimensionalStatement,\n  TodaProp511FiniteDimensionalStatement,\n  TodaProp515Pi12_5HopfIsomorphismStatement,\n  TodaProp56FiniteDimensionalStatement,\n  TodaProp56Pi8_5QuotientStatement,\n  TodaSigmaFamilyDefinitionStatement,\n  TodaSuspensionInjectiveStatement,\n  TodaSuspensionKernelFreeCyclicStatement,\n)\n'
RENDER_FUNCTION = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  presentation = (\n    build_toda_group_proof_narrative_semantic_closure_presentation(\n      presentation\n    )\n  )\n\n  phase134_24_pi15_8 = (\n    _phase134_24_render_pi15_8_narrative(\n      presentation\n    )\n  )\n\n  if phase134_24_pi15_8 is not None:\n    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        phase134_24_pi15_8,\n      )\n    )\n\n  if (\n    _is_phase134_3_pi6_3_presentation(\n      presentation\n    )\n    or _is_phase150_rc4_generic_route_target(\n      presentation\n    )\n  ):\n    semantic_sidecar = (\n      build_toda_group_proof_narrative_semantic_sidecar(\n        presentation\n      )\n    )\n    blocks = (\n      build_toda_group_proof_narrative_blocks(\n        presentation,\n        semantic_sidecar=semantic_sidecar,\n      )\n    )\n    arguments = (\n      build_toda_group_proof_narrative_arguments(\n        presentation,\n        blocks,\n        semantic_sidecar=semantic_sidecar,\n      )\n    )\n\n    rendered = (\n      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n        presentation,\n        blocks,\n        semantic_sidecar,\n        arguments,\n      )\n    )\n\n    if _is_phase150_rc4_generic_route_target(\n      presentation\n    ):\n      return _wrap_phase150_rc4_generic_public_narrative(\n        presentation,\n        rendered,\n      )\n\n    return rendered\n\n  if _is_phase134_9_pi8_5_presentation(\n    presentation\n  ):\n    rendered = (\n      _render_phase134_9_pi8_5_narrative_markdown(\n        presentation\n      )\n    )\n\n    return (\n      _phase153_r3_10_connect_public_reference_section(\n        presentation,\n        rendered,\n      )\n    )\n\n  reference_entries = (\n    build_toda_group_proof_narrative_reference_entries(\n      presentation\n    )\n    if presentation.max_depth >= 2\n    else ()\n  )\n  statement_lines_by_reference_number = (\n    _toda_group_proof_narrative_reference_statement_lines_by_number(\n      presentation,\n      reference_entries,\n    )\n    if reference_entries\n    else {}\n  )\n  (\n    reference_entries,\n    statement_lines_by_reference_number,\n  ) = (\n    exclude_toda_group_proof_narrative_root_reference(\n      reference_entries,\n      statement_lines_by_reference_number,\n      presentation.root_step,\n    )\n  )\n  reference_section = (\n    render_toda_group_proof_narrative_reference_entries_markdown(\n      reference_entries,\n      statement_lines_by_reference_number,\n    )\n  )\n  reference_marker_by_step_id = {\n    id(proof_step): f"[R{entry.number}]"\n    for entry in reference_entries\n    for proof_step in entry.proof_steps\n  }\n  reference_reuse_marker_by_step_id = (\n    build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(\n      presentation,\n      reference_entries,\n    )\n  )\n\n  lines = [\n    "# Group proof narrative",\n    "",\n  ]\n\n  if reference_section:\n    lines.extend(\n      (\n        "## 使用する結果",\n        "",\n        reference_section,\n        "",\n        "## 証明",\n        "",\n      )\n    )\n\n  root_edges = (\n    _narrative_edges_for_parent(\n      presentation,\n      presentation.root_step,\n    )\n  )\n\n  if root_edges:\n    target = (\n      presentation\n      .source_replay\n      .group_result\n      .target\n    )\n\n    if (\n      target.group_dimension == 16\n      and target.sphere_dimension == 9\n    ):\n      lines.extend(\n        (\n          (\n            "$\\\\sigma_{9}$ の位数を確認し、"\n            "これが $\\\\pi_{16}^{9}$ を生成することを示す。"\n          ),\n          "",\n        )\n      )\n\n    _append_narrative_for_step(\n      lines,\n      presentation,\n      presentation.root_step,\n      set(),\n      set(),\n      reference_marker_by_step_id,\n      reference_reuse_marker_by_step_id,\n    )\n\n    lines.extend(\n      (\n        "",\n        (\n          "したがって、"\n          + _render_group_proof_narrative_fact(\n            presentation.root_step\n          )\n          + "を得る。"\n        ),\n      )\n    )\n  else:\n    lines.append(\n      (\n        "したがって、"\n        + _render_group_proof_narrative_fact(\n          presentation.root_step\n        )\n        + "である。"\n      )\n    )\n\n  rendered = (\n    "\\n".join(\n      lines\n    )\n    + "\\n"\n  )\n\n  if reference_section:\n    proof_section_marker = "## 証明\\n\\n"\n    proof_section_index = rendered.find(\n      proof_section_marker\n    )\n\n    if proof_section_index >= 0:\n      body_start = (\n        proof_section_index\n        + len(\n          proof_section_marker\n        )\n      )\n      body = rendered[\n        body_start:\n      ]\n      suppressed_body = (\n        suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(\n          presentation,\n          body,\n          reference_entries,\n        )\n      )\n      suppressed_body = (\n        suppress_toda_group_proof_narrative_reference_body_duplicates(\n          suppressed_body,\n          statement_lines_by_reference_number,\n        )\n      )\n      suppressed_body = (\n        link_toda_group_proof_narrative_reference_body_consumers(\n          presentation,\n          suppressed_body,\n          reference_entries,\n        )\n      )\n      (\n        filtered_reference_entries,\n        filtered_statement_lines,\n        suppressed_body,\n      ) = (\n        filter_toda_group_proof_narrative_reference_entries_by_body_usage(\n          reference_entries,\n          statement_lines_by_reference_number,\n          suppressed_body,\n        )\n      )\n      filtered_reference_section = (\n        render_toda_group_proof_narrative_reference_entries_markdown(\n          filtered_reference_entries,\n          filtered_statement_lines,\n        )\n      )\n      prefix_lines = [\n        "# Group proof narrative",\n        "",\n      ]\n\n      if filtered_reference_section:\n        prefix_lines.extend(\n          (\n            "## 使用する結果",\n            "",\n            filtered_reference_section,\n            "",\n            "## 証明",\n            "",\n          )\n        )\n\n      rendered = (\n        "\\n".join(\n          prefix_lines\n        )\n        + "\\n"\n        + suppressed_body\n        + "\\n"\n      )\n\n  return rendered\n'


def replace_import_prefix(
  source: str,
  replacement: str,
) -> str:
  first_function = source.find(
    "\ndef "
  )

  if first_function < 0:
    raise RuntimeError(
      "first function not found"
    )

  return (
    replacement.rstrip()
    + "\n\n"
    + source[
      first_function + 1:
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
    return (
      source[
        :start
      ]
      + replacement.rstrip()
      + "\n"
    )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      next_def + 1:
    ]
  )


def main() -> int:
  if not TARGET.exists():
    raise RuntimeError(
      "missing production file: "
      + str(
        TARGET
      )
    )

  BACKUP.parent.mkdir(
    parents=True,
    exist_ok=True,
  )
  shutil.copy2(
    TARGET,
    BACKUP,
  )

  source = TARGET.read_text(
    encoding="utf-8",
  )
  source = replace_import_prefix(
    source,
    IMPORT_BLOCK,
  )
  source = replace_function(
    source,
    "render_toda_group_proof_narrative_markdown",
    RENDER_FUNCTION,
  )
  TARGET.write_text(
    source,
    encoding="utf-8",
  )

  test_source = (
    Path(__file__).resolve().parent
    / "tests"
    / "test_phase154_r5_fix1_repair2_legacy_route_linkage.py"
  )
  test_target = (
    REPO_ROOT
    / "tests"
    / "test_phase154_r5_fix1_repair2_legacy_route_linkage.py"
  )
  shutil.copy2(
    test_source,
    test_target,
  )

  print(
    "updated:",
    TARGET.name,
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
