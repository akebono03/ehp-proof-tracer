from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent


def _replace_once(
    path: Path,
    old: str,
    new: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )
    count = text.count(
        old
    )
    if count != 1:
        raise RuntimeError(
            str(path.relative_to(REPO_ROOT))
            + ": expected exactly one replacement target, found "
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


TEST_CONTENT = r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
)


_PHASE153_R3_6_TYPES = (
  Toda52CompositionIsomorphismStatement,
  TodaLemma54Statement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaLemma513Statement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaLemma514SigmaPrimeStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  TodaLemma514Sigma8Statement,
)


def _phase153_r3_6_is_fallback(
  proof_step,
  rendered: str,
) -> bool:
  inference_rule = proof_step.inference_rule

  return (
    (
      inference_rule is not None
      and rendered
      == inference_rule.name
    )
    or rendered
    == (
      "`"
      + type(
        proof_step.conclusion
      ).__name__
      + "`"
    )
    or rendered
    == repr(
      proof_step.conclusion
    )
    or rendered
    == str(
      proof_step.conclusion
    )
  )


def test_phase153_r3_6_all_previously_unresolved_reference_types_render_semantically():
  seen_type_names = set()
  occurrences = 0

  for n in range(
    2,
    16,
  ):
    for k in range(
      0,
      8,
    ):
      report = build_standard_toda_report(
        n=n,
        k=k,
      )

      if not report.candidates:
        continue

      group_result = (
        report.candidates[
          0
        ].source_candidate.group_result
      )
      replay = build_toda_group_result_proof_replay(
        group_result,
        max_depth=2,
      )
      presentation = (
        build_toda_group_proof_presentation(
          replay
        )
      )
      presentation = (
        build_toda_group_proof_narrative_semantic_closure_presentation(
          presentation
        )
      )
      entries = (
        build_toda_group_proof_narrative_reference_entries(
          presentation
        )
      )

      for entry in entries:
        for proof_step in entry.proof_steps:
          statement = proof_step.conclusion

          if not isinstance(
            statement,
            _PHASE153_R3_6_TYPES,
          ):
            continue

          occurrences += 1
          seen_type_names.add(
            type(
              statement
            ).__name__
          )

          rendered = (
            _render_generic_narrative_step(
              proof_step
            )
          )

          assert rendered
          assert not (
            _phase153_r3_6_is_fallback(
              proof_step,
              rendered,
            )
          ), (
            type(statement).__name__,
            n,
            k,
            rendered,
          )

  assert occurrences == 37
  assert seen_type_names == {
    statement_type.__name__
    for statement_type in (
      _PHASE153_R3_6_TYPES
    )
  }
'''


def main() -> int:
    renderer_path = (
        REPO_ROOT
        / "toda_group_proof_generic_narrative_renderer.py"
    )
    test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_6_unresolved_reference_statement_rendering.py"
    )

    old_scalar_import_anchor = r'''from proof import (
  ProofStep,
)
'''

    new_scalar_import_anchor = r'''from proof import (
  ProofStep,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
'''

    _replace_once(
        renderer_path,
        old_scalar_import_anchor,
        new_scalar_import_anchor,
    )

    old_proof_renderer_import = r'''from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
)
'''

    new_proof_renderer_import = r'''from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
  render_toda_proof_statement_latex,
  render_toda_raw_group_structure_latex,
)
'''

    _replace_once(
        renderer_path,
        old_proof_renderer_import,
        new_proof_renderer_import,
    )

    old_rules_import = r'''from toda_rules import (
  Toda45IsomorphismStatement,
  TodaDeltaInjectiveStatement,
  TodaDeltaZeroStatement,
  TodaHopfInvariantInjectiveStatement,
  TodaHopfInvariantIsomorphismStatement,
  TodaHopfInvariantSurjectiveStatement,
  TodaHopfInvariantZeroStatement,
  TodaIteratedSuspensionInjectiveStatement,
  TodaNuFamilyDefinitionStatement,
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionSurjectiveStatement,
)
'''

    new_rules_import = r'''from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda45IsomorphismStatement,
  Toda52CompositionIsomorphismStatement,
  Toda53NuPrimeBracketSpecializationStatement,
  Toda55NuFamilyFiniteDimensionalStatement,
  TodaDeltaInjectiveStatement,
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
  TodaProp42ExactnessStatement,
  TodaProp44SuspensionInjectiveStatement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaSigmaFamilyDefinitionStatement,
  TodaSuspensionInjectiveStatement,
  TodaSuspensionIsomorphismStatement,
  TodaSuspensionSurjectiveStatement,
)
'''

    _replace_once(
        renderer_path,
        old_rules_import,
        new_rules_import,
    )

    prose_marker = r'''def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
