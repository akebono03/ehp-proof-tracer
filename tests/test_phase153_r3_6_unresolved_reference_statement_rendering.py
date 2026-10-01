from toda_calculation_facade import (
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

  assert occurrences == 42
  assert seen_type_names == {
    statement_type.__name__
    for statement_type in (
      _PHASE153_R3_6_TYPES
    )
  }
