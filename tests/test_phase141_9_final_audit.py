import inspect

from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
  recognize_toda_group_proof_narrative_step_role,
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
  Toda55NuFamilyFiniteDimensionalStatement,
  Toda56Nu4DecompositionStatement,
  TodaProp44IsomorphismStatement,
)


def _presentation(
  n,
  k,
  max_depth=3,
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

  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=max_depth,
    )
  )

  return build_toda_group_proof_presentation(
    replay
  )


def _blocks(
  presentation,
):
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )

  return (
    sidecar,
    build_toda_group_proof_narrative_blocks(
      presentation,
      semantic_sidecar=sidecar,
    ),
  )


def _assert_exact_coverage(
  presentation,
  blocks,
):
  block_steps = tuple(
    proof_step
    for block in blocks
    for proof_step in block.steps
  )

  assert len(
    block_steps
  ) == len(
    presentation.nodes
  )

  assert len(
    {
      id(
        proof_step
      )
      for proof_step in block_steps
    }
  ) == len(
    presentation.nodes
  )

  assert {
    id(
      proof_step
    )
    for proof_step in block_steps
  } == {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }


def test_phase141_9_pi6_3_final_blocks_have_no_other():
  presentation = _presentation(
    3,
    3,
  )

  _, blocks = _blocks(
    presentation
  )

  _assert_exact_coverage(
    presentation,
    blocks,
  )

  assert all(
    block.role
    is not TodaGroupProofNarrativeMathematicalBlockRole.OTHER
    for block in blocks
  )


def test_phase141_9_pi8_5_block_layer_preserves_exact_graph_coverage():
  presentation = _presentation(
    5,
    3,
  )

  _, blocks = _blocks(
    presentation
  )

  _assert_exact_coverage(
    presentation,
    blocks,
  )


def test_phase141_9_pi8_5_known_reference_types_are_reference():
  presentation = _presentation(
    5,
    3,
  )

  sidecar, _ = _blocks(
    presentation
  )

  seen = set()

  for node in presentation.nodes:
    statement = (
      node.proof_step.conclusion
    )

    if not isinstance(
      statement,
      (
        Toda55NuFamilyFiniteDimensionalStatement,
        Toda56Nu4DecompositionStatement,
      ),
    ):
      continue

    seen.add(
      type(
        statement
      )
    )

    assert (
      recognize_toda_group_proof_narrative_step_role(
        presentation,
        node.proof_step,
        semantic_sidecar=sidecar,
      )
      is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE
    )

  assert seen


def test_phase141_9_pi15_8_block_layer_preserves_exact_graph_coverage():
  presentation = _presentation(
    8,
    7,
  )

  _, blocks = _blocks(
    presentation
  )

  _assert_exact_coverage(
    presentation,
    blocks,
  )


def test_phase141_9_pi15_8_prop44_is_reference():
  presentation = _presentation(
    8,
    7,
  )

  sidecar, _ = _blocks(
    presentation
  )

  prop44_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaProp44IsomorphismStatement,
    )
  )

  assert (
    recognize_toda_group_proof_narrative_step_role(
      presentation,
      prop44_step,
      semantic_sidecar=sidecar,
    )
    is TodaGroupProofNarrativeMathematicalBlockRole.REFERENCE
  )


def test_phase141_9_block_recognizer_has_no_pi6_target_hardcoding():
  source = inspect.getsource(
    recognize_toda_group_proof_narrative_step_role
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source


def test_phase141_9_block_builder_has_no_pi6_target_hardcoding():
  source = inspect.getsource(
    build_toda_group_proof_narrative_blocks
  )

  forbidden_fragments = (
    "(6, 3)",
    "pi6",
    "nu_prime",
    "ν′",
    "Proposition 5.6",
  )

  for fragment in forbidden_fragments:
    assert fragment not in source
