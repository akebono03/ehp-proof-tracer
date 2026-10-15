from collections import deque

from barratt_hilton_rules import (
  HomotopyGroupMembershipStatement,
)
from expression import (
  HomotopyElement,
)
from proof import (
  ProofStep,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_arguments import (
  _argument_direct_dependency_indices,
  build_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_blocks import (
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
from toda_proof_dependency import (
  TodaProofDependencyRole,
  extract_toda_recursive_proof_provenance,
)
from toda_rules import (
  TodaNuFamilyDefinitionStatement,
)
from toda_upstream_bootstrap import (
  build_toda_53_nu_prime_steps,
  build_toda_prop56_upstream_core,
)


def _render_step(step):
  rendered = _render_generic_narrative_step(step)
  if rendered:
    return rendered
  return type(step.conclusion).__name__


def _describe_step(step):
  return (
    f"id={id(step)} "
    f"type={type(step.conclusion).__name__} "
    f"rule={step.rule.value if hasattr(step.rule, 'value') else step.rule} "
    f"text={_render_step(step)!r}"
  )


def _contains_nu_prime(
  value,
  visited=None,
):
  if visited is None:
    visited = set()

  if isinstance(value, HomotopyElement):
    return value.name in ("ν′", "ν'", "nu_prime")

  if isinstance(value, str):
    return "ν′" in value or "ν'" in value or "nu_prime" in value

  if isinstance(value, (int, float, bool, type(None))):
    return False

  value_id = id(value)
  if value_id in visited:
    return False
  visited.add(value_id)

  if isinstance(value, (tuple, list)):
    return any(
      _contains_nu_prime(
        item,
        visited,
      )
      for item in value
    )

  if hasattr(value, "__dict__"):
    return any(
      _contains_nu_prime(
        item,
        visited,
      )
      for item in vars(value).values()
    )

  return False


def _is_pi5_3_relation(step):
  text = _render_step(step).replace(" ", "")
  return (
    type(step.conclusion).__name__ == "Relation"
    and r"\pi_{5}^{3}" in text
    and r"\mathbb{Z}/2" in text
  )


def _all_paths_to_target(
  dependencies,
  start,
  target,
):
  paths = []

  def visit(node, path, active):
    if node == target:
      paths.append(tuple(path))
      return

    if node in active:
      return

    next_active = active | {node}
    for dependency in dependencies[node]:
      visit(
        dependency,
        path + [dependency],
        next_active,
      )

  visit(start, [start], set())
  return tuple(paths)


def _build_depth2():
  report = build_standard_toda_report(n=3, k=3)
  group_result = report.candidates[0].source_candidate.group_result
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(replay)
  sidecar = build_toda_group_proof_narrative_semantic_sidecar(
    presentation
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
  dependencies = _argument_direct_dependency_indices(
    presentation,
    blocks,
    sidecar,
  )
  return (
    group_result,
    presentation,
    sidecar,
    blocks,
    arguments,
    dependencies,
  )


def main():
  print("=" * 80)
  print("Phase 144-6 R25-7 root construction + exact block-path audit")
  print("Production changes: none")
  print("=" * 80)

  print("")
  print("A. Direct nu-prime upstream construction")
  print("-" * 80)
  membership_step, hopf_step, double_step = (
    build_toda_53_nu_prime_steps()
  )
  upstream = build_toda_prop56_upstream_core()

  returned_steps = (
    ("membership", membership_step),
    ("hopf", hopf_step),
    ("double", double_step),
  )
  for name, step in returned_steps:
    print(f"{name}: {_describe_step(step)}")
    print(
      "  premise_types="
      + repr(tuple(
        type(premise.conclusion).__name__
        for premise in step.premises
      ))
    )
    print(
      "  direct_definition_premise="
      + str(any(
        isinstance(
          premise.conclusion,
          TodaNuFamilyDefinitionStatement,
        )
        for premise in step.premises
      ))
    )

  print("")
  print("upstream core identity correspondence:")
  for key in (
    "membership_step",
    "hopf_nu_prime_step",
    "double_step",
  ):
    step = upstream[key]
    print(
      f"  {key}: {_describe_step(step)}"
    )

  print("")
  print("B. Nu-prime definition search in complete root provenance")
  print("-" * 80)
  (
    group_result,
    presentation,
    sidecar,
    blocks,
    arguments,
    dependencies,
  ) = _build_depth2()
  provenance = extract_toda_recursive_proof_provenance(
    group_result
  )

  definition_nodes = tuple(
    node
    for node in provenance.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaNuFamilyDefinitionStatement,
    )
  )
  nu_prime_nodes = tuple(
    node
    for node in provenance.nodes
    if _contains_nu_prime(node.proof_step.conclusion)
  )

  print(f"provenance_nodes={len(provenance.nodes)}")
  print(f"nu_family_definition_nodes={len(definition_nodes)}")
  print(f"nu_prime_related_nodes={len(nu_prime_nodes)}")
  for node in nu_prime_nodes:
    print(
      f"  depth={node.shortest_depth} "
      f"role={node.role.value} "
      + _describe_step(node.proof_step)
    )

  print("")
  print("C. Exact block membership")
  print("-" * 80)
  block_index_by_step_id = {}
  duplicate_memberships = []
  for block_index, block in enumerate(blocks):
    for step in block.steps:
      step_id = id(step)
      if step_id in block_index_by_step_id:
        duplicate_memberships.append(
          (
            step_id,
            block_index_by_step_id[step_id],
            block_index,
          )
        )
      block_index_by_step_id[step_id] = block_index

  print(f"blocks={len(blocks)}")
  print(f"duplicate_step_memberships={duplicate_memberships}")

  pi5_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if _is_pi5_3_relation(node.proof_step)
  )
  print(f"pi5_3_relation_steps={len(pi5_steps)}")

  for step in pi5_steps:
    block_index = block_index_by_step_id[id(step)]
    block = blocks[block_index]
    print(
      f"pi5_3 step={id(step)} block=B{block_index:02d} "
      f"role={block.role.value}"
    )
    print("  " + _describe_step(step))

  print("")
  print("D. Production direct block dependencies")
  print("-" * 80)
  for dependent_index, prerequisite_indices in enumerate(
    dependencies
  ):
    if not prerequisite_indices:
      continue
    print(
      f"B{dependent_index:02d}({blocks[dependent_index].role.value})"
      " <- "
      + ", ".join(
        f"B{index:02d}({blocks[index].role.value})"
        for index in prerequisite_indices
      )
    )

  print("")
  print("E. Exact pi_5^3 paths into each Argument")
  print("-" * 80)
  pi5_block_indices = tuple(
    block_index_by_step_id[id(step)]
    for step in pi5_steps
  )

  for argument_index, argument in enumerate(arguments):
    conclusion_index = next(
      index
      for index, block in enumerate(blocks)
      if block is argument.conclusion_block
    )
    local_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        sidecar,
        arguments,
        argument_index,
      )
    )
    local_indices = tuple(
      next(
        index
        for index, candidate in enumerate(blocks)
        if candidate is block
      )
      for block in local_blocks
    )
    print(
      f"A{argument_index:02d} role={argument.role.value} "
      f"conclusion=B{conclusion_index:02d} "
      f"local={local_indices}"
    )

    for pi5_index in pi5_block_indices:
      paths = _all_paths_to_target(
        dependencies,
        conclusion_index,
        pi5_index,
      )
      print(
        f"  target=B{pi5_index:02d} "
        f"in_local={pi5_index in local_indices} "
        f"path_count={len(paths)}"
      )
      for path_number, path in enumerate(paths, start=1):
        print(
          f"    path[{path_number}]="
          + " -> ".join(
            f"B{index:02d}({blocks[index].role.value})"
            for index in path
          )
        )

  print("")
  print("F. Proof and semantic edges touching the pi_5^3 block")
  print("-" * 80)
  pi5_ids = {id(step) for step in pi5_steps}
  for edge in presentation.edges:
    if (
      id(edge.parent_step) in pi5_ids
      or id(edge.premise_step) in pi5_ids
    ):
      parent_block = block_index_by_step_id[
        id(edge.parent_step)
      ]
      premise_block = block_index_by_step_id[
        id(edge.premise_step)
      ]
      print(
        f"proof: B{parent_block:02d} "
        f"-- premise[{edge.premise_index}] --> "
        f"B{premise_block:02d}"
      )
      print("  parent  " + _describe_step(edge.parent_step))
      print("  premise " + _describe_step(edge.premise_step))

  for semantic in sidecar.dependency_semantics:
    if (
      id(semantic.dependent_step) in pi5_ids
      or id(semantic.prerequisite_step) in pi5_ids
    ):
      dependent_block = block_index_by_step_id[
        id(semantic.dependent_step)
      ]
      prerequisite_block = block_index_by_step_id[
        id(semantic.prerequisite_step)
      ]
      print(
        f"semantic: B{dependent_block:02d} "
        f"<-- B{prerequisite_block:02d}"
      )
      print(
        "  dependent    "
        + _describe_step(semantic.dependent_step)
      )
      print(
        "  prerequisite "
        + _describe_step(semantic.prerequisite_step)
      )

  print("")
  print("=" * 80)
  print("R25-7 AUDIT COMPLETE")
  print("No production repair was applied.")
  print("=" * 80)


if __name__ == "__main__":
  main()
