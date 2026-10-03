from main import (
  _run_group_proof_command,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_narrative_semantics import (
  build_toda_group_proof_narrative_semantic_closure_presentation,
  build_toda_group_proof_narrative_semantic_sidecar,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaBracketMembershipStatement,
  Toda53NuPrimeBracketSpecializationStatement,
)


PI5_3_TEXT = (
  r"\pi_{5}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}"
)


def _pi6_3_depth2():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = (
    build_toda_group_result_proof_replay(
      group_result,
      max_depth=2,
    )
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )

  return (
    replay,
    presentation,
  )


def test_phase144_6_r25_9b_keeps_source_replay_depth2_unchanged():
  replay, presentation = (
    _pi6_3_depth2()
  )

  assert replay.max_depth == 2
  assert presentation.max_depth == 2
  assert all(
    node.depth <= 2
    for node in presentation.nodes
  )
  assert any(
    isinstance(
      node.proof_step.conclusion,
      Toda53NuPrimeBracketSpecializationStatement,
    )
    for node in presentation.nodes
  )
  assert not any(
    isinstance(
      node.proof_step.conclusion,
      TodaBracketMembershipStatement,
    )
    for node in presentation.nodes
  )


def test_phase144_6_r25_9b_adds_only_required_definition_endpoint():
  _, presentation = (
    _pi6_3_depth2()
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  original_ids = {
    id(
      node.proof_step
    )
    for node in presentation.nodes
  }
  added_nodes = tuple(
    node
    for node in closure.nodes
    if (
      id(
        node.proof_step
      )
      not in original_ids
    )
  )

  assert len(
    added_nodes
  ) == 3
  assert sum(
    isinstance(
      node.proof_step.conclusion,
      TodaBracketMembershipStatement,
    )
    for node in added_nodes
  ) == 1


def test_phase144_6_r25_9b_depth2_builds_definition_argument():
  _, presentation = (
    _pi6_3_depth2()
  )
  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      closure
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      closure,
      semantic_sidecar=sidecar,
    )
  )
  arguments = (
    build_toda_group_proof_narrative_arguments(
      closure,
      blocks,
      semantic_sidecar=sidecar,
    )
  )

  assert tuple(
    argument.role
    for argument in arguments
  ) == (
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )


def test_phase144_6_r25_9b_depth2_narrative_has_definition():
  _, presentation = (
    _pi6_3_depth2()
  )

  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  reference_part = (
    rendered.split(
      "次に",
      1,
    )[
      0
    ]
  )

  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in reference_part
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in reference_part
  )
  assert (
    r"$\nu'$ を定める."
    not in rendered
  )
  assert (
    r"$2\eta_{3} = 0$"
    not in rendered
  )
  assert (
    r"2\nu' = \eta_{3}^{3}"
    in rendered
  )
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in rendered
  )
def test_phase144_6_r25_9b_cli_depth2_narrative_has_definition(
  capsys,
):
  exit_code = (
    _run_group_proof_command(
      3,
      3,
      max_depth=2,
      mode="narrative",
    )
  )
  output = (
    capsys.readouterr().out
  )

  assert exit_code == 0
  assert (
    r"\nu' \in \{\eta_{3}, 2\iota_{4}, \eta_{4}\}_{1}"
    in output
    or
    r"\nu' \in \{\eta_{3},2\iota_{4},\eta_{4}\}_{1}"
    in output
  )
  assert (
    r"$\nu'$ を定める."
    not in output
  )
  assert (
    r"$2\eta_{3} = 0$"
    not in output
  )
  assert (
    r"\pi_{6}^{3} = "
    r"\mathbb{Z}/4\{\nu'\}"
    in output
  )
