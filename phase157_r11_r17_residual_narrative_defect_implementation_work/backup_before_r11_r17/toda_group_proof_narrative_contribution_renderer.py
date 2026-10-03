from collections import deque
from dataclasses import (
  fields,
  is_dataclass,
  replace,
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
  _render_generic_narrative_step,
)
from toda_human_readable_renderer import (
  _render_scalar_latex,
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
)
from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  exclude_toda_group_proof_narrative_root_reference,
  filter_phase157_r3_pi6_3_reference_entries,
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
          else anchor_index
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
      insertion_index < len(markdown)
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

  if len(
    relation_components
  ) <= 1:
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

  if not external_consumers:
    return None

  matching_components = []

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
      matching_components.append(
        component
      )

  if len(
    matching_components
  ) != 1:
    return None

  return matching_components[
    0
  ]


def _phase153_r6_render_reference_statement(
  presentation: TodaGroupProofPresentation,
  entry,
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
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

    rendered_selected_by_step_id = {
      id(
        proof_step
      ): (
        _phase153_r6_render_reference_statement(
          presentation,
          entry,
          proof_step,
          rendered_by_step_id[
            id(
              proof_step
            )
          ],
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

  normalized = "\n\n".join(
    retained
  )

  normalized_paragraphs = normalized.split(
    "\n\n"
  )

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


def order_toda_group_proof_narrative_surjectivity_support(
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
      ) == target_key
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

    map_index = paragraph_index_for_step(
      map_step
    )

    if map_index is None:
      continue

    short_exact_reason_index = next(
      (
        index
        for index in range(
          map_index
        )
        if (
          "右の写像が全射"
          in paragraphs[
            index
          ]
          and "短完全列"
          in paragraphs[
            index
          ]
        )
      ),
      None,
    )

    if short_exact_reason_index is None:
      continue

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

    block_start = (
      min(
        support_indices
      )
      if support_indices
      else map_index
    )
    block_end = map_index + 1

    if block_start <= short_exact_reason_index:
      continue

    dependency_block = paragraphs[
      block_start:
      block_end
    ]

    del paragraphs[
      block_start:
      block_end
    ]

    paragraphs[
      short_exact_reason_index:
      short_exact_reason_index
    ] = dependency_block

  for map_index, paragraph in enumerate(
    tuple(
      paragraphs
    )
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$H:"
      )
      or " は全射である." not in stripped
      or r"\to " not in stripped
    ):
      continue

    target_fragment = stripped.split(
      r"\to ",
      1,
    )[1].split(
      "$",
      1,
    )[0].strip()

    group_index = next(
      (
        index
        for index in range(
          map_index + 1,
          len(
            paragraphs
          ),
        )
        if paragraphs[
          index
        ].strip().startswith(
          "$"
          + target_fragment
          + " = "
        )
      ),
      None,
    )

    if group_index is None:
      continue

    group_paragraph = paragraphs.pop(
      group_index
    )
    paragraphs.insert(
      map_index,
      group_paragraph,
    )

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
      stripped.startswith(
        "$"
      )
      and stripped.endswith(
        "$"
      )
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


def _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(
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
  if not isinstance(markdown, str):
    raise TypeError("markdown must be a str")

  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  if not (
    target.group_dimension == 6
    and target.sphere_dimension == 3
    and presentation.max_depth >= 3
  ):
    return markdown

  suspension_step = (
    _phase157_r3_find_recursive_proof_step_by_rule_name(
      presentation.root_step,
      "Toda Proposition 5.3 n=3 suspension isomorphism",
    )
  )
  hopf_step = (
    _phase157_r3_find_recursive_proof_step_by_rule_name(
      presentation.root_step,
      "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity",
    )
  )

  if suspension_step is None:
    return markdown

  suspension_line = _render_generic_narrative_step(
    suspension_step
  )

  if not suspension_line:
    return markdown

  if suspension_line in markdown:
    return markdown

  if hopf_step is not None:
    hopf_line = _render_generic_narrative_step(
      hopf_step
    )

    if hopf_line:
      hopf_index = markdown.find(
        hopf_line
      )

      if hopf_index >= 0:
        return (
          markdown[:hopf_index]
          + suspension_line
          + "\n\n"
          + markdown[hopf_index:]
        )

  final_group_marker = (
    "最後に, $\\pi_{6}^{3}$ の群構造を決定するために"
  )
  final_group_index = markdown.find(
    final_group_marker
  )

  if final_group_index >= 0:
    return (
      markdown[:final_group_index]
      + suspension_line
      + "\n\n"
      + markdown[final_group_index:]
    )

  return (
    markdown.rstrip()
    + "\n\n"
    + suspension_line
  )


def _phase157_r3_restore_pi6_3_earlier_prop56_reference(
  presentation: TodaGroupProofPresentation,
  original_entries,
  original_statement_lines_by_reference_number,
  filtered_entries,
  filtered_statement_lines_by_reference_number,
):
  target = (
    presentation
    .source_replay
    .group_result
    .target
  )

  if not (
    target.group_dimension == 6
    and target.sphere_dimension == 3
  ):
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
    )

  if any(
    entry.reference.locator == "Proposition 5.6"
    for entry in filtered_entries
  ):
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
    )

  source_entries = tuple(
    entry
    for entry in original_entries
    if entry.reference.locator == "Proposition 5.6"
  )

  if len(source_entries) != 1:
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
    )

  source_entry = source_entries[0]

  if source_entry.number not in (
    original_statement_lines_by_reference_number
  ):
    return (
      filtered_entries,
      filtered_statement_lines_by_reference_number,
    )

  new_number = len(filtered_entries) + 1
  restored_entry = replace(
    source_entry,
    number=new_number,
  )
  restored_lines = dict(
    filtered_statement_lines_by_reference_number
  )
  restored_lines[new_number] = (
    original_statement_lines_by_reference_number[
      source_entry.number
    ]
  )

  return (
    filtered_entries + (restored_entry,),
    restored_lines,
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
  reference_entries = (
    filter_phase157_r3_pi6_3_reference_entries(
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
  phase157_r3_entries_before_usage_filter = reference_entries
  phase157_r3_lines_before_usage_filter = (
    statement_lines_by_reference_number
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
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
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

  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    _phase157_r3_restore_pi6_3_earlier_prop56_reference(
      presentation,
      phase157_r3_entries_before_usage_filter,
      phase157_r3_lines_before_usage_filter,
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
