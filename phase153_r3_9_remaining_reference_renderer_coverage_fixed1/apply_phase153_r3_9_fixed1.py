from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent


def _ensure_replacement(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )

    if new in text:
        print(
            "already applied: "
            + label
        )
        return

    count = text.count(
        old
    )
    if count != 1:
        raise RuntimeError(
            label
            + ": expected old target exactly once "
            "or new target already present; found "
            + str(count)
        )

    path.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )
    print(
        "applied: "
        + label
    )


def _ensure_helper(
    path: Path,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )
    helper_name = (
        "def _render_phase153_r3_9_reference_statement_prose("
    )

    if helper_name in text:
        print(
            "already applied: R3-9 reference helpers"
        )
        return

    marker = 'def _render_phase153_r3_6_reference_statement_prose(\n  statement,\n) -> str | None:\n'
    count = text.count(
        marker
    )
    if count != 1:
        raise RuntimeError(
            "R3-6 reference statement helper marker "
            "not found exactly once; found "
            + str(count)
        )

    path.write_text(
        text.replace(
            marker,
            'def _render_phase153_r3_9_group_term_latex(\n  group,\n) -> str | None:\n  if isinstance(\n    group,\n    TodaPrimaryGroup,\n  ):\n    return (\n      render_toda_primary_group_latex(\n        group\n      )\n    )\n\n  if isinstance(\n    group,\n    DirectSumGroup,\n  ):\n    rendered_summands = tuple(\n      _render_phase153_r3_9_group_term_latex(\n        summand\n      )\n      for summand in group.summands\n    )\n\n    if any(\n      rendered is None\n      for rendered in rendered_summands\n    ):\n      return None\n\n    return r" \\oplus ".join(\n      rendered\n      for rendered in rendered_summands\n      if rendered is not None\n    )\n\n  return None\n\n\ndef _render_phase153_r3_9_reference_statement_prose(\n  statement,\n) -> str | None:\n  if isinstance(\n    statement,\n    TodaProp44IsomorphismStatement,\n  ):\n    decomposition_map = (\n      statement.map\n    )\n    source_latex = (\n      _render_phase153_r3_9_group_term_latex(\n        decomposition_map.source_group\n      )\n    )\n    target_latex = (\n      _render_phase153_r3_9_group_term_latex(\n        decomposition_map.target_group\n      )\n    )\n\n    if (\n      source_latex is None\n      or target_latex is None\n    ):\n      return None\n\n    return (\n      "$("\n      + render_toda_expression_latex(\n        decomposition_map.beta\n      )\n      + ", "\n      + render_toda_expression_latex(\n        decomposition_map.gamma\n      )\n      + r") \\mapsto "\n      + render_toda_expression_latex(\n        decomposition_map.formula\n      )\n      + ": "\n      + source_latex\n      + r" \\to "\n      + target_latex\n      + "$ は同型写像である."\n    )\n\n  if isinstance(\n    statement,\n    TodaProp44SecondSummandRestrictionStatement,\n  ):\n    return (\n      "分解写像の第二成分は $"\n      + render_toda_expression_latex(\n        statement.composition\n      )\n      + "$ で与えられる."\n    )\n\n  if isinstance(\n    statement,\n    TodaProp53FiniteDimensionalStatement,\n  ):\n    return (\n      _render_phase153_r3_6_component_list_prose(\n        (\n          statement.pi4_2_group_relation,\n          statement.pi5_3_group_relation,\n          statement.pi6_4_group_relation,\n          statement.higher_eta_squared_group_relation,\n          statement.higher_range,\n        )\n      )\n    )\n\n  if isinstance(\n    statement,\n    TodaProp58FiniteDimensionalStatement,\n  ):\n    return (\n      _render_phase153_r3_6_component_list_prose(\n        (\n          statement.pi6_2_group_relation,\n          statement.pi7_3_group_relation,\n          statement.pi8_4_group_relation,\n          statement.pi9_5_group_relation,\n          statement.higher_four_stem_zero,\n          statement.higher_range,\n        )\n      )\n    )\n\n  if isinstance(\n    statement,\n    TodaProp59FiniteDimensionalStatement,\n  ):\n    return (\n      _render_phase153_r3_6_component_list_prose(\n        (\n          statement.pi7_2_group_relation,\n          statement.pi8_3_group_relation,\n          statement.pi9_4_group_relation,\n          statement.pi10_5_group_relation,\n          statement.pi11_6_group_relation,\n          statement.higher_five_stem_zero,\n          statement.higher_range,\n        )\n      )\n    )\n\n  if isinstance(\n    statement,\n    TodaProp511NuSquaredFiniteDimensionalStatement,\n  ):\n    return (\n      _render_phase153_r3_6_component_list_prose(\n        (\n          statement.pi11_5_group_relation,\n          statement.pi12_6_group_relation,\n          statement.pi13_7_group_relation,\n          statement.pi14_8_group_relation,\n          statement.higher_six_stem_group_relation,\n          statement.higher_range,\n        )\n      )\n    )\n\n  if isinstance(\n    statement,\n    TodaDeltaKernelFreeCyclicStatement,\n  ):\n    map_latex = (\n      _render_generic_narrative_group_map_latex(\n        statement.map\n      )\n    )\n\n    if map_latex is None:\n      return None\n\n    return (\n      r"$\\ker\\Delta = "\n      + render_toda_raw_group_structure_latex(\n        statement.kernel_group\n      )\n      + "$ が成り立つ."\n    )\n\n  if isinstance(\n    statement,\n    TodaProp27HopfInvariantUpToSignStatement,\n  ):\n    return (\n      "$H("\n      + render_toda_expression_latex(\n        statement.argument\n      )\n      + r") = \\pm "\n      + render_toda_expression_latex(\n        statement.positive_value\n      )\n      + "$ が成り立つ."\n    )\n\n  return None\n\n\n'
            + marker,
            1,
        ),
        encoding="utf-8",
    )
    print(
        "applied: R3-9 reference helpers"
    )


