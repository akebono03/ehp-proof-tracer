from collections import deque
from dataclasses import (
  fields,
  is_dataclass,
  replace,
)

from expression import (
  ScalarSum,
  ScalarSymbol,
)
from homotopy_groups import (
  TodaPrimaryGroup,
  TodaPrimaryGroupZeroStatement,
)

from proof import (
  ProofStep,
  Relation,
  RelationType,
)
from scalar_rules import (
  ScalarGreaterEqualStatement,
)
from toda_group_proof_generic_narrative_renderer import (
  _generic_short_exact_sequence_latex,
  _generic_short_exact_sequence_reason_prose,
  _render_generic_narrative_step,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
  render_toda_expression_latex,
)
from toda_group_proof_narrative_argument_discourse import (
  TodaGroupProofNarrativeArgumentDiscourseRole,
  classify_toda_group_proof_narrative_argument_discourse_roles,
)
from toda_group_proof_narrative_argument_local_body import (
  extract_toda_group_proof_narrative_argument_local_body_blocks,
)
from toda_group_proof_narrative_argument_multi_renderer import (
  render_toda_group_proof_narrative_multi_argument_markdown,
)
from toda_group_proof_narrative_argument_ordering import (
  order_toda_group_proof_narrative_arguments,
)
from toda_group_proof_narrative_argument_renderer import (
  render_toda_group_proof_narrative_argument_purpose_sentence,
)
from toda_group_proof_narrative_arguments import (
  TodaGroupProofNarrativeArgument,
  extract_toda_group_proof_narrative_argument_conclusion_step,
)
from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeBlock,
)
from toda_group_proof_narrative_contribution_ordering import (
  TodaGroupProofNarrativeContributionPlacement,
  build_toda_group_proof_narrative_ordered_contributions,
)
from toda_group_proof_narrative_hidden_bridge_semantics import (
  TodaGroupProofNarrativeHiddenBridgeOperationKind,
  TodaGroupProofNarrativeHiddenBridgeSemanticRole,
  build_toda_group_proof_narrative_hidden_bridge_semantics,
)
from toda_group_proof_narrative_proof_chains import (
  build_toda_group_proof_narrative_proof_chains,
)
from toda_group_proof_narrative_reason_renderer import (
  insert_toda_group_proof_narrative_reason_prose,
  order_toda_group_proof_narrative_injective_image_order_reason,
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  extract_toda_group_proof_step_literature_reference,
  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary,
  filter_toda_group_proof_narrative_reference_entries_by_body_usage,
  filter_toda_group_proof_narrative_reference_entries_by_step_usage,
  restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage,
  render_toda_group_proof_narrative_reference_entries_markdown,
  select_toda_group_proof_narrative_reference_statement_steps,
)
from toda_group_proof_narrative_semantics import (
  TodaGroupProofNarrativeDependencySemanticRole,
  TodaGroupProofNarrativeSemanticSidecar,
)
from toda_group_proof_presentation import (
  TodaGroupProofPresentation,
)
from toda_proof_narrative_renderer import (
  render_toda_primary_group_latex,
)
from toda_proof_dependency import (
  TodaProofDependencyRole,
  classify_toda_proof_step_role,
)
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
)


def _provider_anchor_index(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  provider_keys: tuple[
    tuple[str, int],
    ...,
  ],
) -> int | None:
  block_by_id = {
    id(block): block
    for block in blocks
  }
  anchor_indices = []

  for provider_kind, provider_id in provider_keys:
    if provider_kind != "block":
      continue

    block = block_by_id.get(
      provider_id
    )
    if block is None:
      continue

    for proof_step in block.steps:
      line = _render_generic_narrative_step(
        proof_step
      )
      if not line:
        continue

      line_index = markdown.find(
        line
      )
      if line_index < 0:
        continue

      anchor_indices.append(
        line_index + len(line)
      )

  if not anchor_indices:
    return None

  return max(
    anchor_indices
  )


def _argument_fallback_anchor_index(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  argument: TodaGroupProofNarrativeArgument,
  contributions,
) -> int | None:
  purpose = (
    render_toda_group_proof_narrative_argument_purpose_sentence(
      argument
    )
  )

  if purpose is None:
    return None

  purpose_index = markdown.find(
    purpose
  )

  if purpose_index < 0:
    return None

  provider_anchor_indices = tuple(
    anchor_index
    for contribution in contributions
    for anchor_index in (
      _provider_anchor_index(
        markdown,
        blocks,
        contribution.provider_keys,
      ),
    )
    if anchor_index is not None
  )

  if provider_anchor_indices:
    return max(
      provider_anchor_indices
    )

  return (
    purpose_index
    + len(
      purpose
    )
  )


def _contribution_insertion_indices(
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> tuple[
  tuple[
    int | None,
    ...,
  ],
  ...,
]:
  result = []

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    if not contributions:
      result.append(())
      continue

    argument = arguments[
      argument_index
    ]
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )
    conclusion_index = None

    if conclusion_step is not None:
      conclusion_line = (
        _render_generic_narrative_step(
          conclusion_step
        )
      )
      candidate_index = markdown.find(
        conclusion_line
      )

      if candidate_index >= 0:
        conclusion_index = candidate_index

        prefix = markdown[
          :conclusion_index
        ].rstrip()
        previous_paragraph_start = (
          prefix.rfind(
            "\n\n"
          )
          + 2
        )
        previous_paragraph = prefix[
          previous_paragraph_start:
        ].strip()
        standalone_conclusion_connectors = {
          "以上より,",
          "したがって,",
          "これより,",
          "これらより,",
        }

        if (
          previous_paragraph
          in standalone_conclusion_connectors
        ):
          conclusion_index = (
            previous_paragraph_start
          )

    if conclusion_index is None:
      conclusion_index = (
        _argument_fallback_anchor_index(
          markdown,
          blocks,
          argument,
          contributions,
        )
      )

    if conclusion_index is None:
      result.append(
        tuple(
          None
          for _ in contributions
        )
      )
      continue

    indices = [
      None
      for _ in contributions
    ]

    for contribution_index, contribution in enumerate(
      contributions
    ):
      if (
        contribution.placement
        is TodaGroupProofNarrativeContributionPlacement
        .AT_PROVIDER_ANCHOR
      ):
        anchor_index = _provider_anchor_index(
          markdown,
          blocks,
          contribution.provider_keys,
        )
        indices[
          contribution_index
        ] = (
          conclusion_index
          if anchor_index is None
          else min(
            anchor_index,
            conclusion_index,
          )
        )
        continue

      if (
        contribution.placement
        is TodaGroupProofNarrativeContributionPlacement
        .BEFORE_ARGUMENT_CONCLUSION
      ):
        indices[
          contribution_index
        ] = conclusion_index

    for contribution_index in range(
      len(contributions) - 1,
      -1,
      -1,
    ):
      contribution = contributions[
        contribution_index
      ]
      if (
        contribution.placement
        is not TodaGroupProofNarrativeContributionPlacement
        .BEFORE_DEPENDENT_CONTRIBUTION
      ):
        continue

      dependent_index = next(
        (
          indices[index]
          for index in range(
            contribution_index + 1,
            len(contributions),
          )
          if indices[index] is not None
        ),
        conclusion_index,
      )
      indices[
        contribution_index
      ] = dependent_index

    result.append(
      tuple(
        indices
      )
    )

  return tuple(
    result
  )

def _direct_contribution_dependency_pairs(
  presentation: TodaGroupProofPresentation,
  ordered_contributions,
) -> frozenset[
  tuple[
    int,
    int,
  ]
]:
  contribution_step_ids = {
    id(contribution.proof_step)
    for contributions in ordered_contributions
    for contribution in contributions
  }

  return frozenset(
    (
      id(edge.premise_step),
      id(edge.parent_step),
    )
    for edge in presentation.edges
    if (
      id(edge.premise_step)
      in contribution_step_ids
      and id(edge.parent_step)
      in contribution_step_ids
    )
  )


def _shortest_path_between_steps(
  presentation: TodaGroupProofPresentation,
  source_step,
  target_step,
):
  children = {}

  for edge in presentation.edges:
    children.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  source_id = id(
    source_step
  )
  target_id = id(
    target_step
  )
  queue = deque(
    [
      source_step,
    ]
  )
  predecessor = {}
  visited = {
    source_id,
  }

  while queue:
    current = queue.popleft()

    if id(
      current
    ) == target_id:
      break

    for child in children.get(
      id(
        current
      ),
      (),
    ):
      child_id = id(
        child
      )

      if child_id in visited:
        continue

      visited.add(
        child_id
      )
      predecessor[
        child_id
      ] = current
      queue.append(
        child
      )

  if target_id not in visited:
    return ()

  reversed_path = [
    target_step,
  ]
  current = target_step

  while id(
    current
  ) != source_id:
    current = predecessor[
      id(
        current
      )
    ]
    reversed_path.append(
      current
    )

  return tuple(
    reversed(
      reversed_path
    )
  )


def _transport_chain_connector(
  presentation: TodaGroupProofPresentation,
  source_step,
  target_step,
) -> str | None:
  path = _shortest_path_between_steps(
    presentation,
    source_step,
    target_step,
  )

  if len(
    path
  ) != 5:
    return None

  hidden_steps = path[
    1:-1
  ]
  semantic_by_step_id = {
    id(
      semantic.proof_step
    ): semantic
    for semantic in (
      build_toda_group_proof_narrative_hidden_bridge_semantics(
        presentation
      )
    )
  }
  hidden_semantics = tuple(
    semantic_by_step_id.get(
      id(
        proof_step
      )
    )
    for proof_step in hidden_steps
  )

  if any(
    semantic is None
    for semantic in hidden_semantics
  ):
    return None

  if not all(
    semantic.role
    is TodaGroupProofNarrativeHiddenBridgeSemanticRole
    .TRANSPORT
    for semantic in hidden_semantics
  ):
    return None

  reference_identities = {
    semantic.reference_identity
    for semantic in hidden_semantics
  }

  if reference_identities != {
    "Proposition 5.3",
  }:
    return None

  operation_kinds = {
    semantic.operation_kind
    for semantic in hidden_semantics
    if semantic.operation_kind is not None
  }

  if operation_kinds != {
    (
      TodaGroupProofNarrativeHiddenBridgeOperationKind
      .SUSPENSION_STABILIZATION
    ),
  }:
    return None

  return (
    "Proposition 5.3 を順次適用し, "
    "suspension による安定化を用いると, "
  )


def _contribution_connector_lines(
  presentation: TodaGroupProofPresentation,
  ordered_contributions,
) -> dict[
  int,
  str,
]:
  direct_pairs = (
    _direct_contribution_dependency_pairs(
      presentation,
      ordered_contributions,
    )
  )
  connector_by_target_step_id = {}

  for contributions in ordered_contributions:
    for contribution_index in range(
      1,
      len(contributions),
    ):
      source = contributions[
        contribution_index - 1
      ]
      target = contributions[
        contribution_index
      ]
      pair = (
        id(source.proof_step),
        id(target.proof_step),
      )

      if pair in direct_pairs:
        connector_by_target_step_id[
          id(target.proof_step)
        ] = "これより, "
        continue

      transport_connector = (
        _transport_chain_connector(
          presentation,
          source.proof_step,
          target.proof_step,
        )
      )

      if transport_connector is None:
        continue

      connector_by_target_step_id[
        id(target.proof_step)
      ] = transport_connector

  return connector_by_target_step_id


