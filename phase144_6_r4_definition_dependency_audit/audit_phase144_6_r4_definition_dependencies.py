from __future__ import annotations

from tests.test_phase143_19_method_evidence import _method_evidence_data
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)


def label(step, index_by_id):
  return f"S{index_by_id[id(step)]:02d}"


def describe(step):
  return repr(step.conclusion)


presentation, blocks, sidecar, arguments = _method_evidence_data(3, 3)

steps = tuple(node.proof_step for node in presentation.nodes)
index_by_id = {id(step): i for i, step in enumerate(steps)}

definition_argument = next(
  argument for argument in arguments
  if argument.role
  is TodaGroupProofNarrativeArgumentRole.ESTABLISH_DEFINITION
)
conclusion = extract_toda_group_proof_narrative_argument_conclusion_step(
  definition_argument
)

local_ids = {
  id(step)
  for block in (
    definition_argument.supporting_blocks
    + (definition_argument.conclusion_block,)
  )
  for step in block.steps
}

print("=" * 110)
print("Phase 144-6-R4 Definition dependency-path audit")
print("=" * 110)
print("definition conclusion:", label(conclusion, index_by_id), describe(conclusion))
print()

print("A. Definition argument blocks")
for block in definition_argument.supporting_blocks:
  print("support block:", block.role)
  for step in block.steps:
    print(" ", label(step, index_by_id), describe(step))
print("conclusion block:", definition_argument.conclusion_block.role)
for step in definition_argument.conclusion_block.steps:
  print(" ", label(step, index_by_id), describe(step))

print()
print("B. ProofStep.premises edges inside/into Definition argument")
for parent in steps:
  if id(parent) not in local_ids:
    continue
  for premise in parent.premises:
    if id(premise) not in index_by_id:
      continue
    print(
      label(premise, index_by_id),
      "->",
      label(parent, index_by_id),
      "|",
      describe(premise),
      "=>",
      describe(parent),
    )

print()
print("C. presentation.edges inside/into Definition argument")
for edge in presentation.edges:
  if id(edge.parent_step) not in local_ids:
    continue
  print(
    label(edge.premise_step, index_by_id),
    "->",
    label(edge.parent_step, index_by_id),
    f"| premise_index={edge.premise_index}",
    "|",
    describe(edge.premise_step),
    "=>",
    describe(edge.parent_step),
  )

print()
print("D. semantic_sidecar.dependency_semantics touching Definition argument")
for semantic in sidecar.dependency_semantics:
  if (
    id(semantic.prerequisite_step) not in local_ids
    and id(semantic.dependent_step) not in local_ids
  ):
    continue
  print(
    label(semantic.prerequisite_step, index_by_id),
    "->",
    label(semantic.dependent_step, index_by_id),
    "| role=",
    semantic.role,
    "|",
    describe(semantic.prerequisite_step),
    "=>",
    describe(semantic.dependent_step),
  )

print()
print("E. One-step protection as CURRENT helper sees it")
direct = tuple(conclusion.premises)
print("conclusion direct premises:")
for step in direct:
  print(" ", label(step, index_by_id), describe(step))
print("premises of those direct premises:")
for step in direct:
  for premise in step.premises:
    if id(premise) in index_by_id:
      print(
        " ",
        label(premise, index_by_id),
        "->",
        label(step, index_by_id),
        describe(premise),
      )

print()
print("F. Presentation-edge predecessors of conclusion direct premises")
direct_ids={id(step) for step in direct}
for edge in presentation.edges:
  if id(edge.parent_step) in direct_ids:
    print(
      " ",
      label(edge.premise_step, index_by_id),
      "->",
      label(edge.parent_step, index_by_id),
      describe(edge.premise_step),
    )

print()
print("G. Semantic predecessors of conclusion / direct premises")
target_ids=direct_ids | {id(conclusion)}
for semantic in sidecar.dependency_semantics:
  if id(semantic.dependent_step) in target_ids:
    print(
      " ",
      label(semantic.prerequisite_step, index_by_id),
      "->",
      label(semantic.dependent_step, index_by_id),
      semantic.role,
      describe(semantic.prerequisite_step),
    )
