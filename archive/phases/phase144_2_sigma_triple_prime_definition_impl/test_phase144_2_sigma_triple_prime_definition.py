from toda_calculation_facade import build_standard_toda_report
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaLemma513Statement,
)


def _argument_data(
  n: int,
  k: int,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=3,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=sidecar,
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      presentation,
      blocks,
      semantic_sidecar=sidecar,
    )
  )
  return (
    presentation,
    blocks,
    arguments,
  )


def test_phase144_2_pi12_5_lemma513_is_definition_block():
  _, blocks, _ = _argument_data(
    5,
    7,
  )

  block = next(
    block
    for block in blocks
    if any(
      isinstance(
        proof_step.conclusion,
        TodaLemma513Statement,
      )
      for proof_step in block.steps
    )
  )

  assert (
    block.role
    is TodaGroupProofNarrativeMathematicalBlockRole
    .DEFINITION
  )


def test_phase144_2_pi12_5_sigma_triple_prime_is_definition_subject():
  _, _, arguments = _argument_data(
    5,
    7,
  )
  expected_name = "σ" + "'" * 3

  matching_arguments = []

  for argument in arguments:
    if (
      argument.role
      is not TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_DEFINITION
    ):
      continue

    subject = (
      extract_toda_group_proof_narrative_argument_purpose_subject(
        argument
      )
    )

    if (
      subject is not None
      and subject.name == expected_name
    ):
      matching_arguments.append(
        argument
      )

  assert len(
    matching_arguments
  ) == 1

  conclusion_step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      matching_arguments[
        0
      ]
    )
  )

  assert conclusion_step is not None
  assert isinstance(
    conclusion_step.conclusion,
    TodaLemma513Statement,
  )


def test_phase144_2_existing_definition_subjects_remain_supported():
  for n, k, expected_name in (
    (
      5,
      3,
      "ν_5",
    ),
    (
      9,
      7,
      "σ_9",
    ),
  ):
    _, _, arguments = _argument_data(
      n,
      k,
    )

    subjects = tuple(
      extract_toda_group_proof_narrative_argument_purpose_subject(
        argument
      )
      for argument in arguments
      if (
        argument.role
        is TodaGroupProofNarrativeArgumentRole
        .ESTABLISH_DEFINITION
      )
    )

    assert any(
      subject is not None
      and subject.name == expected_name
      for subject in subjects
    )
