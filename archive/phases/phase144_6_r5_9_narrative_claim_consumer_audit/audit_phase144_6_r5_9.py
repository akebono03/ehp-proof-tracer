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


def _group_result(
  n,
  k,
):
  report = build_standard_toda_report(
    n=n,
    k=k,
  )
  return (
    report.candidates[
      0
    ].source_candidate.group_result
  )


def _full_state(
  n,
  k,
):
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
    semantic_sidecar,
    blocks,
    arguments,
  )


def _root_indices(
  presentation,
  arguments,
):
  return tuple(
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


def _root_group_relation(
  presentation,
  arguments,
  root_index,
):
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


def _group_claim_components(
  group,
):
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
    components = []
    for summand_index, summand in enumerate(
      group.summands
    ):
      if isinstance(
        summand,
        FreeCyclicGroup,
      ):
        components.append(
          (
            f"summand[{summand_index}].generator",
            summand.generator,
            None,
          )
        )
        continue

      if isinstance(
        summand,
        FiniteCyclicGroup,
      ):
        components.extend(
          (
            (
              f"summand[{summand_index}].generator",
              summand.generator,
              summand.order,
            ),
            (
              f"summand[{summand_index}].order",
              summand.generator,
              summand.order,
            ),
          )
        )

    return tuple(
      components
    )

  return ()


def _definition_subject(
  argument,
):
  if (
    argument.role
    is not TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    return None

  return (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )


def _order_claim(
  argument,
):
  if (
    argument.role
    is not TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER
  ):
    return None

  subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )
  if subject is None:
    return None

  step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
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
    is not RelationType.ORDER
  ):
    return None

  return (
    subject,
    statement.rhs,
  )


def _claim_matches_argument(
  component,
  argument,
):
  (
    component_kind,
    generator,
    order,
  ) = component

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_DEFINITION
  ):
    subject = _definition_subject(
      argument
    )
    return (
      component_kind.endswith(
        "generator"
      )
      and subject == generator
    )

  if (
    argument.role
    is TodaGroupProofNarrativeArgumentRole
    .ESTABLISH_ORDER
  ):
    order_claim = _order_claim(
      argument
    )
    if order_claim is None:
      return False

    (
      subject,
      claimed_order,
    ) = order_claim
    return (
      component_kind.endswith(
        "order"
      )
      and subject == generator
      and claimed_order == order
    )

  return False


def _argument_signature(
  argument,
):
  subject = (
    extract_toda_group_proof_narrative_argument_purpose_subject(
      argument
    )
  )
  step = (
    extract_toda_group_proof_narrative_argument_conclusion_step(
      argument
    )
  )
  statement_type = (
    None
    if step is None
    else type(
      step.conclusion
    ).__name__
  )
  return (
    argument.role.value,
    repr(
      subject
    ),
    statement_type,
  )


def _safe_repr(
  value,
):
  return repr(
    value
  )


