from dataclasses import fields, is_dataclass

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
  (4, 6),
  (5, 7),
  (8, 7),
  (9, 7),
)

STRUCTURAL_TYPES = {
  "TodaProp515Pi12_5HopfIsomorphismStatement",
  "Toda515Sigma8TransportedDecompositionStatement",
  "Toda48Pi16_9OrderAndE4InjectiveStatement",
}


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


def _state(n, k):
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
    provenance,
    full_depth,
    presentation,
    blocks,
    arguments,
  )


def _root_argument_index(
  presentation,
  arguments,
):
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


def _root_relation(
  presentation,
  arguments,
  root_index,
):
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
  if not isinstance(
    statement,
    Relation,
  ):
    return None
  if (
    statement.relation_type
    is not RelationType.EQUALITY
  ):
    return None
  if not isinstance(
    statement.lhs,
    TodaPrimaryGroup,
  ):
    return None

  return statement


def _claim_components(group):
  if isinstance(
    group,
    FreeCyclicGroup,
  ):
    return (
      (
        "generator",
        group.generator,
        None,
      ),
    )

  if isinstance(
    group,
    FiniteCyclicGroup,
  ):
    return (
      (
        "generator",
        group.generator,
        group.order,
      ),
      (
        "order",
        group.generator,
        group.order,
      ),
    )

  if isinstance(
    group,
    DirectSumGroup,
  ):
    result = []
    for index, summand in enumerate(
      group.summands
    ):
      if isinstance(
        summand,
        FreeCyclicGroup,
      ):
        result.append(
          (
            f"summand[{index}].generator",
            summand.generator,
            None,
          )
        )
      elif isinstance(
        summand,
        FiniteCyclicGroup,
      ):
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
    return tuple(
      result
    )

  return ()


def _safe_value(value):
  if is_dataclass(
    value
  ):
    return repr(
      value
    )
  if isinstance(
    value,
    (
      tuple,
      list,
      dict,
      set,
      frozenset,
    ),
  ):
    return repr(
      value
    )
  return repr(
    value
  )


def _statement_fields(statement):
  if not is_dataclass(
    statement
  ):
    return ()

  return tuple(
    (
      field.name,
      type(
        getattr(
          statement,
          field.name,
        )
      ).__name__,
      _safe_value(
        getattr(
          statement,
          field.name,
        )
      ),
    )
    for field in fields(
      statement
    )
  )


def _block_map(blocks):
  return {
    id(step): (
      index,
      block.role.value,
    )
    for index, block in enumerate(
      blocks
    )
    for step in block.steps
  }


def _depth_map(provenance):
  return {
    id(
      node.proof_step
    ): node.shortest_depth
    for node in provenance.nodes
  }


