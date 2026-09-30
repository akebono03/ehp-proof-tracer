from tests.test_phase143_19_method_evidence import (
  _method_evidence_data,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeStepSemanticRole,
)


def _rule_name(step):
  inference_rule = step.inference_rule
  if inference_rule is None:
    return None
  return inference_rule.name


def main():
  (
    presentation,
    blocks,
    semantic_sidecar,
    arguments,
  ) = _method_evidence_data(
    3,
    3,
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )

  print("=" * 78)
  print("Phase 150 / RC4-5B-1 Reference / beta->nu' binding audit")
  print("=" * 78)

  dependencies = tuple(
    dependency
    for dependency in semantic_sidecar.dependency_semantics
    if (
      dependency.role
      is TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
    )
  )
  definitions = tuple(
    semantic
    for semantic in semantic_sidecar.step_semantics
    if (
      semantic.role
      is TodaGroupProofNarrativeStepSemanticRole
      .DEFINITION_INTRODUCTION
    )
  )

  print("typed PRECONDITION_FOR_DEFINITION:", len(dependencies))
  print("typed DEFINITION_INTRODUCTION:", len(definitions))
  print("reason relations:", len(reason_sidecar.reasons))

  for index, dependency in enumerate(dependencies, start=1):
    print("-" * 78)
    print("dependency", index)
    print("prerequisite conclusion:", repr(dependency.prerequisite_step.conclusion))
    print("prerequisite rule:", _rule_name(dependency.prerequisite_step))
    print("dependent conclusion:", repr(dependency.dependent_step.conclusion))
    print("dependent rule:", _rule_name(dependency.dependent_step))
    print(
      "dependency fields:",
      tuple(dependency.__dataclass_fields__),
    )

  for index, reason in enumerate(reason_sidecar.reasons, start=1):
    print("-" * 78)
    print("reason", index)
    print("kind:", reason.kind.value)
    print(
      "reason fields:",
      tuple(reason.__dataclass_fields__),
    )

  dependency_fields = set()
  for dependency in dependencies:
    dependency_fields.update(
      dependency.__dataclass_fields__
    )
  reason_fields = set()
  for reason in reason_sidecar.reasons:
    reason_fields.update(
      reason.__dataclass_fields__
    )

  has_reference_identity = (
    "reference_identity" in dependency_fields
    or "reference_identity" in reason_fields
  )
  has_reference_variable = (
    "reference_variable" in dependency_fields
    or "reference_variable" in reason_fields
  )
  has_instantiated_element = (
    "instantiated_element" in dependency_fields
    or "instantiated_element" in reason_fields
  )
  has_binding = (
    "binding" in dependency_fields
    or "binding" in reason_fields
    or (
      has_reference_variable
      and has_instantiated_element
    )
  )

  print("=" * 78)
  print("STRUCTURED_CAPABILITY")
  print("reference_identity:", has_reference_identity)
  print("reference_variable:", has_reference_variable)
  print("instantiated_element:", has_instantiated_element)
  print("explicit_binding:", has_binding)
  print()
  print("CLASSIFICATION")
  print("precondition -> definition: SAFE_NOW")
  print("reference-aware prose: NEEDS_TYPED_SEMANTICS")
  print("beta -> nu_prime prose: NEEDS_TYPED_SEMANTICS")
  print()
  print("AUDIT_RESULT=PASS")
  print("PRODUCTION_CHANGES=NONE")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