def _insert_toda_group_proof_narrative_argument_contributions(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> str:
  insertion_indices = (
    _contribution_insertion_indices(
      markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  connector_by_target_step_id = (
    _contribution_connector_lines(
      presentation,
      ordered_contributions,
    )
  )

  insertions_by_index = {}

  for argument_index, contributions in enumerate(
    ordered_contributions
  ):
    for contribution_index, contribution in enumerate(
      contributions
    ):
      contribution_line = (
        _render_generic_narrative_step(
          contribution.proof_step
        )
      )

      if not contribution_line:
        continue

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          contribution.proof_step,
          contribution_line,
        )
      ):
        continue

      if contribution_line in markdown:
        continue

      insertion_index = insertion_indices[
        argument_index
      ][
        contribution_index
      ]

      if insertion_index is None:
        continue

      connector = (
        connector_by_target_step_id.get(
          id(
            contribution.proof_step
          )
        )
      )
      lines = []

      if connector is not None:
        lines.append(
          connector
        )

      lines.append(
        contribution_line
      )

      insertions_by_index.setdefault(
        insertion_index,
        [],
      ).append(
        "\n\n".join(
          lines
        )
      )

  rendered = markdown

  for insertion_index in sorted(
    insertions_by_index,
    reverse=True,
  ):
    contribution_fragments = insertions_by_index[
      insertion_index
    ]
    insertion = (
      "\n\n"
      + "\n\n".join(
        contribution_fragments
      )
    )

    if (
      insertion_index < len(
        markdown
      )
      and not markdown[
        insertion_index:
      ].startswith(
        "\n\n"
      )
    ):
      insertion += "\n\n"

    rendered = (
      rendered[
        :insertion_index
      ]
      + insertion
      + rendered[
        insertion_index:
      ]
    )

  return rendered

def _is_toda_group_proof_narrative_reference_statement_candidate(
  proof_step,
  rendered_statement: str,
) -> bool:
  if not rendered_statement:
    return False

  inference_rule = proof_step.inference_rule

  if (
    inference_rule is not None
    and rendered_statement == inference_rule.name
  ):
    return False

  if (
    rendered_statement
    == "`"
    + type(
      proof_step.conclusion
    ).__name__
    + "`"
  ):
    return False

  if rendered_statement == repr(
    proof_step.conclusion
  ):
    return False

  if rendered_statement == str(
    proof_step.conclusion
  ):
    return False

  return True


def _phase153_r6_nested_value_contains(
  container,
  needle,
) -> bool:
  if container is needle:
    return True

  if isinstance(
    container,
    (
      str,
      bytes,
      int,
      float,
      bool,
      type(None),
    ),
  ):
    return False

  if isinstance(
    container,
    tuple,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container
    )

  if isinstance(
    container,
    list,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container
    )

  if isinstance(
    container,
    dict,
  ):
    return any(
      _phase153_r6_nested_value_contains(
        value,
        needle,
      )
      for value in container.values()
    )

  if not is_dataclass(
    container
  ):
    return False

  return any(
    _phase153_r6_nested_value_contains(
      getattr(
        container,
        field.name,
      ),
      needle,
    )
    for field in fields(
      container
    )
  )


def _phase153_r6_group_relation_generators(
  statement,
) -> tuple:
  if not isinstance(
    statement,
    Relation,
  ):
    return ()

  if (
    statement.relation_type
    is not RelationType.EQUALITY
  ):
    return ()

  rhs = statement.rhs
  generator = getattr(
    rhs,
    "generator",
    None,
  )

  if generator is not None:
    return (
      generator,
    )

  summands = getattr(
    rhs,
    "summands",
    None,
  )

  if not isinstance(
    summands,
    tuple,
  ):
    return ()

  return tuple(
    generator
    for summand in summands
    for generator in (
      getattr(
        summand,
        "generator",
        None,
      ),
    )
    if generator is not None
  )


def _phase157_r20_reference_scalar_value(
  value,
  symbol,
  binding: int,
):
  if isinstance(
    value,
    int,
  ):
    return value

  if isinstance(
    value,
    ScalarSymbol,
  ):
    if value == symbol:
      return binding

    return None

  if isinstance(
    value,
    ScalarSum,
  ):
    left = (
      _phase157_r20_reference_scalar_value(
        value.left,
        symbol,
        binding,
      )
    )
    right = (
      _phase157_r20_reference_scalar_value(
        value.right,
        symbol,
        binding,
      )
    )

    if (
      left is None
      or right is None
    ):
      return None

    return left + right

  return None


def _phase157_r20_specialize_reference_value(
  value,
  symbol,
  binding: int,
):
  if isinstance(
    value,
    ScalarSymbol,
  ):
    if value == symbol:
      return binding

    return value

  if isinstance(
    value,
    ScalarSum,
  ):
    left = (
      _phase157_r20_specialize_reference_value(
        value.left,
        symbol,
        binding,
      )
    )
    right = (
      _phase157_r20_specialize_reference_value(
        value.right,
        symbol,
        binding,
      )
    )

    if (
      isinstance(
        left,
        int,
      )
      and isinstance(
        right,
        int,
      )
    ):
      return left + right

    return replace(
      value,
      left=left,
      right=right,
    )

  if isinstance(
    value,
    tuple,
  ):
    return tuple(
      _phase157_r20_specialize_reference_value(
        item,
        symbol,
        binding,
      )
      for item in value
    )

  if isinstance(
    value,
    list,
  ):
    return [
      _phase157_r20_specialize_reference_value(
        item,
        symbol,
        binding,
      )
      for item in value
    ]

  if isinstance(
    value,
    dict,
  ):
    return {
      key: (
        _phase157_r20_specialize_reference_value(
          item,
          symbol,
          binding,
        )
      )
      for key, item in value.items()
    }

  if not is_dataclass(
    value
  ):
    return value

  changes = {}

  for field in fields(
    value
  ):
    if not field.init:
      continue

    original = getattr(
      value,
      field.name,
    )
    specialized = (
      _phase157_r20_specialize_reference_value(
        original,
        symbol,
        binding,
      )
    )

    if specialized != original:
      changes[
        field.name
      ] = specialized

  if not changes:
    return value

  return replace(
    value,
    **changes,
  )


def _phase157_r20_nested_primary_groups(
  value,
) -> tuple[
  TodaPrimaryGroup,
  ...,
]:
  groups = []

  def walk(
    current,
  ):
    if isinstance(
      current,
      TodaPrimaryGroup,
    ):
      groups.append(
        current
      )
      return

    if isinstance(
      current,
      tuple,
    ):
      for item in current:
        walk(
          item
        )
      return

    if isinstance(
      current,
      list,
    ):
      for item in current:
        walk(
          item
        )
      return

    if isinstance(
      current,
      dict,
    ):
      for item in current.values():
        walk(
          item
        )
      return

    if not is_dataclass(
      current
    ):
      return

    for field in fields(
      current
    ):
      walk(
        getattr(
          current,
          field.name,
        )
      )

  walk(
    value
  )

  unique = []

  for group in groups:
    if group not in unique:
      unique.append(
        group
      )

  return tuple(
    unique
  )


def _phase157_r20_reference_descendants(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
) -> tuple[
  ProofStep,
  ...,
]:
  consumers_by_step_id = {}

  for edge in presentation.edges:
    consumers_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  frontier = list(
    consumers_by_step_id.get(
      id(
        proof_step
      ),
      (),
    )
  )
  seen = {
    id(
      proof_step
    )
  }
  descendants = []

  while frontier:
    current = frontier.pop(
      0
    )
    current_id = id(
      current
    )

    if current_id in seen:
      continue

    seen.add(
      current_id
    )
    descendants.append(
      current
    )
    frontier.extend(
      consumers_by_step_id.get(
        current_id,
        (),
      )
    )

  return tuple(
    descendants
  )


def _phase157_r20_reference_range_allows(
  aggregate_statement,
  symbol,
  binding: int,
) -> bool:
  if not is_dataclass(
    aggregate_statement
  ):
    return True

  matching_ranges = tuple(
    value
    for field in fields(
      aggregate_statement
    )
    for value in (
      getattr(
        aggregate_statement,
        field.name,
      ),
    )
    if (
      isinstance(
        value,
        ScalarGreaterEqualStatement,
      )
      and value.left == symbol
      and isinstance(
        value.right,
        int,
      )
    )
  )

  return all(
    binding
    >= range_statement.right
    for range_statement
    in matching_ranges
  )


def _phase157_r20_specialize_reference_relation(
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
  relation: Relation,
):
  group = relation.lhs

  if not isinstance(
    group,
    TodaPrimaryGroup,
  ):
    return None

  symbol = (
    group.sphere_dimension
  )

  if not isinstance(
    symbol,
    ScalarSymbol,
  ):
    return None

  descendants = (
    _phase157_r20_reference_descendants(
      presentation,
      proof_step,
    )
  )

  concrete_groups = []

  for descendant in descendants:
    concrete_groups.extend(
      _phase157_r20_nested_primary_groups(
        descendant.conclusion
      )
    )

  specializations = []

  for concrete_group in concrete_groups:
    if (
      not isinstance(
        concrete_group.group_dimension,
        int,
      )
      or not isinstance(
        concrete_group.sphere_dimension,
        int,
      )
    ):
      continue

    binding = (
      concrete_group.sphere_dimension
    )

    expected_sphere = (
      _phase157_r20_reference_scalar_value(
        group.sphere_dimension,
        symbol,
        binding,
      )
    )
    expected_dimension = (
      _phase157_r20_reference_scalar_value(
        group.group_dimension,
        symbol,
        binding,
      )
    )

    if (
      expected_sphere
      != concrete_group.sphere_dimension
      or expected_dimension
      != concrete_group.group_dimension
    ):
      continue

    if not (
      _phase157_r20_reference_range_allows(
        proof_step.conclusion,
        symbol,
        binding,
      )
    ):
      continue

    specialized = (
      _phase157_r20_specialize_reference_value(
        relation,
        symbol,
        binding,
      )
    )

    if specialized not in specializations:
      specializations.append(
        specialized
      )

  if len(
    specializations
  ) != 1:
    return None

  return specializations[
    0
  ]


def _phase157_r20_canonical_fixed_reference_line(
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(\alpha\circ E\beta)"
      r" = H(\alpha)\circ E\beta$."
    )

  return rendered_statement


def _phase153_r6_reference_aggregate_component(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
):
  statement = proof_step.conclusion

  if not is_dataclass(
    statement
  ):
    return None

  relation_components = tuple(
    value
    for field in fields(
      statement
    )
    for value in (
      getattr(
        statement,
        field.name,
      ),
    )
    if (
      isinstance(
        value,
        Relation,
      )
      and _phase153_r6_group_relation_generators(
        value
      )
    )
  )

  if not relation_components:
    return None

  external_consumers = tuple(
    edge.parent_step
    for edge in presentation.edges
    if (
      edge.premise_step
      is proof_step
      and extract_toda_group_proof_step_literature_reference(
        edge.parent_step
      )
      != entry.reference
    )
  )

  direct_matches = []

  for component in relation_components:
    generators = (
      _phase153_r6_group_relation_generators(
        component
      )
    )

    if any(
      _phase153_r6_nested_value_contains(
        consumer.conclusion,
        generator,
      )
      for consumer in external_consumers
      for generator in generators
    ):
      direct_matches.append(
        component
      )

  if len(
    direct_matches
  ) == 1:
    return direct_matches[
      0
    ]

  specialized_matches = []

  for component in relation_components:
    specialized = (
      _phase157_r20_specialize_reference_relation(
        presentation,
        proof_step,
        component,
      )
    )

    if (
      specialized is not None
      and specialized
      not in specialized_matches
    ):
      specialized_matches.append(
        specialized
      )

  if len(
    specialized_matches
  ) != 1:
    return None

  return specialized_matches[
    0
  ]


def _phase153_r6_render_reference_statement(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.classification
    is TodaLiteratureStatementClassification.FIXED_STATEMENT
    and boundary.reference_locator
    == "Proposition 2.2"
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(lpha\circ Eeta) = "
      r"H(lpha)\circ Eeta$."
    )

  component = (
    _phase153_r6_reference_aggregate_component(
      presentation,
      entry,
      proof_step,
    )
  )

  if component is None:
    return rendered_statement

  component_step = ProofStep(
    conclusion=component,
    premises=(),
    rule=proof_step.rule,
    note=proof_step.note,
    inference_rule=proof_step.inference_rule,
  )

  return _render_generic_narrative_step(
    component_step
  )


def build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  str,
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  marker_by_step_id = {}

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )
    marker = (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )

    for proof_step in selected_steps:
      marker_by_step_id[
        id(
          proof_step
        )
      ] = marker

  return marker_by_step_id


def _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines(
  selected_steps: tuple[
    ProofStep,
    ...,
  ],
  rendered_by_step_id: dict[
    int,
    str,
  ],
) -> tuple[
  str,
  ...,
]:
  boundaries = tuple(
    classify_toda_literature_statement_step(
      proof_step
    )
    for proof_step in selected_steps
  )

  fixed_component_keys = tuple(
    (
      boundary.component_key
      if (
        boundary is not None
        and boundary.classification
        is TodaLiteratureStatementClassification
        .FIXED_STATEMENT
      )
      else None
    )
    for boundary in boundaries
  )

  definition_indices = tuple(
    index
    for index, component_key in enumerate(
      fixed_component_keys
    )
    if (
      component_key is not None
      and component_key.endswith(
        "_definition"
      )
    )
  )

  if (
    len(
      definition_indices
    ) != 1
    or len(
      selected_steps
    ) < 2
  ):
    return tuple(
      rendered_by_step_id[
        id(
          proof_step
        )
      ]
      for proof_step in selected_steps
    )

  definition_index = (
    definition_indices[
      0
    ]
  )
  definition_step = selected_steps[
    definition_index
  ]
  consequence_steps = tuple(
    proof_step
    for index, proof_step in enumerate(
      selected_steps
    )
    if index != definition_index
  )
  ordered_steps = (
    definition_step,
    *consequence_steps,
  )

  lines = []

  for index, proof_step in enumerate(
    ordered_steps
  ):
    line = rendered_by_step_id[
      id(
        proof_step
      )
    ].rstrip()

    if line.endswith(
      "."
    ) or line.endswith(
      ","
    ):
      line = line[
        :-1
      ]

    if index == 0:
      lines.append(
        line
        + " とすると,"
      )
      continue

    lines.append(
      line
      + "."
    )

  return tuple(
    lines
  )








def _toda_group_proof_narrative_reference_statement_lines_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    str,
    ...,
  ],
]:
  statement_lines_by_reference_number = {}

  for entry in reference_entries:
    candidate_steps = []
    rendered_by_step_id = {}
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )
      rendered_statement = (
        _phase157_r20_canonical_fixed_reference_line(
          proof_step,
          rendered_statement,
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if (
        rendered_statement
        in seen_rendered_statements
      ):
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )
      rendered_by_step_id[
        id(
          proof_step
        )
      ] = rendered_statement

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    aggregate_specializations = tuple(
      (
        proof_step,
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          proof_step,
        ),
      )
      for proof_step in selected_steps
      if is_dataclass(
        proof_step.conclusion
      )
    )
    aggregate_specializations = tuple(
      pair
      for pair in aggregate_specializations
      if pair[
        1
      ] is not None
    )

    if len(
      aggregate_specializations
    ) == 1:
      selected_steps = (
        aggregate_specializations[
          0
        ][
          0
        ],
      )

    rendered_selected_by_step_id = {
      id(
        proof_step
      ): (
        _phase157_r20_canonical_fixed_reference_line(
          proof_step,
          _phase153_r6_render_reference_statement(
            presentation,
            entry,
            proof_step,
            rendered_by_step_id[
              id(
                proof_step
              )
            ],
          ),
        )
      )
      for proof_step in selected_steps
    }

    statement_lines = (
      _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines(
        selected_steps,
        rendered_selected_by_step_id,
      )
    )

    if statement_lines:
      statement_lines_by_reference_number[
        entry.number
      ] = statement_lines

  return statement_lines_by_reference_number


def _phase153_r7_reaches_root_without_steps(
  presentation: TodaGroupProofPresentation,
  source_step: ProofStep,
  excluded_steps: tuple[
    ProofStep,
    ...,
  ],
) -> bool:
  excluded_step_ids = {
    id(
      proof_step
    )
    for proof_step in excluded_steps
  }
  children_by_step_id = {}

  for edge in presentation.edges:
    if (
      id(
        edge.parent_step
      )
      in excluded_step_ids
    ):
      continue

    children_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  target_id = id(
    presentation.root_step
  )
  stack = [
    source_step,
  ]
  visited = set()

  while stack:
    current = stack.pop()
    current_id = id(
      current
    )

    if current_id in visited:
      continue

    visited.add(
      current_id
    )

    if current_id == target_id:
      return True

    stack.extend(
      child_step
      for child_step in children_by_step_id.get(
        current_id,
        (),
      )
      if (
        id(
          child_step
        )
        not in excluded_step_ids
      )
    )

  return False


def suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  suppressed_fragments = set()
  aggregate_reference_labels = set()

  for entry in reference_entries:
    for aggregate_step in entry.proof_steps:
      component = (
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          aggregate_step,
        )
      )

      if component is None:
        continue

      retained_premises = tuple(
        premise_step
        for premise_step in aggregate_step.premises
        if premise_step.conclusion == component
      )

      if len(
        retained_premises
      ) != 1:
        continue

      aggregate_reference_labels.add(
        entry.reference.label
      )

      unselected_premises = tuple(
        premise_step
        for premise_step in aggregate_step.premises
        if premise_step is not retained_premises[0]
      )

      for premise_step in unselected_premises:
        blocked_sibling_steps = tuple(
          sibling_step
          for sibling_step in unselected_premises
          if sibling_step is not premise_step
        )

        if (
          _phase153_r7_reaches_root_without_steps(
            presentation,
            premise_step,
            (
              aggregate_step,
              *blocked_sibling_steps,
            ),
          )
        ):
          continue

        if isinstance(
          premise_step.conclusion,
          ScalarGreaterEqualStatement,
        ):
          rendered = (
            "$"
            + _render_scalar_latex(
              premise_step.conclusion.left
            )
            + r" \ge "
            + _render_scalar_latex(
              premise_step.conclusion.right
            )
            + "$"
          )
        else:
          rendered = (
            _render_generic_narrative_step(
              premise_step
            )
          )

        if rendered:
          suppressed_fragments.add(
            rendered
          )

  if not suppressed_fragments and not aggregate_reference_labels:
    return body_markdown

  lines = []

  for line in body_markdown.splitlines():
    if any(
      fragment in line
      for fragment in suppressed_fragments
    ):
      continue

    if (
      any(
        reference_label in line
        for reference_label in aggregate_reference_labels
      )
      and (
        "有限次元結果を得る" in line
        or "有限次元結果を示す" in line
      )
    ):
      continue

    lines.append(
      line
    )

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()


