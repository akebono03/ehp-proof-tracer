from collections import deque

from homotopy_groups import (
  DirectSumGroup,
  FiniteCyclicGroup,
  FreeCyclicGroup,
  TodaPrimaryGroup,
)
from proof import (
  Relation,
  RelationType,
)
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgumentRole,
  build_toda_group_proof_narrative_arguments,
  extract_toda_group_proof_narrative_argument_conclusion_step,
  extract_toda_group_proof_narrative_argument_purpose_subject,
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
  extract_toda_recursive_proof_provenance,
)


TARGETS = (
  (3, 3),
  (5, 3),
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)


def _group_result(n, k):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _full_state(n, k):
  group_result = _group_result(
    n,
    k,
  )
  provenance = (
    extract_toda_recursive_proof_provenance(
      group_result
    )
  )
  full_depth = max(
    node.shortest_depth
    for node in provenance.nodes
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=full_depth,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      presentation
    )
  )
  blocks = build_toda_group_proof_narrative_blocks(
    presentation,
    semantic_sidecar=semantic_sidecar,
  )
  arguments = build_toda_group_proof_narrative_arguments(
    presentation,
    blocks,
    semantic_sidecar=semantic_sidecar,
  )
  return (
    provenance,
    full_depth,
    presentation,
    blocks,
    arguments,
  )


def _root_index(presentation, arguments):
  roots = tuple(
    index
    for index, argument in enumerate(
      arguments
    )
    if (
      argument.role
      is TodaGroupProofNarrativeArgumentRole
      .ESTABLISH_GROUP_STRUCTURE
      and any(
        step is presentation.root_step
        for step in argument.conclusion_block.steps
      )
    )
  )
  if len(roots) != 1:
    return None
  return roots[0]


def _root_relation(presentation, arguments, root_index):
  if root_index is None:
    return None
  step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      arguments[
        root_index
      ]
    )
  )
  if step is None:
    return None
  statement = step.conclusion
  if not isinstance(statement, Relation):
    return None
  if statement.relation_type is not RelationType.EQUALITY:
    return None
  if not isinstance(statement.lhs, TodaPrimaryGroup):
    return None
  return statement


def _claim_components(group):
  if isinstance(group, FreeCyclicGroup):
    return (
      ("generator", group.generator, None),
    )

  if isinstance(group, FiniteCyclicGroup):
    return (
      ("generator", group.generator, group.order),
      ("order", group.generator, group.order),
    )

  if isinstance(group, DirectSumGroup):
    result = []
    for index, summand in enumerate(group.summands):
      if isinstance(summand, FreeCyclicGroup):
        result.append(
          (
            f"summand[{index}].generator",
            summand.generator,
            None,
          )
        )
      elif isinstance(summand, FiniteCyclicGroup):
        result.extend(
          (
            (
              f"summand[{index}].generator",
              summand.generator,
              summand.order,
            ),
            (
              f"summand[{index}].order",
              summand.generator,
              summand.order,
            ),
          )
        )
    return tuple(result)

  return ()


def _contains_value(value, target, seen=None):
  if value == target:
    return True

  if value is None:
    return False

  if seen is None:
    seen = set()

  value_id = id(value)
  if value_id in seen:
    return False
  seen.add(value_id)

  if isinstance(
    value,
    (
      str,
      bytes,
      int,
      float,
      bool,
    ),
  ):
    return False

  if isinstance(value, dict):
    return any(
      _contains_value(key, target, seen)
      or _contains_value(item, target, seen)
      for key, item in value.items()
    )

  if isinstance(
    value,
    (
      tuple,
      list,
      set,
      frozenset,
    ),
  ):
    return any(
      _contains_value(item, target, seen)
      for item in value
    )

  fields = getattr(
    value,
    "__dataclass_fields__",
    None,
  )
  if fields is not None:
    return any(
      _contains_value(
        getattr(value, field_name),
        target,
        seen,
      )
      for field_name in fields
    )

  return False