def _print_step(
  prefix,
  step,
  depth_by_id,
  block_by_id,
):
  block = block_by_id.get(
    id(step),
    (
      None,
      None,
    ),
  )
  print(
    f"{prefix} "
    f"depth={depth_by_id.get(id(step))} "
    f"block={block} "
    f"statement={type(step.conclusion).__name__}"
  )
  print(
    f"{prefix} rule="
    f"{None if step.inference_rule is None else step.inference_rule.name!r}"
  )
  statement_fields = _statement_fields(
    step.conclusion
  )
  if not statement_fields:
    print(
      f"{prefix} fields=NONE_OR_NON_DATACLASS"
    )
  else:
    for name, type_name, value in statement_fields:
      print(
        f"{prefix} field "
        f"{name}: {type_name} = {value}"
      )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-11 structural provider semantics audit")
  print("=" * 120)
  print(
    "Audit only. Inspect typed fields of known structural provider statements "
    "and the root inference/premises for pi_10^4 and pi_16^9."
  )
  print(
    "No production code, tests, or documents are modified."
  )
  print()

  found_structural_types = set()

  for n, k in TARGETS:
    (
      provenance,
      full_depth,
      presentation,
      blocks,
      arguments,
    ) = _state(
      n,
      k,
    )
    root_index = _root_argument_index(
      presentation,
      arguments,
    )
    relation = _root_relation(
      presentation,
      arguments,
      root_index,
    )
    depth_by_id = _depth_map(
      provenance
    )
    block_by_id = _block_map(
      blocks
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
      print(
        "root_status=UNSUPPORTED"
      )
      print()
      continue

    print(
      f"root_claim={relation!r}"
    )
    print(
      f"claim_components={_claim_components(relation.rhs)!r}"
    )

    root_step = presentation.root_step
    _print_step(
      "ROOT",
      root_step,
      depth_by_id,
      block_by_id,
    )
    print(
      f"ROOT premise_count={len(root_step.premises)}"
    )

    for premise_index, premise in enumerate(
      root_step.premises
    ):
      _print_step(
        f"ROOT.P{premise_index:02d}",
        premise,
        depth_by_id,
        block_by_id,
      )

    print(
      "STRUCTURAL STATEMENTS IN FULL PROVENANCE"
    )

    structural_count = 0
    for node in provenance.nodes:
      step = node.proof_step
      statement_type = type(
        step.conclusion
      ).__name__

      if statement_type not in STRUCTURAL_TYPES:
        continue

      found_structural_types.add(
        statement_type
      )
      structural_count += 1
      _print_step(
        f"STRUCT[{structural_count:02d}]",
        step,
        depth_by_id,
        block_by_id,
      )
      print(
        f"STRUCT[{structural_count:02d}] "
        f"is_root_direct_premise="
        f"{any(step is premise for premise in root_step.premises)}"
      )

    print(
      f"structural_statement_count={structural_count}"
    )

    print(
      "ROOT-DIRECT NON-RELATION SEMANTIC FIELD INVENTORY"
    )
    for premise_index, premise in enumerate(
      root_step.premises
    ):
      if isinstance(
        premise.conclusion,
        Relation,
      ):
        continue

      print(
        f"ROOT.NONREL[{premise_index:02d}] "
        f"type={type(premise.conclusion).__name__}"
      )
      for name, type_name, value in _statement_fields(
        premise.conclusion
      ):
        print(
          f"ROOT.NONREL[{premise_index:02d}] "
          f"field {name}: {type_name} = {value}"
        )

    print()

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    f"found_structural_types={tuple(sorted(found_structural_types))}"
  )
  print(
    f"missing_structural_types="
    f"{tuple(sorted(STRUCTURAL_TYPES - found_structural_types))}"
  )
  print()
  print("=" * 120)
  print("INTERPRETATION GUIDE")
  print("=" * 120)
  print(
    "1. For pi_12^5, inspect TodaProp515Pi12_5HopfIsomorphismStatement fields. "
    "The question is whether its typed data carries the order-two/group claim "
    "without parsing the rule name."
  )
  print(
    "2. For pi_15^8, inspect Toda515Sigma8TransportedDecompositionStatement. "
    "The expected useful field is transported_group, which should encode the "
    "direct-sum generators and finite summand order structurally."
  )
  print(
    "3. For pi_16^9, inspect Toda48Pi16_9OrderAndE4InjectiveStatement. "
    "If its fields contain target group/order/injectivity data, R5-10 missed it "
    "because generator equality was too restrictive, not because proof data was absent."
  )
  print(
    "4. For pi_10^4, inspect ROOT and ROOT.Pxx. If no non-root statement stores "
    "the composite generator/order claim, determine whether the root inference "
    "is integrating lower typed facts directly. That is a representation boundary, "
    "not a reason to parse the rule name."
  )
  print(
    "5. A production provider semantic must be derivable from statement type and "
    "typed fields. Rule-name text is diagnostic output only and must not become "
    "a production classifier."
  )


if __name__ == "__main__":
  main()