def _phase154_r5_reference_source_steps_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    ProofStep,
    ...,
  ],
]:
  source_steps_by_number = {}

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not rendered_statement:
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    ordered_source_steps = []
    seen_step_ids = set()

    for proof_step in (
      *selected_steps,
      *entry.proof_steps,
    ):
      proof_step_id = id(
        proof_step
      )

      if proof_step_id in seen_step_ids:
        continue

      seen_step_ids.add(
        proof_step_id
      )
      ordered_source_steps.append(
        proof_step
      )

    if ordered_source_steps:
      source_steps_by_number[
        entry.number
      ] = tuple(
        ordered_source_steps
      )

  return source_steps_by_number


def _phase154_r5_unique_visible_non_root_consumer_line(
  presentation: TodaGroupProofPresentation,
  source_steps: tuple[
    ProofStep,
    ...,
  ],
  body_markdown: str,
) -> str | None:
  if not source_steps:
    return None

  source_step_ids = {
    id(
      source_step
    )
    for source_step in source_steps
  }
  children_by_step_id = {}

  for edge in presentation.edges:
    children_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  queue = deque(
    (
      source_step,
      0,
    )
    for source_step in source_steps
  )
  visited_distance_by_step_id = {}
  visible_by_distance = {}

  while queue:
    current_step, distance = queue.popleft()
    current_step_id = id(
      current_step
    )
    known_distance = visited_distance_by_step_id.get(
      current_step_id
    )

    if (
      known_distance is not None
      and known_distance <= distance
    ):
      continue

    visited_distance_by_step_id[
      current_step_id
    ] = distance

    for child_step in children_by_step_id.get(
      current_step_id,
      (),
    ):
      child_step_id = id(
        child_step
      )
      child_distance = distance + 1

      if child_step_id in source_step_ids:
        queue.append(
          (
            child_step,
            child_distance,
          )
        )
        continue

      if child_step is presentation.root_step:
        continue

      rendered_child = (
        _render_generic_narrative_step(
          child_step
        )
      )

      if (
        rendered_child
        and rendered_child in body_markdown
      ):
        visible_by_distance.setdefault(
          child_distance,
          [],
        ).append(
          rendered_child
        )
        continue

      queue.append(
        (
          child_step,
          child_distance,
        )
      )

  if not visible_by_distance:
    return None

  nearest_distance = min(
    visible_by_distance
  )
  nearest_lines = tuple(
    dict.fromkeys(
      visible_by_distance[
        nearest_distance
      ]
    )
  )

  if len(
    nearest_lines
  ) != 1:
    return None

  return nearest_lines[
    0
  ]


def link_toda_group_proof_narrative_reference_body_consumers(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  source_steps_by_number = (
    _phase154_r5_reference_source_steps_by_number(
      presentation,
      reference_entries,
    )
  )
  lines = body_markdown.splitlines()

  for reference_number, source_steps in (
    source_steps_by_number.items()
  ):
    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    marker_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if (
        marker in line
        and line.rstrip().endswith(
          marker
          + "を用いる."
        )
      )
    )

    if len(
      marker_indices
    ) != 1:
      continue

    current_body = "\n".join(
      lines
    )
    consumer_line = (
      _phase154_r5_unique_visible_non_root_consumer_line(
        presentation,
        source_steps,
        current_body,
      )
    )

    if consumer_line is None:
      continue

    consumer_indices = tuple(
      index
      for index, line in enumerate(
        lines
      )
      if (
        index != marker_indices[0]
        and consumer_line in line
      )
    )

    if len(
      consumer_indices
    ) != 1:
      continue

    marker_index = marker_indices[
      0
    ]
    consumer_index = consumer_indices[
      0
    ]

    if consumer_index <= marker_index:
      continue

    lines[
      marker_index
    ] = (
      marker
      + "より, "
      + consumer_line
    )
    del lines[
      consumer_index
    ]

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()

def suppress_toda_group_proof_narrative_reference_body_restatements(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  derivation_tokens = (
    "これらから",
    "このことから",
    "したがって",
    "従って",
    "よって",
    "ゆえに",
    "以上より",
    "ここから",
    "計算",
    "導く",
    "導か",
    "得る",
    "従う",
    "分かる",
    "わかる",
    "示す",
    "確認",
  )

  lines = body_markdown.splitlines()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        stripped = line.strip()

        if stripped == statement_line:
          continue

        if any(
          token in line
          for token in derivation_tokens
        ):
          updated_lines.append(
            line
          )
          continue

        if marker in line:
          updated_lines.append(
            marker
            + "を用いる."
          )
          continue

        replaced_line = line.replace(
          statement_line,
          marker,
        )

        if replaced_line.rstrip().endswith(
          marker
        ):
          replaced_line = (
            replaced_line.rstrip()
            + "を用いる."
          )

        updated_lines.append(
          replaced_line
        )

      lines = updated_lines

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()



def suppress_toda_group_proof_narrative_repeated_reference_restatements(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  reference_keys = set()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      reference_keys.add(
        _phase157_r11_reference_statement_match_key(
          statement_line
        )
      )

  if not reference_keys:
    return body_markdown

  retained = []
  seen_reference_keys = set()

  for paragraph in body_markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()
    comparable = stripped

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]"
      )

      if marker_end >= 0:
        suffix = stripped[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            comparable = suffix[
              len(
                prefix
              ):
            ]
            break

    key = (
      _phase157_r11_reference_statement_match_key(
        comparable
      )
    )

    if key not in reference_keys:
      retained.append(
        paragraph
      )
      continue

    if key in seen_reference_keys:
      continue

    seen_reference_keys.add(
      key
    )
    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )
def _phase157_r11_reference_statement_match_key(
  line: str,
) -> str:
  if not isinstance(
    line,
    str,
  ):
    raise TypeError(
      "line must be a str"
    )

  normalized = line.strip().rstrip(
    ".,"
  )
  marker = r"\tag{"

  while True:
    marker_index = normalized.find(
      marker
    )

    if marker_index < 0:
      break

    number_start = (
      marker_index
      + len(
        marker
      )
    )
    number_end = normalized.find(
      "}",
      number_start,
    )

    if number_end < 0:
      break

    number_text = normalized[
      number_start:
      number_end
    ]

    if not number_text.isdigit():
      break

    normalized = (
      normalized[
        :marker_index
      ]
      + normalized[
        number_end + 1:
      ]
    )

  return normalized


def suppress_toda_group_proof_narrative_reference_body_duplicates(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  lines = body_markdown.splitlines()

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    if (
      isinstance(
        reference_number,
        bool,
      )
      or not isinstance(
        reference_number,
        int,
      )
    ):
      raise TypeError(
        "statement_lines_by_reference_number keys "
        "must be integers"
      )

    if not isinstance(
      statement_lines,
      tuple,
    ):
      raise TypeError(
        "statement_lines_by_reference_number values "
        "must be tuples"
      )

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        stripped_line = line.strip()
        statement_match_key = (
          _phase157_r11_reference_statement_match_key(
            statement_line
          )
        )
        line_match_key = (
          _phase157_r11_reference_statement_match_key(
            stripped_line
          )
        )

        if line_match_key == statement_match_key:
          display_line = stripped_line.rstrip(
            ".,"
          )
          updated_lines.append(
            marker
            + "より, "
            + display_line
            + "."
          )
          continue

        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        if marker in line:
          updated_lines.append(
            marker
            + "を用いる."
          )
          continue

        replaced_line = line.replace(
          statement_line,
          marker,
        )

        if (
          marker in replaced_line
          and (
            replaced_line.rstrip().endswith(
              marker
              + "を得る."
            )
            or replaced_line.rstrip().endswith(
              marker
              + "を得る."
            )
          )
        ):
          updated_lines.append(
            marker
            + "を用いる."
          )
          continue

        if replaced_line.rstrip().endswith(
          marker
        ):
          updated_lines.append(
            replaced_line.rstrip()
            + "を用いる."
          )
          continue

        updated_lines.append(
          replaced_line
        )

      lines = updated_lines

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()

def build_toda_group_proof_narrative_generic_used_step_ids(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  ordered_contributions,
) -> frozenset[
  int
]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  ordered_arguments = (
    order_toda_group_proof_narrative_arguments(
      arguments
    )
  )
  discourse_roles = (
    classify_toda_group_proof_narrative_argument_discourse_roles(
      arguments
    )
  )
  source_index_by_identity = {
    id(
      argument
    ): index
    for index, argument in enumerate(
      arguments
    )
  }
  used_step_ids = set()

  for ordered_position, argument in enumerate(
    ordered_arguments
  ):
    if (
      discourse_roles[
        ordered_position
      ]
      is TodaGroupProofNarrativeArgumentDiscourseRole.DETACHED
    ):
      continue

    argument_index = source_index_by_identity[
      id(
        argument
      )
    ]
    local_body_blocks = (
      extract_toda_group_proof_narrative_argument_local_body_blocks(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
        argument_index,
      )
    )

    used_step_ids.update(
      id(
        proof_step
      )
      for block in local_body_blocks
      for proof_step in block.steps
    )

  used_step_ids.update(
    id(
      contribution.proof_step
    )
    for contributions in ordered_contributions
    for contribution in contributions
  )

  return frozenset(
    used_step_ids
  )


def _toda_group_proof_narrative_reference_boundary_step_ids(
  reference_entries,
) -> frozenset[int]:
  return frozenset(
    id(
      proof_step
    )
    for entry in reference_entries
    for proof_step in entry.proof_steps
  )


def _toda_group_proof_narrative_reference_owned_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[int]:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  consumers_by_step_id = {}

  for edge in presentation.edges:
    consumers_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  all_owned_step_ids = set()

  for entry in reference_entries:
    entry_step_ids = {
      id(
        proof_step
      )
      for proof_step in entry.proof_steps
    }
    owned_step_ids = set(
      entry_step_ids
    )

    changed = True

    while changed:
      changed = False

      for edge in presentation.edges:
        if (
          id(
            edge.parent_step
          )
          not in owned_step_ids
        ):
          continue

        premise_step = edge.premise_step
        premise_step_id = id(
          premise_step
        )

        if (
          premise_step
          is presentation.root_step
          or premise_step_id
          in owned_step_ids
        ):
          continue

        premise_reference = (
          extract_toda_group_proof_step_literature_reference(
            premise_step
          )
        )

        if premise_reference is not None:
          continue

        consumers = tuple(
          consumers_by_step_id.get(
            premise_step_id,
            (),
          )
        )

        if not consumers:
          continue

        if not all(
          id(
            consumer
          )
          in owned_step_ids
          for consumer in consumers
        ):
          continue

        owned_step_ids.add(
          premise_step_id
        )
        changed = True

    all_owned_step_ids.update(
      owned_step_ids
    )

  return frozenset(
    all_owned_step_ids
  )


def _toda_group_proof_narrative_reference_internal_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[int]:
  selected_step_ids = set()

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if rendered_statement in seen_rendered_statements:
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    selected_step_ids.update(
      id(
        proof_step
      )
      for proof_step in selected_steps
    )

  owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      reference_entries,
    )
  )

  return frozenset(
    step_id
    for step_id in owned_step_ids
    if step_id not in selected_step_ids
  )


def _phase157_r5_r9_selected_fixed_definition_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[
  int
]:
  selected_definition_step_ids = set()

  for entry in reference_entries:
    candidate_steps = []
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if (
        rendered_statement
        in seen_rendered_statements
      ):
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    for proof_step in selected_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        is not TodaLiteratureStatementClassification
        .FIXED_STATEMENT
        or boundary.component_key is None
        or not boundary.component_key.endswith(
          "_definition"
        )
      ):
        continue

      selected_definition_step_ids.add(
        id(
          proof_step
        )
      )

  return frozenset(
    selected_definition_step_ids
  )


def suppress_toda_group_proof_narrative_reference_internal_body(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    semantic_sidecar,
    TodaGroupProofNarrativeSemanticSidecar,
  ):
    raise TypeError(
      "semantic_sidecar must be a "
      "TodaGroupProofNarrativeSemanticSidecar"
    )

  if (
    semantic_sidecar.presentation
    is not presentation
  ):
    raise ValueError(
      "semantic_sidecar must belong to presentation"
    )

  internal_step_ids = (
    _toda_group_proof_narrative_reference_internal_step_ids(
      presentation,
      reference_entries,
    )
  )
  fixed_definition_step_ids = (
    _phase157_r5_r9_selected_fixed_definition_step_ids(
      presentation,
      reference_entries,
    )
  )
  fixed_definition_precondition_step_ids = {
    id(
      dependency.prerequisite_step
    )
    for dependency
    in semantic_sidecar.dependency_semantics
    if (
      dependency.role
      is TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
      and id(
        dependency.dependent_step
      )
      in fixed_definition_step_ids
    )
  }

  suppressed_step_ids = (
    set(
      internal_step_ids
    )
    | set(
      fixed_definition_step_ids
    )
    | fixed_definition_precondition_step_ids
  )

  if not suppressed_step_ids:
    return body_markdown

  suppressed_statement_lines = {
    rendered
    for node in presentation.nodes
    for proof_step in (
      node.proof_step,
    )
    if id(
      proof_step
    )
    in suppressed_step_ids
    for rendered in (
      _render_generic_narrative_step(
        proof_step
      ),
    )
    if rendered
  }

  suppressed_purpose_sentences = set()

  for argument in arguments:
    conclusion_step = (
      extract_toda_group_proof_narrative_argument_conclusion_step(
        argument
      )
    )

    if (
      conclusion_step is None
      or id(
        conclusion_step
      )
      not in suppressed_step_ids
    ):
      continue

    purpose = (
      render_toda_group_proof_narrative_argument_purpose_sentence(
        argument
      )
    )

    if purpose is not None:
      suppressed_purpose_sentences.add(
        purpose
      )

  retained_lines = []

  for line in body_markdown.splitlines():
    stripped = line.strip()

    if stripped in suppressed_statement_lines:
      continue

    if any(
      stripped.endswith(
        purpose
      )
      for purpose in suppressed_purpose_sentences
    ):
      continue

    retained_lines.append(
      line
    )

  compacted_lines = []
  previous_blank = False

  for line in retained_lines:
    is_blank = not line.strip()

    if (
      is_blank
      and previous_blank
    ):
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()
def _toda_group_proof_narrative_reference_externally_used_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[int]:
  internal_step_ids = (
    _toda_group_proof_narrative_reference_internal_step_ids(
      presentation,
      reference_entries,
    )
  )
  internal_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if id(
      node.proof_step
    )
    in internal_step_ids
  )

  externally_used_step_ids = set()

  for entry in reference_entries:
    for proof_step in entry.proof_steps:
      if (
        _phase153_r7_reaches_root_without_steps(
          presentation,
          proof_step,
          internal_steps,
        )
      ):
        externally_used_step_ids.add(
          id(
            proof_step
          )
        )

  return frozenset(
    externally_used_step_ids
  )