def _step_claim_signal(step, component):
  kind, generator, order = component
  statement = step.conclusion

  contains_generator = _contains_value(
    statement,
    generator,
  )
  contains_order = (
    order is not None
    and _contains_value(
      statement,
      order,
    )
  )

  exact_order = (
    isinstance(statement, Relation)
    and statement.relation_type is RelationType.ORDER
    and statement.lhs == generator
    and statement.rhs == order
  )

  exact_group_generator = False
  exact_group_order = False

  if (
    isinstance(statement, Relation)
    and statement.relation_type is RelationType.EQUALITY
    and isinstance(statement.lhs, TodaPrimaryGroup)
  ):
    for candidate in _claim_components(statement.rhs):
      candidate_kind, candidate_generator, candidate_order = candidate
      if (
        candidate_generator == generator
        and candidate_kind.endswith("generator")
      ):
        exact_group_generator = True
      if (
        candidate_generator == generator
        and candidate_order == order
        and candidate_kind.endswith("order")
      ):
        exact_group_order = True

  if kind.endswith("generator"):
    strong = exact_group_generator
  else:
    strong = exact_order or exact_group_order

  return {
    "contains_generator": contains_generator,
    "contains_order": contains_order,
    "exact_order": exact_order,
    "exact_group_generator": exact_group_generator,
    "exact_group_order": exact_group_order,
    "strong": strong,
  }


def _block_by_step_id(blocks):
  return {
    id(step): (
      block_index,
      block.role.value,
    )
    for block_index, block in enumerate(blocks)
    for step in block.steps
  }


def _depth_by_step_id(provenance):
  return {
    id(node.proof_step): node.shortest_depth
    for node in provenance.nodes
  }


def _paths_from_root(presentation):
  children = {}
  for edge in presentation.edges:
    children.setdefault(
      id(edge.parent_step),
      [],
    ).append(
      edge.premise_step
    )

  root = presentation.root_step
  paths = {
    id(root): (
      root,
    )
  }
  pending = deque(
    (
      premise,
      (
        root,
        premise,
      ),
    )
    for premise in children.get(
      id(root),
      (),
    )
  )

  while pending:
    step, path = pending.popleft()
    step_id = id(step)
    if step_id in paths:
      continue
    paths[step_id] = path
    for premise in children.get(
      step_id,
      (),
    ):
      pending.append(
        (
          premise,
          path + (
            premise,
          ),
        )
      )

  return paths


def _provider_class(step, block_role, signal):
  statement = step.conclusion

  if signal["exact_order"]:
    return "EXACT_ORDER"

  if (
    signal["exact_group_generator"]
    or signal["exact_group_order"]
  ):
    if step is not None and block_role == "target":
      return "ROOT_GROUP_STRUCTURE"
    return "GROUP_STRUCTURE"

  if block_role == "definition":
    return "DEFINITION"

  if block_role == "calculation":
    return "CALCULATION_OR_COMPOSITION"

  if block_role == "reference":
    return "REFERENCE_THEOREM"

  if block_role == "map_property":
    return "MAP_OR_TRANSPORT"

  if block_role == "exactness":
    return "EXACTNESS"

  if block_role == "membership":
    return "MEMBERSHIP"

  if block_role == "other":
    return "OTHER_STATEMENT"

  return block_role.upper()