def main() -> int:
    renderer_path = (
        REPO_ROOT
        / "toda_group_proof_generic_narrative_renderer.py"
    )
    test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_9_remaining_reference_renderer_coverage.py"
    )

    _ensure_replacement(
        renderer_path,
        'from homotopy_groups import (\n  TodaDeltaMap,\n  TodaHopfInvariantMap,\n  TodaIteratedSuspensionMap,\n  TodaSuspensionMap,\n)\n',
        'from homotopy_groups import (\n  DirectSumGroup,\n  TodaDeltaMap,\n  TodaHopfInvariantMap,\n  TodaIteratedSuspensionMap,\n  TodaPrimaryGroup,\n  TodaSuspensionMap,\n)\n',
        "homotopy_groups import",
    )

    _ensure_replacement(
        renderer_path,
        'from toda_rules import (\n  Toda36Lemma514SigmaDoublePrimeBridgeStatement,\n  Toda45IsomorphismStatement,\n  Toda52CompositionIsomorphismStatement,\n  Toda53NuPrimeBracketSpecializationStatement,\n  Toda55NuFamilyFiniteDimensionalStatement,\n  TodaDeltaInjectiveStatement,\n  TodaDeltaZeroStatement,\n  TodaHopfInvariantInjectiveStatement,\n  TodaHopfInvariantIsomorphismStatement,\n  TodaHopfInvariantSurjectiveStatement,\n  TodaHopfInvariantZeroStatement,\n  TodaIteratedSuspensionInjectiveStatement,\n  TodaLemma513Statement,\n  TodaLemma514Sigma8Statement,\n  TodaLemma514SigmaPrimeStatement,\n  TodaLemma54Statement,\n  TodaNuFamilyDefinitionStatement,\n  TodaProp42ExactnessStatement,\n  TodaProp44SuspensionInjectiveStatement,\n  TodaProp51FiniteDimensionalStatement,\n  TodaProp511FiniteDimensionalStatement,\n  TodaProp515Pi12_5HopfIsomorphismStatement,\n  TodaProp56FiniteDimensionalStatement,\n  TodaSigmaFamilyDefinitionStatement,\n  TodaSuspensionInjectiveStatement,\n  TodaSuspensionIsomorphismStatement,\n  TodaSuspensionSurjectiveStatement,\n)\n',
        'from toda_rules import (\n  Toda36Lemma514SigmaDoublePrimeBridgeStatement,\n  Toda45IsomorphismStatement,\n  Toda52CompositionIsomorphismStatement,\n  Toda53NuPrimeBracketSpecializationStatement,\n  Toda55NuFamilyFiniteDimensionalStatement,\n  TodaDeltaInjectiveStatement,\n  TodaDeltaKernelFreeCyclicStatement,\n  TodaDeltaSurjectiveStatement,\n  TodaDeltaZeroStatement,\n  TodaHopfInvariantInjectiveStatement,\n  TodaHopfInvariantIsomorphismStatement,\n  TodaHopfInvariantSurjectiveStatement,\n  TodaHopfInvariantZeroStatement,\n  TodaIteratedSuspensionInjectiveStatement,\n  TodaLemma513Statement,\n  TodaLemma514Sigma8Statement,\n  TodaLemma514SigmaPrimeStatement,\n  TodaLemma54Statement,\n  TodaNuFamilyDefinitionStatement,\n  TodaProp27HopfInvariantUpToSignStatement,\n  TodaProp42ExactnessStatement,\n  TodaProp44IsomorphismStatement,\n  TodaProp44SecondSummandRestrictionStatement,\n  TodaProp44SuspensionInjectiveStatement,\n  TodaProp51FiniteDimensionalStatement,\n  TodaProp53FiniteDimensionalStatement,\n  TodaProp58FiniteDimensionalStatement,\n  TodaProp59FiniteDimensionalStatement,\n  TodaProp511FiniteDimensionalStatement,\n  TodaProp511NuSquaredFiniteDimensionalStatement,\n  TodaProp515Pi12_5HopfIsomorphismStatement,\n  TodaProp56FiniteDimensionalStatement,\n  TodaSigmaFamilyDefinitionStatement,\n  TodaSuspensionInjectiveStatement,\n  TodaSuspensionIsomorphismStatement,\n  TodaSuspensionSurjectiveStatement,\n)\n',
        "toda_rules import",
    )

    _ensure_helper(
        renderer_path
    )

    _ensure_replacement(
        renderer_path,
        'def _render_generic_narrative_statement_prose(\n  statement,\n) -> str | None:\n  reference_prose = (\n    _render_phase153_r3_6_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n',
        'def _render_generic_narrative_statement_prose(\n  statement,\n) -> str | None:\n  reference_prose = (\n    _render_phase153_r3_9_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n\n  reference_prose = (\n    _render_phase153_r3_6_reference_statement_prose(\n      statement\n    )\n  )\n\n  if reference_prose is not None:\n    return reference_prose\n',
        "generic narrative statement dispatch",
    )

    _ensure_replacement(
        renderer_path,
        '_GENERIC_SURJECTIVE_STATEMENT_TYPES = (\n  TodaHopfInvariantSurjectiveStatement,\n  TodaSuspensionSurjectiveStatement,\n)\n',
        '_GENERIC_SURJECTIVE_STATEMENT_TYPES = (\n  TodaDeltaSurjectiveStatement,\n  TodaHopfInvariantSurjectiveStatement,\n  TodaSuspensionSurjectiveStatement,\n)\n',
        "generic surjective statement types",
    )

    test_path.write_text(
        'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_generic_narrative_renderer import (\n  _render_generic_narrative_step,\n)\nfrom toda_group_proof_narrative_contribution_renderer import (\n  _toda_group_proof_narrative_reference_statement_lines_by_number,\n)\nfrom toda_group_proof_narrative_references import (\n  build_toda_group_proof_narrative_reference_entries,\n)\nfrom toda_group_proof_narrative_semantics import (\n  build_toda_group_proof_narrative_semantic_closure_presentation,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  TodaDeltaKernelFreeCyclicStatement,\n  TodaDeltaSurjectiveStatement,\n  TodaProp27HopfInvariantUpToSignStatement,\n  TodaProp44IsomorphismStatement,\n  TodaProp44SecondSummandRestrictionStatement,\n  TodaProp53FiniteDimensionalStatement,\n  TodaProp58FiniteDimensionalStatement,\n  TodaProp59FiniteDimensionalStatement,\n  TodaProp511NuSquaredFiniteDimensionalStatement,\n)\n\n\n_PHASE153_R3_9_TYPES = (\n  TodaProp44IsomorphismStatement,\n  TodaProp53FiniteDimensionalStatement,\n  TodaProp44SecondSummandRestrictionStatement,\n  TodaProp59FiniteDimensionalStatement,\n  TodaDeltaSurjectiveStatement,\n  TodaProp58FiniteDimensionalStatement,\n  TodaProp511NuSquaredFiniteDimensionalStatement,\n  TodaDeltaKernelFreeCyclicStatement,\n  TodaProp27HopfInvariantUpToSignStatement,\n)\n\n\ndef _phase153_r3_9_is_fallback(\n  proof_step,\n  rendered: str,\n) -> bool:\n  inference_rule = proof_step.inference_rule\n\n  return (\n    not rendered\n    or (\n      inference_rule is not None\n      and rendered == inference_rule.name\n    )\n    or rendered\n    == (\n      "`"\n      + type(\n        proof_step.conclusion\n      ).__name__\n      + "`"\n    )\n    or rendered == repr(\n      proof_step.conclusion\n    )\n    or rendered == str(\n      proof_step.conclusion\n    )\n  )\n\n\ndef _phase153_r3_9_presentations():\n  for n in range(\n    2,\n    16,\n  ):\n    for k in range(\n      0,\n      8,\n    ):\n      report = build_standard_toda_report(\n        n=n,\n        k=k,\n      )\n\n      if not report.candidates:\n        continue\n\n      group_result = (\n        report.candidates[\n          0\n        ].source_candidate.group_result\n      )\n      replay = build_toda_group_result_proof_replay(\n        group_result,\n        max_depth=2,\n      )\n      presentation = (\n        build_toda_group_proof_presentation(\n          replay\n        )\n      )\n      presentation = (\n        build_toda_group_proof_narrative_semantic_closure_presentation(\n          presentation\n        )\n      )\n\n      yield (\n        n,\n        k,\n        presentation,\n      )\n\n\ndef test_phase153_r3_9_all_remaining_unresolved_reference_types_render_semantically():\n  seen_type_names = set()\n  occurrences = 0\n\n  for n, k, presentation in (\n    _phase153_r3_9_presentations()\n  ):\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n\n    for entry in entries:\n      for proof_step in entry.proof_steps:\n        statement = proof_step.conclusion\n\n        if not isinstance(\n          statement,\n          _PHASE153_R3_9_TYPES,\n        ):\n          continue\n\n        occurrences += 1\n        seen_type_names.add(\n          type(\n            statement\n          ).__name__\n        )\n\n        rendered = (\n          _render_generic_narrative_step(\n            proof_step\n          )\n        )\n\n        assert not (\n          _phase153_r3_9_is_fallback(\n            proof_step,\n            rendered,\n          )\n        ), (\n          type(statement).__name__,\n          n,\n          k,\n          rendered,\n        )\n\n  assert occurrences == 31\n  assert seen_type_names == {\n    statement_type.__name__\n    for statement_type in (\n      _PHASE153_R3_9_TYPES\n    )\n  }\n\n\ndef test_phase153_r3_9_all_reference_entries_have_selected_statement():\n  entries_without_selected_statement = []\n\n  for n, k, presentation in (\n    _phase153_r3_9_presentations()\n  ):\n    entries = (\n      build_toda_group_proof_narrative_reference_entries(\n        presentation\n      )\n    )\n    selected_by_number = (\n      _toda_group_proof_narrative_reference_statement_lines_by_number(\n        presentation,\n        entries,\n      )\n    )\n\n    for entry in entries:\n      if selected_by_number.get(\n        entry.number,\n        (),\n      ):\n        continue\n\n      entries_without_selected_statement.append(\n        (\n          n,\n          k,\n          entry.number,\n          entry.reference.locator\n          or entry.reference.label,\n        )\n      )\n\n  assert entries_without_selected_statement == []\n',
        encoding="utf-8",
    )

    print(
        "updated: toda_group_proof_generic_narrative_renderer.py"
    )
    print(
        "added/updated: "
        "tests\\test_phase153_r3_9_remaining_reference_renderer_coverage.py"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