def _toda_group_proof_narrative_reference_frontier_step_ids(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> frozenset[int]:
  children_by_step_id = {}

  for edge in presentation.edges:
    children_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  root_step = presentation.root_step
  root_reference = (
    extract_toda_group_proof_step_literature_reference(
      root_step
    )
  )
  frontier_step_ids = set()

  for entry in reference_entries:
    for source_step in entry.proof_steps:
      queue = deque(
        [
          source_step,
        ]
      )
      visited = set()

      while queue:
        current_step = queue.popleft()
        current_step_id = id(
          current_step
        )

        if current_step_id in visited:
          continue

        visited.add(
          current_step_id
        )

        if current_step is root_step:
          frontier_step_ids.add(
            id(
              source_step
            )
          )
          break

        for child_step in children_by_step_id.get(
          current_step_id,
          (),
        ):
          if child_step is root_step:
            frontier_step_ids.add(
              id(
                source_step
              )
            )
            queue.clear()
            break

          child_reference = (
            extract_toda_group_proof_step_literature_reference(
              child_step
            )
          )

          if (
            child_reference is not None
            and child_reference != entry.reference
            and child_reference != root_reference
          ):
            continue

          queue.append(
            child_step
          )

  return frozenset(
    frontier_step_ids
  )


def normalize_toda_group_proof_narrative_connectors(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  retained = []

  for index, paragraph in enumerate(
    paragraphs
  ):
    stripped = paragraph.strip()

    if (
      stripped == "以上より,"
      and index + 1 < len(
        paragraphs
      )
      and paragraphs[
        index + 1
      ].strip().startswith(
        "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
      )
    ):
      continue

    retained.append(
      paragraph
    )

  normalized_paragraphs = retained
  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }
  exactness_reason_prefixes = (
    "この完全性と ",
    "完全性より,",
  )
  index = 0

  while index < len(
    normalized_paragraphs
  ) - 1:
    stripped = normalized_paragraphs[
      index
    ].strip()

    if stripped not in standalone_connectors:
      index += 1
      continue

    next_paragraph = normalized_paragraphs[
      index + 1
    ]
    next_stripped = next_paragraph.lstrip()

    if (
      stripped == "これより,"
      and next_stripped.startswith(
        exactness_reason_prefixes
      )
    ):
      normalized_paragraphs.pop(
        index
      )
      continue

    separator = (
      "\n"
      if next_stripped.startswith(
        r"\["
      )
      else " "
    )

    normalized_paragraphs[
      index:
      index + 2
    ] = [
      stripped
      + separator
      + next_paragraph,
    ]

  for index, paragraph in enumerate(
    normalized_paragraphs
  ):
    stripped = paragraph.strip()

    if not stripped:
      continue

    if stripped.startswith(
      "次に, "
    ):
      normalized_paragraphs[
        index
      ] = paragraph.replace(
        "次に, ",
        "まず, ",
        1,
      )

    break

  return "\n\n".join(
    normalized_paragraphs
  )


def suppress_toda_group_proof_narrative_dangling_connectors(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
    "これらより,",
  }

  def numbered_connector_numbers(
    line: str,
  ) -> tuple[
    int,
    ...,
  ] | None:
    stripped = line.strip()

    if (
      not stripped.startswith(
        "("
      )
      or not stripped.endswith(
        "より,"
      )
      or "$" in stripped
      or "[R" in stripped
    ):
      return None

    relation_text = stripped[
      : -len(
        "より,"
      )
    ].strip()
    parts = tuple(
      part.strip()
      for part in relation_text.split(
        " と "
      )
    )

    if not parts:
      return None

    numbers = []

    for part in parts:
      if (
        len(
          part
        ) < 3
        or not part.startswith(
          "("
        )
        or not part.endswith(
          ")"
        )
      ):
        return None

      number_text = part[
        1:-1
      ]

      if not number_text.isdigit():
        return None

      numbers.append(
        int(
          number_text
        )
      )

    return tuple(
      numbers
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  retained_paragraphs = []

  for paragraph_index, paragraph in enumerate(
    paragraphs
  ):
    lines = paragraph.splitlines()

    while lines:
      stripped = lines[
        -1
      ].strip()

      if stripped in standalone_connectors:
        lines.pop()
        continue

      connector_numbers = (
        numbered_connector_numbers(
          stripped
        )
      )

      if connector_numbers is None:
        break

      previous_text = "\n\n".join(
        paragraphs[
          :paragraph_index
        ]
      )
      referenced_tags_exist = all(
        (
          r"\tag{"
          + str(
            number
          )
          + "}"
        )
        in previous_text
        for number in connector_numbers
      )

      next_paragraph = next(
        (
          candidate.strip()
          for candidate in paragraphs[
            paragraph_index + 1:
          ]
          if candidate.strip()
        ),
        "",
      )
      has_following_derivation = (
        "$" in next_paragraph
      )

      if (
        referenced_tags_exist
        and has_following_derivation
      ):
        break

      lines.pop()

    if not lines:
      continue

    normalized = "\n".join(
      lines
    )
    stripped = normalized.lstrip()

    for connector in standalone_connectors:
      prefix = (
        connector
        + " "
      )

      if (
        stripped.startswith(
          prefix
          + "[R"
        )
      ):
        leading = len(
          normalized
        ) - len(
          stripped
        )
        normalized = (
          normalized[
            :leading
          ]
          + stripped[
            len(
              prefix
            ):
          ]
        )
        break

    if normalized.strip():
      retained_paragraphs.append(
        normalized
      )

  return "\n\n".join(
    retained_paragraphs
  )

def order_toda_group_proof_narrative_visible_relation_dependencies(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]"
      )

      if marker_end >= 0:
        suffix = stripped[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            stripped = suffix[
              len(
                prefix
              ):
            ]
            break

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )

    matching_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matching_indices
    ) != 1:
      return None

    return matching_indices[
      0
    ]

  for node in presentation.nodes:
    consumer_step = node.proof_step

    if not isinstance(
      consumer_step.conclusion,
      Relation,
    ):
      continue

    consumer_index = paragraph_index_for_step(
      consumer_step
    )

    if consumer_index is None:
      continue

    relation_premises = tuple(
      premise
      for premise in consumer_step.premises
      if isinstance(
        premise.conclusion,
        Relation,
      )
    )

    for premise in relation_premises:
      premise_index = paragraph_index_for_step(
        premise
      )
      consumer_index = paragraph_index_for_step(
        consumer_step
      )

      if (
        premise_index is None
        or consumer_index is None
        or premise_index < consumer_index
      ):
        continue

      paragraph = paragraphs.pop(
        premise_index
      )

      consumer_index = paragraph_index_for_step(
        consumer_step
      )

      if consumer_index is None:
        paragraphs.insert(
          premise_index,
          paragraph,
        )
        continue

      paragraphs.insert(
        consumer_index,
        paragraph,
      )

  return "\n\n".join(
    paragraphs
  )


def suppress_toda_group_proof_narrative_repeated_unique_step_statements(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  def normalized_step_key(
    line: str,
  ) -> str:
    key = (
      _phase157_r11_reference_statement_match_key(
        line
      )
    )

    for verbose, concise in (
      (
        " は単射である",
        " は単射",
      ),
      (
        " は全射である",
        " は全射",
      ),
    ):
      if key.endswith(
        verbose
      ):
        return (
          key[
            :-len(
              verbose
            )
          ]
          + concise
        )

    return key

  step_ids_by_key = {}

  for node in presentation.nodes:
    proof_step = node.proof_step
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      continue

    key = normalized_step_key(
      rendered
    )

    step_ids_by_key.setdefault(
      key,
      set(),
    ).add(
      id(
        proof_step
      )
    )

  unique_step_keys = {
    key
    for key, step_ids in step_ids_by_key.items()
    if len(
      step_ids
    ) == 1
  }

  connector_prefixes = (
    "以上より, ",
    "したがって, ",
    "これより, ",
    "これらより, ",
    "完全性より, ",
  )

  exactness_map_property_keys = set()

  for paragraph in markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()

    if not stripped.startswith(
      "完全性より, "
    ):
      continue

    comparable = stripped[
      len(
        "完全性より, "
      ):
    ]
    key = normalized_step_key(
      comparable
    )

    if (
      key.endswith(
        " は単射"
      )
      or key.endswith(
        " は全射"
      )
    ):
      exactness_map_property_keys.add(
        key
      )

  retained = []
  seen_unique_keys = set()
  seen_exactness_map_property_keys = set()

  for paragraph in markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()
    comparable = stripped

    for prefix in connector_prefixes:
      if comparable.startswith(
        prefix
      ):
        comparable = comparable[
          len(
            prefix
          ):
        ]
        break

    key = normalized_step_key(
      comparable
    )

    if key in exactness_map_property_keys:
      if stripped.startswith(
        "完全性より, "
      ):
        if (
          key
          in seen_exactness_map_property_keys
        ):
          continue

        seen_exactness_map_property_keys.add(
          key
        )
        retained.append(
          paragraph
        )

      continue

    if key not in unique_step_keys:
      retained.append(
        paragraph
      )
      continue

    if key in seen_unique_keys:
      continue

    seen_unique_keys.add(
      key
    )
    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )


def _toda_group_proof_narrative_equation_tag_number(
  paragraph: str,
) -> int | None:
  marker = r"\tag{"
  marker_index = paragraph.find(
    marker
  )

  if marker_index < 0:
    return None

  number_start = (
    marker_index
    + len(
      marker
    )
  )
  number_end = paragraph.find(
    "}",
    number_start,
  )

  if number_end < 0:
    return None

  number_text = paragraph[
    number_start:
    number_end
  ]

  if not number_text.isdigit():
    return None

  return int(
    number_text
  )


def _toda_group_proof_narrative_two_equation_reference_numbers(
  paragraph: str,
) -> tuple[
  int,
  int,
] | None:
  stripped = paragraph.strip()

  if not stripped.startswith(
    "("
  ):
    return None

  first_close = stripped.find(
    ")"
  )

  if first_close <= 1:
    return None

  first_text = stripped[
    1:
    first_close
  ]

  separator = ") と ("
  separator_index = stripped.find(
    separator
  )

  if separator_index != first_close:
    return None

  second_start = (
    separator_index
    + len(
      separator
    )
  )
  second_close = stripped.find(
    ")",
    second_start,
  )

  if second_close <= second_start:
    return None

  second_text = stripped[
    second_start:
    second_close
  ]
  suffix = stripped[
    second_close + 1:
  ].strip()

  if not suffix.startswith(
    "より,"
  ):
    return None

  if (
    not first_text.isdigit()
    or not second_text.isdigit()
  ):
    return None

  return (
    int(
      first_text
    ),
    int(
      second_text
    ),
  )


def order_toda_group_proof_narrative_order_support(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )

    matching = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      ) == target_key
    )

    if len(
      matching
    ) != 1:
      return None

    return matching[
      0
    ]

  for node in presentation.nodes:
    order_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        order_step
      )
      is not TodaProofDependencyRole.ORDER
    ):
      continue

    conclusion_index = paragraph_index_for_step(
      order_step
    )

    if conclusion_index is None:
      continue

    premise_indices = tuple(
      index
      for premise in order_step.premises
      for index in (
        paragraph_index_for_step(
          premise
        ),
      )
      if index is not None
    )

    if not premise_indices:
      continue

    latest_premise_index = max(
      premise_indices
    )

    if latest_premise_index < conclusion_index:
      continue

    block_end = conclusion_index + 1

    if (
      block_end < len(
        paragraphs
      )
      and paragraphs[
        block_end
      ].strip()
      == "以上より,"
    ):
      block_end += 1

    conclusion_block = paragraphs[
      conclusion_index:
      block_end
    ]

    del paragraphs[
      conclusion_index:
      block_end
    ]

    premise_indices_after_removal = tuple(
      index
      for premise in order_step.premises
      for index in (
        paragraph_index_for_step(
          premise
        ),
      )
      if index is not None
    )

    if not premise_indices_after_removal:
      continue

    insertion_index = (
      max(
        premise_indices_after_removal
      )
      + 1
    )

    paragraphs[
      insertion_index:
      insertion_index
    ] = conclusion_block

  return "\n\n".join(
    paragraphs
  )