'''

    helpers = r'''def _render_phase153_r3_6_component_latex(
  component,
) -> str | None:
  if isinstance(
    component,
    ScalarGreaterEqualStatement,
  ):
    return (
      _render_scalar_latex(
        component.left
      )
      + r" \ge "
      + _render_scalar_latex(
        component.right
      )
    )

  try:
    latex = (
      render_repository_conclusion_latex(
        component
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    latex = None

  if latex is not None:
    return latex

  try:
    return (
      render_toda_proof_statement_latex(
        component
      )
    )
  except (
    TypeError,
    ValueError,
  ):
    return None


def _render_phase153_r3_6_component_list_prose(
  components: tuple[
    object,
    ...,
  ],
) -> str | None:
  rendered = tuple(
    latex
    for latex in (
      _render_phase153_r3_6_component_latex(
        component
      )
      for component in components
    )
    if latex is not None
  )

  if not rendered:
    return None

  return (
    ", ".join(
      "$"
      + latex
      + "$"
      for latex in rendered
    )
    + " が成り立つ."
  )


def _render_phase153_r3_6_reference_statement_prose(
  statement,
) -> str | None:
  if isinstance(
    statement,
    Toda52CompositionIsomorphismStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.composition.left
      )
      + r"\circ -: "
      + render_toda_primary_group_latex(
        statement.source_group
      )
      + r" \to "
      + render_toda_primary_group_latex(
        statement.target_group
      )
      + "$ は同型写像である."
    )

  if isinstance(
    statement,
    Toda53NuPrimeBracketSpecializationStatement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.nu_prime
      )
      + r" \in "
      + render_toda_expression_latex(
        statement
        .bracket_membership
        .bracket
      )
      + "$ が成り立つ."
    )

  if isinstance(
    statement,
    TodaLemma54Statement,
  ):
    membership = (
      statement.membership
    )
    membership_latex = (
      render_toda_expression_latex(
        membership.element
      )
      + r" \in \pi_{"
      + _render_scalar_latex(
        membership.group_dimension
      )
      + r"}^{"
      + _render_scalar_latex(
        membership.sphere_dimension
      )
      + "}"
    )
    relations = (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.hopf_relation,
          statement.double_suspension_relation,
        )
      )
    )

    if relations is None:
      return (
        "$"
        + membership_latex
        + "$."
      )

    return (
      "$"
      + membership_latex
      + "$, "
      + relations
    )

  if isinstance(
    statement,
    TodaProp51FiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi3_2_group_relation,
          statement.eta2_hopf_relation,
          statement.delta_iota5_relation,
          statement.higher_eta_group_relation,
        )
      )
    )

  if isinstance(
    statement,
    TodaProp56FiniteDimensionalStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi5_2_group_relation,
          statement.pi6_3_group_relation,
          statement.pi7_4_group_relation,
          statement.pi8_5_group_relation,
          statement.higher_nu_group_relation,
          statement.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    Toda55NuFamilyFiniteDimensionalStatement,
  ):
    definition = (
      statement.nu_family_definition
    )
    definition_latex = (
      render_toda_expression_latex(
        definition.element
      )
      + " = "
      + render_toda_expression_latex(
        definition.iterated_suspension
      )
    )
    relations = (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.n_range,
          statement.double_nu_relation,
          statement.quadruple_nu_relation,
        )
      )
    )

    if relations is None:
      return (
        "$"
        + definition_latex
        + "$."
      )

    return (
      "$"
      + definition_latex
      + "$, "
      + relations
    )

  if isinstance(
    statement,
    TodaProp511FiniteDimensionalStatement,
  ):
    six_stem = (
      statement.nu_squared_finite_dimensional
    )

    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.pi8_2_group_relation,
          statement.pi9_3_zero,
          statement.pi10_4_group_relation,
          six_stem.pi11_5_group_relation,
          six_stem.pi12_6_group_relation,
          six_stem.pi13_7_group_relation,
          six_stem.pi14_8_group_relation,
          six_stem.higher_six_stem_group_relation,
          six_stem.higher_range,
        )
      )
    )

  if isinstance(
    statement,
    TodaProp515Pi12_5HopfIsomorphismStatement,
  ):
    return (
      "$H: "
      + render_toda_primary_group_latex(
        statement.map.source_group
      )
      + r" \xrightarrow{\cong} "
      + render_toda_raw_group_structure_latex(
        statement.image_group
      )
      + "$, $H("
      + render_toda_expression_latex(
        statement.source_generator
      )
      + ") = "
      + render_toda_expression_latex(
        statement.image_generator
      )
      + "$ が成り立つ."
    )

  if isinstance(
    statement,
    TodaLemma513Statement,
  ):
    return (
      "$"
      + render_toda_expression_latex(
        statement.sigma_triple_prime
      )
      + r" \in "
      + render_toda_expression_latex(
        statement.bracket
      )
      + "$, $H("
      + render_toda_expression_latex(
        statement.sigma_triple_prime
      )
      + ") = "
      + render_toda_expression_latex(
        statement.hopf_image
      )
      + "$ が成り立つ."
    )

  if isinstance(
    statement,
    Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.odd_parameter_statement,
          statement.bridge_relation,
        )
      )
    )

  if isinstance(
    statement,
    TodaLemma514SigmaPrimeStatement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.double_relation,
          statement.hopf_relation,
        )
      )
    )

  if isinstance(
    statement,
    TodaLemma514Sigma8Statement,
  ):
    return (
      _render_phase153_r3_6_component_list_prose(
        (
          statement.definition_relation,
          statement.hopf_relation,
          statement.suspension_relation,
          statement.double_suspension_relation,
        )
      )
    )

  return None


'''

    renderer_text = renderer_path.read_text(
        encoding="utf-8",
    )
    if renderer_text.count(
        prose_marker
    ) != 1:
        raise RuntimeError(
            "generic narrative prose marker not found exactly once"
        )
    renderer_text = renderer_text.replace(
        prose_marker,
        helpers + prose_marker,
        1,
    )
    renderer_path.write_text(
        renderer_text,
        encoding="utf-8",
    )

    old_prose_start = r'''def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  aggregate_prose = (
'''

    new_prose_start = r'''def _render_generic_narrative_statement_prose(
  statement,
) -> str | None:
  reference_prose = (
    _render_phase153_r3_6_reference_statement_prose(
      statement
    )
  )

  if reference_prose is not None:
    return reference_prose

  aggregate_prose = (
'''

    _replace_once(
        renderer_path,
        old_prose_start,
        new_prose_start,
    )

    test_path.write_text(
        TEST_CONTENT,
        encoding="utf-8",
    )

    print(
        "updated: toda_group_proof_generic_narrative_renderer.py"
    )
    print(
        "added: tests\\\\test_phase153_r3_6_unresolved_reference_statement_rendering.py"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
