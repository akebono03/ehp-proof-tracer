from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

if str(
  REPO_ROOT
) not in sys.path:
  sys.path.insert(
    0,
    str(
      REPO_ROOT
    ),
  )


from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReasonKind,
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)


def _rule_name(
  proof_step,
) -> str:
  inference_rule = getattr(
    proof_step,
    "inference_rule",
    None,
  )

  if inference_rule is not None:
    name = getattr(
      inference_rule,
      "name",
      None,
    )

    if name:
      return str(
        name
      )

  return str(
    getattr(
      proof_step,
      "rule",
      None,
    )
  )


def _render(
  proof_step,
) -> str:
  rendered = (
    _render_generic_narrative_step(
      proof_step
    )
  )

  if rendered:
    return rendered

  return (
    "<"
    + type(
      proof_step.conclusion
    ).__name__
    + ">"
  )


def main() -> int:
  (
    presentation,
    _,
    semantic_sidecar,
    _,
  ) = _method_evidence_data(
    2,
    1,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  rendered_public = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  print(
    "=============================================================="
  )
  print(
    "Phase 159 pi3_2 dependency semantics audit11"
  )
  print(
    "=============================================================="
  )

  print()
  print(
    "=== Public narrative ==="
  )
  print(
    rendered_public
  )

  print()
  print(
    "=== Candidate presentation nodes ==="
  )

  target_fragments = (
    r"\pi_{2}^{1} = 0",
    r"\pi_{3}^{3}",
    "は単射",
    "は全射",
    "は同型",
    r"H(\eta_{2})",
  )

  target_steps = []

  for node_index, node in enumerate(
    presentation.nodes
  ):
    proof_step = node.proof_step
    line = _render(
      proof_step
    )

    if not any(
      fragment in line
      for fragment in target_fragments
    ):
      continue

    target_steps.append(
      proof_step
    )

    print()
    print(
      "node_index="
      + str(
        node_index
      )
    )
    print(
      "step_id="
      + str(
        id(
          proof_step
        )
      )
    )
    print(
      "statement_type="
      + type(
        proof_step.conclusion
      ).__name__
    )
    print(
      "rule="
      + _rule_name(
        proof_step
      )
    )
    print(
      "rendered="
      + repr(
        line
      )
    )
    print(
      "premise_count="
      + str(
        len(
          proof_step.premises
        )
      )
    )

    for premise_index, premise_step in enumerate(
      proof_step.premises
    ):
      print(
        "  premise["
        + str(
          premise_index
        )
        + "] id="
        + str(
          id(
            premise_step
          )
        )
        + " type="
        + type(
          premise_step.conclusion
        ).__name__
        + " rule="
        + _rule_name(
          premise_step
        )
        + " rendered="
        + repr(
          _render(
            premise_step
          )
        )
      )

  target_step_ids = {
    id(
      proof_step
    )
    for proof_step in target_steps
  }

  print()
  print(
    "=== Presentation edges touching candidate nodes ==="
  )

  edge_count = 0

  for edge in presentation.edges:
    premise_step = edge.premise_step
    parent_step = edge.parent_step

    if (
      id(
        premise_step
      )
      not in target_step_ids
      and id(
        parent_step
      )
      not in target_step_ids
    ):
      continue

    edge_count += 1

    print(
      "edge "
      + str(
        edge_count
      )
    )
    print(
      "  premise_id="
      + str(
        id(
          premise_step
        )
      )
      + " "
      + repr(
        _render(
          premise_step
        )
      )
    )
    print(
      "  parent_id="
      + str(
        id(
          parent_step
        )
      )
      + " "
      + repr(
        _render(
          parent_step
        )
      )
    )

  print()
  print(
    "=== Semantic dependency records ==="
  )

  print(
    "dependency_count="
    + str(
      len(
        semantic_sidecar.dependency_semantics
      )
    )
  )

  for dependency_index, dependency in enumerate(
    semantic_sidecar.dependency_semantics
  ):
    prerequisite = dependency.prerequisite_step
    dependent = dependency.dependent_step

    print()
    print(
      "dependency["
      + str(
        dependency_index
      )
      + "] role="
      + str(
        dependency.role
      )
    )
    print(
      "  prerequisite_id="
      + str(
        id(
          prerequisite
        )
      )
      + " type="
      + type(
        prerequisite.conclusion
      ).__name__
      + " rendered="
      + repr(
        _render(
          prerequisite
        )
      )
    )
    print(
      "  dependent_id="
      + str(
        id(
          dependent
        )
      )
      + " type="
      + type(
        dependent.conclusion
      ).__name__
      + " rendered="
      + repr(
        _render(
          dependent
        )
      )
    )

  print()
  print(
    "=== Narrative reasons ==="
  )

  print(
    "reason_count="
    + str(
      len(
        reason_sidecar.reasons
      )
    )
  )

  for reason_index, reason in enumerate(
    reason_sidecar.reasons
  ):
    print()
    print(
      "reason["
      + str(
        reason_index
      )
      + "] kind="
      + str(
        reason.kind
      )
    )
    print(
      "  conclusion_id="
      + str(
        id(
          reason.conclusion_step
        )
      )
      + " type="
      + type(
        reason.conclusion_step.conclusion
      ).__name__
      + " rendered="
      + repr(
        _render(
          reason.conclusion_step
        )
      )
    )

    for premise_index, premise_step in enumerate(
      reason.premise_steps
    ):
      print(
        "  premise["
        + str(
          premise_index
        )
        + "] id="
        + str(
          id(
            premise_step
          )
        )
        + " type="
        + type(
          premise_step.conclusion
        ).__name__
        + " rendered="
        + repr(
          _render(
            premise_step
          )
        )
      )

  exactness_count = sum(
    1
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .EXACTNESS_TO_MAP_PROPERTY
    )
  )
  definition_count = sum(
    1
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )

  print()
  print(
    "=== Summary ==="
  )
  print(
    "EXACTNESS_TO_MAP_PROPERTY count="
    + str(
      exactness_count
    )
  )
  print(
    "DEFINITION_APPLICABILITY count="
    + str(
      definition_count
    )
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