def main():
  print("=" * 120)
  print("Phase 144-6-R5-10 Narrative claim-provider classification audit")
  print("=" * 120)
  print(
    "Audit only. For each final claim component, inspect the root-to-premise "
    "provenance and classify candidate provider statements by block role and "
    "statement type."
  )
  print(
    "No production selection rule is implemented."
  )
  print()

  summary = {}

  for n, k in TARGETS:
    (
      provenance,
      full_depth,
      presentation,
      blocks,
      arguments,
    ) = _full_state(
      n,
      k,
    )
    root_index = _root_index(
      presentation,
      arguments,
    )
    relation = _root_relation(
      presentation,
      arguments,
      root_index,
    )

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"arguments={len(arguments)} "
      f"root_index={root_index}"
    )
    print("-" * 120)

    if relation is None:
      print("root_status=UNSUPPORTED")
      print()
      continue

    components = _claim_components(
      relation.rhs
    )
    depth_by_id = _depth_by_step_id(
      provenance
    )
    block_by_id = _block_by_step_id(
      blocks
    )
    paths = _paths_from_root(
      presentation
    )

    for component_index, component in enumerate(
      components
    ):
      kind, generator, order = component
      print(
        f"C{component_index:02d} "
        f"kind={kind} "
        f"generator={generator!r} "
        f"order={order!r}"
      )

      candidates = []

      for node in provenance.nodes:
        step = node.proof_step
        step_id = id(step)

        if step_id not in paths:
          continue

        signal = _step_claim_signal(
          step,
          component,
        )

        if not signal[
          "contains_generator"
        ]:
          continue

        block_info = block_by_id.get(
          step_id
        )
        if block_info is None:
          continue

        block_index, block_role = block_info
        provider_class = _provider_class(
          step,
          block_role,
          signal,
        )
        path = paths[
          step_id
        ]

        candidates.append(
          (
            node.shortest_depth,
            len(path) - 1,
            provider_class,
            block_role,
            type(step.conclusion).__name__,
            signal,
            step,
            block_index,
          )
        )

      candidates.sort(
        key=lambda item: (
          item[0],
          item[1],
          item[2],
          item[4],
        )
      )

      non_root_candidates = tuple(
        item
        for item in candidates
        if item[6] is not presentation.root_step
      )
      strong_non_root = tuple(
        item
        for item in non_root_candidates
        if item[5]["strong"]
      )
      first_depth = (
        None
        if not non_root_candidates
        else non_root_candidates[0][0]
      )
      nearest = tuple(
        item
        for item in non_root_candidates
        if item[0] == first_depth
      )

      print(
        f"  non_root_candidate_count={len(non_root_candidates)}"
      )
      print(
        f"  strong_non_root_count={len(strong_non_root)}"
      )
      print(
        f"  nearest_non_root_depth={first_depth}"
      )

      display = (
        strong_non_root[:8]
        if strong_non_root
        else nearest[:8]
      )

      if not display:
        print(
          "  provider_status=NO_NON_ROOT_PROVIDER_CANDIDATE"
        )
        summary[
          "NO_NON_ROOT_PROVIDER_CANDIDATE"
        ] = summary.get(
          "NO_NON_ROOT_PROVIDER_CANDIDATE",
          0,
        ) + 1
        continue

      classes = []
      for (
        depth,
        path_length,
        provider_class,
        block_role,
        statement_type,
        signal,
        step,
        block_index,
      ) in display:
        classes.append(
          provider_class
        )
        print(
          f"  provider class={provider_class} "
          f"depth={depth} "
          f"path_len={path_length} "
          f"block=B{block_index:03d}:{block_role} "
          f"statement={statement_type}"
        )
        print(
          "    "
          f"exact_order={signal['exact_order']} "
          f"exact_group_generator={signal['exact_group_generator']} "
          f"exact_group_order={signal['exact_group_order']} "
          f"contains_order={signal['contains_order']}"
        )
        rule = step.inference_rule
        print(
          f"    rule={None if rule is None else rule.name!r}"
        )

      class_key = "|".join(
        sorted(
          set(classes)
        )
      )
      summary[
        class_key
      ] = summary.get(
        class_key,
        0,
      ) + 1

    print()

  print("=" * 120)
  print("SUMMARY BY DISPLAYED PROVIDER CLASS SET")
  print("=" * 120)
  for key in sorted(summary):
    print(
      f"{key}: {summary[key]}"
    )
  print()
  print("=" * 120)
  print("INTERPRETATION GUIDE")
  print("=" * 120)
  print(
    "1. R5-9 claim components remain the starting point. This audit does not "
    "broaden the final claims to every element seen in the proof."
  )
  print(
    "2. Strong providers are exact ORDER claims or non-root group-structure "
    "claims containing the same final generator/order."
  )
  print(
    "3. If no strong non-root provider exists, the audit prints the nearest "
    "non-root statements containing the final generator. Their block role, "
    "statement type, and inference rule show what provider category is missing."
  )
  print(
    "4. CALCULATION_OR_COMPOSITION suggests a derived/composite generator "
    "provider. MAP_OR_TRANSPORT suggests suspension/transport. "
    "REFERENCE_THEOREM or GROUP_STRUCTURE suggests the final component is "
    "guaranteed by a theorem-level structural fact rather than an independent "
    "Definition/Order Argument."
  )
  print(
    "5. Do not implement provider selection from this output unless the six "
    "representative groups exhibit a small, coherent set of generic categories."
  )


if __name__ == "__main__":
  main()