def main():
  print("=" * 120)
  print("Phase 144-6-R5-9 Narrative claim-consumer audit")
  print("=" * 120)
  print(
    "Audit only: derive semantic claim components directly from the final "
    "root group-structure claim, then compare those components with "
    "Definition and Order Argument conclusions."
  )
  print(
    "No production selection rule is implemented."
  )
  print()

  total_claim_components = 0
  total_matched_components = 0
  total_matching_arguments = 0
  total_unmatched_components = 0
  total_duplicate_component_matches = 0

  for n, k in TARGETS:
    (
      provenance,
      full_depth,
      presentation,
      semantic_sidecar,
      blocks,
      arguments,
    ) = _full_state(
      n,
      k,
    )
    roots = _root_indices(
      presentation,
      arguments,
    )

    print("-" * 120)
    print(
      f"TARGET n={n}, k={k} "
      f"full_depth={full_depth} "
      f"arguments={len(arguments)} "
      f"roots={roots}"
    )
    print("-" * 120)

    if len(
      roots
    ) != 1:
      print(
        "root_status=UNSUPPORTED "
        f"root_count={len(roots)}"
      )
      print()
      continue

    root_index = roots[
      0
    ]
    relation = _root_group_relation(
      presentation,
      arguments,
      root_index,
    )

    if relation is None:
      print(
        "root_status=UNSUPPORTED_ROOT_CLAIM"
      )
      print()
      continue

    components = _group_claim_components(
      relation.rhs
    )
    total_claim_components += len(
      components
    )

    print(
      f"root_target={_safe_repr(relation.lhs)}"
    )
    print(
      f"root_group={_safe_repr(relation.rhs)}"
    )
    print(
      f"claim_component_count={len(components)}"
    )

    matched_argument_indices = set()

    for component_index, component in enumerate(
      components
    ):
      (
        component_kind,
        generator,
        order,
      ) = component

      matches = tuple(
        argument_index
        for argument_index, argument in enumerate(
          arguments
        )
        if _claim_matches_argument(
          component,
          argument,
        )
      )

      if matches:
        total_matched_components += 1
      else:
        total_unmatched_components += 1

      if len(
        matches
      ) > 1:
        total_duplicate_component_matches += 1

      matched_argument_indices.update(
        matches
      )

      print(
        f"C{component_index:02d} "
        f"kind={component_kind} "
        f"generator={_safe_repr(generator)} "
        f"order={_safe_repr(order)}"
      )
      print(
        f"  matching_arguments={matches}"
      )
      for argument_index in matches:
        print(
          f"    A{argument_index:02d} "
          f"signature={_argument_signature(arguments[argument_index])}"
        )

    total_matching_arguments += len(
      matched_argument_indices
    )

    unmatched_order_definition_indices = tuple(
      argument_index
      for argument_index, argument in enumerate(
        arguments
      )
      if (
        argument.role
        in (
          TodaGroupProofNarrativeArgumentRole
          .ESTABLISH_ORDER,
          TodaGroupProofNarrativeArgumentRole
          .ESTABLISH_DEFINITION,
        )
        and argument_index
        not in matched_argument_indices
      )
    )

    print(
      f"claim_matched_argument_indices="
      f"{tuple(sorted(matched_argument_indices))}"
    )
    print(
      f"unmatched_order_definition_count="
      f"{len(unmatched_order_definition_indices)}"
    )

    preview = unmatched_order_definition_indices[
      :12
    ]
    print(
      f"unmatched_order_definition_preview={preview}"
    )
    for argument_index in preview:
      print(
        f"    A{argument_index:02d} "
        f"signature={_argument_signature(arguments[argument_index])}"
      )

    print()

  print("=" * 120)
  print("SUMMARY")
  print("=" * 120)
  print(
    f"total_claim_components={total_claim_components}"
  )
  print(
    f"matched_claim_components={total_matched_components}"
  )
  print(
    f"unmatched_claim_components={total_unmatched_components}"
  )
  print(
    f"total_matching_arguments={total_matching_arguments}"
  )
  print(
    f"components_with_duplicate_argument_matches="
    f"{total_duplicate_component_matches}"
  )
  print()
  print("=" * 120)
  print("INTERPRETATION GUIDE")
  print("=" * 120)
  print(
    "1. A claim component comes only from the final root group structure: "
    "generator and, for finite cyclic summands, its order."
  )
  print(
    "2. A Definition Argument matches only a generator component whose "
    "generator equals the Definition purpose subject."
  )
  print(
    "3. An Order Argument matches only an order component whose generator "
    "and order equal the Argument's ORDER conclusion."
  )
  print(
    "4. A promising result is that pi_6^3 selects the Definition and Order "
    "Arguments for nu-prime while excluding definitions/orders of elements "
    "that merely occur in intermediate calculations."
  )
  print(
    "5. Duplicate matches are important. If many historical Arguments prove "
    "the same final claim component, claim matching identifies the correct "
    "semantic subject but does not yet choose the correct proof occurrence."
  )
  print(
    "6. If duplicates dominate, the next audit should choose among duplicate "
    "claim providers by provenance proximity / direct claim consumption, "
    "rather than weakening the claim-component criterion."
  )
  print(
    "7. This audit intentionally does not treat every element appearing in "
    "the final proof as a Narrative claim."
  )


if __name__ == "__main__":
  main()