def suppress_toda_group_proof_narrative_literal_reflexive_equalities(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  retained = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    comparable = paragraph.strip()

    if comparable.startswith(
      "[R"
    ):
      marker_end = comparable.find(
        "]"
      )

      if marker_end >= 0:
        suffix = comparable[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            comparable = suffix[
              len(
                prefix
              ):
            ]
            break

    comparable = comparable.rstrip(
      "."
    ).strip()

    if (
      comparable.startswith(
        "$"
      )
      and comparable.endswith(
        "$"
      )
    ):
      equation = comparable[
        1:-1
      ]

      if equation.count(
        "="
      ) == 1:
        lhs, rhs = equation.split(
          "=",
          1,
        )

        if (
          lhs.strip()
          == rhs.strip()
        ):
          continue

    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )


def suppress_toda_group_proof_narrative_reflexive_equalities(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  reflexive_keys = set()

  for node in presentation.nodes:
    statement = node.proof_step.conclusion

    if (
      not isinstance(
        statement,
        Relation,
      )
      or statement.relation_type
      is not RelationType.EQUALITY
    ):
      continue

    try:
      rendered = (
        _render_generic_narrative_step(
          node.proof_step
        )
      )
    except (
      TypeError,
      ValueError,
    ):
      continue

    if (
      not rendered.startswith(
        "$"
      )
      or not rendered.endswith(
        "$"
      )
    ):
      continue

    equation = rendered[
      1:-1
    ]
    separator = " = "

    if separator not in equation:
      continue

    lhs_rendered, rhs_rendered = equation.split(
      separator,
      1,
    )

    if (
      lhs_rendered
      != rhs_rendered
    ):
      continue

    reflexive_keys.add(
      _phase157_r11_reference_statement_match_key(
        rendered
      )
    )

  if not reflexive_keys:
    return markdown

  retained = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    key = (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

    if key in reflexive_keys:
      continue

    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )


def order_toda_group_proof_narrative_surjectivity_support(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  reference_entries=(),
  statement_lines_by_reference_number=None,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    reference_entries,
    tuple,
  ):
    raise TypeError(
      "reference_entries must be a tuple"
    )

  if statement_lines_by_reference_number is None:
    statement_lines_by_reference_number = {}

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def strip_reference_prefix(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if not stripped.startswith(
      "[R"
    ):
      return stripped

    marker_end = stripped.find(
      "]"
    )

    if marker_end < 0:
      return stripped

    suffix = stripped[
      marker_end + 1:
    ]

    for prefix in (
      "より, ",
      "を用いて, ",
    ):
      if suffix.startswith(
        prefix
      ):
        return suffix[
          len(
            prefix
          ):
        ]

    return stripped

  def paragraph_match_key(
    paragraph: str,
  ) -> str:
    return (
      _phase157_r11_reference_statement_match_key(
        strip_reference_prefix(
          paragraph
        )
      )
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered_statement = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered_statement:
      return None

    target_key = (
      _phase157_r11_reference_statement_match_key(
        rendered_statement
      )
    )

    matching_indices = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if paragraph_match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matching_indices
    ) != 1:
      return None

    return matching_indices[
      0
    ]

  for node in presentation.nodes:
    map_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        map_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    map_index = paragraph_index_for_step(
      map_step
    )

    if map_index is None:
      continue

    equality_premises = tuple(
      premise
      for premise in map_step.premises
      if (
        isinstance(
          premise.conclusion,
          Relation,
        )
        and premise.conclusion.relation_type
        is RelationType.EQUALITY
      )
    )

    support_steps = []

    for equality_premise in equality_premises:
      support_steps.extend(
        premise
        for premise in equality_premise.premises
        if (
          isinstance(
            premise.conclusion,
            Relation,
          )
          and premise.conclusion.relation_type
          is RelationType.EQUALITY
        )
      )
      support_steps.append(
        equality_premise
      )

    support_indices = tuple(
      index
      for proof_step in support_steps
      for index in (
        paragraph_index_for_step(
          proof_step
        ),
      )
      if index is not None
    )

    if (
      support_steps
      and len(
        support_indices
      ) == len(
        support_steps
      )
    ):
      first_support_index = min(
        support_indices
      )
      last_support_index = max(
        support_indices
      )

      if not (
        first_support_index < map_index
        and last_support_index < map_index
      ):
        support_block = paragraphs[
          first_support_index:
          last_support_index + 1
        ]

        del paragraphs[
          first_support_index:
          last_support_index + 1
        ]

        map_index = paragraph_index_for_step(
          map_step
        )

        if map_index is not None:
          paragraphs[
            map_index:
            map_index
          ] = support_block

  for map_index, paragraph in enumerate(
    tuple(
      paragraphs
    )
  ):
    map_paragraph = strip_reference_prefix(
      paragraph
    )

    if (
      not map_paragraph.startswith(
        "$H:"
      )
      or " は全射である." not in map_paragraph
      or r"\to " not in map_paragraph
    ):
      continue

    if paragraph.strip() != map_paragraph:
      paragraphs[
        map_index
      ] = map_paragraph

    target_fragment = map_paragraph.split(
      r"\to ",
      1,
    )[1].split(
      "$",
      1,
    )[0].strip()

    group_prefix = (
      "$"
      + target_fragment
      + " = "
    )

    existing_group_index = next(
      (
        index
        for index, candidate in enumerate(
          paragraphs
        )
        if (
          index != map_index
          and strip_reference_prefix(
            candidate
          ).startswith(
            group_prefix
          )
        )
      ),
      None,
    )

    if existing_group_index is not None:
      if existing_group_index > map_index:
        group_paragraph = paragraphs.pop(
          existing_group_index
        )
        paragraphs.insert(
          map_index,
          group_paragraph,
        )
    else:
      reference_matches = []

      for entry in reference_entries:
        lines = (
          statement_lines_by_reference_number.get(
            entry.number,
            (),
          )
        )

        for line in lines:
          normalized_line = line.strip()

          if not normalized_line.startswith(
            group_prefix
          ):
            continue

          reference_matches.append(
            (
              entry.number,
              normalized_line,
            )
          )

      unique_matches = tuple(
        dict.fromkeys(
          reference_matches
        )
      )

      if len(
        unique_matches
      ) == 1:
        reference_number, statement_line = (
          unique_matches[
            0
          ]
        )
        support_paragraph = (
          "[R"
          + str(
            reference_number
          )
          + "]より, "
          + statement_line
        )

        if support_paragraph not in paragraphs:
          paragraphs.insert(
            map_index,
            support_paragraph,
          )

    map_index = next(
      (
        index
        for index, candidate in enumerate(
          paragraphs
        )
        if strip_reference_prefix(
          candidate
        )
        == map_paragraph
      ),
      None,
    )

    if map_index is None:
      continue

    kernel_index = next(
      (
        index
        for index, candidate in enumerate(
          paragraphs
        )
        if (
          r"\ker \Delta"
          in candidate
          and r"\operatorname{Im}H"
          in candidate
          and target_fragment
          in candidate
        )
      ),
      None,
    )

    if kernel_index is None:
      continue

    exactness_index = next(
      (
        index
        for index in range(
          map_index + 1,
          len(
            paragraphs
          ),
        )
        if (
          target_fragment
          in paragraphs[
            index
          ]
          and "は完全である."
          in paragraphs[
            index
          ]
        )
      ),
      None,
    )

    kernel_paragraph = paragraphs.pop(
      kernel_index
    )

    map_index = next(
      (
        index
        for index, candidate in enumerate(
          paragraphs
        )
        if strip_reference_prefix(
          candidate
        )
        == map_paragraph
      ),
      None,
    )

    if map_index is None:
      paragraphs.append(
        kernel_paragraph
      )
      continue

    if exactness_index is not None:
      exactness_index = next(
        (
          index
          for index in range(
            map_index + 1,
            len(
              paragraphs
            ),
          )
          if (
            target_fragment
            in paragraphs[
              index
            ]
            and "は完全である."
            in paragraphs[
              index
            ]
          )
        ),
        None,
      )

    insertion_index = (
      map_index + 1
      if exactness_index is None
      else exactness_index + 1
    )

    paragraphs.insert(
      insertion_index,
      kernel_paragraph,
    )

  return "\n\n".join(
    paragraphs
  )



def order_toda_group_proof_narrative_short_exact_support(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]"
      )

      if marker_end >= 0:
        suffix = stripped[
          marker_end + 1:
        ]

        for prefix in (
          "より, ",
          "を用いて, ",
        ):
          if suffix.startswith(
            prefix
          ):
            stripped = suffix[
              len(
                prefix
              ):
            ]
            break

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def unique_index_for_rendered(
    rendered: str,
  ) -> int | None:
    target_key = match_key(
      rendered
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  def map_support_step(
    source_group,
    target_group,
    map_name: str,
    property_prose: str,
  ) -> ProofStep | None:
    matches = []

    for node in presentation.nodes:
      proof_step = node.proof_step
      statement = proof_step.conclusion
      group_map = getattr(
        statement,
        "map",
        None,
      )

      if group_map is None:
        continue

      if (
        getattr(
          group_map,
          "source_group",
          None,
        )
        != source_group
        or getattr(
          group_map,
          "target_group",
          None,
        )
        != target_group
        or _toda_group_proof_narrative_map_name_latex(
          group_map
        )
        != map_name
      ):
        continue

      rendered = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if (
        not rendered
        or property_prose not in rendered
      ):
        continue

      matches.append(
        proof_step
      )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  for node in presentation.nodes:
    exactness_step = node.proof_step
    short_exact_latex = (
      _generic_short_exact_sequence_latex(
        presentation,
        exactness_step,
      )
    )

    if short_exact_latex is None:
      continue

    reason = (
      _generic_short_exact_sequence_reason_prose(
        presentation,
        exactness_step,
      )
    )

    if reason is None:
      continue

    window = getattr(
      exactness_step.conclusion,
      "window",
      None,
    )

    if window is None:
      continue

    first_map_name = (
      _toda_group_proof_narrative_map_name_latex(
        window.first_map
      )
    )
    second_map_name = (
      _toda_group_proof_narrative_map_name_latex(
        window.second_map
      )
    )

    if (
      first_map_name is None
      or second_map_name is None
    ):
      continue

    injective_step = map_support_step(
      window.source_term,
      window.middle_term,
      first_map_name,
      "は単射である.",
    )
    surjective_step = map_support_step(
      window.middle_term,
      window.target_term,
      second_map_name,
      "は全射である.",
    )

    if (
      injective_step is None
      or surjective_step is None
    ):
      continue

    injective_rendered = (
      _render_generic_narrative_step(
        injective_step
      )
    )
    surjective_rendered = (
      _render_generic_narrative_step(
        surjective_step
      )
    )

    if (
      not injective_rendered
      or not surjective_rendered
    ):
      continue

    injective_index = unique_index_for_rendered(
      injective_rendered
    )
    surjective_index = unique_index_for_rendered(
      surjective_rendered
    )

    short_exact_paragraph = (
      "$"
      + short_exact_latex
      + "$"
    )
    reason_index = unique_index_for_rendered(
      reason
    )
    sequence_index = unique_index_for_rendered(
      short_exact_paragraph
    )

    if (
      injective_index is None
      or surjective_index is None
      or reason_index is None
      or sequence_index is None
    ):
      continue

    support_anchor = max(
      injective_index,
      surjective_index,
    )

    if (
      reason_index > support_anchor
      and sequence_index > support_anchor
    ):
      continue

    moved = [
      paragraphs[
        reason_index
      ],
      paragraphs[
        sequence_index
      ],
    ]

    removal_indices = sorted(
      {
        reason_index,
        sequence_index,
      },
      reverse=True,
    )

    for index in removal_indices:
      paragraphs.pop(
        index
      )

    support_anchor = unique_index_for_rendered(
      surjective_rendered
      if surjective_index >= injective_index
      else injective_rendered
    )

    if support_anchor is None:
      continue

    insertion_index = (
      support_anchor + 1
    )
    paragraphs[
      insertion_index:
      insertion_index
    ] = moved

  return "\n\n".join(
    paragraphs
  )

def insert_toda_group_proof_narrative_reference_map_values_before_surjectivity(
  markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  for reference_number, statement_lines in (
    statement_lines_by_reference_number.items()
  ):
    for statement_line in statement_lines:
      if not (
        statement_line.startswith(
          "$H\\left("
        )
        and " = " in statement_line
      ):
        continue

      if any(
        statement_line in paragraph
        for paragraph in paragraphs
      ):
        continue

      map_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if (
            paragraph.strip().startswith(
              "$H:"
            )
            and " は全射である." in paragraph
          )
        ),
        None,
      )

      if map_index is None:
        continue

      paragraphs.insert(
        map_index,
        (
          "[R"
          + str(reference_number)
          + "]より, "
          + statement_line
        ),
      )

  return "\n\n".join(
    paragraphs
  )


def _toda_group_proof_narrative_map_name_latex(
  group_map,
) -> str | None:
  name = getattr(
    group_map,
    "name",
    None,
  )

  if name is not None:
    if name in (
      "Δ",
      "Delta",
    ):
      return r"\Delta"

    return str(
      name
    )

  map_type_name = type(
    group_map
  ).__name__

  if map_type_name in (
    "TodaSuspensionMap",
    "TodaIteratedSuspensionMap",
  ):
    return "E"

  if (
    map_type_name
    == "TodaHopfInvariantMap"
  ):
    return "H"

  if (
    map_type_name
    == "TodaDeltaMap"
  ):
    return r"\Delta"

  return None




def merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  exactness_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if classify_toda_proof_step_role(
      node.proof_step
    )
    is TodaProofDependencyRole.EHP_EXACTNESS
  )

  for left_step in exactness_steps:
    left_window = getattr(
      left_step.conclusion,
      "window",
      None,
    )

    if left_window is None:
      continue

    for right_step in exactness_steps:
      if right_step is left_step:
        continue

      right_window = getattr(
        right_step.conclusion,
        "window",
        None,
      )

      if right_window is None:
        continue

      if not (
        left_window.middle_term
        == right_window.source_term
        and left_window.target_term
        == right_window.middle_term
        and _toda_group_proof_narrative_map_name_latex(
          left_window.second_map
        )
        == _toda_group_proof_narrative_map_name_latex(
          right_window.first_map
        )
      ):
        continue

      left_line = (
        _render_generic_narrative_step(
          left_step
        )
      )
      right_line = (
        _render_generic_narrative_step(
          right_step
        )
      )

      left_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if paragraph.strip()
          == left_line.strip()
        ),
        None,
      )
      right_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if paragraph.strip()
          == right_line.strip()
        ),
        None,
      )

      if (
        left_index is None
        or right_index is None
      ):
        continue

      first_map = (
        _toda_group_proof_narrative_map_name_latex(
          left_window.first_map
        )
      )
      second_map = (
        _toda_group_proof_narrative_map_name_latex(
          left_window.second_map
        )
      )
      third_map = (
        _toda_group_proof_narrative_map_name_latex(
          right_window.second_map
        )
      )

      if None in (
        first_map,
        second_map,
        third_map,
      ):
        continue

      bare_sequence = (
        "$"
        + render_toda_primary_group_latex(
          left_window.source_term
        )
        + r" \xrightarrow{"
        + first_map
        + "} "
        + render_toda_primary_group_latex(
          left_window.middle_term
        )
        + r" \xrightarrow{"
        + second_map
        + "} "
        + render_toda_primary_group_latex(
          left_window.target_term
        )
        + r" \xrightarrow{"
        + third_map
        + "} "
        + render_toda_primary_group_latex(
          right_window.target_term
        )
        + "$"
      )
      merged = (
        bare_sequence
        + " は完全である."
      )

      bare_indices = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if paragraph.strip().rstrip(
          "."
        )
        == bare_sequence
      )

      introduction_index = (
        bare_indices[
          0
        ]
        if len(
          bare_indices
        ) == 1
        else None
      )

      removal_indices = {
        left_index,
        right_index,
      }

      if introduction_index is not None:
        removal_indices.add(
          introduction_index
        )
        insertion_index = (
          introduction_index
        )
      else:
        insertion_index = min(
          left_index,
          right_index,
        )

      for index in sorted(
        removal_indices,
        reverse=True,
      ):
        paragraphs.pop(
          index
        )

      removed_before_insertion = sum(
        1
        for index in removal_indices
        if index < insertion_index
      )
      insertion_index -= (
        removed_before_insertion
      )

      paragraphs.insert(
        insertion_index,
        merged,
      )

      return "\n\n".join(
        paragraphs
      )

  return markdown

def insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  reference_entries=(),
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    reference_entries,
    tuple,
  ):
    raise TypeError(
      "reference_entries must be a tuple"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def reference_entry_for_step(
    proof_step: ProofStep,
  ):
    direct = tuple(
      entry
      for entry in reference_entries
      if any(
        candidate is proof_step
        for candidate in entry.proof_steps
      )
    )

    if len(
      direct
    ) == 1:
      return direct[
        0
      ]

    reference = (
      extract_toda_group_proof_step_literature_reference(
        proof_step
      )
    )

    if (
      reference is None
      or reference.locator is None
    ):
      return None

    by_locator = tuple(
      entry
      for entry in reference_entries
      if (
        entry.reference.locator
        == reference.locator
      )
    )

    if len(
      by_locator
    ) != 1:
      return None

    return by_locator[
      0
    ]

  def display_line(
    proof_step: ProofStep,
  ) -> str | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    entry = reference_entry_for_step(
      proof_step
    )

    if entry is not None:
      rendered = (
        _phase153_r6_render_reference_statement(
          presentation,
          entry,
          proof_step,
          rendered,
        )
      )
      rendered = (
        _phase157_r20_canonical_fixed_reference_line(
          proof_step,
          rendered,
        )
      )

      return (
        "[R"
        + str(
          entry.number
        )
        + "]より, "
        + rendered
      )

    return rendered

  def visible_indices(
    proof_step: ProofStep,
  ) -> tuple[
    int,
    ...,
  ]:
    rendered = display_line(
      proof_step
    )

    if not rendered:
      return ()

    target_key = match_key(
      rendered
    )

    return tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if match_key(
        paragraph
      )
      == target_key
    )

  for node in presentation.nodes:
    consumer_step = node.proof_step

    definition_steps = tuple(
      premise
      for premise in consumer_step.premises
      if type(
        premise.conclusion
      ).__name__
      == "TodaEtaFamilyDefinitionStatement"
    )

    if len(
      definition_steps
    ) < 2:
      continue

    ordered = tuple(
      sorted(
        definition_steps,
        key=lambda step: (
          step.conclusion.index
        ),
      )
    )

    consumer_indices = visible_indices(
      consumer_step
    )

    if len(
      consumer_indices
    ) != 1:
      continue

    consumer_index = consumer_indices[
      0
    ]

    visible_direct_premise_indices = tuple(
      index
      for premise in consumer_step.premises
      if premise not in definition_steps
      for premise_indices in (
        visible_indices(
          premise
        ),
      )
      if len(
        premise_indices
      ) == 1
      for index in premise_indices
      if index < consumer_index
    )

    insertion_index = min(
      (
        consumer_index,
        *visible_direct_premise_indices,
      )
    )

    for lower_step, upper_step in zip(
      ordered,
      ordered[
        1:
      ],
    ):
      lower = lower_step.conclusion
      upper = upper_step.conclusion

      if (
        not isinstance(
          lower.index,
          int,
        )
        or isinstance(
          lower.index,
          bool,
        )
        or not isinstance(
          upper.index,
          int,
        )
        or isinstance(
          upper.index,
          bool,
        )
        or upper.index
        != lower.index + 1
      ):
        continue

      bridge = (
        "$"
        + render_toda_expression_latex(
          upper.element
        )
        + "=E"
        + render_toda_expression_latex(
          lower.element
        )
        + "$ である."
      )

      bridge_key = match_key(
        bridge
      )

      if any(
        match_key(
          paragraph
        )
        == bridge_key
        for paragraph in paragraphs
      ):
        continue

      paragraphs.insert(
        insertion_index,
        bridge,
      )
      insertion_index += 1

  return "\n\n".join(
    paragraphs
  )






