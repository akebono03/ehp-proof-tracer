from tests.test_phase143_19_method_evidence import _method_evidence_data
import toda_group_proof_narrative_reasons as reasons_module
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeReason,
  TodaGroupProofNarrativeReasonKind,
)


def _step_text(step):
  return (
    f"id={id(step)} "
    f"rule={getattr(step, 'rule', None)!r} "
    f"conclusion={step.conclusion!r}"
  )


def _report_reason(reason, allowed_ids):
  print("  kind:", reason.kind.name)
  print(
    "  conclusion in presentation:",
    id(reason.conclusion_step) in allowed_ids,
  )
  print(
    "  conclusion:",
    _step_text(reason.conclusion_step),
  )
  for index, premise in enumerate(reason.premise_steps):
    print(
      f"  premise[{index}] in presentation:",
      id(premise) in allowed_ids,
    )
    print(
      f"  premise[{index}]:",
      _step_text(premise),
    )


def main():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(4, 6)

  allowed_ids = {
    id(node.proof_step)
    for node in presentation.nodes
  }

  print("=" * 78)
  print("Phase 150 RC4 closure diagnosis R1")
  print("Target: pi_10^4")
  print("=" * 78)
  print("presentation nodes:", len(presentation.nodes))
  print(
    "dependency semantics:",
    len(semantic_sidecar.dependency_semantics),
  )

  candidates = []

  print("-" * 78)
  print("A. DEFINITION_APPLICABILITY candidates")
  for dependency in semantic_sidecar.dependency_semantics:
    if (
      dependency.role
      is not TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
    ):
      continue
    reason = TodaGroupProofNarrativeReason(
      kind=TodaGroupProofNarrativeReasonKind.DEFINITION_APPLICABILITY,
      premise_steps=(dependency.prerequisite_step,),
      conclusion_step=dependency.dependent_step,
    )
    candidates.append(reason)
    _report_reason(reason, allowed_ids)

  print("-" * 78)
  print("B. Node-derived candidates")
  classifiers = (
    (
      "EXACTNESS_TO_MAP_PROPERTY",
      reasons_module._exactness_to_map_property_reason,
    ),
    (
      "MULTIPLE_RELATION_TO_ORDER",
      reasons_module._multiple_relation_to_order_reason,
    ),
    (
      "FINAL_GROUP_STRUCTURE",
      reasons_module._final_group_structure_reason,
    ),
  )

  for node_index, node in enumerate(presentation.nodes):
    for label, classifier in classifiers:
      reason = classifier(node.proof_step)
      if reason is None:
        continue
      candidates.append(reason)
      print(
        f"node[{node_index}] classifier={label}"
      )
      _report_reason(reason, allowed_ids)

  print("-" * 78)
  print("C. Invalid reason summary")
  invalid = []
  for reason in candidates:
    missing_premises = tuple(
      premise
      for premise in reason.premise_steps
      if id(premise) not in allowed_ids
    )
    missing_conclusion = (
      id(reason.conclusion_step) not in allowed_ids
    )
    if missing_premises or missing_conclusion:
      invalid.append(
        (
          reason,
          missing_premises,
          missing_conclusion,
        )
      )

  print("candidate count:", len(candidates))
  print("invalid count:", len(invalid))
  for index, (
    reason,
    missing_premises,
    missing_conclusion,
  ) in enumerate(invalid):
    print(
      f"INVALID[{index}] kind={reason.kind.name} "
      f"missing_premises={len(missing_premises)} "
      f"missing_conclusion={missing_conclusion}"
    )
    for premise in missing_premises:
      print(
        "  missing premise:",
        _step_text(premise),
      )
    if missing_conclusion:
      print(
        "  missing conclusion:",
        _step_text(reason.conclusion_step),
      )

  if not invalid:
    print("DIAGNOSIS=NO_INVALID_REASON_FOUND")
    raise SystemExit(1)

  invalid_kinds = tuple(
    reason.kind.name
    for reason, _, _ in invalid
  )
  print("INVALID_KINDS=", invalid_kinds)

  only_definition = all(
    reason.kind
    is TodaGroupProofNarrativeReasonKind.DEFINITION_APPLICABILITY
    for reason, _, _ in invalid
  )
  print(
    "ONLY_DEFINITION_APPLICABILITY_INVALID=",
    only_definition,
  )

  if only_definition:
    print(
      "DIAGNOSIS=semantic dependency crosses the presentation-node "
      "boundary; inspect reason-builder filtering rather than adding "
      "a new reason kind."
    )
  else:
    print(
      "DIAGNOSIS=node-derived reason captures a premise outside "
      "presentation; inspect classifier visibility contract."
    )


if __name__ == "__main__":
  main()
