from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativePremiseSemanticRole,
  TodaGroupProofNarrativeStepSemanticRole,
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
from toda_upstream_bootstrap import (
  build_toda_53_nu_prime_steps,
)


def _rule_name(step):
  if step.inference_rule is None:
    return None
  return step.inference_rule.name


def _describe(step):
  return (
    f"id={id(step)} "
    f"type={type(step.conclusion).__name__} "
    f"rule={_rule_name(step)!r} "
    f"conclusion={step.conclusion!r}"
  )


def _presentation_data(max_depth):
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
    max_depth=max_depth,
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
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=sidecar,
  )
  return (
    presentation,
    sidecar,
    blocks,
    arguments,
  )


def main():
  print("=" * 80)
  print("Phase 144-6 R25-8R1 rollback + semantic-route audit")
  print("Production changes after rollback: none")
  print("=" * 80)

  print("")
  print("A. Canonical nu-prime upstream route")
  print("-" * 80)
  membership_step, hopf_step, double_step = (
    build_toda_53_nu_prime_steps()
  )
  for name, step in (
    ("membership", membership_step),
    ("hopf", hopf_step),
    ("double", double_step),
  ):
    print(name + ": " + _describe(step))
    for index, premise in enumerate(step.premises):
      print(
        f"  premise[{index}]: "
        + _describe(premise)
      )

  print("")
  print("B. Depth boundary for semantic definition route")
  print("-" * 80)

  for depth in (1, 2, 3):
    (
      presentation,
      sidecar,
      blocks,
      arguments,
    ) = _presentation_data(depth)

    definition_semantics = tuple(
      semantic
      for semantic in sidecar.step_semantics
      if (
        semantic.role
        is TodaGroupProofNarrativeStepSemanticRole
        .DEFINITION_INTRODUCTION
      )
    )
    precondition_semantics = tuple(
      semantic
      for semantic in sidecar.premise_semantics
      if (
        semantic.role
        is TodaGroupProofNarrativePremiseSemanticRole
        .PRECONDITION
      )
    )

    bracket_memberships = tuple(
      node.proof_step
      for node in presentation.nodes
      if isinstance(
        node.proof_step.conclusion,
        TodaBracketMembershipStatement,
      )
    )
    bracket_specializations = tuple(
      node.proof_step
      for node in presentation.nodes
      if isinstance(
        node.proof_step.conclusion,
        Toda53NuPrimeBracketSpecializationStatement,
      )
    )

    print(
      f"depth={depth} "
      f"nodes={len(presentation.nodes)} "
      f"blocks={len(blocks)} "
      f"arguments={len(arguments)}"
    )
    print(
      "  argument_roles="
      + repr(tuple(
        argument.role.value
        for argument in arguments
      ))
    )
    print(
      f"  bracket_memberships={len(bracket_memberships)} "
      f"bracket_specializations={len(bracket_specializations)}"
    )
    print(
      f"  definition_step_semantics={len(definition_semantics)} "
      f"precondition_semantics={len(precondition_semantics)} "
      f"dependency_semantics={len(sidecar.dependency_semantics)}"
    )

    for semantic in definition_semantics:
      print(
        "  definition: "
        + _describe(semantic.proof_step)
      )

    for semantic in sidecar.dependency_semantics:
      print(
        "  semantic dependency:"
      )
      print(
        "    prerequisite: "
        + _describe(semantic.prerequisite_step)
      )
      print(
        "    dependent:    "
        + _describe(semantic.dependent_step)
      )
      print(
        "    role="
        + semantic.role.value
      )

  print("")
  print("C. Depth-3 definition consumer edge")
  print("-" * 80)
  presentation, sidecar, _, _ = _presentation_data(3)

  definition_ids = {
    id(semantic.proof_step)
    for semantic in sidecar.step_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativeStepSemanticRole
      .DEFINITION_INTRODUCTION
    )
  }

  for edge in presentation.edges:
    if id(edge.premise_step) not in definition_ids:
      continue
    print(
      f"consumer premise_index={edge.premise_index}"
    )
    print(
      "  premise: "
      + _describe(edge.premise_step)
    )
    print(
      "  parent:  "
      + _describe(edge.parent_step)
    )

  print("")
  print("D. Audit conclusion boundary")
  print("-" * 80)
  print(
    "If depth=2 has zero bracket membership / definition semantic "
    "while depth=3 has exactly one, the semantic rule already exists "
    "but cannot act before replay selection includes its endpoint."
  )
  print(
    "No production repair is applied by this audit."
  )

  print("")
  print("=" * 80)
  print("R25-8R1 AUDIT COMPLETE")
  print("=" * 80)


if __name__ == "__main__":
  main()
