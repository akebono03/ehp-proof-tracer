from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
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
  TodaDeltaKernelFreeCyclicStatement,
  TodaDeltaSurjectiveStatement,
  TodaProp27HopfInvariantUpToSignStatement,
  TodaProp44IsomorphismStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
)


_PHASE153_R3_9_TYPES = (
  TodaProp44IsomorphismStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp44SecondSummandRestrictionStatement,
  TodaProp59FiniteDimensionalStatement,
  TodaDeltaSurjectiveStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp511NuSquaredFiniteDimensionalStatement,
  TodaDeltaKernelFreeCyclicStatement,
  TodaProp27HopfInvariantUpToSignStatement,
)


def _phase153_r3_9_is_fallback(
  proof_step,
  rendered: str,
) -> bool:
  inference_rule = proof_step.inference_rule

  return (
    not rendered
    or (
      inference_rule is not None
      and rendered == inference_rule.name
    )
    or rendered
    == (
      "`"
      + type(
        proof_step.conclusion
      ).__name__
      + "`"
    )
    or rendered == repr(
      proof_step.conclusion
    )
    or rendered == str(
      proof_step.conclusion
    )
  )


def _phase153_r3_9_presentations():
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

      yield (
        n,
        k,
        presentation,
      )


def test_phase153_r3_9_all_remaining_unresolved_reference_types_render_semantically():
  seen_type_names = set()
  occurrences = 0

  for n, k, presentation in (
    _phase153_r3_9_presentations()
  ):
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
          _PHASE153_R3_9_TYPES,
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

        assert not (
          _phase153_r3_9_is_fallback(
            proof_step,
            rendered,
          )
        ), (
          type(statement).__name__,
          n,
          k,
          rendered,
        )

  assert occurrences == 33
  assert seen_type_names == {
    statement_type.__name__
    for statement_type in (
      _PHASE153_R3_9_TYPES
    )
  }