def insert_toda_group_proof_narrative_map_property_dependencies(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  reference_entries=(),
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    reference_entries,
    tuple,
  ):
    raise TypeError(
      "reference_entries must be a tuple"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def reference_entry_for_step(
    proof_step: ProofStep,
  ):
    direct = tuple(
      entry
      for entry in reference_entries
      if any(
        candidate is proof_step
        for candidate in entry.proof_steps
      )
    )

    if len(
      direct
    ) == 1:
      return direct[
        0
      ]

    reference = (
      extract_toda_group_proof_step_literature_reference(
        proof_step
      )
    )

    if (
      reference is None
      or reference.locator is None
    ):
      return None

    by_locator = tuple(
      entry
      for entry in reference_entries
      if (
        entry.reference.locator
        == reference.locator
      )
    )

    if len(
      by_locator
    ) != 1:
      return None

    return by_locator[
      0
    ]

  def reference_number_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    entry = reference_entry_for_step(
      proof_step
    )

    if entry is None:
      return None

    return entry.number

  def display_line(
    proof_step: ProofStep,
  ) -> str | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    entry = reference_entry_for_step(
      proof_step
    )

    if entry is not None:
      rendered = (
        _phase153_r6_render_reference_statement(
          presentation,
          entry,
          proof_step,
          rendered,
        )
      )
      rendered = (
        _phase157_r20_canonical_fixed_reference_line(
          proof_step,
          rendered,
        )
      )

    reference_number = (
      reference_number_for_step(
        proof_step
      )
    )

    if reference_number is None:
      return rendered

    return (
      "[R"
      + str(
        reference_number
      )
      + "]より, "
      + rendered
    )

  def paragraph_index_for_step(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = display_line(
      proof_step
    )

    if not rendered:
      return None

    target_key = match_key(
      rendered
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  relevant_roles = {
    TodaProofDependencyRole.EHP_EXACTNESS,
    TodaProofDependencyRole.EHP_WINDOW,
    TodaProofDependencyRole.GROUP_STRUCTURE,
    TodaProofDependencyRole.MAP_PROPERTY,
    TodaProofDependencyRole.RELATION,
  }

  visiting = set()

  def ensure_before(
    proof_step: ProofStep,
    anchor_index: int,
  ) -> int:
    proof_step_id = id(
      proof_step
    )

    if proof_step_id in visiting:
      return anchor_index

    visiting.add(
      proof_step_id
    )

    boundary = (
      classify_toda_literature_statement_step(
        proof_step
      )
    )
    is_fixed_boundary = (
      boundary is not None
      and boundary.classification
      is TodaLiteratureStatementClassification.FIXED_STATEMENT
    )

    if not is_fixed_boundary:
      for premise in proof_step.premises:
        premise_role = (
          classify_toda_proof_step_role(
            premise
          )
        )

        if premise_role not in relevant_roles:
          continue

        anchor_index = ensure_before(
          premise,
          anchor_index,
        )

    line = display_line(
      proof_step
    )

    if line is None:
      visiting.remove(
        proof_step_id
      )
      return anchor_index

    current_index = (
      paragraph_index_for_step(
        proof_step
      )
    )

    if current_index is not None:
      if current_index < anchor_index:
        visiting.remove(
          proof_step_id
        )
        return anchor_index

      paragraph = paragraphs.pop(
        current_index
      )
      paragraphs.insert(
        anchor_index,
        paragraph,
      )

      visiting.remove(
        proof_step_id
      )
      return anchor_index + 1

    paragraphs.insert(
      anchor_index,
      line,
    )

    visiting.remove(
      proof_step_id
    )
    return anchor_index + 1

  visible_map_steps = []

  for node in presentation.nodes:
    proof_step = node.proof_step

    if (
      classify_toda_proof_step_role(
        proof_step
      )
      is not TodaProofDependencyRole.MAP_PROPERTY
    ):
      continue

    if (
      paragraph_index_for_step(
        proof_step
      )
      is None
    ):
      continue

    visible_map_steps.append(
      proof_step
    )

  for map_step in visible_map_steps:
    map_index = paragraph_index_for_step(
      map_step
    )

    if map_index is None:
      continue

    for premise in map_step.premises:
      role = classify_toda_proof_step_role(
        premise
      )

      if role not in relevant_roles:
        continue

      map_index = ensure_before(
        premise,
        map_index,
      )

  return "\n\n".join(
    paragraphs
  )


def insert_toda_group_proof_narrative_hidden_zero_map_premises(
  presentation: TodaGroupProofPresentation,
  markdown: str,
  reference_entries=(),
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  if not isinstance(
    reference_entries,
    tuple,
  ):
    raise TypeError(
      "reference_entries must be a tuple"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  def match_key(
    paragraph: str,
  ) -> str:
    stripped = paragraph.strip()

    if stripped.startswith(
      "[R"
    ):
      marker_end = stripped.find(
        "]より, "
      )

      if marker_end >= 0:
        stripped = stripped[
          marker_end
          + len(
            "]より, "
          ):
        ]

    return (
      _phase157_r11_reference_statement_match_key(
        stripped
      )
    )

  def visible_index(
    proof_step: ProofStep,
  ) -> int | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    target_key = match_key(
      rendered
    )
    matches = tuple(
      index
      for index, paragraph in enumerate(
        paragraphs
      )
      if match_key(
        paragraph
      )
      == target_key
    )

    if len(
      matches
    ) != 1:
      return None

    return matches[
      0
    ]

  def concise_map_property_reason(
    proof_step: ProofStep,
  ) -> str | None:
    rendered = (
      _render_generic_narrative_step(
        proof_step
      )
    )

    if not rendered:
      return None

    concise = rendered

    for verbose, short in (
      (
        " は単射である.",
        " は単射.",
      ),
      (
        " は全射である.",
        " は全射.",
      ),
    ):
      if concise.endswith(
        verbose
      ):
        concise = (
          concise[
            :-len(
              verbose
            )
          ]
          + short
        )
        break

    if concise == rendered:
      return None

    return (
      "完全性より, "
      + concise
    )

  def map_latex(
    group_map,
  ) -> str | None:
    name = getattr(
      group_map,
      "name",
      None,
    )

    if name is None:
      return None

    if name in (
      "Δ",
      "Delta",
    ):
      return r"\Delta"

    return str(
      name
    )

  def exactness_reason(
    zero_step: ProofStep,
  ) -> str | None:
    surjective_step = next(
      (
        premise
        for premise in zero_step.premises
        if (
          classify_toda_proof_step_role(
            premise
          )
          is TodaProofDependencyRole.MAP_PROPERTY
          and "全射である."
          in (
            _render_generic_narrative_step(
              premise
            )
            or ""
          )
        )
      ),
      None,
    )

    exactness_step = next(
      (
        premise
        for premise in zero_step.premises
        if classify_toda_proof_step_role(
          premise
        )
        in (
          TodaProofDependencyRole.EHP_EXACTNESS,
          TodaProofDependencyRole.EHP_WINDOW,
        )
      ),
      None,
    )

    if (
      surjective_step is None
      or exactness_step is None
    ):
      return None

    window = getattr(
      exactness_step.conclusion,
      "window",
      None,
    )

    if window is None:
      return None

    first_map = map_latex(
      window.first_map
    )
    second_map = map_latex(
      window.second_map
    )

    if (
      first_map is None
      or second_map is None
    ):
      return None

    return (
      "完全性より, "
      r"$\ker "
      + second_map
      + r"=\operatorname{Im}"
      + first_map
      + "="
      + render_toda_primary_group_latex(
        window.middle_term
      )
      + "$ である."
    )

  candidate_zero_steps = []
  seen_zero_step_ids = set()

  for node in presentation.nodes:
    for proof_step in (
      node.proof_step,
      *node.proof_step.premises,
    ):
      rendered = (
        _render_generic_narrative_step(
          proof_step
        )
      )

      if (
        not rendered
        or "零写像である."
        not in rendered
      ):
        continue

      proof_step_id = id(
        proof_step
      )

      if proof_step_id in seen_zero_step_ids:
        continue

      seen_zero_step_ids.add(
        proof_step_id
      )
      candidate_zero_steps.append(
        proof_step
      )

  for zero_step in candidate_zero_steps:
    zero_line = (
      _render_generic_narrative_step(
        zero_step
      )
    )

    if not zero_line:
      continue

    zero_index = visible_index(
      zero_step
    )

    if zero_index is None:
      consumer_match = next(
        (
          (
            node.proof_step,
            visible_index(
              node.proof_step
            ),
          )
          for node in presentation.nodes
          if (
            zero_step
            in node.proof_step.premises
            and visible_index(
              node.proof_step
            )
            is not None
          )
        ),
        None,
      )

      if consumer_match is None:
        continue

      (
        consumer_step,
        consumer_index,
      ) = consumer_match
      insertion_index = consumer_index

      if insertion_index > 0:
        previous = paragraphs[
          insertion_index - 1
        ]
        concise_reason = (
          concise_map_property_reason(
            consumer_step
          )
        )

        if (
          "零写像"
          in previous
          or "Δ=0"
          in previous
          or r"\Delta=0"
          in previous
          or (
            r"\ker E"
            in previous
            and r"\operatorname{Im}"
            in previous
          )
          or (
            concise_reason is not None
            and previous.strip()
            == concise_reason
          )
        ):
          insertion_index -= 1

      paragraphs.insert(
        insertion_index,
        zero_line,
      )
      zero_index = insertion_index

    reason = exactness_reason(
      zero_step
    )

    if reason is None:
      continue

    if any(
      paragraph.strip()
      == reason
      for paragraph in paragraphs
    ):
      continue

    zero_index = next(
      (
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if match_key(
          paragraph
        )
        == match_key(
          zero_line
        )
      ),
      zero_index,
    )

    paragraphs.insert(
      zero_index,
      reason,
    )

  return "\n\n".join(
    paragraphs
  )

def trim_toda_group_proof_narrative_redundant_left_ehp_terms(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  injective_maps = []

  for index, paragraph in enumerate(
    paragraphs
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$E: "
      )
      or "$ は単射である."
      not in stripped
      or r" \to "
      not in stripped
    ):
      continue

    map_expression = stripped[
      len(
        "$E: "
      ):
      stripped.find(
        "$ は単射である."
      )
    ]
    pieces = map_expression.split(
      r" \to ",
      1,
    )

    if len(
      pieces
    ) != 2:
      continue

    injective_maps.append(
      (
        index,
        pieces[
          0
        ],
        pieces[
          1
        ],
      )
    )

  delta_arrow = r"\xrightarrow{\Delta} "

  for index, paragraph in enumerate(
    tuple(
      paragraphs
    )
  ):
    stripped = paragraph.strip()

    if (
      delta_arrow not in stripped
      or r"\xrightarrow{E}" not in stripped
      or r"\xrightarrow{H}" not in stripped
    ):
      continue

    matching_injective = next(
      (
        (
          injective_index,
          domain,
          codomain,
        )
        for (
          injective_index,
          domain,
          codomain,
        ) in injective_maps
        if (
          injective_index < index
          and (
            domain
            + r" \xrightarrow{E} "
            + codomain
          )
          in stripped
        )
      ),
      None,
    )

    if matching_injective is None:
      continue

    _, tail = stripped.split(
      delta_arrow,
      1,
    )
    paragraphs[
      index
    ] = (
      "$"
      + tail
    )

  return "\n\n".join(
    paragraphs
  )


def normalize_toda_group_proof_narrative_repeated_numeric_equalities(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  characters = []
  index = 0

  while index < len(
    markdown
  ):
    if markdown[
      index
    ] != "=":
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    first_equals_index = index
    first_number_start = (
      first_equals_index + 1
    )

    while (
      first_number_start < len(
        markdown
      )
      and markdown[
        first_number_start
      ].isspace()
    ):
      first_number_start += 1

    first_number_end = first_number_start

    while (
      first_number_end < len(
        markdown
      )
      and markdown[
        first_number_end
      ].isdigit()
    ):
      first_number_end += 1

    if first_number_end == first_number_start:
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    second_equals_index = first_number_end

    while (
      second_equals_index < len(
        markdown
      )
      and markdown[
        second_equals_index
      ].isspace()
    ):
      second_equals_index += 1

    if (
      second_equals_index >= len(
        markdown
      )
      or markdown[
        second_equals_index
      ] != "="
    ):
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    second_number_start = (
      second_equals_index + 1
    )

    while (
      second_number_start < len(
        markdown
      )
      and markdown[
        second_number_start
      ].isspace()
    ):
      second_number_start += 1

    second_number_end = second_number_start

    while (
      second_number_end < len(
        markdown
      )
      and markdown[
        second_number_end
      ].isdigit()
    ):
      second_number_end += 1

    first_number = markdown[
      first_number_start:
      first_number_end
    ]
    second_number = markdown[
      second_number_start:
      second_number_end
    ]

    if (
      not second_number
      or first_number != second_number
    ):
      characters.append(
        markdown[
          index
        ]
      )
      index += 1
      continue

    characters.append(
      markdown[
        first_equals_index:
        first_number_end
      ]
    )
    index = second_number_end

  return "".join(
    characters
  )


def link_toda_group_proof_narrative_unmarked_reference_consumers(
  presentation: TodaGroupProofPresentation,
  body_markdown: str,
  reference_entries,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  paragraphs = body_markdown.split(
    "\n\n"
  )
  consumers_by_step_id = {}

  for edge in presentation.edges:
    consumers_by_step_id.setdefault(
      id(
        edge.premise_step
      ),
      [],
    ).append(
      edge.parent_step
    )

  for entry in reference_entries:
    marker = (
      "[R"
      + str(
        entry.number
      )
      + "]"
    )

    if marker in "\n\n".join(
      paragraphs
    ):
      continue

    visible_non_root_consumers = []
    visible_root_consumers = []

    for proof_step in entry.proof_steps:
      for consumer in consumers_by_step_id.get(
        id(
          proof_step
        ),
        (),
      ):
        if (
          classify_toda_proof_step_role(
            consumer
          )
          is TodaProofDependencyRole.MAP_PROPERTY
        ):
          continue

        rendered_consumer = (
          _render_generic_narrative_step(
            consumer
          )
        )

        if not rendered_consumer:
          continue

        matching_indices = tuple(
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if rendered_consumer in paragraph
        )

        if len(
          matching_indices
        ) != 1:
          continue

        consumer_index = matching_indices[
          0
        ]

        if consumer is presentation.root_step:
          visible_root_consumers.append(
            (
              id(
                consumer
              ),
              consumer_index,
            )
          )
          continue

        consumer_reference = (
          extract_toda_group_proof_step_literature_reference(
            consumer
          )
        )

        if consumer_reference is not None:
          continue

        visible_non_root_consumers.append(
          (
            id(
              consumer
            ),
            consumer_index,
          )
        )

    non_root_candidates = tuple(
      dict.fromkeys(
        visible_non_root_consumers
      )
    )
    root_candidates = tuple(
      dict.fromkeys(
        visible_root_consumers
      )
    )

    if len(
      non_root_candidates
    ) == 1:
      _, consumer_index = non_root_candidates[
        0
      ]
    elif (
      not non_root_candidates
      and len(
        root_candidates
      ) == 1
    ):
      _, consumer_index = root_candidates[
        0
      ]
    else:
      continue

    paragraph = paragraphs[
      consumer_index
    ]

    if marker in paragraph:
      continue

    paragraphs[
      consumer_index
    ] = (
      marker
      + "を用いて, "
      + paragraph
    )

  return "\n\n".join(
    paragraphs
  )


def normalize_toda_group_proof_narrative_display_math_periods(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  normalized_lines = []

  for line in markdown.splitlines():
    stripped = line.strip()

    if (
      stripped.endswith(
        "$"
      )
      and "$" in stripped
      and stripped != r"$\square$"
    ):
      line = line.rstrip() + "."

    normalized_lines.append(
      line
    )

  return "\n".join(
    normalized_lines
  )




def order_toda_group_proof_narrative_local_equation_derivations(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )

  while True:
    tag_index_by_number = {
      tag_number: index
      for index, paragraph in enumerate(
        paragraphs
      )
      for tag_number in (
        _toda_group_proof_narrative_equation_tag_number(
          paragraph
        ),
      )
      if tag_number is not None
    }
    moved = False

    for connector_index in range(
      len(
        paragraphs
      ) - 1
    ):
      reference_numbers = (
        _toda_group_proof_narrative_two_equation_reference_numbers(
          paragraphs[
            connector_index
          ]
        )
      )

      if reference_numbers is None:
        continue

      if any(
        number not in tag_index_by_number
        for number in reference_numbers
      ):
        continue

      derived_tag = (
        _toda_group_proof_narrative_equation_tag_number(
          paragraphs[
            connector_index + 1
          ]
        )
      )

      if derived_tag is None:
        continue

      source_anchor_index = max(
        tag_index_by_number[
          number
        ]
        for number in reference_numbers
      )
      desired_connector_index = (
        source_anchor_index + 1
      )

      if (
        connector_index
        == desired_connector_index
      ):
        continue

      derivation_paragraphs = paragraphs[
        connector_index:
        connector_index + 2
      ]
      del paragraphs[
        connector_index:
        connector_index + 2
      ]

      if connector_index < desired_connector_index:
        desired_connector_index -= 2

      paragraphs[
        desired_connector_index:
        desired_connector_index
      ] = derivation_paragraphs
      moved = True
      break

    if not moved:
      break

  return "\n\n".join(
    paragraphs
  )


def _phase157_r3_find_recursive_proof_step_by_rule_name(
  root_step: ProofStep,
  rule_name: str,
) -> ProofStep | None:
  if not isinstance(root_step, ProofStep):
    raise TypeError("root_step must be a ProofStep")
  if not isinstance(rule_name, str):
    raise TypeError("rule_name must be a str")

  stack = [
    root_step,
  ]
  visited_step_ids = set()

  while stack:
    current_step = stack.pop()
    current_step_id = id(
      current_step
    )

    if current_step_id in visited_step_ids:
      continue

    visited_step_ids.add(
      current_step_id
    )

    inference_rule = current_step.inference_rule

    if (
      inference_rule is not None
      and inference_rule.name == rule_name
    ):
      return current_step

    stack.extend(
      reversed(
        current_step.premises
      )
    )

  return None





def _phase159_r1_7c_r3_specialize_primary_group(
  group: TodaPrimaryGroup,
  symbol,
  binding: int,
) -> TodaPrimaryGroup | None:
  group_dimension = (
    _phase157_r20_reference_scalar_value(
      group.group_dimension,
      symbol,
      binding,
    )
  )
  sphere_dimension = (
    _phase157_r20_reference_scalar_value(
      group.sphere_dimension,
      symbol,
      binding,
    )
  )

  if (
    group_dimension is None
    or sphere_dimension is None
  ):
    return None

  return TodaPrimaryGroup(
    group_dimension=group_dimension,
    sphere_dimension=sphere_dimension,
  )


def _phase159_r1_7c_r3_aggregate_zero_specializes_to(
  statement,
  target_group: TodaPrimaryGroup,
) -> bool:
  if not isinstance(
    target_group,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "target_group must be a TodaPrimaryGroup"
    )

  if not is_dataclass(
    statement
  ):
    return False

  target_sphere_dimension = (
    target_group.sphere_dimension
  )

  if (
    not isinstance(
      target_sphere_dimension,
      int,
    )
    or isinstance(
      target_sphere_dimension,
      bool,
    )
  ):
    return False

  statement_values = tuple(
    getattr(
      statement,
      field.name,
    )
    for field in fields(
      statement
    )
  )
  range_statements = tuple(
    value
    for value in statement_values
    if isinstance(
      value,
      ScalarGreaterEqualStatement,
    )
  )

  for value in statement_values:
    if not isinstance(
      value,
      TodaPrimaryGroupZeroStatement,
    ):
      continue

    template_group = value.group
    symbol = (
      template_group.sphere_dimension
    )

    if not isinstance(
      symbol,
      ScalarSymbol,
    ):
      continue

    specialized_group = (
      _phase159_r1_7c_r3_specialize_primary_group(
        template_group,
        symbol,
        target_sphere_dimension,
      )
    )

    if specialized_group != target_group:
      continue

    applicable_range_found = False

    for range_statement in range_statements:
      left = (
        _phase157_r20_reference_scalar_value(
          range_statement.left,
          symbol,
          target_sphere_dimension,
        )
      )
      right = (
        _phase157_r20_reference_scalar_value(
          range_statement.right,
          symbol,
          target_sphere_dimension,
        )
      )

      if (
        left is not None
        and right is not None
        and left >= right
      ):
        applicable_range_found = True
        break

    if applicable_range_found:
      return True

  return False


def _phase159_r1_7c_r3_decomposition_specialization(
  statement,
  target_group: TodaPrimaryGroup,
):
  prop44_statement = getattr(
    statement,
    "prop44_isomorphism",
    None,
  )

  if prop44_statement is not None:
    decomposition_map = getattr(
      prop44_statement,
      "map",
      None,
    )
  else:
    decomposition_map = getattr(
      statement,
      "map",
      None,
    )

  if decomposition_map is None:
    return None

  source_group = getattr(
    decomposition_map,
    "source_group",
    None,
  )
  map_target_group = getattr(
    decomposition_map,
    "target_group",
    None,
  )
  summands = getattr(
    source_group,
    "summands",
    None,
  )

  if (
    not isinstance(
      map_target_group,
      TodaPrimaryGroup,
    )
    or not isinstance(
      summands,
      tuple,
    )
    or len(
      summands
    ) != 2
    or not all(
      isinstance(
        summand,
        TodaPrimaryGroup,
      )
      for summand in summands
    )
  ):
    return None

  target_dimension = (
    target_group.group_dimension
  )

  if (
    not isinstance(
      target_dimension,
      int,
    )
    or isinstance(
      target_dimension,
      bool,
    )
  ):
    return None

  map_dimension = (
    map_target_group.group_dimension
  )

  if isinstance(
    map_dimension,
    ScalarSymbol,
  ):
    symbol = map_dimension
    binding = target_dimension
  elif isinstance(
    map_dimension,
    int,
  ) and not isinstance(
    map_dimension,
    bool,
  ):
    if map_target_group != target_group:
      return None

    symbol = ScalarSymbol(
      name="_phase159_r1_7c_r3_unused",
    )
    binding = target_dimension
  else:
    return None

  specialized_target = (
    _phase159_r1_7c_r3_specialize_primary_group(
      map_target_group,
      symbol,
      binding,
    )
  )

  if specialized_target != target_group:
    return None

  specialized_summands = tuple(
    _phase159_r1_7c_r3_specialize_primary_group(
      summand,
      symbol,
      binding,
    )
    for summand in summands
  )

  if any(
    summand is None
    for summand in specialized_summands
  ):
    return None

  return (
    specialized_summands,
    target_group,
  )


def _phase159_r1_7c_r3_root_zero_direct_premise_plan(
  presentation: TodaGroupProofPresentation,
):
  root_step = presentation.root_step

  if not isinstance(
    root_step.conclusion,
    TodaPrimaryGroupZeroStatement,
  ):
    return None

  target_group = (
    root_step.conclusion.group
  )
  decomposition_matches = tuple(
    (
      premise_step,
      specialization,
    )
    for premise_step in root_step.premises
    for specialization in (
      _phase159_r1_7c_r3_decomposition_specialization(
        premise_step.conclusion,
        target_group,
      ),
    )
    if specialization is not None
  )

  if len(
    decomposition_matches
  ) != 1:
    return None

  (
    decomposition_step,
    decomposition_specialization,
  ) = decomposition_matches[0]
  (
    specialized_summands,
    specialized_target,
  ) = decomposition_specialization
  support_records = []

  for summand in specialized_summands:
    direct_zero_matches = tuple(
      premise_step
      for premise_step in root_step.premises
      if (
        isinstance(
          premise_step.conclusion,
          TodaPrimaryGroupZeroStatement,
        )
        and premise_step.conclusion.group
        == summand
      )
    )

    if len(
      direct_zero_matches
    ) == 1:
      support_records.append(
        (
          summand,
          direct_zero_matches[0],
          "known_zero",
        )
      )
      continue

    aggregate_matches = tuple(
      premise_step
      for premise_step in root_step.premises
      if (
        premise_step is not decomposition_step
        and _phase159_r1_7c_r3_aggregate_zero_specializes_to(
          premise_step.conclusion,
          summand,
        )
      )
    )

    if len(
      aggregate_matches
    ) != 1:
      return None

    support_records.append(
      (
        summand,
        aggregate_matches[0],
        "aggregate_zero",
      )
    )

  support_kinds = {
    support_kind
    for _, _, support_kind in support_records
  }

  if support_kinds != {
    "known_zero",
    "aggregate_zero",
  }:
    return None

  return (
    tuple(
      support_records
    ),
    decomposition_step,
    specialized_summands,
    specialized_target,
  )


def _phase159_r1_7c_r3_reference_marker(
  paragraph: str,
) -> str | None:
  stripped = paragraph.lstrip()

  if not stripped.startswith(
    "[R"
  ):
    return None

  closing_index = stripped.find(
    "]"
  )

  if closing_index < 0:
    return None

  number = stripped[
    2:closing_index
  ]

  if not number.isdigit():
    return None

  return stripped[
    :closing_index + 1
  ]


def _phase159_r1_7c_r3_specialized_zero_paragraph(
  paragraph: str,
  group: TodaPrimaryGroup,
) -> str:
  marker = (
    _phase159_r1_7c_r3_reference_marker(
      paragraph
    )
  )
  statement = (
    "$"
    + render_toda_primary_group_latex(
      group
    )
    + " = 0$."
  )

  if marker is None:
    return statement

  return (
    marker
    + "より, "
    + statement
  )


def _phase159_r1_7c_r3_specialized_decomposition_paragraph(
  paragraph: str,
  summands: tuple[
    TodaPrimaryGroup,
    ...,
  ],
  target_group: TodaPrimaryGroup,
) -> str:
  marker = (
    _phase159_r1_7c_r3_reference_marker(
      paragraph
    )
  )
  source_latex = r" \oplus ".join(
    render_toda_primary_group_latex(
      summand
    )
    for summand in summands
  )
  statement = (
    "$"
    + source_latex
    + r" \xrightarrow{\cong} "
    + render_toda_primary_group_latex(
      target_group
    )
    + "$."
  )

  if marker is None:
    return statement

  return (
    marker
    + "より, "
    + statement
  )


def specialize_toda_group_proof_narrative_root_zero_direct_premises(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  plan = (
    _phase159_r1_7c_r3_root_zero_direct_premise_plan(
      presentation
    )
  )

  if plan is None:
    return markdown

  (
    support_records,
    decomposition_step,
    specialized_summands,
    specialized_target,
  ) = plan
  replacement_by_rendered_step = {}

  for (
    summand,
    support_step,
    support_kind,
  ) in support_records:
    if support_kind != "aggregate_zero":
      continue

    rendered_support = (
      _render_generic_narrative_step(
        support_step
      )
    )

    if rendered_support:
      replacement_by_rendered_step[
        rendered_support
      ] = (
        "zero",
        summand,
      )

  rendered_decomposition = (
    _render_generic_narrative_step(
      decomposition_step
    )
  )

  if rendered_decomposition:
    replacement_by_rendered_step[
      rendered_decomposition
    ] = (
      "decomposition",
      (
        specialized_summands,
        specialized_target,
      ),
    )

  direct_premise_ids = {
    id(
      premise_step
    )
    for premise_step in (
      presentation.root_step.premises
    )
  }
  ancestor_steps = []
  seen_ancestor_ids = set()
  stack = [
    ancestor_step
    for premise_step in (
      presentation.root_step.premises
    )
    for ancestor_step in (
      premise_step.premises
    )
  ]

  while stack:
    proof_step = stack.pop()
    proof_step_id = id(
      proof_step
    )

    if (
      proof_step_id
      in seen_ancestor_ids
      or proof_step_id
      in direct_premise_ids
    ):
      continue

    seen_ancestor_ids.add(
      proof_step_id
    )
    ancestor_steps.append(
      proof_step
    )
    stack.extend(
      proof_step.premises
    )

  ancestor_fragments = tuple(
    rendered
    for rendered in (
      _render_generic_narrative_step(
        proof_step
      )
      for proof_step in ancestor_steps
    )
    if rendered
  )
  root_rendered = (
    _render_generic_narrative_step(
      presentation.root_step
    )
  )
  retained_paragraphs = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    replacement = next(
      (
        replacement
        for rendered_step, replacement
        in replacement_by_rendered_step.items()
        if rendered_step in paragraph
      ),
      None,
    )

    if replacement is not None:
      replacement_kind, value = replacement

      if replacement_kind == "zero":
        retained_paragraphs.append(
          _phase159_r1_7c_r3_specialized_zero_paragraph(
            paragraph,
            value,
          )
        )
      else:
        (
          summands,
          target_group,
        ) = value
        retained_paragraphs.append(
          _phase159_r1_7c_r3_specialized_decomposition_paragraph(
            paragraph,
            summands,
            target_group,
          )
        )

      continue

    if (
      root_rendered
      and root_rendered in paragraph
    ):
      retained_paragraphs.append(
        paragraph
      )
      continue

    if any(
      fragment in paragraph
      for fragment in ancestor_fragments
    ):
      continue

    retained_paragraphs.append(
      paragraph
    )

  return "\n\n".join(
    retained_paragraphs
  )


def _phase159_r1_7c_r3_repair4_aggregate_zero_component_line(
  statement,
  target_group: TodaPrimaryGroup,
) -> str | None:
  if not isinstance(
    target_group,
    TodaPrimaryGroup,
  ):
    raise TypeError(
      "target_group must be a TodaPrimaryGroup"
    )

  if not is_dataclass(
    statement
  ):
    return None

  target_sphere_dimension = (
    target_group.sphere_dimension
  )

  if (
    not isinstance(
      target_sphere_dimension,
      int,
    )
    or isinstance(
      target_sphere_dimension,
      bool,
    )
  ):
    return None

  statement_values = tuple(
    getattr(
      statement,
      field.name,
    )
    for field in fields(
      statement
    )
  )
  range_statements = tuple(
    value
    for value in statement_values
    if isinstance(
      value,
      ScalarGreaterEqualStatement,
    )
  )

  for value in statement_values:
    if not isinstance(
      value,
      TodaPrimaryGroupZeroStatement,
    ):
      continue

    template_group = value.group
    symbol = (
      template_group.sphere_dimension
    )

    if not isinstance(
      symbol,
      ScalarSymbol,
    ):
      continue

    specialized_group = (
      _phase159_r1_7c_r3_specialize_primary_group(
        template_group,
        symbol,
        target_sphere_dimension,
      )
    )

    if specialized_group != target_group:
      continue

    applicable_range = next(
      (
        range_statement
        for range_statement in range_statements
        for left, right in (
          (
            _phase157_r20_reference_scalar_value(
              range_statement.left,
              symbol,
              target_sphere_dimension,
            ),
            _phase157_r20_reference_scalar_value(
              range_statement.right,
              symbol,
              target_sphere_dimension,
            ),
          ),
        )
        if (
          left is not None
          and right is not None
          and left >= right
        )
      ),
      None,
    )

    if applicable_range is None:
      continue

    return (
      "$"
      + render_toda_primary_group_latex(
        template_group
      )
      + " = 0$, $"
      + _render_scalar_latex(
        applicable_range.left
      )
      + r" \ge "
      + _render_scalar_latex(
        applicable_range.right
      )
      + "$ が成り立つ."
    )

  return None


def prune_toda_group_proof_narrative_root_zero_direct_premise_references(
  presentation: TodaGroupProofPresentation,
  reference_entries,
  statement_lines_by_reference_number,
):
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  plan = (
    _phase159_r1_7c_r3_root_zero_direct_premise_plan(
      presentation
    )
  )

  if plan is None:
    return (
      reference_entries,
      statement_lines_by_reference_number,
    )

  (
    support_records,
    decomposition_step,
    _,
    _,
  ) = plan

  required_records = tuple(
    (
      support_step,
      support_kind,
      summand,
    )
    for (
      summand,
      support_step,
      support_kind,
    ) in support_records
  ) + (
    (
      decomposition_step,
      "decomposition",
      None,
    ),
  )

  required_by_reference = {}

  for (
    required_step,
    required_kind,
    target_group,
  ) in required_records:
    reference = (
      extract_toda_group_proof_step_literature_reference(
        required_step
      )
    )

    if reference is None:
      continue

    required_by_reference.setdefault(
      reference,
      [],
    ).append(
      (
        required_step,
        required_kind,
        target_group,
      )
    )

  if not required_by_reference:
    return (
      reference_entries,
      statement_lines_by_reference_number,
    )

  pruned_entries = []

  for entry in reference_entries:
    required_for_entry = (
      required_by_reference.get(
        entry.reference,
      )
    )

    if not required_for_entry:
      pruned_entries.append(
        entry
      )
      continue

    required_step_ids = {
      id(
        required_step
      )
      for (
        required_step,
        _,
        _,
      ) in required_for_entry
    }

    retained_steps = tuple(
      proof_step
      for proof_step in entry.proof_steps
      if id(
        proof_step
      ) in required_step_ids
    )

    if not retained_steps:
      pruned_entries.append(
        entry
      )
      continue

    pruned_entries.append(
      replace(
        entry,
        proof_steps=retained_steps,
      )
    )

  pruned_entries = tuple(
    pruned_entries
  )
  pruned_lines = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      pruned_entries,
    )
  )

  for entry in pruned_entries:
    required_for_entry = (
      required_by_reference.get(
        entry.reference,
      )
    )

    if not required_for_entry:
      continue

    aggregate_records = tuple(
      (
        required_step,
        target_group,
      )
      for (
        required_step,
        required_kind,
        target_group,
      ) in required_for_entry
      if required_kind == "aggregate_zero"
    )

    if len(
      aggregate_records
    ) != 1:
      continue

    (
      aggregate_step,
      target_group,
    ) = aggregate_records[0]
    component_line = (
      _phase159_r1_7c_r3_repair4_aggregate_zero_component_line(
        aggregate_step.conclusion,
        target_group,
      )
    )

    if component_line is None:
      continue

    pruned_lines[
      entry.number
    ] = (
      component_line,
    )

  return (
    pruned_entries,
    pruned_lines,
  )


def suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  retained = []
  prior_sequence_cores = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$"
      )
      or r"\xrightarrow{"
      not in stripped
    ):
      retained.append(
        paragraph
      )
      continue

    closing_math_index = stripped.find(
      "$",
      1,
    )

    if closing_math_index < 0:
      retained.append(
        paragraph
      )
      continue

    sequence_core = stripped[
      1:
      closing_math_index
    ]
    arrow_count = sequence_core.count(
      r"\xrightarrow{"
    )

    if arrow_count < 1:
      retained.append(
        paragraph
      )
      continue

    is_late_prefix_restatement = any(
      prior_core.startswith(
        sequence_core
      )
      and prior_core != sequence_core
      and prior_core.count(
        r"\xrightarrow{"
      ) > arrow_count
      for prior_core in prior_sequence_cores
    )

    if is_late_prefix_restatement:
      continue

    prior_sequence_cores.append(
      sequence_core
    )
    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )




def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  semantic_sidecar: TodaGroupProofNarrativeSemanticSidecar,
  arguments: tuple[
    TodaGroupProofNarrativeArgument,
    ...,
  ],
) -> str:
  base_markdown = (
    render_toda_group_proof_narrative_multi_argument_markdown(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
    )
  )
  proof_chains = (
    build_toda_group_proof_narrative_proof_chains(
      presentation,
      semantic_sidecar,
      arguments,
    )
  )
  ordered_contributions = (
    build_toda_group_proof_narrative_ordered_contributions(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      proof_chains,
      current_markdown=base_markdown,
    )
  )
  contribution_markdown = (
    _insert_toda_group_proof_narrative_argument_contributions(
      presentation,
      base_markdown,
      blocks,
      arguments,
      ordered_contributions,
    )
  )
  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_entries = (
    filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
      reference_entries,
      presentation.root_step,
    )
  )
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
  )
  phase157_r4_reference_entries_before_usage_filter = (
    reference_entries
  )
  phase157_r4_statement_lines_before_usage_filter = dict(
    statement_lines_by_reference_number
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
  reference_owned_step_ids = (
    _toda_group_proof_narrative_reference_owned_step_ids(
      presentation,
      reference_entries,
    )
  )
  reason_sidecar = (
    build_toda_group_proof_narrative_reason_sidecar(
      presentation,
      semantic_sidecar,
    )
  )
  boundary_filtered_reason_sidecar = type(
    reason_sidecar
  )(
    presentation=reason_sidecar.presentation,
    reasons=tuple(
      reason
      for reason in reason_sidecar.reasons
      if id(
        reason.conclusion_step
      )
      not in reference_owned_step_ids
    ),
  )

  rendered = (
    insert_toda_group_proof_narrative_reason_prose(
      contribution_markdown,
      boundary_filtered_reason_sidecar,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reference_internal_body(
      presentation,
      rendered,
      reference_entries,
      arguments,
      semantic_sidecar,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines_by_reference_number,
    )
  )
  rendered = (
    link_toda_group_proof_narrative_reference_body_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      rendered
    )
  )
  rendered = (
    order_toda_group_proof_narrative_local_equation_derivations(
      rendered
    )
  )
  rendered = (
    order_toda_group_proof_narrative_order_support(
      presentation,
      rendered,
    )
  )

  rendered = (
    insert_toda_group_proof_narrative_hidden_zero_map_premises(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    insert_toda_group_proof_narrative_map_property_dependencies(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
      presentation,
      rendered,
    )
  )
  rendered = (
    trim_toda_group_proof_narrative_redundant_left_ehp_terms(
      rendered
    )
  )
  rendered = (
    normalize_toda_group_proof_narrative_connectors(
      rendered
    )
  )
  rendered = (
    normalize_toda_group_proof_narrative_repeated_numeric_equalities(
      rendered
    )
  )
  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      rendered,
    )
  )
  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
  rendered = (
    order_toda_group_proof_narrative_short_exact_support(
      presentation,
      rendered,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_repeated_reference_restatements(
      rendered,
      statement_lines_by_reference_number,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )
  rendered = (
    order_toda_group_proof_narrative_visible_relation_dependencies(
      presentation,
      rendered,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_repeated_unique_step_statements(
      presentation,
      rendered,
    )
  )
  rendered = (
    insert_toda_group_proof_narrative_map_property_dependencies(
      presentation,
      rendered,
      reference_entries,
    )
  )
  rendered = (
    suppress_toda_group_proof_narrative_repeated_unique_step_statements(
      presentation,
      rendered,
    )
  )
  rendered = (
    order_toda_group_proof_narrative_injective_image_order_reason(
      rendered,
      reason_sidecar,
    )
  )
  rendered = (
    specialize_toda_group_proof_narrative_root_zero_direct_premises(
      presentation,
      rendered,
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_literal_reflexive_equalities(
      rendered
    )
  )

  rendered = (
    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
      rendered
    )
  )

  generic_used_step_ids = (
    build_toda_group_proof_narrative_generic_used_step_ids(
      presentation,
      blocks,
      semantic_sidecar,
      arguments,
      ordered_contributions,
    )
  )

  if "[R" in rendered:
    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_body_usage(
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
      )
    )
    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage(
        phase157_r4_reference_entries_before_usage_filter,
        phase157_r4_statement_lines_before_usage_filter,
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
        presentation.root_step,
        generic_used_step_ids,
        presentation=presentation,
      )
    )
  else:
    frontier_step_ids = (
      _toda_group_proof_narrative_reference_frontier_step_ids(
        presentation,
        reference_entries,
      )
    )
    boundary_visible_used_step_ids = frozenset(
      step_id
      for step_id in generic_used_step_ids
      if step_id in frontier_step_ids
    )

    (
      reference_entries,
      statement_lines_by_reference_number,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_step_usage(
        reference_entries,
        statement_lines_by_reference_number,
        boundary_visible_used_step_ids,
        presentation.root_step,
      )
    )

  if "[R" in rendered:
    (
      reference_entries,
      statement_lines_by_reference_number,
      rendered,
    ) = (
      filter_toda_group_proof_narrative_reference_entries_by_body_usage(
        reference_entries,
        statement_lines_by_reference_number,
        rendered,
      )
    )

  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    prune_toda_group_proof_narrative_root_zero_direct_premise_references(
      presentation,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  if not reference_section:
    return rendered

  legacy_intro = (
    "使用する結果を先にまとめる.\n\n"
  )

  public_reference_section = (
    reference_section
  )

  if public_reference_section.startswith(
    legacy_intro
  ):
    public_reference_section = (
      public_reference_section[
        len(
          legacy_intro
        ):
      ]
    )

  if rendered.startswith(
    legacy_intro
  ):
    rendered = rendered[
      len(
        legacy_intro
      ):
    ]

  return (
    normalize_toda_group_proof_narrative_display_math_periods(
      (
        "# Group proof narrative\n\n"
        "## 使用する結果\n\n"
        + public_reference_section
        + "\n\n"
        "---\n\n"
        "## 証明\n\n"
        + rendered
      )
    )
  )
