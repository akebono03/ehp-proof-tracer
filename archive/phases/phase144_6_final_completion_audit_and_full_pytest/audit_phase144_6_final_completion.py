from pathlib import Path

from main import _run_group_proof_command
from toda_calculation_facade import build_standard_toda_report
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
from toda_rules import TodaBracketMembershipStatement


PI5_3_TEXT = (
  r"\pi_{5}^{3} = "
  r"\mathbb{Z}/2\{\eta_{3}\eta_{4}\}"
)


def _depth2_pi6_3():
  report = build_standard_toda_report(
    n=3,
    k=3,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  return replay, presentation


def main() -> None:
  replay, presentation = _depth2_pi6_3()

  if replay.max_depth != 2:
    raise AssertionError(
      "source replay max_depth changed"
    )

  if presentation.max_depth != 2:
    raise AssertionError(
      "ordinary presentation max_depth changed"
    )

  if any(
    node.depth > 2
    for node in presentation.nodes
  ):
    raise AssertionError(
      "ordinary presentation contains depth > 2"
    )

  closure = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  original_ids = {
    id(node.proof_step)
    for node in presentation.nodes
  }
  added_nodes = tuple(
    node
    for node in closure.nodes
    if id(node.proof_step) not in original_ids
  )

  if len(added_nodes) != 1:
    raise AssertionError(
      "semantic closure must add exactly one node "
      f"for pi_6^3 depth=2; got {len(added_nodes)}"
    )

  if not isinstance(
    added_nodes[0].proof_step.conclusion,
    TodaBracketMembershipStatement,
  ):
    raise AssertionError(
      "semantic closure added the wrong endpoint"
    )

  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    closure
  )
  blocks = build_toda_group_proof_narrative_blocks(
    closure,
    semantic_sidecar=sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    closure,
    blocks,
    semantic_sidecar=sidecar,
  )
  roles = tuple(
    argument.role
    for argument in arguments
  )

  expected_roles = (
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_GROUP_STRUCTURE,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER,
    TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION,
  )

  if roles != expected_roles:
    raise AssertionError(
      "unexpected depth=2 Narrative argument roles: "
      f"{roles!r}"
    )

  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  required = (
    r"$\nu'$ を定める.",
    r"2\nu' = \eta_{3}^{3}",
    r"\pi_{6}^{3} = \mathbb{Z}/4\{\nu'\}",
  )

  for fragment in required:
    if fragment not in rendered:
      raise AssertionError(
        "missing required depth=2 Narrative fragment: "
        + fragment
      )

  if PI5_3_TEXT in rendered:
    raise AssertionError(
      "internal pi_5^3 supporting fact leaked "
      "into depth=2 Narrative"
    )

  print(
    "depth=2 source replay: PASS "
    f"(nodes={len(presentation.nodes)})"
  )
  print(
    "semantic closure: PASS "
    f"(added={len(added_nodes)}, "
    f"closure_nodes={len(closure.nodes)})"
  )
  print(
    "argument roles: PASS "
    + repr(
      tuple(
        role.value
        for role in roles
      )
    )
  )
  print(
    "nu-prime definition visibility: PASS"
  )
  print(
    "pi_5^3 suppression: PASS"
  )


if __name__ == "__main__":
  main()
